"""
amrkt - Async Python library for Telegram Gift Market API.

Example usage:
    from amrkt import MarketClient

    async with MarketClient(api_id, api_hash) as client:
        user = await client.get_user_info()
        balance = await client.get_balance()
"""

from .client import MarketClient
from .models import (
    UserInfo,
    Balance,
    Gift,
    GiftList,
    PurchaseResult,
    SearchParams,
    Wallet,
    ConfigItem,
    RefCoefsDto,
    DepositAwaitTransaction,
    ClaimTransactionResult,
    FeedItem,
    FeedResponse,
    SaleResult,
)
from .exceptions import (
    MarketError,
    AuthenticationError,
    NotFoundError,
    NotForSaleError,
    InsufficientBalanceError,
    APIError,
)

__version__ = "1.4.2"
__all__ = [
    "MarketClient",
    "UserInfo",
    "Balance", 
    "Gift",
    "GiftList",
    "PurchaseResult",
    "SearchParams",
    "Wallet",
    "ConfigItem",
    "RefCoefsDto",
    "DepositAwaitTransaction",
    "ClaimTransactionResult",
    "FeedItem",
    "FeedResponse",
    "SaleResult",
    "MarketError",
    "AuthenticationError",
    "NotFoundError",
    "NotForSaleError",
    "InsufficientBalanceError",
    "APIError",
]

