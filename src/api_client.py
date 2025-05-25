import json
import logging
import time
from typing import List, Dict, Optional
import cloudscraper
from constants import API_CONFIG, PROXY, AUTH_DATA
from crypto_utils import generate_wtf

class APIClient:
    def __init__(self):
        self.scraper = self._init_scraper()
        self.base_url = API_CONFIG['BASE_URL']
        
    def _init_scraper(self):
        """Initialize cloudscraper instance with configuration."""
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            },
            delay=5
        )
        # Only set proxies if configured
        if PROXY.get('http') or PROXY.get('https'):
            scraper.proxies = {k: v for k, v in PROXY.items() if v}
        return scraper

    def _make_request(self, endpoint: str, payload: Dict) -> Optional[Dict]:
        """Generic method for making API requests."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.scraper.post(
                url,
                data=json.dumps(payload),
                headers=API_CONFIG['HEADERS']
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logging.error(f"API request failed: {e}")
            return None

    def get_sale_history(self, page: int = 1, limit: int = 30, **filters) -> List[Dict]:
        """Get gift sale history with optional filters."""
        filter_data = {
            "price": {"$exists": True},
            "refunded": {"$ne": True},
            "buyer": {"$exists": False},
            "export_at": {"$exists": True},
            "asset": "TON",
            **filters
        }
        payload = {
            "user_auth": AUTH_DATA,
            "page": page,
            "limit": limit,
            "filter": json.dumps(filter_data),
            "ref": 0,
            "sort": json.dumps({"message_post_time": -1, "gift_id": -1})
        }
        return self._make_request(API_CONFIG['ENDPOINTS']['SALE_HISTORY'], payload) or []

    def get_gift_floor(self, gift_name: str) -> float:
        """Get floor price for a specific gift."""
        payload = {
            "asset": "TON",
            "authData": AUTH_DATA,
            "gift_name": gift_name
        }
        response = self._make_request(API_CONFIG['ENDPOINTS']['GIFT_FLOOR'], payload)
        return response.get('floor', 0.0) if response else 0.0

    def buy_gift(self, gift_id: int, price: float) -> Dict:
        """Attempt to purchase a gift."""
        current_time = str(int(time.time()))
        payload = {
            "authData": AUTH_DATA,
            "asset": "TON",
            "price": price,
            "timestamp": current_time,
            "wtf": generate_wtf(current_time)
        }
        url = f"{API_CONFIG['BUY_URL']}{gift_id}"
        try:
            response = self.scraper.post(url, data=json.dumps(payload), headers=API_CONFIG['HEADERS'])
            return response.json() if response.status_code == 200 else {"status": "error"}
        except Exception as e:
            logging.error(f"Purchase failed: {e}")
            return {"status": "error", "message": str(e)}
