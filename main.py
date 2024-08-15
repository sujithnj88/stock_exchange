import sys
from extract_nse_data import NseExchangeData


def main():
    exchange_handler = NseExchangeData()
    exchange_handler.fetch_nse_data()
    print(exchange_handler.share_data_frame)
    exchange_handler.write_data_to_excel()


if __name__ == "__main__":
    sys.exit(main())
