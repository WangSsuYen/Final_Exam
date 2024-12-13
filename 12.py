import tkinter as tk
import requests, re
from bs4 import BeautifulSoup
from lib import *  # 假設 DataCrawl 是在這裡定義的


# 顯示抓取資料的功能
def show_word_details(word_data):
    """將資料展示於 GUI 上的表格"""
    # 清空現有內容
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # 設置初始行數
    row = 0

    # 檢查是否有 block 資料
    for key, value in word_data.items():
        for block_key, block_value in value.items():
            if re.findall(r'^block', block_key):
                # 添加字彙類別
                tk.Label(canvas_frame, text="詞類", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('word_class', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加描述
                tk.Label(canvas_frame, text="描述", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('description', 'N/A'), font=("Arial", 12), wraplength=400).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加翻譯
                tk.Label(canvas_frame, text="翻譯", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('word_translation', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加例句
                tk.Label(canvas_frame, text="例句", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('example_sentence', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加翻譯例句
                tk.Label(canvas_frame, text="翻譯例句", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('example_sentence_translation', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 在顯示資料的末尾進行換行
                tk.Label(canvas_frame, text="-------------------", font=("Arial", 12, "italic")).grid(row=row, columnspan=2, pady=10)
                row += 1

            # 片語
            else :
                # 添加字彙類別
                tk.Label(canvas_frame, text="片語", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('phrase', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加描述
                tk.Label(canvas_frame, text="片語描述", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('description', 'N/A'), font=("Arial", 12), wraplength=400).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加翻譯
                tk.Label(canvas_frame, text="片語翻譯", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('word_translation', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加例句
                tk.Label(canvas_frame, text="片語例句", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('example_sentence', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 添加翻譯例句
                tk.Label(canvas_frame, text="片語翻譯例句", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=5)
                tk.Label(canvas_frame, text=block_value.get('example_sentence_translation', 'N/A'), font=("Arial", 12)).grid(row=row, column=1, sticky="w", padx=5, pady=5)
                row += 1

                # 在顯示資料的末尾進行換行
                tk.Label(canvas_frame, text="--------------------", font=("Arial", 12, "italic")).grid(row=row, columnspan=2, pady=10)
                row += 1

    # 更新滾動區域範圍
    canvas.configure(scrollregion=canvas.bbox("all"))

# 查詢資料的函數
def search_translation():
    """查詢使用者輸入的翻譯文字"""
    input_word = input_entry.get().strip().lower()

    # 使用爬蟲類來抓取網頁資料
    crawler = DataCrawl(input_word)
    data = crawler.crawl()
    print(data)

    # 若爬取到的資料包含結果，則顯示
    show_word_details(data)


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

# 顯示細節區域 - 使用 Canvas 和 Scrollbar
canvas_frame = tk.Frame(root, bg="#f7b84e")
canvas_frame.pack(fill="both", expand=True)

# 創建 Canvas 和 Scrollbar
canvas = tk.Canvas(canvas_frame)
canvas.pack(side="left", fill="both", expand=True)

# 創建垂直滾動條
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# 將滾動條與 Canvas 綁定
canvas.configure(yscrollcommand=scrollbar.set)

# 包裝顯示內容的框架
content_frame = tk.Frame(canvas, bg="#f7b84e")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# 需要更新 canvas 的滾動區域大小
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# 啟動主迴圈
root.mainloop()