import logging
import time
import json
from typing import Set, Dict
from colorama import Fore, Style
from constants import ANALYSIS_PARAMS, LOG_CONFIG, AUTH_DATA
from api_client import APIClient

class GiftAnalyzer:
    def __init__(self):
        if not AUTH_DATA:
            raise ValueError("AUTH_DATA must be configured in constants.py or .env")
            
        self.api = APIClient()
        self.processed_gifts = set()
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging with colors."""
        logging.basicConfig(level=LOG_CONFIG['LEVEL'], format=LOG_CONFIG['FORMAT'])

    @staticmethod
    def calculate_profit(current_price: float, reference_price: float) -> float:
        """Calculate profit percentage between two prices."""
        return ((reference_price - current_price) / current_price) * 100 if current_price else 0

    def analyze_gift(self, gift: Dict) -> bool:
        """Analyze a single gift for potential purchase."""
        gift_id = gift.get("gift_id")
        if not gift_id or gift_id in self.processed_gifts or gift.get("status") != "forsale":
            return False

        logging.info(f"{Fore.CYAN}🎁 Analyzing gift: {gift['name']} | {gift['model']} (ID: {gift_id})")
        
        try:
            # Get market data
            market_data = self.api.get_sale_history(
                limit=ANALYSIS_PARAMS['PRICE_HISTORY_LIMIT'],
                gift_name=gift["name"],
                model=gift["model"]
            )
            
            if not market_data:
                return False

            # Calculate prices and profits
            last_price = market_data[1]['price'] * 1.1
            current_price = gift['price'] * 1.1
            profit = self.calculate_profit(current_price, last_price)
            
            floor_price = self.api.get_gift_floor(gift['name']) * 1.1
            floor_profit = self.calculate_profit(current_price, floor_price)

            # Log analysis results
            logging.info(
                f"{Fore.YELLOW}Price: {current_price:.2f} TON | "
                f"{Fore.RED}Avg: {last_price:.2f} | "
                f"{Fore.GREEN}Profit: {profit:.2f}% | "
                f"{Fore.MAGENTA}Floor: {floor_price:.2f} | "
                f"{Fore.GREEN}Floor profit: {floor_profit:.2f}%"
            )

            # Check purchase conditions
            if (profit >= ANALYSIS_PARAMS['WANTED_PROFIT_PERCENT'] and 
                current_price <= ANALYSIS_PARAMS['PRICE_LIMIT'] and
                floor_profit >= ANALYSIS_PARAMS['WANTED_FLOOR_PROFIT']):
                return self._attempt_purchase(gift_id, gift['price'])
                
        except Exception as e:
            logging.error(f"{Fore.RED}Error processing gift {gift_id}: {e}")
        return False

    def _attempt_purchase(self, gift_id: int, price: float) -> bool:
        """Attempt to purchase a gift with retry logic."""
        logging.info(f"{Fore.LIGHTGREEN_EX}🚀 PURCHASE ATTEMPT: ID {gift_id}")
        
        for attempt in range(3):
            result = self.api.buy_gift(gift_id, price)
            if result.get('message') == 'Success':
                self._log_purchase(gift_id)
                return True
            time.sleep(1)
            
        return False

    def _log_purchase(self, gift_id: int):
        """Log successful purchases to file."""
        with open("bought_gifts.jsonl", "a") as f:
            json.dump({"gift_id": gift_id, "timestamp": int(time.time())}, f)
            f.write("\n")
        self.processed_gifts.add(gift_id)

    def run(self):
        """Main analysis loop."""
        while True:
            try:
                gifts = self.api.get_sale_history()
                for gift in gifts:
                    self.analyze_gift(gift)
                    time.sleep(1)
            except Exception as e:
                logging.error(f"{Fore.RED}Main loop error: {e}")
            time.sleep(1)
