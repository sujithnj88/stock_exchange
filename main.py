import time, sys
from data_scrapper.nse_scrapper import NseScrapper


def main():
    exchange_handler = NseScrapper()
    data_frame_len = 0
    for i in range(1000):
        start = time.time()
        while data_frame_len == 0:
            exchange_handler.fetch_nse_data() 
            data_frame_len = exchange_handler.share_data_frame.size
            if data_frame_len > 0:
                data_frame_len = 0
                break
            time.sleep(5)
        end = time.time()
        print(exchange_handler.share_data_frame)
        with open("test_log.log", "a") as fp:
            fp.write(f"Trial {i} : {end - start} \n")

    exchange_handler.write_data_to_excel()


if __name__ == "__main__":
    sys.exit(main())