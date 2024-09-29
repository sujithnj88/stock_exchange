import pandas as pd
import requests

from typing import List

from data_scrapper.data_classes import ShareAttributes, ShareVal


class NseScrapper:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
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
        response = self.session.get(self.url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            for _, share_info in {key: data[key].get("data") for key in filters if key in data}.items():
                for share in share_info:
                    volume = share.get("trade_quantity")
                    change = share.get("perChange")
                    if volume > 150000 and change > 2:
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
