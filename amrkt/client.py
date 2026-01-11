"""Main client for amrkt library."""

from typing import Optional, List
from urllib.parse import unquote

from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from curl_cffi import requests

from .models import (
    UserInfo,
    Balance,
    Gift,
    GiftList,
    PurchaseResult,
    SearchParams,
)
from .exceptions import (
    AuthenticationError,
    APIError,
    NotFoundError,
    NotForSaleError,
)


class MarketClient:
    """
    Async client for Telegram Gift Market API.
    
    Usage:
        async with MarketClient(api_id, api_hash) as client:
            user = await client.get_user_info()
            balance = await client.get_balance()
    """
    
    API_URL = "https://api.tgmrkt.io/api/v1"
    
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_name: str = "amrkt_session",
        workdir: str = "."
    ):
        """
        Initialize the Market client.
        
        Args:
            api_id: Telegram API ID from https://my.telegram.org/auth
            api_hash: Telegram API hash from https://my.telegram.org/auth
            session_name: Name for the Pyrogram session file
            workdir: Working directory for session storage
        """
        self._api_id = api_id
        self._api_hash = api_hash
        self._session_name = session_name
        self._workdir = workdir
        self._client: Optional[Client] = None
        self._token: Optional[str] = None
    
    async def __aenter__(self) -> "MarketClient":
        """Async context manager entry - authenticates the client."""
        await self._ensure_authenticated()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        pass
    
    def _get_headers(self) -> dict:
        """Get authorization headers."""
        return {"Authorization": self._token} if self._token else {}
    
    def _is_token_valid(self) -> bool:
        """Check if current token is valid."""
        if not self._token:
            return False
        
        try:
            response = requests.get(
                f"{self.API_URL}/gifts/saling",
                headers=self._get_headers()
            )
            return response.status_code != 401
        except Exception:
            return False
    
    async def _get_new_token(self) -> str:
        """Get a new authentication token from Telegram."""
        client = Client(
            self._session_name,
            self._api_id,
            self._api_hash,
            workdir=self._workdir
        )
        
        async with client:
            peer = await client.resolve_peer("mrkt")
            bot_app = InputBotAppShortName(bot_id=peer, short_name="app")
            
            web_view = await client.invoke(
                RequestAppWebView(
                    peer=peer,
                    app=bot_app,
                    platform="android",
                )
            )
            
            init_data = unquote(
                web_view.url.split("tgWebAppData=", 1)[1].split("&tgWebAppVersion", 1)[0]
            )
            
            response = requests.post(
                f"{self.API_URL}/auth",
                json={"data": init_data}
            )
            
            if response.status_code != 200:
                raise AuthenticationError(f"Auth failed: {response.status_code}")
            
            data = response.json()
            token = data.get("token")
            
            if not token:
                raise AuthenticationError("No token in auth response")
            
            return token
    
    async def _ensure_authenticated(self) -> None:
        """Ensure we have a valid token, refreshing if needed."""
        if not self._is_token_valid():
            self._token = await self._get_new_token()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        json: dict = None,
        retry_on_401: bool = True
    ) -> dict:
        """Make an API request with automatic token refresh."""
        await self._ensure_authenticated()
        
        url = f"{self.API_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=self._get_headers())
        else:
            response = requests.post(url, headers=self._get_headers(), json=json)
        
        # Handle token expiration
        if response.status_code == 401 and retry_on_401:
            self._token = await self._get_new_token()
            return await self._request(method, endpoint, json, retry_on_401=False)
        
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {endpoint}")
        
        if response.status_code != 200:
            raise APIError(
                f"API error: {response.status_code}",
                status_code=response.status_code,
                response_text=response.text
            )
        
        return response.json()
    
    # ==================== User API ====================
    
    async def get_user_info(self) -> UserInfo:
        """
        Get current user information.
        
        Returns:
            UserInfo: User profile data
        """
        data = await self._request("GET", "/me")
        return UserInfo.model_validate(data)
    
    # ==================== Balance API ====================
    
    async def get_balance(self) -> Balance:
        """
        Get account balance.
        
        Returns:
            Balance: Account balance information
        """
        data = await self._request("GET", "/balance")
        return Balance.model_validate(data)
    
    # ==================== Gifts API ====================
    
    async def search_gifts(
        self,
        collection_names: List[str] = None,
        model_names: List[str] = None,
        backdrop_names: List[str] = None,
        symbol_names: List[str] = None,
        ordering: str = "Price",
        low_to_high: bool = True,
        max_price: int = None,
        min_price: int = None,
        mintable: bool = None,
        number: int = None,
        count: int = 20,
        cursor: str = "",
        query: str = None,
        promoted_first: bool = False,
    ) -> GiftList:
        """
        Search for gifts on sale.
        
        Args:
            collection_names: Filter by collection names (e.g., ["Lunar Snake"])
            model_names: Filter by model names (e.g., ["Albino"])
            backdrop_names: Filter by backdrop names
            symbol_names: Filter by symbol names
            ordering: Sort order ("Price", "Date", etc.)
            low_to_high: Sort ascending if True
            max_price: Maximum price in nanoTON
            min_price: Minimum price in nanoTON
            mintable: Filter by mintable status
            number: Filter by specific number
            count: Number of results (default 20)
            cursor: Pagination cursor
            query: Search query
            promoted_first: Show promoted gifts first
        
        Returns:
            GiftList: List of matching gifts
        """
        params = SearchParams(
            collection_names=collection_names or [],
            model_names=model_names or [],
            backdrop_names=backdrop_names or [],
            symbol_names=symbol_names or [],
            ordering=ordering,
            low_to_high=low_to_high,
            max_price=max_price,
            min_price=min_price,
            mintable=mintable,
            number=number,
            count=count,
            cursor=cursor,
            query=query,
            promoted_first=promoted_first,
        )
        
        data = await self._request("POST", "/gifts/saling", json=params.to_api_dict())
        return GiftList.model_validate(data)
    
    async def get_gift(self, gift_id: str) -> Gift:
        """
        Get information about a specific gift.
        
        Args:
            gift_id: The gift ID
        
        Returns:
            Gift: Gift information
        """
        data = await self._request("GET", f"/gifts/gift/{gift_id}")
        return Gift.model_validate(data)
    
    async def buy_gifts(self, gift_ids: List[str]) -> List[PurchaseResult]:
        """
        Buy gifts by their IDs.
        
        Args:
            gift_ids: List of gift IDs to buy
        
        Returns:
            List[PurchaseResult]: Purchase results
        
        Raises:
            NotForSaleError: If any gift is not for sale
        """
        data = await self._request("POST", "/gifts/buy", json={"Ids": gift_ids})
        
        if isinstance(data, list):
            return [PurchaseResult.model_validate(item) for item in data]
        return []
    
    # ==================== Inventory API ====================
    
    async def get_inventory(
        self,
        collection_names: List[str] = None,
        model_names: List[str] = None,
        backdrop_names: List[str] = None,
        symbol_names: List[str] = None,
        ordering: str = "Price",
        low_to_high: bool = False,
        max_price: int = None,
        min_price: int = None,
        mintable: bool = None,
        number: int = None,
        count: int = 50,
        cursor: str = "",
        query: str = None,
        promoted_first: bool = False,
    ) -> GiftList:
        """
        Get user's inventory.
        
        Args:
            Same as search_gifts()
        
        Returns:
            GiftList: List of owned gifts
        """
        params = SearchParams(
            collection_names=collection_names or [],
            model_names=model_names or [],
            backdrop_names=backdrop_names or [],
            symbol_names=symbol_names or [],
            ordering=ordering,
            low_to_high=low_to_high,
            max_price=max_price,
            min_price=min_price,
            mintable=mintable,
            number=number,
            count=count,
            cursor=cursor,
            query=query,
            promoted_first=promoted_first,
        )
        
        data = await self._request("POST", "/gifts", json=params.to_api_dict())
        return GiftList.model_validate(data)
    
    # ==================== Return API ====================
    
    async def return_gifts(self, gift_ids: List[str]) -> bool:
        """
        Return gifts to Telegram.
        
        Args:
            gift_ids: List of gift IDs to return
        
        Returns:
            bool: True if successful
        """
        await self._request("POST", "/gifts/return", json={"Ids": gift_ids})
        return True
