from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class ShareVal:
    name: str
    open: float
    high: float
    low: float
    prev_close: float
    ltp: float
    change: float
    volume: float
    value: float
    tc: float = 0.0
    pivot: float = 0.0
    bc: float = 0.0
    res_1: float = 0.0
    res_2: float = 0.0
    res_3: float = 0.0
    res_4: float = 0.0
    sup_1: float = 0.0
    sup_2: float = 0.0
    sup_3: float = 0.0
    sup_4: float = 0.0

    def __post_init__(self):
        self.open = float(self.open.replace(",", ""))
        self.high = float(self.high.replace(",", ""))
        self.low = float(self.low.replace(",", ""))
        self.prev_close = float(self.prev_close.replace(",", ""))
        self.ltp = float(self.ltp.replace(",", ""))
        self.value = float(self.value.replace(",", ""))

        self.pivot = (self.high + self.low + self.ltp) / 3
        self.bc = (self.high + self.low) / 2
        self.tc = 2 * self.pivot - self.bc

        self.res_1 = 2 * self.pivot - self.low
        self.res_2 = self.pivot + self.high - self.low
        self.res_3 = self.res_1 + self.high - self.low
        self.res_4 = self.res_3 + self.res_2 - self.res_1

        self.sup_1 = 2 * self.pivot - self.high
        self.sup_2 = self.pivot - self.high + self.low
        self.sup_3 = self.sup_1 - self.high + self.low
        self.sup_4 = self.sup_3 - self.sup_1 + self.sup_2


@dataclass
class ShareAttributes:
    share_info: list = field(default_factory=list)


class NseExchangeData:
    def __init__(self) -> None:
        options = Options()
        options.headless = True  # Run in headless mode
        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
        self.share_holder = ShareAttributes()
        self.driver.get("https://www.nseindia.com/market-data/top-gainers-losers")

    def __del__(self):
        self.driver.close()

    @property
    def share_data_frame(self):
        return pd.DataFrame(self.share_holder.share_info)

    def write_data_to_excel(self):
        self.share_holder.share_info.sort(key=lambda x: x.change, reverse=True)
        pd.DataFrame(self.share_holder.share_info).to_excel("output.xlsx")

    def fetch_nse_data(self):
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#topGainerTable"))
        )

        for elements in ["NIFTY NEXT 50", "Securities > Rs 20"]:
            drop_down = Select(self.driver.find_element(By.CSS_SELECTOR, r"#index0"))
            drop_down.select_by_visible_text(elements)

            script_data = self.driver.find_element(
                By.CSS_SELECTOR, r"#topgainer-Table > tbody:nth-child(2)"
            )
            share_data = script_data.text.split("\n")

            for data in share_data:
                data_attr = data.split(" ")
                volume = float(data_attr[7].replace(",", ""))
                change = float(data_attr[6].replace(",", ""))
                if volume > 150000 and change >= 5:
                    share_in_scope = ShareVal(
                            name=data_attr[0],
                            open=data_attr[1],
                            high=data_attr[2],
                            low=data_attr[3],
                            prev_close=data_attr[4],
                            ltp=data_attr[5],
                            change=change,
                            volume=volume,
                            value=data_attr[8],
                        )
                    if share_in_scope not in self.share_holder.share_info:
                        self.share_holder.share_info.append(
                            share_in_scope
                        )
