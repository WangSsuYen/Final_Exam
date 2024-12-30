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

    # 資料庫新增操作
    current_word = WordDatas.search_data(db, list(word_data)[0])
    if current_word  == None:
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
    tk.Label(phrase_frame, text="延伸學習", font=("Arial", 18, "bold"), background='#e6f2ff').grid(row=phrase_row, column=0, columnspan=5, pady=10)
    phrase_row += 1
    for key, value in word_data.items():
        for phrase_key, phrase_value in value.items():
            if re.findall(r'^phrase', phrase_key):  # 找出 phrase 資料
                for label, field in [("片語", "phrase"), ("描述", "description"), ("翻譯", "word_translation"),("例句", "example_sentence"), ("翻譯例句", "example_sentence_translation")]:
                    tk.Label(phrase_frame, text=f"{label}:", font=("Arial", 12, "bold"),relief='groove', background='#e6f2ff').grid(row=phrase_row, column=0,sticky="e", padx=10, pady=10)
                    tk.Label(phrase_frame, text=phrase_value.get(field, "N/A"), font=("Arial", 12),wraplength=400, background='#e6f2ff').grid(row=phrase_row, column=1, sticky="w", padx=10,pady=5)
                    phrase_row += 1
                tk.Label(phrase_frame, text="-" * 100, font=("Arial", 12, "italic"), background='#e6f2ff').grid(row=phrase_row, column=0,columnspan=2, pady=10)
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


def search_translation(word=None):
    """查詢使用者輸入的翻譯文字"""
    if word is None:
        word = input_entry.get().strip().lower()

    # 清空舊有結果
    for widget in block_frame.winfo_children():
        widget.destroy()
    for widget in phrase_frame.winfo_children():
        widget.destroy()

    # 開始查詢
    crawler = DataCrawl(word)
    data = crawler.crawl()

    if isinstance(data, list) and data[0] == "Error":  # 當資料為錯誤時
        messagebox.showerror("查詢錯誤", f"ఠ_ఠ? 沒有你要找的單字 ： '{word}'")
    else:
        # 限制歷史紀錄
        if word not in history_word:
            if len(history_word) >= 15:
                history_word.pop(0)
            history_word.append(word)

        history_box.delete(0, tk.END)
        for word in history_word:
            history_box.insert(tk.END, word)

        show_word_details(data)


def on_history_select(event):
    """當歷史紀錄被選擇時，執行搜尋"""
    selected_index = history_box.curselection()
    if selected_index:
        selected_word = history_box.get(selected_index)
        search_translation(selected_word)





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
screen_width = root.winfo_screenwidth()
root.geometry(f"1200x{screen_height - 120}")
root.configure(bg="#ffffff")


# ----------------------歷史搜尋紀錄-------------------------
history_word = []


# -------------------修改ttk默認樣式-------------------------
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12), padding=[10, 5], background="#f0f0f0", foreground="#000000")
style.map("TNotebook.Tab", background=[("selected", "#ffa07a")], foreground=[("selected", "#ff0000")])


# -------------------創建 Notebook(活頁籤)--------------------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, pady=(10,10), padx=(10,10))


# ---------------------------查詢頁面---------------------------
query_page = ttk.Frame(notebook)
notebook.add(query_page, text="查詢頁面")


# --------------------------輸入區域的框架---------------------
input_frame = tk.Frame(query_page, bg="#f7b84e", pady=10)
input_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=5)

input_contain = tk.Frame(input_frame, pady=10, bg="#f7b84e")
input_contain.pack(expand=True)
input_label = tk.Label(input_contain, text="翻譯文字", bg="#f7b84e", font=("Arial", 14), relief='groove')
input_label.grid(row=0, column=0, padx=(10, 5), pady=(10,5), sticky="w")
input_entry = tk.Entry(input_contain, font=("Arial", 14))
input_entry.grid(row=0, column=1, padx=(10, 5), pady=(10,5), sticky="e")
query_button = tk.Button(input_contain, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=search_translation)
query_button.grid(row=0, column=2, padx=(10, 5), pady=(10,5), sticky="nse")


# --------------------------歷史搜尋紀錄區---------------------
history_frame = tk.Frame(query_page, bg="#f7b84e", pady=10)
history_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

history_contain = tk.Frame(history_frame, pady=10, bg="#f7b84e")
history_contain.pack(expand=True)
history_label = tk.Label(history_contain, text="歷史搜尋紀錄", bg="#f7b84e", font=("Arial", 14), relief='groove')
history_label.grid(row=0, column=0, padx=(10, 5), pady=(10,5), sticky="we")
history_box = tk.Listbox(history_contain, font=("Arial", 12), bg="#ffffff", fg="#000000", height=6, borderwidth=2, relief="groove")
history_box.grid(row=0, column=1, padx=(10, 5), pady=(10,5), sticky="we")
history_scrollbar = tk.Scrollbar(history_contain, orient="vertical", command=history_box.yview)
history_scrollbar.grid(row=0, column=2, pady=(10,5), sticky="ns")
history_box.config(yscrollcommand=history_scrollbar.set)

