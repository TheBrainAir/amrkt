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
    workdir: str = "."              # Session file directory
)
```

---

### User Methods

#### `get_user_info() → UserInfo`

Get current user profile information.

```python
user = await client.get_user_info()

print(user.id)              # User ID
print(user.full_name)       # Display name
print(user.is_vip)          # VIP status
print(user.wallet.ton)      # TON wallet address
print(user.ref_url)         # Referral URL
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

## Data Models

### UserInfo

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | User ID |
| `full_name` | `str` | Display name |
| `wallet` | `Wallet` | Wallet info |
| `is_vip` | `bool` | VIP status |
| `ref_url` | `str` | Referral URL |

### Balance

| Field | Type | Description |
|-------|------|-------------|
| `soft` / `soft_ton` | `int` / `float` | Soft balance |
| `hard` / `hard_ton` | `int` / `float` | Hard balance |
| `stars` | `int` | Stars count |
| `spices` | `int` | Spices count |
| `friends_count` | `int` | Referral count |

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
| `model_rarity_per_mille` | `int` | Model rarity (per mille) |
| `backdrop_name` | `str` | Backdrop name |
| `backdrop_rarity_per_mille` | `int` | Backdrop rarity (per mille) |
| `symbol_name` | `str` | Symbol name |
| `symbol_rarity_per_mille` | `int` | Symbol rarity (per mille) |
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
| `premarket_status` | `str` | Premarket status |
| `model_rarity_percent` | `float` | Model rarity % (property) |
| `backdrop_rarity_percent` | `float` | Backdrop rarity % (property) |
| `symbol_rarity_percent` | `float` | Symbol rarity % (property) |

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

