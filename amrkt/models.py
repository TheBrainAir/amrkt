"""Pydantic models for amrkt library."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Wallet(BaseModel):
    """User wallet information."""
    ton: Optional[str] = None
    device_id: Optional[str] = Field(default=None, alias="deviceId")

    class Config:
        populate_by_name = True


class ConfigItem(BaseModel):
    """Key-value config entry from /me response."""
    key: str
    value: str


class RefCoefsDto(BaseModel):
    """Referral coefficients for different product types."""
    referral_coef: float = Field(default=0, alias="referralCoef")
    sticker_referral_coef: float = Field(default=0, alias="stickerReferralCoef")
    not_games_referral_coef: float = Field(default=0, alias="notGamesReferralCoef")
    channel_referral_coef: float = Field(default=0, alias="channelReferralCoef")
    gifts_collection_referral_coef: float = Field(default=0, alias="giftsCollectionReferralCoef")
    stars_referral_coef: float = Field(default=0, alias="starsReferralCoef")
    tg_premium_referral_coef: float = Field(default=0, alias="tgPremiumReferralCoef")

    class Config:
        populate_by_name = True


class UserInfo(BaseModel):
    """User profile information from /me API."""
    id: int
    account_id: Optional[int] = Field(default=None, alias="accountId")
    user_ton_id: Optional[str] = Field(default=None, alias="userTonId")
    registered_at: Optional[str] = Field(default=None, alias="registeredAt")
    category: Optional[str] = None
    photo: Optional[str] = None
    full_name: str = Field(alias="fullName")
    ref_url: Optional[str] = Field(default=None, alias="refUrl")
    invited_by: Optional[int] = Field(default=None, alias="invitedBy")
    wallet: Optional[Wallet] = None
    allows_pm: bool = Field(default=True, alias="allowsPm")
    current_language_code: Optional[str] = Field(default=None, alias="currentLanguageCode")
    wallet_for_payment: Optional[str] = Field(default=None, alias="walletForPayment")
    is_vip: bool = Field(default=False, alias="isVIP")
    payer_id: Optional[str] = Field(default=None, alias="payerId")
    server_time: Optional[str] = Field(default=None, alias="serverTime")
    in_game_link: Optional[str] = Field(default=None, alias="inGameLink")
    referral_revenue_coef: float = Field(default=0, alias="referralRevenueCoef")
    giveaway_badge: Optional[str] = Field(default=None, alias="giveawayBadge")
    channel_validation_bot_name: Optional[str] = Field(default=None, alias="channelValidationBotName")
    configs: List[ConfigItem] = Field(default_factory=list)
    ref_coefs_dto: Optional[RefCoefsDto] = Field(default=None, alias="refCoefsDto")
    disable_withdrawal_limit: bool = Field(default=False, alias="disableWithdrawalLimit")
    disallowed_sections: List[str] = Field(default_factory=list, alias="disallowedSections")

    class Config:
        populate_by_name = True


class Balance(BaseModel):
    """Account balance information."""
    soft: int = 0
    hard: int = 0
    total_hard: int = Field(default=0, alias="totalHard")
    hard_locked: int = Field(default=0, alias="hardLocked")
    stars: int = 0
    stars_for_withdraw: int = Field(default=0, alias="starsFotWithdraw")
    spices: int = 0
    friends_count: int = Field(default=0, alias="friendsCount")
    lucky_buy_cards: int = Field(default=0, alias="luckyBuyCards")
    stacking_points: int = Field(default=0, alias="stackingPoints")
    space_monkeys_points: int = Field(default=0, alias="spaceMonkeysPoints")
    
    class Config:
        populate_by_name = True
    
    @property
    def soft_ton(self) -> float:
        """Soft balance in TON."""
        return self.soft / 1_000_000_000
    
    @property
    def hard_ton(self) -> float:
        """Hard balance in TON."""
        return self.hard / 1_000_000_000
    
    @property
    def total_hard_ton(self) -> float:
        """Total hard balance in TON."""
        return self.total_hard / 1_000_000_000
    
    @property
    def hard_locked_ton(self) -> float:
        """Locked hard balance in TON."""
        return self.hard_locked / 1_000_000_000


class DepositAwaitTransaction(BaseModel):
    """Pending deposit transaction from /transactions/await."""
    id: str
    currency_type: str = Field(alias="currencyType")
    value: int = 0
    soft_value: int = Field(default=0, alias="softValue")
    received_at: str = Field(alias="receivedAt")
    is_claimed: bool = Field(default=False, alias="isClaimed")
    is_refunded: bool = Field(default=False, alias="isRefunded")

    class Config:
        populate_by_name = True

    @property
    def value_ton(self) -> float:
        """Value in TON."""
        return self.value / 1_000_000_000


class ClaimTransactionResult(BaseModel):
    """Result item from claiming a deposit via POST /transactions/{id}."""
    value: int = 0
    type: str = ""
    source: Optional[str] = None

    class Config:
        populate_by_name = True

    @property
    def value_ton(self) -> float:
        """Value in TON."""
        return self.value / 1_000_000_000


class Gift(BaseModel):
    """Gift item model."""
    id: str
    name: Optional[str] = None
    gift_id: Optional[int] = Field(default=None, alias="giftId")
    gift_id_string: Optional[str] = Field(default=None, alias="giftIdString")
    number: Optional[int] = None
    title: Optional[str] = None
    
    # Collection info
    collection_name: Optional[str] = Field(default=None, alias="collectionName")
    collection_title: Optional[str] = Field(default=None, alias="collectionTitle")
    gifts_collection_id: Optional[str] = Field(default=None, alias="giftsCollectionId")
    
    # Model info
    model_name: Optional[str] = Field(default=None, alias="modelName")
    model_title: Optional[str] = Field(default=None, alias="modelTitle")
    model_rarity_per_mille: Optional[int] = Field(default=0, alias="modelRarityPerMille")
    model_rarity_name: Optional[str] = Field(default=None, alias="modelRarityName")
    model_sticker_key: Optional[str] = Field(default=None, alias="modelStickerKey")
    model_sticker_thumbnail_key: Optional[str] = Field(default=None, alias="modelStickerThumbnailKey")
    
    # Backdrop info
    backdrop_name: Optional[str] = Field(default=None, alias="backdropName")
    backdrop_rarity_per_mille: Optional[int] = Field(default=0, alias="backdropRarityPerMille")
    backdrop_rarity_name: Optional[str] = Field(default=None, alias="backdropRarityName")
    backdrop_colors_center_color: Optional[int] = Field(default=None, alias="backdropColorsCenterColor")
    backdrop_colors_edge_color: Optional[int] = Field(default=None, alias="backdropColorsEdgeColor")
    backdrop_colors_text_color: Optional[int] = Field(default=None, alias="backdropColorsTextColor")
    backdrop_colors_symbol_color: Optional[int] = Field(default=None, alias="backdropColorsSymbolColor")
    
    # Symbol info
    symbol_name: Optional[str] = Field(default=None, alias="symbolName")
    symbol_rarity_per_mille: Optional[int] = Field(default=0, alias="symbolRarityPerMille")
    symbol_rarity_name: Optional[str] = Field(default=None, alias="symbolRarityName")
    symbol_sticker_key: Optional[str] = Field(default=None, alias="symbolStickerKey")
    symbol_sticker_thumbnail_key: Optional[str] = Field(default=None, alias="symbolStickerThumbnailKey")
    
    # Pricing
    sale_price: int = Field(default=0, alias="salePrice")
    sale_price_without_fee: int = Field(default=0, alias="salePriceWithoutFee")
    floor_price_by_collection: Optional[int] = Field(default=None, alias="floorPriceNanoTONsByCollection")
    floor_price_by_backdrop_model: Optional[int] = Field(default=None, alias="floorPriceNanoTONsByBackdropModel")
    
    # Sale status
    is_on_sale: bool = Field(default=False, alias="isOnSale")
    is_on_auction: bool = Field(default=False, alias="isOnAuction")
    is_locked: bool = Field(default=False, alias="isLocked")
    is_locked_for_sale: bool = Field(default=False, alias="isLockedForSale")
    is_mine: bool = Field(default=False, alias="isMine")
    sales_count: int = Field(default=0, alias="salesCount")
    promote_end_at: Optional[str] = Field(default=None, alias="promoteEndAt")
    
    # Dates
    unlock_date: Optional[str] = Field(default=None, alias="unlockDate")
    next_resale_date: Optional[str] = Field(default=None, alias="nextResaleDate")
    next_transfer_date: Optional[str] = Field(default=None, alias="nextTransferDate")
    received_date: Optional[str] = Field(default=None, alias="receivedDate")
    export_date: Optional[str] = Field(default=None, alias="exportDate")
    next_give_available_at: Optional[str] = Field(default=None, alias="nextGiveAvailableAt")
    validate_regular_gift_at: Optional[str] = Field(default=None, alias="validateRegularGiftAt")
    return_locked_until: Optional[str] = Field(default=None, alias="returnLockedUntil")
    
    # Upgrade info
    total_upgraded_count: int = Field(default=0, alias="totalUpgradedCount")
    max_upgraded_count: int = Field(default=0, alias="maxUpgradedCount")
    
    # Type and status
    gift_type: Optional[str] = Field(default=None, alias="giftType")
    lucky_buy: bool = Field(default=False, alias="luckyBuy")
    craftable: bool = Field(default=False)
    is_crafted: bool = Field(default=False, alias="isCrafted")
    tg_can_be_crafted: bool = Field(default=False, alias="tgCanBeCrafted")
    minted: bool = Field(default=False)
    premarket_status: Optional[str] = Field(default=None, alias="premarketStatus")
    wait_gift_until: Optional[str] = Field(default=None, alias="waitGiftUntil")
    regular_gift_validation: Optional[str] = Field(default=None, alias="regularGiftValidation")
    return_lock_reason: Optional[str] = Field(default=None, alias="returnLockReason")
    
    # Platform status
    is_on_platform: bool = Field(default=True, alias="isOnPlatform")
    is_giveaway_received: bool = Field(default=False, alias="isGiveawayReceived")
    is_space_monkey: bool = Field(default=False, alias="isSpaceMonkey")
    space_monkeys_points: Optional[int] = Field(default=None, alias="spaceMonkeysPoints")
    
    class Config:
        populate_by_name = True
    
    @property
    def sale_price_ton(self) -> float:
        """Sale price in TON."""
        return self.sale_price / 1_000_000_000
    
    @property
    def sale_price_without_fee_ton(self) -> float:
        """Sale price without fee in TON."""
        return self.sale_price_without_fee / 1_000_000_000
    
    @property
    def floor_price_ton(self) -> Optional[float]:
        """Floor price in TON."""
        if self.floor_price_by_collection is None:
            return None
        return self.floor_price_by_collection / 1_000_000_000
    
    @property
    def model_rarity_percent(self) -> float:
        """Model rarity as percentage."""
        return (self.model_rarity_per_mille or 0) / 10
    
    @property
    def backdrop_rarity_percent(self) -> float:
        """Backdrop rarity as percentage."""
        return (self.backdrop_rarity_per_mille or 0) / 10
    
    @property
    def symbol_rarity_percent(self) -> float:
        """Symbol rarity as percentage."""
        return (self.symbol_rarity_per_mille or 0) / 10


class GiftList(BaseModel):
    """List of gifts with pagination."""
    items: List[Gift] = Field(default_factory=list, alias="gifts")
    total: int = 0
    cursor: Optional[str] = None
    
    class Config:
        populate_by_name = True


class PurchaseResult(BaseModel):
    """Result of a gift purchase."""
    user_gift: Optional[Gift] = Field(default=None, alias="userGift")
    price: int = 0
    
    class Config:
        populate_by_name = True
    
    @property
    def price_ton(self) -> float:
        """Price in TON."""
        return self.price / 1_000_000_000


class FeedItem(BaseModel):
    """Feed item model representing a market activity event."""
    type: str  # "listing", "sale", "change_price"
    id: str
    gift: Gift
    amount: int = 0
    date: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
    
    @property
    def amount_ton(self) -> float:
        """Amount in TON."""
        return self.amount / 1_000_000_000


class FeedResponse(BaseModel):
    """Response from the feed API."""
    items: List[FeedItem] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class SaleResult(BaseModel):
    """Result of selling gifts."""
    ids: List[str] = Field(default_factory=list)
    prices: List[int] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True
    
    @property
    def prices_ton(self) -> List[float]:
        """Prices in TON."""
        return [p / 1_000_000_000 for p in self.prices]
    
    def get_sale_info(self) -> List[dict]:
        """Get list of sale info as dicts with id and price."""
        return [
            {"id": gift_id, "price": price, "price_ton": price / 1_000_000_000}
            for gift_id, price in zip(self.ids, self.prices)
        ]


class SearchParams(BaseModel):
    """Parameters for gift search."""
    collection_names: List[str] = Field(default_factory=list, alias="collectionNames")
    model_names: List[str] = Field(default_factory=list, alias="modelNames")
    backdrop_names: List[str] = Field(default_factory=list, alias="backdropNames")
    symbol_names: List[str] = Field(default_factory=list, alias="symbolNames")
    ordering: str = "Price"
    low_to_high: bool = Field(default=True, alias="lowToHigh")
    max_price: Optional[int] = Field(default=None, alias="maxPrice")
    min_price: Optional[int] = Field(default=None, alias="minPrice")
    mintable: Optional[bool] = None
    number: Optional[int] = None
    count: int = 20
    cursor: str = ""
    query: Optional[str] = None
    promoted_first: bool = Field(default=False, alias="promotedFirst")
    
    class Config:
        populate_by_name = True
    
    def to_api_dict(self) -> dict:
        """Convert to API request format."""
        return {
            "collectionNames": self.collection_names,
            "modelNames": self.model_names,
            "backdropNames": self.backdrop_names,
            "symbolNames": self.symbol_names,
            "ordering": self.ordering,
            "lowToHigh": self.low_to_high,
            "maxPrice": self.max_price,
            "minPrice": self.min_price,
            "mintable": self.mintable,
            "number": self.number,
            "count": self.count,
            "cursor": self.cursor,
            "query": self.query,
            "promotedFirst": self.promoted_first,
        }