# 清單選擇
history_box.bind('<<ListboxSelect>>', on_history_select)


# ----------------- 顯示區域 - Canvas ------------------------
canvas_frame = tk.Frame(query_page, bg="#f7b84e")
canvas_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
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

# 綁定滾動事件
def bind_canvas_scroll(canvas):
    """綁定 Canvas 滾動事件"""
    canvas.bind("<Enter>", lambda _: root.bind_all("<MouseWheel>", lambda e: _on_mouse_wheel(canvas, e)))
    canvas.bind("<Leave>", lambda _: root.unbind_all("<MouseWheel>"))

bind_canvas_scroll(canvas_1)
bind_canvas_scroll(canvas_2)



# -------------------配置權重---------------------
query_page.rowconfigure(1, weight=1)  # Canvas 框架垂直權重
query_page.columnconfigure(1, weight=1)  # history_frame 水平權重
query_page.columnconfigure(0, weight=1)  # input_frame 水平權重

canvas_frame.columnconfigure(0, weight=1)  # block canvas 框架權重
canvas_frame.columnconfigure(2, weight=1)  # phrase canvas 框架權重
canvas_frame.rowconfigure(0, weight=1)    # canvas frame 垂直權重



# ---------------------------歷史紀錄頁面---------------------------
def on_tab_change(event):
    """當頁籤切換時執行動作"""
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]
    if selected_tab == "已學習單字":
        refresh_words_page()


def refresh_words_page():
    """刷新已學習單字頁籤內容"""
    for widget in content_frame.winfo_children():
        widget.destroy()  # 清空原有內容

    # 從資料庫重新獲取資料
    result = WordDatas.select_all(db)

    for key, value in result.items():
        # 標題
        title_area = tk.Label(content_frame, text=f'{key.upper()}', font=("Arial", 20, "bold"), bg="#333d51", fg="#ffffff", anchor="center", relief="groove")
        title_area.pack(fill="x", padx=5, pady=(15, 0))

        # 單字框架
        frame = tk.Frame(content_frame, bg="#cbd0d8", bd=2, relief="groove")
        frame.pack(fill="x", padx=5, pady=(0,15))

        # 渲染單字與按鈕
        rows, columns = 0, 0
        for individual_value in value:
            # 容器
            individual_contain = tk.Frame(frame, bg="#d3ac2b")
            individual_contain.grid(row=rows, column=columns + 1, padx=5, pady=5)

            # 單字顯示
            individual_entry = tk.Entry(individual_contain, bg="#d3ac2b", font=("Arial", 18), state='normal', width=15)
            individual_entry.insert(0, individual_value)
            individual_entry.config(state='readonly', justify='center')
            individual_entry.pack(side='top', padx=(5, 5), pady=(5, 5))

            # 觸發方法
            def on_button_click_search(entry_widget=individual_entry):
                """處理按鈕點擊事件，顯示 Entry 內的文字"""
                # 獲取 Entry 中的文字
                text = entry_widget.get()
                result = WordDatas.search_data(db, text)
                show_info_window(result)

            def on_button_click_update(entry_widget=individual_entry):
                """處理按鈕點擊事件，更新 Entry 內的文字"""
                # 獲取 Entry 中的文字
                text = entry_widget.get()
                result = WordDatas.search_data(db, text)
                revise_info_window(result)

            def on_button_click_remove(entry_widget=individual_entry):
                """處理按鈕點擊事件，刪除 Entry 內的文字"""
                # 獲取 Entry 中的文字
                text = entry_widget.get()
                # 資料庫刪除操作
                result = WordDatas.delete_word(db, text)
                if result[0] == "Error":
                    messagebox.showerror(result[0], result[1])
                else:
                    messagebox.showinfo(result[0], result[1])
                # 更新頁面
                refresh_words_page()


            # 修改與刪除按鈕
            inner_button1 = tk.Button(individual_contain, text="查看", bg="#00ffff", font=("Arial", 12), width=6, command=lambda e=individual_entry: on_button_click_search(e))
            inner_button1.pack(side="left", padx=(5,5))
            inner_button2 = tk.Button(individual_contain, text="修改", bg="#a9a9a9", font=("Arial", 12), width=6, command=lambda e=individual_entry: on_button_click_update(e))
            inner_button2.pack(side="left", padx=(5,5))
            inner_button3 = tk.Button(individual_contain, text="刪除", bg="#ff0000", font=("Arial", 12), width=6, command=lambda e=individual_entry: on_button_click_remove(e))
            inner_button3.pack(side="left", padx=(5,5))

            columns += 1
            if columns >= 4:
                rows += 1
                columns = 0

    # 更新滾動區域
    content_frame.update_idletasks()
    word_contain.config(scrollregion=word_contain.bbox("all"))


