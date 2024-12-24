import tkinter as tk
from tkinter import messagebox, ttk
import re
from lib import *

db = "word_traslation.db"


def show_word_details(word_data):
    """顯示 word_data 資料在兩個 Canvas 中，block 在 canvas_1，phrase 在 canvas_2"""
    # 清空 canvas_1 和 canvas_2 的內容

    for widget in block_frame.winfo_children():
        widget.destroy()
    for widget in phrase_frame.winfo_children():
        widget.destroy()

    current_word = WordDatas.search_data(db, list(word_data)[0])
    if current_word  == None:
        # 新增單字置資料庫
        result = WordDatas.insert_word(db, word_data)
        if result[0] == "Error":
            messagebox.showerror(result[0], result[1])

    # 顯示 block 資料
    block_row = 0
    for key, value in word_data.items():
        tk.Label(block_frame, text=f"查詢字：{key}", font=("Arial", 18, "bold")).grid(row=block_row, column=0, columnspan=5, pady=10)
        block_row += 1
        for block_key, block_value in value.items():
            if re.findall(r'^block', block_key):  # 找出 block 資料
                for label, field in [("詞類", "word_class"), ("描述", "description"), ("翻譯", "word_translation"),("例句", "example_sentence"), ("翻譯例句", "example_sentence_translation")]:
                    tk.Label(block_frame, text=f"{label}:", font=("Arial", 12, "bold"),relief='groove').grid(row=block_row, column=0,sticky="e", padx=10, pady=10)
                    tk.Label(block_frame, text=block_value.get(field, "N/A"), font=("Arial", 12),wraplength=400).grid(row=block_row, column=1, sticky="w", padx=10,pady=5)
                    block_row += 1
                tk.Label(block_frame, text="-" * 100, font=("Arial", 12, "italic")).grid(row=block_row, column=0,columnspan=2, pady=10)
                block_row += 1

    # 顯示 phrase 資料
    phrase_row = 0
    tk.Label(phrase_frame, text="延伸學習", font=("Arial", 18, "bold")).grid(row=phrase_row, column=0, columnspan=5, pady=10)
    phrase_row += 1
    for key, value in word_data.items():
        for phrase_key, phrase_value in value.items():
            if re.findall(r'^phrase', phrase_key):  # 找出 phrase 資料
                for label, field in [("片語", "phrase"), ("描述", "description"), ("翻譯", "word_translation"),("例句", "example_sentence"), ("翻譯例句", "example_sentence_translation")]:
                    tk.Label(phrase_frame, text=f"{label}:", font=("Arial", 12, "bold"),relief='groove').grid(row=phrase_row, column=0,sticky="e", padx=10, pady=10)
                    tk.Label(phrase_frame, text=phrase_value.get(field, "N/A"), font=("Arial", 12),wraplength=400).grid(row=phrase_row, column=1, sticky="w", padx=10,pady=5)
                    phrase_row += 1
                tk.Label(phrase_frame, text="-" * 100, font=("Arial", 12, "italic")).grid(row=phrase_row, column=0,columnspan=2, pady=10)
                phrase_row += 1


    # 強制更新滾動區域，並且重新設定滾動範圍
    canvas_1.update_idletasks()
    canvas_2.update_idletasks()

    # 使用 after 延遲執行更新，確保資料顯示穩定
    root.after(100, lambda: update_scrollregion())


def update_scrollregion():
    """更新 Canvas 滾動範圍"""
    canvas_1.configure(scrollregion=canvas_1.bbox("all"))
    canvas_2.configure(scrollregion=canvas_2.bbox("all"))
    canvas_1.itemconfig(block_window_id, width=block_frame.winfo_width())
    canvas_2.itemconfig(phrase_window_id, width=phrase_frame.winfo_width())


def search_translation():
    """查詢使用者輸入的翻譯文字"""
    input_word = input_entry.get().strip().lower()

    # 清空舊有結果
    for widget in block_frame.winfo_children():
        widget.destroy()
    for widget in phrase_frame.winfo_children():
        widget.destroy()

    # 開始查詢
    crawler = DataCrawl(input_word)
    data = crawler.crawl()

    if isinstance(data, list) and data[0] == "Error":  # 當資料為錯誤時
        messagebox.showerror("查詢錯誤", f"ఠ_ఠ? 沒有你要找的單字 ： '{input_word}'")
    else:
        show_word_details(data)


