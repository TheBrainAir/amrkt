# amrkt

[![PyPI version](https://badge.fury.io/py/amrkt.svg)](https://badge.fury.io/py/amrkt)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Typing: typed](https://img.shields.io/badge/typing-typed-green.svg)](https://www.python.org/dev/peps/pep-0561/)

**Async Python library for mrkt marketplace**

A fast, type-safe, and secure library with automatic authentication handling.

## Features

- 🚀 **Async** - All operations are asynchronous
- 🔐 **Auto-authentication** - Token refresh handled automatically  
- 📦 **Type-safe** - Full Pydantic models with type hints
- 🎯 **Simple API** - Intuitive method names
- 🛡️ **Anti-detection** - Browser TLS fingerprint, headers, and User-Agent rotation

## Installation

```bash
pip install amrkt
```

Or install from source:

```bash
git clone https://github.com/thebrainair/amrkt.git
cd amrkt
pip install -e .
```

## Requirements

- Python 3.9+
- Telegram API credentials from [my.telegram.org](https://my.telegram.org/auth)

## Quick Start

```python
import asyncio
from amrkt import MarketClient

async def main():
    async with MarketClient(
        api_id=12345,               # Your API ID
        api_hash='your_api_hash',   # Your API hash
        session_name='my_session'   # Session file name
    ) as client:
        # Get user info
        user = await client.get_user_info()
        print(f"Hello, {user.full_name}!")
        
        # Check balance
        balance = await client.get_balance()
        print(f"Balance: {balance.hard_ton:.2f} TON")

asyncio.run(main())
```

## API Reference

### MarketClient

Main client class for interacting with the market API.

```python
MarketClient(
    api_id: int,                    # Telegram API ID
    api_hash: str,                  # Telegram API hash
    session_name: str = "amrkt",    # Pyrogram session name
    workdir: str = ".",             # Session file directory
    proxy: str = None,              # Optional: http://host:port, socks5://host:port
    proxy_api_only: bool = False,   # Use True if HTTP proxy gives 407
    impersonate: str = "chrome124", # TLS fingerprint (chrome99-chrome124, safari15_3, etc.)
    user_agent: str = None,         # Custom User-Agent (random by default)
)
```

---

### User Methods

#### `get_user_info() → UserInfo`

Get current user profile information.

```python
user = await client.get_user_info()

print(user.id)                    # User ID
print(user.full_name)             # Display name
print(user.is_vip)                # VIP status
print(user.wallet.ton)            # TON wallet address
print(user.ref_url)               # Referral URL
print(user.photo)                 # Avatar URL
print(user.wallet_for_payment)     # Payment wallet
print(user.server_time)           # Server timestamp
# Access config: user.configs, user.ref_coefs_dto
```

---

### Balance Methods

#### `get_balance() → Balance`

Get account balance information.

```python
balance = await client.get_balance()

# Raw values (in nanoTON)
print(balance.soft)         # Soft balance
print(balance.hard)         # Hard balance
print(balance.stars)        # Stars count

# Converted to TON (helper properties)
print(balance.soft_ton)     # Soft in TON
print(balance.hard_ton)     # Hard in TON
print(balance.total_hard_ton)  # Total hard in TON
```

#### `get_deposit_await() → List[DepositAwaitTransaction]`

Get pending deposit transactions awaiting confirmation.

```python
deposits = await client.get_deposit_await()

for dep in deposits:
    print(f"ID: {dep.id}")
    print(f"Type: {dep.currency_type}")    # "Hard" or "Soft"
    print(f"Value: {dep.value_ton:.2f} TON")
    print(f"Claimed: {dep.is_claimed}")
    print(f"Refunded: {dep.is_refunded}")
    print(f"Received: {dep.received_at}")
```

#### `claim_transaction(transaction_id) → List[ClaimTransactionResult]`

Claim a pending deposit transaction by its ID (from `get_deposit_await()`).

```python
deposits = await client.get_deposit_await()

for dep in deposits:
    if not dep.is_claimed:
        results = await client.claim_transaction(dep.id)
        for r in results:
            print(f"Claimed {r.value_ton:.2f} TON ({r.type})")
```

---

### Gift Methods

#### `search_gifts(...) → GiftList`

Search for gifts on sale with filters.

```python
gifts = await client.search_gifts(
    collection_names=["Lunar Snake"],   # Filter by collection
    model_names=["Albino"],             # Filter by model
    backdrop_names=[],                  # Filter by backdrop
    symbol_names=[],                    # Filter by symbol
    ordering="Price",                   # Sort: "Price", "Date"
    low_to_high=True,                   # Sort ascending
    min_price=None,                     # Min price (nanoTON)
    max_price=None,                     # Max price (nanoTON)
    count=20,                           # Results per page
    cursor="",                          # Pagination cursor
    query=None,                         # Search query
)

print(f"Found {gifts.total} gifts")
for gift in gifts.items:
    print(f"{gift.name}: {gift.sale_price_ton:.2f} TON")
```

#### `get_gift(gift_id) → Gift`

Get detailed information about a specific gift.

```python
gift = await client.get_gift("abc123")

print(gift.id)                  # Gift ID
print(gift.name)                # Gift name
print(gift.collection_name)     # Collection
print(gift.model_name)          # Model
print(gift.sale_price_ton)      # Price in TON
print(gift.is_on_sale)          # Sale status
print(gift.model_rarity_percent)  # Rarity %
```

#### `buy_gifts(gift_ids) → List[PurchaseResult]`

Purchase gifts by their IDs.

```python
results = await client.buy_gifts(["gift_id_1", "gift_id_2"])

for result in results:
    print(f"Bought: {result.user_gift.name}")
    print(f"Paid: {result.price_ton:.2f} TON")
```

---

### Inventory Methods

#### `get_inventory(...) → GiftList`

Get user's owned gifts. Accepts same parameters as `search_gifts()`.

```python
inventory = await client.get_inventory(
    count=50,
    ordering="Price",
    low_to_high=False
)

print(f"You own {inventory.total} gifts")
for gift in inventory.items:
    on_sale = "🟢 On sale" if gift.is_on_sale else "⚪ Not listed"
    print(f"{gift.name} - {on_sale}")
```

#### `return_gifts(gift_ids) → bool`

Return gifts back to Telegram.

```python
success = await client.return_gifts(["gift_id"])
if success:
    print("Gift returned successfully!")
```

---

### Sale Methods

#### `sell_gifts(gift_ids, prices) → SaleResult`

List gifts for sale on the market.

```python
# Sell a gift for 10 TON
result = await client.sell_gifts(
    ["gift_id_1"],           # List of gift IDs
    [10_000_000_000]         # Prices in nanoTON (10 TON)
)

# Multiple gifts at once
result = await client.sell_gifts(
    ["gift_id_1", "gift_id_2"],
    [5_000_000_000, 15_000_000_000]  # 5 TON and 15 TON
)

# Get confirmed info
for info in result.get_sale_info():
    print(f"Listed {info['id']} for {info['price_ton']:.2f} TON")
```

#### `cancel_sale(gift_ids) → List[str]`

Cancel sale listings and remove gifts from the market.

```python
# Cancel a single listing
cancelled = await client.cancel_sale(["gift_id_1"])

# Cancel multiple listings
cancelled = await client.cancel_sale(["gift_id_1", "gift_id_2"])
print(f"Cancelled {len(cancelled)} listings")
```

#### `change_price(gift_ids, prices) → SaleResult`

Change prices for gifts already listed for sale.

```python
# Update price to 15 TON
result = await client.change_price(
    ["gift_id_1"],
    [15_000_000_000]  # New price in nanoTON
)

# Update multiple prices
result = await client.change_price(
    ["gift_id_1", "gift_id_2"],
    [10_000_000_000, 20_000_000_000]
)

for info in result.get_sale_info():
    print(f"Updated {info['id']} to {info['price_ton']:.2f} TON")
```

---

### Offer Methods

#### `create_offer(gift_sale_id, price) → bool`

Create an offer for a gift on sale.

```python
# Make an offer of 2 TON on a gift
success = await client.create_offer(
    "gift_sale_id",          # Sale ID of the gift
    2_000_000_000            # Price in nanoTON (2 TON)
)
if success:
    print("Offer created!")
```

#### `cancel_offer(offer_id) → bool`

Cancel an existing offer by its ID.

```python
success = await client.cancel_offer("offer_id")
if success:
    print("Offer cancelled!")
```

---

### Feed Methods

#### `get_feed() → FeedResponse`

Get market activity feed including listings, sales, and price changes.

```python
feed = await client.get_feed()

for item in feed.items:
    print(f"[{item.type}] {item.gift.title}")
    print(f"  Price: {item.amount_ton:.2f} TON")
    print(f"  Date: {item.date}")
```

Item types:
- `listing` - New gift listed for sale
- `sale` - Gift was sold
- `change_price` - Price was changed

---

### Activities Methods

#### `get_activities(...) → List[ActivityItem]`

Get user activities.

```python
activities = await client.get_activities(offset=0, count=20, is_active=True)

for activity in activities:
    print(activity.type)
    print(activity.date)
    if activity.offer:
        print(f"Offer Price: {activity.offer.price_ton} TON")
```

---

## Data Models

### UserInfo

User profile from `GET /me` API.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | User ID |
| `account_id` | `Optional[int]` | Account ID |
| `user_ton_id` | `Optional[str]` | TON user ID |
| `registered_at` | `Optional[str]` | Registration date (ISO 8601) |
| `category` | `Optional[str]` | User category (e.g. "User") |
| `photo` | `Optional[str]` | Avatar URL |
| `full_name` | `str` | Display name |
| `ref_url` | `Optional[str]` | Referral URL |
| `invited_by` | `Optional[int]` | Inviter account ID |
| `wallet` | `Optional[Wallet]` | Wallet info |
| `allows_pm` | `bool` | Allow private messages |
| `current_language_code` | `Optional[str]` | Language code |
| `wallet_for_payment` | `Optional[str]` | Payment wallet address |
| `is_vip` | `bool` | VIP status |
| `payer_id` | `Optional[str]` | Payer ID |
| `server_time` | `Optional[str]` | Server timestamp (ISO 8601) |
| `in_game_link` | `Optional[str]` | In-game link base URL |
| `referral_revenue_coef` | `float` | Referral revenue coefficient |
| `giveaway_badge` | `Optional[str]` | Giveaway badge (e.g. "NoneBadge") |
| `channel_validation_bot_name` | `Optional[str]` | Channel validation bot |
| `configs` | `List[ConfigItem]` | App config key-value pairs |
| `ref_coefs_dto` | `Optional[RefCoefsDto]` | Referral coefficients by product type |
| `disable_withdrawal_limit` | `bool` | Withdrawal limit disabled |
| `disallowed_sections` | `List[str]` | Disallowed app sections |

### Wallet

| Field | Type | Description |
|-------|------|-------------|
| `ton` | `Optional[str]` | TON wallet address |
| `device_id` | `Optional[str]` | Device ID |

### ConfigItem

| Field | Type | Description |
|-------|------|-------------|
| `key` | `str` | Config key |
| `value` | `str` | Config value (may be JSON string) |

### RefCoefsDto

| Field | Type | Description |
|-------|------|-------------|
| `referral_coef` | `float` | General referral coefficient |
| `sticker_referral_coef` | `float` | Sticker referral coefficient |
| `not_games_referral_coef` | `float` | Not-games referral coefficient |
| `channel_referral_coef` | `float` | Channel referral coefficient |
| `gifts_collection_referral_coef` | `float` | Gifts collection referral coefficient |
| `stars_referral_coef` | `float` | Stars referral coefficient |
| `tg_premium_referral_coef` | `float` | Telegram Premium referral coefficient |

### Balance

| Field | Type | Description |
|-------|------|-------------|
| `soft` / `soft_ton` | `int` / `float` | Soft balance |
| `hard` / `hard_ton` | `int` / `float` | Hard balance |
| `stars` | `int` | Stars count |
| `spices` | `int` | Spices count |
| `friends_count` | `int` | Referral count |

### DepositAwaitTransaction

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Transaction ID (UUID) |
| `currency_type` | `str` | Currency type ("Hard" or "Soft") |
| `value` / `value_ton` | `int` / `float` | Value in nanoTON |
| `soft_value` | `int` | Soft value in nanoTON |
| `received_at` | `str` | Received timestamp (ISO 8601) |
| `is_claimed` | `bool` | Whether deposit was claimed |
| `is_refunded` | `bool` | Whether deposit was refunded |

### ClaimTransactionResult

| Field | Type | Description |
|-------|------|-------------|
| `value` / `value_ton` | `int` / `float` | Claimed amount in nanoTON / TON |
| `type` | `str` | Currency type ("hard" or "soft") |
| `source` | `Optional[str]` | Claim source |

### Gift

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Gift ID |
| `name` | `str` | Gift name |
| `gift_id` | `int` | Telegram gift ID |
| `gift_id_string` | `str` | Telegram gift ID as string |
| `number` | `int` | Gift number |
| `title` | `str` | Gift title |
| `collection_name` | `str` | Collection name |
| `collection_title` | `str` | Collection title |
| `model_name` | `str` | Model name |
| `model_title` | `str` | Model title |
| `model_rarity_per_mille` | `Optional[int]` | Model rarity (per mille), may be None |
| `model_rarity_name` | `str` | Model rarity name |
| `backdrop_name` | `str` | Backdrop name |
| `backdrop_rarity_per_mille` | `Optional[int]` | Backdrop rarity (per mille), may be None |
| `backdrop_rarity_name` | `str` | Backdrop rarity name |
| `symbol_name` | `str` | Symbol name |
| `symbol_rarity_per_mille` | `Optional[int]` | Symbol rarity (per mille), may be None |
| `symbol_rarity_name` | `str` | Symbol rarity name |
| `sale_price` / `sale_price_ton` | `int` / `float` | Sale price |
| `sale_price_without_fee` | `int` | Price without fee |
| `is_on_sale` | `bool` | Sale status |
| `is_on_auction` | `bool` | Auction status |
| `is_locked` | `bool` | Lock status |
| `is_mine` | `bool` | Ownership status |
| `sales_count` | `int` | Number of sales |
| `unlock_date` | `str` | Unlock date |
| `received_date` | `str` | Date received |
| `export_date` | `str` | Export date |
| `gift_type` | `str` | Gift type ("Upgraded", etc.) |
| `lucky_buy` | `bool` | Lucky buy status |
| `craftable` | `bool` | Craftable status |
| `is_crafted` | `bool` | Whether gift is crafted |
| `tg_can_be_crafted` | `bool` | Can be crafted in Telegram |
| `minted` | `bool` | Minted status |
| `premarket_status` | `str` | Premarket status |
| `model_rarity_percent` | `float` | Model rarity % (property) |
| `backdrop_rarity_percent` | `float` | Backdrop rarity % (property) |
| `symbol_rarity_percent` | `float` | Symbol rarity % (property) |

### FeedItem

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Event type: "listing", "sale", "change_price" |
| `id` | `str` | Event ID |
| `gift` | `Gift` | Gift object |
| `amount` / `amount_ton` | `int` / `float` | Price in nanoTON / TON |
| `date` | `datetime` | Event timestamp |

### FeedResponse

| Field | Type | Description |
|-------|------|-------------|
| `items` | `List[FeedItem]` | List of feed items |

### SaleResult

| Field | Type | Description |
|-------|------|-------------|
| `ids` | `List[str]` | List of gift IDs listed for sale |
| `prices` / `prices_ton` | `List[int]` / `List[float]` | Prices in nanoTON / TON |

---

## Exceptions

```python
from amrkt import (
    MarketError,              # Base exception
    AuthenticationError,      # Auth/token issues
    APIError,                 # API errors (has status_code)
    NotFoundError,            # Resource not found
    NotForSaleError,          # Gift not on sale
    InsufficientBalanceError, # Not enough TON
)
```

Example error handling:

```python
from amrkt import MarketClient, NotFoundError, APIError

try:
    gift = await client.get_gift("invalid_id")
except NotFoundError:
    print("Gift not found!")
except APIError as e:
    print(f"API error {e.status_code}: {e.response_text}")
```

---

## Advanced Usage

### Custom Session Directory

```python
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    session_name="my_bot",
    workdir="/path/to/sessions"
)
```

### Proxy (HTTP / SOCKS5)

Route all API requests and Telegram auth through a proxy. Supports HTTP and SOCKS5 with optional authentication.

```python
# HTTP proxy (no auth)
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    proxy="http://proxy.example.com:8080"
)

# HTTP proxy with auth
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    proxy="http://username:password@proxy.example.com:8080"
)

# SOCKS5 proxy with auth
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    proxy="socks5://user:password@proxy.example.com:1080"
)

# HTTP proxy with 407 error? Use proxy_api_only — proxy for API only, direct Telegram
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    proxy="http://user:pass@proxy.example.com:8080",
    proxy_api_only=True  # API via proxy, Telegram connection direct
)
```

### Anti-Detection (TLS Fingerprint & User-Agent)

All requests use browser-like headers, Cookie, and TLS fingerprint impersonation by default. You can customize the fingerprint and User-Agent:

```python
# Custom TLS fingerprint
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    impersonate="safari17_4_1"  # or "chrome120", "chrome124", etc.
)

# Custom User-Agent
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    user_agent="Mozilla/5.0 (Linux; Android 14; ...) Chrome/124.0.6367.82 Mobile Safari/537.36"
)

# Disable TLS impersonation
client = MarketClient(
    api_id=12345,
    api_hash="hash",
    impersonate=""  # Empty string disables it
)
```

### Pagination

```python
cursor = ""
all_gifts = []

while True:
    result = await client.search_gifts(
        collection_names=["Lunar Snake"],
        count=50,
        cursor=cursor
    )
    all_gifts.extend(result.items)
    
    if not result.cursor or len(result.items) < 50:
        break
    cursor = result.cursor

print(f"Loaded {len(all_gifts)} gifts total")
```

---

## License

MIT License - see [LICENSE](LICENSE) file.