def show_info_window(result):
    """顯示帶有 Label 和 Entry 的自定義提示框"""
    # 創建一個新的 Toplevel 視窗作為提示框
    info_window = tk.Toplevel()
    info_window.title("詳細資訊")


    # 設置滾動條和畫布
    show_info_canvas = tk.Canvas(info_window)
    scroll_y = tk.Scrollbar(info_window, orient="vertical", command=show_info_canvas.yview)
    show_info_canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    show_info_canvas.pack(side="left", fill="both", expand=True)

    show_info_frame = tk.Frame(show_info_canvas, bd=5, relief='raised')
    show_info_canvas.create_window((0, 0), window=show_info_frame, anchor="nw")

    # 轉出字典
    description_data = eval(result['description'])

    # 顯示資料
    for block, data in description_data.items():
        if isinstance(data, dict):
            # 文字翻譯
            if re.findall(r'^block', block):
                word_class = data.get('word_class', '未知分類')
                color = "#191970"
                # 文字標籤
                tk.Label(show_info_frame, text=f"分類: {word_class}", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            else:
                phrase = data.get('phrase')
                color = '#ff0000'
                tk.Label(show_info_frame, text=f"片語: {phrase}", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")

            # 描述
            tk.Label(show_info_frame, text="描述:", font=("Arial", 12, 'bold'), wraplength=350, fg="white", bg=color, anchor='w', bd=5, relief='raised').pack(fill="x")
            description_entry = tk.Text(show_info_frame, font=("Arial", 12), height=4, bg="white", wrap="word", bd=0)
            description_entry.insert("1.0", data.get('description', 'N/A'))
            description_entry.config(state=tk.DISABLED)
            description_entry.pack(fill='x')

            # 翻譯
            if re.findall(r'^block', block):
                tk.Label(show_info_frame, text="翻譯:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
                translation_entry = tk.Text(show_info_frame, font=("Arial", 12), height=4, width=20, bg="white", wrap="word", bd=0)
                translation_entry.insert("1.0", data.get('word_translation', 'N/A'))
                translation_entry.config(state=tk.DISABLED)
                translation_entry.pack(fill="x")

            # 範例句子
            tk.Label(show_info_frame, text="範例句子:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            example_entry = tk.Text(show_info_frame, font=("Arial", 12), height=4, width=20, bg="white", wrap="word", bd=0)
            example_entry.insert("1.0", data.get('example_sentence', 'N/A'))
            example_entry.config(state=tk.DISABLED)
            example_entry.pack(fill="x")

            # 翻譯句子
            tk.Label(show_info_frame, text="翻譯句子:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            example_translation_entry = tk.Text(show_info_frame, font=("Arial", 12), height=4, width=20, bg="white", wrap="word", bd=0)
            example_translation_entry.insert("1.0", data.get('example_sentence_translation', 'N/A'))
            example_translation_entry.config(state=tk.DISABLED)
            example_translation_entry.pack(pady=(0, 15), fill="x")


    # 更新滾動區域
    show_info_frame.update_idletasks()
    show_info_canvas.config(scrollregion=show_info_canvas.bbox("all"))
    bind_canvas_scroll(show_info_canvas)


    # 設置確認按鈕
    def close_window():
        info_window.destroy()
    tk.Button(info_window, text="確認", command=close_window, font=("Arial", 12), bg="#8fbc8f").pack(padx=(10,10), pady=10)


    # 更新視窗大小的邏輯
    def update_window_size():
        info_window.update_idletasks()
        width = description_entry.winfo_width()
        info_window.geometry(f"{width + 100}x600")
    # 使用 after 延遲更新大小
    info_window.after(100, update_window_size)




def revise_info_window(result):
    """創建可修改文字的視窗"""
    # 創建新的 Toplevel 視窗
    info_window = tk.Toplevel()
    

    # 設置滾動條和畫布
    revise_info_canvas = tk.Canvas(info_window)
    scroll_y = tk.Scrollbar(info_window, orient="vertical", command=revise_info_canvas.yview)
    revise_info_canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    revise_info_canvas.pack(side="left", fill="both", expand=True)

    revise_info_frame = tk.Frame(revise_info_canvas, bd=5, relief='raised')
    revise_info_canvas.create_window((0, 0), window=revise_info_frame, anchor="nw")

    # 轉出字典
    description_data = eval(result['description'])
    print(description_data)


    for block, data in description_data.items():
        if isinstance(data, dict):
            # 文字翻譯
            if re.findall(r'^block', block):
                word_class = data.get('word_class', '未知分類')
                color = "#191970"
                # 文字標籤
                tk.Label(revise_info_frame, text=f"分類: {word_class}", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            else:
                phrase = data.get('phrase')
                color = '#ff0000'
                tk.Label(revise_info_frame, text=f"片語: {phrase}", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")

            # 描述
            tk.Label(revise_info_frame, text="描述:", font=("Arial", 12, 'bold'), fg="white", bg=color, anchor='w', bd=5, relief='raised').pack(fill="x")
            description_entry = tk.Text(revise_info_frame, font=("Arial", 12), height=4, bg="white", wrap="word", bd=0)
            description_entry.insert("1.0", data.get('description', 'N/A'))
            description_entry.pack(fill='x')

            # 翻譯
            if re.findall(r'^block', block):
                tk.Label(revise_info_frame, text="翻譯:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
                translation_entry = tk.Text(revise_info_frame, font=("Arial", 12), height=4, bg="white", wrap="word", bd=0)
                translation_entry.insert("1.0", data.get('word_translation', 'N/A'))
                translation_entry.pack(fill="x")

            # 範例句子
            tk.Label(revise_info_frame, text="範例句子:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            example_entry = tk.Text(revise_info_frame, font=("Arial", 12), height=4, bg="white", wrap="word", bd=0)
            example_entry.insert("1.0", data.get('example_sentence', 'N/A'))
            example_entry.pack(fill="x")

            # 翻譯句子
            tk.Label(revise_info_frame, text="翻譯句子:", font=("Arial", 12, 'bold'), anchor="w", fg="white", bg=color, bd=5, relief='raised').pack(fill="x")
            example_translation_entry = tk.Text(revise_info_frame, font=("Arial", 12), height=4, bg="white", wrap="word", bd=0)
            example_translation_entry.insert("1.0", data.get('example_sentence_translation', 'N/A'))
            example_translation_entry.pack(pady=(0, 15), fill="x")


    # 儲存按鈕，更新文字
    def save_changes():
        result['word_class'] = category_entry.get()  # 更新分類
        result['description'] = description_entry.get()  # 更新描述
        result['word_translation'] = translation_entry.get()  # 更新翻譯
        result['example_sentence'] = example_entry.get()  # 更新範例句子
        result['example_sentence_translation'] = example_translation_entry.get()  # 更新翻譯句子
        info_window.destroy()  # 關閉視窗

    save_button = tk.Button(info_window, text="儲存變更", command=save_changes, font=("Arial", 12), bg="#00ffff")
    save_button.pack(padx=(10,10), pady=(10,10))

    # 關閉視窗按鈕
    close_button = tk.Button(info_window, text="關閉", command=info_window.destroy, font=("Arial", 12), bg="#ff0000")
    close_button.pack(padx=(10,10), pady=(10,10))

    # 更新滾動區域
    revise_info_frame.update_idletasks()
    revise_info_canvas.config(scrollregion=revise_info_canvas.bbox("all"))
    bind_canvas_scroll(revise_info_canvas)


    # 更新視窗大小的邏輯
    def update_window_size():
        info_window.update_idletasks()
        width = description_entry.winfo_width()
        info_window.geometry(f"{width + 150}x600")
    # 使用 after 延遲更新大小
    info_window.after(100, update_window_size)
    # 設定抬頭
    info_window.title(f" {result['english_word']} 的修改頁面")



words_page = ttk.Frame(notebook)
notebook.add(words_page, text="已學習單字")

word_contain = tk.Canvas(words_page, bg="#a9a9a9")
word_contain.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
word_scrollbar = tk.Scrollbar(words_page, orient="vertical", command=word_contain.yview)
word_scrollbar.grid(row=0, column=1, pady=5, sticky="ns")
word_contain.config(yscrollcommand=word_scrollbar.set)

# 創建一個框架來放置所有內容
content_frame = tk.Frame(word_contain)
word_window_id = word_contain.create_window((0, 0), window=content_frame, anchor="nw")

# 動態調整 content_frame 寬度
def adjust_content_frame_width(event):
    canvas_width = event.width
    word_contain.itemconfig(word_window_id, width=canvas_width)

word_contain.bind("<Configure>", adjust_content_frame_width)

# 綁定滾動事件
bind_canvas_scroll(word_contain)

words_page.grid_rowconfigure(0, weight=1)
words_page.grid_columnconfigure(0, weight=1)

# 綁定頁籤切換事件
notebook.bind("<<NotebookTabChanged>>", on_tab_change)



# --------------------資料庫初始化---------------------------
result = WordDatas.init_db(db)
if result != None:
    messagebox.showerror(result[0], result[1])


root.mainloop()
