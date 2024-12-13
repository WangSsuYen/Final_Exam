import tkinter as tk
from lib import *

def perform_search():
    search_key = input_entry.get()
    if not search_key.strip():
        output_label.config(text="請輸入有效的搜尋詞")
        return

    try:
        # 初始化爬蟲類別並爬取資料
        crawler = DataCrawl(search_key)
        result = crawler.crawl()
        output_label.config(text=result)
    except Exception as e:
        output_label.config(text=f"發生錯誤: {e}")

def add_entry():
    entry_data = input_entry.get()
    if not entry_data.strip():
        output_label.config(text="請輸入有效的資料")
        return

    try:
        # 新增資料到資料庫
        WordDatas.insert_word(entry_data)  # 假設使用 WordDatas 資料表
        output_label.config(text=f"成功新增: {entry_data}")
        input_entry.delete(0, tk.END)  # 清空輸入框
    except Exception as e:
        output_label.config(text=f"新增失敗: {e}")

def delete_entry():
    entry_data = input_entry.get()
    if not entry_data.strip():
        output_label.config(text="請輸入有效的資料")
        return

    try:
        # 檢查資料是否存在於資料庫
        if not WordDatas.word_exists(entry_data):  # 假設有 word_exists 方法
            output_label.config(text=f"刪除失敗: 資料 '{entry_data}' 不存在")
            return

        # 從資料庫刪除資料
        WordDatas.delete_word(entry_data)
        output_label.config(text=f"成功刪除: {entry_data}")
        input_entry.delete(0, tk.END)  # 清空輸入框
    except Exception as e:
        output_label.config(text=f"刪除失敗: {e}")

# 創建主視窗
root = tk.Tk()
root.title("翻譯介面")
root.geometry("600x400")
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
query_button = tk.Button(input_frame, text="查詢", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=perform_search)
query_button.pack(pady=5)

# 翻譯結果的框架
output_frame = tk.Frame(root, bg="#f7b84e", pady=20)
output_frame.pack(fill="both", expand=True)

# 結果框
output_label = tk.Label(output_frame, text="翻譯出來的文字內容", bg="#f7b84e", font=("Arial", 14))
output_label.pack(pady=10)

# 新增與刪除按鈕
buttons_frame = tk.Frame(output_frame, bg="#f7b84e")
buttons_frame.pack(pady=10, side="right", anchor="e")

add_button = tk.Button(buttons_frame, text="新增", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=add_entry)
add_button.pack(pady=5)

delete_button = tk.Button(buttons_frame, text="刪除", font=("Arial", 12), bg="#e0e0e0", relief="flat", width=8, command=delete_entry)
delete_button.pack(pady=5)

# 啟動主迴圈
root.mainloop()
