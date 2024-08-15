import sys
from data_scrapper.nse_scrapper import NseScrapper


def main():
    exchange_handler = NseScrapper()
    exchange_handler.fetch_nse_data()
    print(exchange_handler.share_data_frame)
    exchange_handler.write_data_to_excel()


if __name__ == "__main__":
    sys.exit(main())