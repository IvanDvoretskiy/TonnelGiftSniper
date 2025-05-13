import logging

# API Configuration
API_CONFIG = {
    'BASE_URL': "https://gifts2.tonnel.network/api",
    'BUY_URL': "https://gifts.coffin.meme/api/buyGift/",
    'ENDPOINTS': {
        'SALE_HISTORY': "/pageGifts",
        'GIFT_FLOOR': "/giftFloor"
    },
    'HEADERS': {"Content-Type": "application/json"}
}

# Authentication
AUTH_DATA = "" # Your personal AUTH_DATA wich you can find on https://market.tonnel.network/
SECRET_KEY = "yowtfisthispieceofshitiiit" # Secter yousin by tonnel for create wtf

# Proxy Configuration (optional)
PROXY = {
    'http': 'http://user:pass@ip:port',  # Leave empty if not using proxy
    'https': 'http://user:pass@ip:port'  # Leave empty if not using proxy
}

# Analysis Parameters
ANALYSIS_PARAMS = {
    'WANTED_PROFIT_PERCENT': 120,  # Minimum profit % from average price
    'PRICE_LIMIT': 2,  # Max TON to spend per gift
    'WANTED_FLOOR_PROFIT': 30,  # Minimum profit % from floor price
    'PRICE_HISTORY_LIMIT': 30  # Number of historical prices to consider
}

# Logging Configuration
LOG_CONFIG = {
    'LEVEL': logging.INFO,
    'FORMAT': '%(message)s',
    'COLORS': {
        'INFO': '\033[96m',      # CYAN
        'WARNING': '\033[93m',   # YELLOW
        'ERROR': '\033[91m',     # RED
        'SUCCESS': '\033[92m',   # GREEN
        'HIGHLIGHT': '\033[95m'  # MAGENTA
    }
}