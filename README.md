# Tonnel Marketplace Gift Auto-Trader

![Tonnel Marketplace](https://avatars.githubusercontent.com/u/157980243?s=200&v=4)

An automated trading bot that monitors and purchases Telegram gifts on Tonnel Marketplace when they meet specified profitability criteria.

## Key Features

- **Real-time Market Monitoring**: Instant detection of newly listed gifts
- **Dual-Price Analysis**: Compares against both historical sales and floor prices
- **Smart Purchasing**: Automated buying when all profit conditions are met
- **Secure Transactions**: Properly signed API requests with WTF token generation
- **Proxy Support**: Optional proxy configuration for request routing

## How It Works

### Monitoring Phase
1. Continuously polls Tonnel API for newly listed gifts
2. Filters out already processed and non-sale items
3. Logs each potential gift with detailed price information

### Analysis Phase
For each valid gift:
```python
# Price calculations (including 10% fee)
adjusted_last_price = last_sale_price * 1.1
adjusted_current_price = current_price * 1.1
adjusted_floor_price = floor_price * 1.1

# Profit calculations
average_profit = ((adjusted_last_price - adjusted_current_price) / adjusted_current_price) * 100
floor_profit = ((adjusted_floor_price - adjusted_current_price) / adjusted_current_price) * 100
```

### Purchase Decision
A gift is purchased when ALL conditions are met:
1. `average_profit ≥ WANTED_PROFIT_PERCENT`
2. `floor_profit ≥ WANTED_FLOOR_PROFIT`
3. `adjusted_current_price ≤ PRICE_LIMIT`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/IvanDvoretskiy/TonnelGiftSniper.git
cd TonnelGiftSniper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

## Configuration

### Required Settings (in `.env`):
```ini
AUTH_DATA=your_tonnel_auth_data  # From browser cookies at market.tonnel.network
SECRET_KEY=yowtfisthispieceofshitiiit  # Tonnel's signature key
```

### Optional Settings:
```ini
# Proxy Configuration
HTTP_PROXY=http://user:pass@ip:port
HTTPS_PROXY=http://user:pass@ip:port

# Trading Parameters
WANTED_PROFIT_PERCENT=120  # Minimum profit % from average
WANTED_FLOOR_PROFIT=30     # Minimum profit % from floor
PRICE_LIMIT=2              # Max TON to spend per gift
```

## Usage

```python
from tonnel_gift_trader import GiftAnalyzer

analyzer = GiftAnalyzer()
analyzer.run()  # Starts the automated trading process
```

## Sample Output
```
🎁 Analyzing gift: Diamond | Premium (ID: 42)
Price: 1.85 TON | Avg: 4.20 TON | Profit: 127% | Floor: 2.50 TON | Floor Profit: 35%
🚀 PURCHASE ATTEMPT: ID 42
Purchase result: {'status': 'success', 'gift_id': 42}
```

## Documentation Files

1. [API Reference](docs/API_REFERENCE.md) - Detailed endpoint specifications
2. [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
3. [Security Notes](docs/SECURITY.md) - Data handling and privacy information

