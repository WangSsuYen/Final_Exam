import tkinter as tk
from tkinter import messagebox, scrolledtext, Menu, Frame
import requests, re
from bs4 import BeautifulSoup
from lib import *  # 假設 DataCrawl 是在這裡定義的


# 顯示抓取資料的功能
def show_word_details(word_data):
    """將資料展示於 GUI 上的表格"""
    # 清空現有內容
    for widget in content_frame.winfo_children():
        widget.destroy()
    for widget in phrase_frame.winfo_children():
        widget.destroy()

    # 設置初始行數
    block_row = 0

    # 單字
    for key, value in word_data.items():
        tk.Label(content_frame, text=f"查詢字：{key}", font=("Arial", 20, "bold")).grid(row=block_row, column=0, columnspan=5, pady=10)
        block_row += 1
        for block_key, block_value in value.items():
            if re.findall(r'^block', block_key):
                # 各字段的顯示
                for label, field in [("詞類", "word_class"), ("描述", "description"), ("翻譯", "word_translation"),("例句", "example_sentence"), ("翻譯例句", "example_sentence_translation")]:
                    tk.Label(content_frame, text=label, font=("Arial", 12, "bold"), bg="#ffffff", relief='groove').grid(row=block_row, column=0, sticky="w", padx=10, pady=5)
                    tk.Label(content_frame, text=block_value.get(field, "N/A"), font=("Arial", 12), bg="#ffffff", wraplength=400).grid(row=block_row, column=1, sticky="w", padx=10, pady=5)
                    block_row += 1

                tk.Label(content_frame, text="-" * 100, font=("Arial", 12, "italic"), bg="#ffffff").grid(row=block_row, columnspan=2, pady=10)
                block_row += 1


    # 動態調整 phrase_frame 的位置
    content_frame.update_idletasks()  # 確保已完成布局
    content_frame_height = content_frame.winfo_height()  # 獲取 content_frame 的高度
    canvas.coords(phrase_window_id, 0, content_frame_height + 20)

    # 判斷是否有phrase
    has_phrase = any(re.match(r'^phrase', phrase_key) for key, value in word_data.items() for phrase_key in value)

    if has_phrase:
        phrase_row = 0
        tk.Label(phrase_frame, text="延伸學習", font=("Arial", 20, "bold"), bg="#e6f2ff").grid(row=phrase_row, column=0, columnspan=5, pady=10)
        phrase_row += 1
        # 片語
        for key, value in word_data.items():
            for phrase_key, phrase_value in value.items():
                if re.findall(r'^phrase', phrase_key):  # 如果是片語的資料
                    # 各字段的顯示
                    for label, field in [("片語", "phrase"), ("片語描述", "description"), ("片語翻譯", "word_translation"),("片語例句", "example_sentence"), ("片語翻譯例句", "example_sentence_translation")]:
                        tk.Label(phrase_frame, text=label, font=("Arial", 12, "bold"), bg="#e6f2ff", relief='groove').grid(row=phrase_row, column=0, sticky="w", padx=10, pady=5)
                        tk.Label(phrase_frame, text=phrase_value.get(field, "N/A"), font=("Arial", 12), bg="#e6f2ff", wraplength=400).grid(row=phrase_row, column=1, sticky="w", padx=10, pady=5)
                        phrase_row += 1

                    tk.Label(phrase_frame, text="-" * 100, font=("Arial", 12, "italic"), bg="#e6f2ff").grid(row=phrase_row, columnspan=2, pady=10)
                    phrase_row += 1

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



def _on_mouse_wheel(event):
    # Windows 和 Linux
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")



# 創建主視窗
root = tk.Tk()
root.title("翻譯小工具")
root.geometry("900x900")
root.configure(bg="#f7b84e")

#----------------------------- Menu bar-----------------------
menu_bar = Menu(root, bg="black", fg="white")
root.config(menu=menu_bar)

# "常用" Menu
common_menu = Menu(menu_bar, tearoff=0)
common_menu.add_command(label="Option 1")
common_menu.add_command(label="Option 2")
menu_bar.add_cascade(label="常用", menu=common_menu)

# "插入" Menu
insert_menu = Menu(menu_bar, tearoff=0)
insert_menu.add_command(label="Option 1")
insert_menu.add_command(label="Option 2")
menu_bar.add_cascade(label="插入", menu=insert_menu)

# "內容" Menu
content_menu = Menu(menu_bar, tearoff=0)
content_menu.add_command(label="Option 1")
content_menu.add_command(label="Option 2")
menu_bar.add_cascade(label="內容", menu=content_menu)
#----------------------------- Menu bar-----------------------

# --------------------------輸入區域的框架---------------------
input_frame = tk.Frame(root, bg="#f7b84e", pady=10)
input_frame.pack(fill="x")
# 輸入框
input_label = tk.Label(input_frame, text="翻譯文字", bg="#f7b84e", font=("Arial", 14), relief='groove').grid(row=0, column=0, padx=(10, 5), sticky="w")
input_entry = tk.Entry(input_frame, font=("Arial", 14))
input_entry.grid(row=0, column=1, padx=(10, 5), sticky="we")
query_button = tk.Button(input_frame, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=search_translation).grid(row=0, column=2, padx=(10, 5), sticky="we")
# 欄位高度隨字體變更
input_frame.columnconfigure(1, weight=1)
# --------------------------輸入區域的框架---------------------


#----------------- 顯示細節區域 - 使用 Canvas 和 Scrollbar-------
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

# 包裝 block 資料顯示的框架
content_frame = tk.Frame(canvas, bg="#ffffff", borderwidth=2, relief="groove")
content_window_id = canvas.create_window((0, 0), window=content_frame, anchor='nw')

# 包裝 phrase 資料顯示的框架
phrase_frame = tk.Frame(canvas, bg="#e6f2ff", borderwidth=2, relief="groove")
phrase_window_id = canvas.create_window((0, 500), window=phrase_frame, anchor='nw')


# 需要更新 canvas 的滾動區域大小
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# 滑鼠滾輪綁定到 canvas 的滾動
canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# 啟動主迴圈
root.mainloop()