import tkinter as tk
from lib import *

# 新的展示資料功能
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

# 查詢和顯示資料
def display_fish_data():
    """顯示'fish'資料中所有包含的細節"""
    fish_data = {
        'block1': {'word_class': 'noun', 'description': 'an animal that lives in water, is covered with scales, and breathes by taking water in through its mouth, or the flesh of these animals eaten as food', 'word_translation': '魚;魚肉', 'example_sentence': 'Several large fish live in the pond.', 'example_sentence_translation': '池塘裡有幾條大魚。'},
        'phrase1': {'phrase': 'an odd/queer fish', 'description': 'a strange person', 'word_translation': 'N/A', 'example_sentence': "He's a bit of an odd fish, but I think he's basically sound.", 'example_sentence_translation': 'N/A'},
        'block2': {'word_class': 'verb', 'description': 'to try to find something, using your fingers to look for it', 'word_translation': '摸找，翻找，搜尋', 'example_sentence': 'She fished in her tool box for the right screwdriver.', 'example_sentence_translation': '她在工具箱裡翻找合適的螺絲刀。'},
        'block3': {'word_class': 'verb', 'description': 'to try to get something, without asking directly', 'word_translation': '拐彎抹角地引出；間接探聽', 'example_sentence': 'The director was fishing for information about our strategy.', 'example_sentence_translation': '那個主管正拐彎抹角地打聽我們的策略。'},
        'block4': {'word_class': 'verb', 'description': 'to catch fish from a river, sea, lake, etc., or to try to do this', 'word_translation': '捕（魚）;釣（魚）', 'example_sentence': "They're fishing for tuna.", 'example_sentence_translation': '他們在捕鮪魚。'},
        'phrase2': {'phrase': 'fished out', 'description': 'If an area of water has been fished out, all or most of the fish in it have been caught', 'word_translation': 'N/A', 'example_sentence': "There's no point going to an area that's fished out.", 'example_sentence_translation': 'N/A'}
    }

    for key, word_data in fish_data.items():
        show_word_details(word_data)

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
query_button = tk.Button(input_frame, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8)
query_button.pack(pady=5)

# 顯示細節區域
word_details_frame = tk.Frame(root, bg="#f7b84e", pady=20)
word_details_frame.pack(fill="both", expand=True)

# 顯示所有魚類資料按鈕
display_button = tk.Button(input_frame, text="顯示魚類資料", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=12, command=display_fish_data)
display_button.pack(pady=10)

# 啟動主迴圈
root.mainloop()
