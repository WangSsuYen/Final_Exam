import tkinter as tk
import requests
from bs4 import BeautifulSoup

class DataCrawl:
    """
    網頁爬蟲
    """
    def __init__(self, search_key):
        self.url = f"https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{search_key}"
        self.word = {}

    def crawl(self):
        headers = {'User-Agent': 'Mozilla/5.0'}  # 反爬蟲機制
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 爬取 <span class="hw dhw">headword</span>
        headword = soup.find('span', class_='hw dhw').text if soup.find('span', class_='hw dhw') else None

        # 初始化區塊索引
        block_index = 1
        phrase_index = 1
        # 區塊
        blocks = {}

        # 2. 爬取每個區塊的資料
        for block in soup.find_all('div', class_='pr entry-body__el'):
            # 預抓詞類
            word_class = block.find('span', class_='pos dpos')

            for sub_block in block.find_all('div', class_='def-block ddef_block'):
                block_data = {}
                phrase_block = {}

                # 片語
                parent_block = sub_block.find_parent('div', class_=['pr phrase-block dphrase-block lmb-25', "pr phrase-block dphrase-block"])
                if parent_block:
                    # 片語
                    phrase_title = parent_block.find('span', class_='phrase-title dphrase-title')
                    phrase_block['phrase'] = phrase_title.text if phrase_title else 'N/A'

                    # 片語描述
                    description = sub_block.find('div', class_='def ddef_d db')
                    phrase_block['description'] = description.text if description else 'N/A'

                    # 片語翻譯
                    word_translation = sub_block.find('span', class_='dtrans')
                    phrase_block['word_translation'] = word_translation.text if word_translation else 'N/A'

                    # 片語例句
                    example_sentence = sub_block.find('span', class_='eg deg')
                    phrase_block['example_sentence'] = example_sentence.text if example_sentence else 'N/A'

                    # 片語例句翻譯
                    example_sentence_translation = sub_block.find('span', class_='trans dtrans dtrans-se hdb break-cj')
                    phrase_block['example_sentence_translation'] = example_sentence_translation.text if example_sentence_translation else 'N/A'

                    blocks[f'phrase{phrase_index}'] = phrase_block
                    phrase_index += 1

                else:
                    # 詞類
                    block_data['word_class'] = word_class.text if word_class else 'N/A'

                    # 描述
                    description = sub_block.find('div', class_='def ddef_d db')
                    block_data['description'] = description.text if description else 'N/A'

                    # 單字翻譯
                    word_translation = sub_block.find('span', class_='dtrans')
                    block_data['word_translation'] = word_translation.text if word_translation else 'N/A'

                    # 例句
                    example_sentence = sub_block.find('span', class_='eg deg')
                    block_data['example_sentence'] = example_sentence.text if example_sentence else 'N/A'

                    # 例句翻譯
                    example_sentence_translation = sub_block.find('span', class_='trans dtrans dtrans-se hdb break-cj')
                    block_data['example_sentence_translation'] = example_sentence_translation.text if example_sentence_translation else 'N/A'

                    # 將資料加入到 blocks 字典
                    blocks[f'block{block_index}'] = block_data
                    block_index += 1

        self.word[headword] = blocks
        print(self.word)      # 可選：用於檢查數據
        return self.word


# 顯示抓取資料的功能
def show_word_details(word_data):
    """將資料展示於 GUI 上的表格"""
    # 清空現有內容
    for widget in word_details_frame.winfo_children():
        widget.destroy()

    # 添加字彙類別
    tk.Label(word_details_frame, text="詞類", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Label(word_details_frame, text=word_data.get('word_class', 'N/A'), font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=5, pady=5)

    # 添加描述
    tk.Label(word_details_frame, text="描述", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Label(word_details_frame, text=word_data.get('description', 'N/A'), font=("Arial", 12), wraplength=400).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # 添加翻譯
    tk.Label(word_details_frame, text="翻譯", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tk.Label(word_details_frame, text=word_data.get('word_translation', 'N/A'), font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=5, pady=5)

    # 添加例句
    tk.Label(word_details_frame, text="例句", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    tk.Label(word_details_frame, text=word_data.get('example_sentence', 'N/A'), font=("Arial", 12)).grid(row=3, column=1, sticky="w", padx=5, pady=5)

    # 添加翻譯例句
    tk.Label(word_details_frame, text="翻譯例句", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", padx=5, pady=5)
    tk.Label(word_details_frame, text=word_data.get('example_sentence_translation', 'N/A'), font=("Arial", 12)).grid(row=4, column=1, sticky="w", padx=5, pady=5)

    # 在顯示資料的末尾進行換行
    tk.Label(word_details_frame, text="------", font=("Arial", 12, "italic")).grid(row=5, columnspan=2, pady=10)

# 查詢資料的函數
def search_translation():
    """查詢使用者輸入的翻譯文字"""
    input_word = input_entry.get().strip().lower()

    # 使用爬蟲類來抓取網頁資料
    crawler = DataCrawl(input_word)
    data = crawler.crawl()

    # 若爬取到的資料包含結果，則顯示
    if input_word in data:
        word_data = data[input_word]
        # 顯示資料
        for key, block_data in word_data.items():
            show_word_details(block_data)
    else:
        # 顯示無資料提示
        show_word_details({'word_class': 'N/A', 'description': 'No data found', 'word_translation': 'N/A', 'example_sentence': 'N/A', 'example_sentence_translation': 'N/A'})


# 創建主視窗
root = tk.Tk()
root.title("翻譯介面")
root.geometry("700x700")
root.configure(bg="#f7b84e")

# 輸入區域的框架
input_frame = tk.Frame(root, bg="#f7b84e", pady=10)
input_frame.pack(fill="x")

# 輸入框
input_label = tk.Label(input_frame, text="輸入翻譯文字", bg="#f7b84e", font=("Arial", 14))
input_label.pack(pady=5)
input_entry = tk.Entry(input_frame, font=("Arial", 14), width=40)
input_entry.pack()

# 查詢按鈕
query_button = tk.Button(input_frame, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=search_translation)
query_button.pack(pady=5)

# 顯示細節區域
word_details_frame = tk.Frame(root, bg="#f7b84e", pady=20)
word_details_frame.pack(fill="both", expand=True)

# 啟動主迴圈
root.mainloop()