def bind_canvas_scroll(canvas):
    """綁定 Canvas 滾動事件"""
    canvas.bind("<Enter>", lambda _: root.bind_all("<MouseWheel>", lambda e: _on_mouse_wheel(canvas, e)))
    canvas.bind("<Leave>", lambda _: root.unbind_all("<MouseWheel>"))


def _on_mouse_wheel(canvas, event):
    """根據滾輪事件滾動指定 Canvas"""
    # 判斷 event.delta 的正負，並根據操作系統調整
    if event.delta:  # Windows 滑鼠滾輪
        scroll_units = -1 * (event.delta // 120)
    else:  # macOS 滑鼠滾輪
        scroll_units = -1 * (event.delta // 3)

    canvas.yview_scroll(scroll_units, "units")



# 創建主視窗
root = tk.Tk()
root.title("翻譯小工具")
screen_height = root.winfo_screenheight()
root.geometry(f"1200x{screen_height - 120}")
root.configure(bg="#ffffff")

# -------------------修改ttk默認樣式-------------------------
style = ttk.Style()
style.configure("TNotebook.Tab",
                font=("Arial", 12),  # 設定字體、大小與樣式
                padding=[10, 5],           # 設定內距
                background="#f0f0f0",      # 頁籤背景顏色
                foreground="#000000")
style.map("TNotebook.Tab",
          background=[("selected", "#ffa07a")],  # 選中頁籤的背景顏色
          foreground=[("selected", "#ff0000")])  # 選中頁籤的文字顏色

# -------------------創建 Notebook(活頁籤)--------------------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, pady=(10,10), padx=(10,10))

# ---------------------------查詢頁面---------------------------
query_page = ttk.Frame(notebook)
notebook.add(query_page, text="查詢頁面")

# --------------------------輸入區域的框架---------------------
input_frame = tk.Frame(query_page, bg="#f7b84e", pady=10)
input_frame.pack(fill="x")
input_label = tk.Label(input_frame, text="翻譯文字", bg="#f7b84e", font=("Arial", 14), relief='groove').grid(row=0, column=0, padx=(10, 5), sticky="w")
input_entry = tk.Entry(input_frame, font=("Arial", 14))
input_entry.grid(row=0, column=1, padx=(10, 5), sticky="we")
query_button = tk.Button(input_frame, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=search_translation)
query_button.grid(row=0, column=2, padx=(10, 5), sticky="we")
input_frame.columnconfigure(1, weight=1)

# ----------------- 顯示區域 - Canvas ------------------------
canvas_frame = tk.Frame(query_page, bg="#f7b84e")
canvas_frame.pack(fill="both", expand=True)
# block
canvas_1 = tk.Canvas(canvas_frame, bg="#ffffff", borderwidth=2, relief="groove")
canvas_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
scrollbar_1 = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas_1.yview)
scrollbar_1.grid(row=0, column=1, sticky="ns")
canvas_1.configure(yscrollcommand=scrollbar_1.set)
# block設定
block_frame = tk.Frame(canvas_1, bg="#ffffff")
block_window_id = canvas_1.create_window((0, 0), window=block_frame, anchor='nw')
# phrase
canvas_2 = tk.Canvas(canvas_frame, bg="#e6f2ff", borderwidth=2, relief="groove")
canvas_2.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
scrollbar_2 = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas_2.yview)
scrollbar_2.grid(row=0, column=3, sticky="ns")
canvas_2.configure(yscrollcommand=scrollbar_2.set)
# phrase設定
phrase_frame = tk.Frame(canvas_2, bg="#e6f2ff")
phrase_window_id = canvas_2.create_window((0, 0), window=phrase_frame, anchor='nw')
# 動態調整布局
canvas_frame.columnconfigure(0, weight=1)
canvas_frame.columnconfigure(2, weight=1)
canvas_frame.rowconfigure(0, weight=1)
# 綁定滾動事件
bind_canvas_scroll(canvas_1)
bind_canvas_scroll(canvas_2)


# ---------------------------歷史紀錄頁面---------------------------
history_page = ttk.Frame(notebook)
notebook.add(history_page, text="歷史紀錄")


# --------------------資料庫初始化---------------------------
result = WordDatas.init_db(db)
if result != None:
    messagebox.showerror(result[0], result[1])


root.mainloop()
