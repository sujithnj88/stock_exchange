import pandas as pd
import requests

from typing import List

from data_scrapper.data_classes import ShareAttributes, ShareVal


class NseScrapper:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': ('_ga=GA1.1.365959423.1723731899; '
                    '_ga_87M7PJ3R97=GS1.1.1723748675.3.1.1723748864.59.0.0; '
                    'bm_sv=608FB240C1615C9E3DBCEBC58836FDF9~YAAQBSozailCw0yRAQAAZVBwVxiTCk/pobfJwWxKyp3i9SnTC6qvo+bEYJbzfczSI8Rz5z++z1vu93r7v1dLhP41FPgQX0/VzVOD3AJaM39U/pqmH0VZ8Ue0HJrBTnHZdspfOS+6ntaDj6LPJp1GPKWwbe6wTLNVPqB6GGTXDd1OH6txtf5BHmuPHgz4Uj/h/Ac87766u3v7dWdXVdXpONFC28yFc3wg2U6/XWU9224685Pii5WrrfWBcg9RyFp0DcA=~1; '
                    'RT="z=1&dm=nseindia.com&si=56a47fda-3d2d-4ffa-89a2-f4c2fe534f6a&ss=lzvngdrg&sl=1&se=8c&tt=p1&bcn=%2F%2F684d0d45.akstat.io%2F"; '
                    'bm_sz=09E99064955C9C542476531FD80AAB15~YAAQBSozaghCw0yRAQAA8U1wVxgHgbvjBqJz276LVOJ1D3aCYRNLeAKEulGxWhYT+DGF7EHO71HvK5Pluy9YI6vbT4FeXYe977cApMZqWGsG3HhFV9XozsuliaWdQLo7fFXxiEryYvHFCfKgCD1KGG30Aq3xcsEAjzv+x6FCGyFxBv8NsntDIIsUat4ideY0OyUcgxE6/lPl/CnnXttRdQ3rSCHUdsZ3S+wmO+YNS3et5/x1tb9e7JsYtAushd6rflrC72Uelai4jMY/UDcU+VtUYCXTovpwEAtuF9WEWvnsAZmT5VkmcWc6rbXUdsE8aP0yyJ52nIwmO941Y+3l0elhLvzb/svFw61T6SOU2E0lLwh1mXIZ1IaTe2AgESzQbSOhOIkPAnOlUy4npJ1cLo176psnYcA=~3360312~4536642; '
                    'defaultLang=en; '
                    'nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcyMzc0ODg2MywiZXhwIjoxNzIzNzU2MDYzfQ.FmlNDxLGaeuZ9MoHlUZ9_7jGGpQQKg8hO0KYe7_0usY; '
                    'nsit=BJTzpGHGDxGXUU0CihaFfxRG; '
                    'ak_bmsc=398F31375CCE62C66B4DE8F19B1E4CC2~000000000000000000000000000000~YAAQBSozah4ew0yRAQAABI5tVxgPMeKzdJIjj+fEnxDlM4o6PAij9hUcI+ivdYYLPCwu+GQaK2zS+ooeX43Tqa6FN9gA1vngM7UPFZhPtsn2Aa3Y+8K9XT5ArMICYgtiuQJd4+zGYYm5PTs6KjtyRNAxGkOrrvTNJrO4bjucqA0RieA01N3R2CltzwW4YFIicN1p2Z1SD/9COFek38fYgqolQO/tul1IhDkP5mkPSFmKc8QXQramptBo6SetbmKo9faPvPriQrRKYVLVxw/P4nkm+h2S0i+LY8Wxr8IdVpsNgSqZLqM8NkghwA6BpoCNsjEcK07H0dsb0RcwiybFrK7YGbTq6fgnuSxSgJz6jSFZW62tcO/b08ZFIIuXG4WrCOb1W6qZEG+1kQh+wF6VESjzI/QAg671vAWDkKQk71ITILHbpxzpoE6quY8nWc6fl7d01HZgtlWJOMfkCgxK/oGtq7FFL6aSIt2K07HmVvpzzxPLQWG6OkrxWAEdWKrTnv7Ii4Sm7ergP3aZ/+At; '
                    'AKA_A2=A; '
                    'bm_mi=F1083B667767D53311BF6D706208362D~YAAQBSozavUdw0yRAQAAR4ptVxh7hxz1ykiy55r1qcrv8coA9CNdWvtjy9SfzBOPmp9n0KHRRBoX1Y+y1s374m2Zk3gETAXN74e+STopzBQoLaAQG0XDWUKKIjdAWEymMgOY1/fU1mFnbCgTnWQn0PQaZ/J75/pxCLB2R6enZyk8Qi5wi+TdsjTdREp+VleGT6N3UdH9nzpQdfCpbtD9dcMto27By/PeWYgXrfI0JAbuBl02jlOfGspPu35rxHkCdUbrxVPYl1/C9T6kmHvpZ3xHqIpVH4yGpkHlAAeDQ5ixsDgDjiRgu4SR28xU/8GTKXKSmz+y7z9i9DDe4PI7hhkjut8/aqGcuedzGepn~1; '
                    '_abck=7BD9E7BC0B915EE1E3E8DEFC486D12E2~0~YAAQBSozasscw0yRAQAA1m1tVwwq1gaSxSRtfUPA0KStynGsjapS+IgYmCLZ0ePDnK/1JKVC3uGbGoOtsG60yyraNzioyjjxQQo4iKTjwImWRVDdssHyGanHBmmJJ8m3otmpFTba49HvW/I7HdDNOjaqHe00ISmp8VWOq50KQl3vREtJKFTDqoPcKVzWd6qW4d4n/k+U7HOHbkIzUDkZHHXTpfh1wUCQJ2B4xYjNF4AznO1XecduVUdn/A0De/i6CW0UBh+LznQrCnqEm7l7EYAy9kfXq1lF6nONIi2JFmcVE1sId78iqfjvFa+HApybFz6F2R7CR0fN4k7pODymtjUHf25w7lDX3FRdILt2h/ry3rJb25bQchcErx46aGTtQT7buQEe8MmmixbuDHr200sby0abvQSjeLku~-1~-1~-1'),
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
        response = requests.get(self.url, headers=self.headers)
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
