from lib import *

while True:
    search_key = input("請輸入搜尋詞 (輸入 'off' 結束): ")
    if search_key.lower() == "off":
        print("\n程式結束，再見!")
        break

    try:
        # 初始化爬蟲類別並爬取資料
        crawler = DataCrawl(search_key)
        result = crawler.crawl()

        print(result)

    except Exception as e:
        print(f"\n發生錯誤: {e}")