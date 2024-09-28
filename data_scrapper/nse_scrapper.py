import pandas as pd
import requests

from typing import List

from data_scrapper.data_classes import ShareAttributes, ShareVal
from data_scrapper.cookie_generator import NseCookie


class NseScrapper:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': NseCookie().cookie.output(),
            'Host': 'www.nseindia.com',
            'Referer': 'https://www.nseindia.com/market-data/top-gainers-losers',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
        }
        self.url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'

        self.share_holder = ShareAttributes()

    @property
    def share_data_frame(self):
        return pd.DataFrame(self.share_holder.share_info)

    def write_data_to_excel(self):
        self.share_holder.share_info.sort(key=lambda x: x.change, reverse=True)
        pd.DataFrame(self.share_holder.share_info).to_excel("output.xlsx")

    def fetch_nse_data(self, filters: List[str] = ["NIFTYNEXT50", "SecGtr20"]):
        response = requests.get(self.url, headers=self.headers, timeout=60)
        print("Response Ready...")
        if response.status_code == 200:
            data = response.json()
            for _, share_info in {key: data[key].get("data") for key in filters if key in data}.items():
                for share in share_info:
                    volume = share.get("trade_quantity")
                    change = share.get("perChange")
                    if volume > 150000 and change > 5:
                        share_val_info = ShareVal(
                            name=share.get("symbol"),
                            open=share.get("open_price"),
                            high=share.get("high_price"),
                            low=share.get("low_price"),
                            prev_close=share.get("prev_price"),
                            ltp=share.get("ltp"),
                            change=change,
                            volume=volume,
                            value=share.get("turnover"),
                        )
                        if not share_val_info in self.share_holder.share_info:
                            self.share_holder.share_info.append(share_val_info)
