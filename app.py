from lib import *
import re

while True:
    search_key = input("請輸入搜尋詞 (輸入 'off' 結束): ")
    if search_key.lower() == "off":
        print("\n程式結束，再見!")
        break

    try:
        # 初始化爬蟲類別並爬取資料
        crawler = DataCrawl(search_key)
        result = crawler.crawl()
        # 處理 blocks
        for key, value in result.items() :
            for block_key, block_value in value.items():
                if re.findall(r'^block', block_key):
                    print(block_value)
                else :
                    print("This is phrase")

    except Exception as e:
        print(f"\n發生錯誤: {e}")