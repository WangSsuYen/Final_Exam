import os, sqlite3, requests, json
from typing import List, Union, Optional, Dict
from bs4 import BeautifulSoup



class WordDatas:
    """
    WordDatas 類別負責操作單字資料表的 CRUD 操作。
    """

    @staticmethod
    def initialize_database(db: str) -> List[str]:
        """
        初始化資料庫，建立必要的資料表。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :return: 狀態和訊息的列表，表示初始化結果。
        """
        if not os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS Word (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                english_word TEXT NOT NULL UNIQUE,
                                word_class TEXT NOT NULL,
                                chinese_translation TEXT NOT NULL,
                                word_description TEXT NOT NULL,
                                example_sentence TEXT,
                                example_sentence_translation TEXT  );''')
                conn.commit()
                return ["Success", "٩(⚙ᴗ⚙)۶ 資料庫建立完成"]

            except sqlite3.Error as error:
                return ["Error", f"ఠ_ఠ? 建立資料庫時發生錯誤：{error}"]

            finally:
                conn.close()



    @staticmethod
    def search_data(db: str, english_word: str) -> Optional[sqlite3.Row]:
        """
        查詢單字單元。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param english_word: 要查詢的英文單字名稱，型態為字串(str)。
        :return: 若存在則返回該單字的資料(sqlite3.Row)，否則返回 None。
        """
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Word WHERE english_word = ?;''', (english_word,))
        result = cur.fetchone()
        conn.close()
        return result



    @staticmethod
    def insert_word(db: str, data: dict) -> List[str]:
        """
        新增單字單元。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param data: 包含單字資料的字典。
        :return: 狀態和訊息的列表，表示新增結果。
        """
        if WordDatas.search_data(db, data["english_word"]):
            return ["Error", f"ఠ_ఠ? 單字 {data['english_word']} 已存在，無法新增。"]

        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''INSERT INTO Word (english_word, word_class, chinese_translation, word_description,
                            example_sentence, example_sentence_translation)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                        (data["english_word"], data["word_class"], data["chinese_translation"],
                         data["word_description"], data["example_sentence"], data["example_sentence_translation"]))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ {data['english_word']} 已成功加入資料庫！"]

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 新增資料時發生錯誤：{error}"]

        finally:
            conn.close()



    @staticmethod
    def delete_word(db: str, english_word: str) -> List[str]:
        """
        刪除單字單元。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param english_word: 要刪除的英文單字名稱，型態為字串(str)。
        :return: 狀態和訊息的列表，表示刪除結果。
        """
        if not WordDatas.search_data(db, english_word):
            return ["Error", f"ఠ_ఠ? 找不到 {english_word}，無法刪除。"]

        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''DELETE FROM Word WHERE english_word = ?;''', (english_word,))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ {english_word} 已刪除！"]

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 刪除資料時發生錯誤：{error}"]

        finally:
            conn.close()



    @staticmethod
    def update_word(db: str, english_word: str, updated_data: dict) -> List[str]:
        """
        更新單字資料單元。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param english_word: 要更新的英文單字名稱，型態為字串(str)。
        :param updated_data: 包含更新資料的字典，未提供的欄位將保持不變。
        :return: 狀態和訊息的列表，表示更新結果。
        """
        if not WordDatas.search_data(db, english_word):
            return ["Error", f"ఠ_ఠ? 找不到 {english_word}，無法更新。"]

        # 更新資料時保留未修改的值
        existing_data = WordDatas.search_data(db, english_word)
        updated_fields = {
            "word_class": updated_data.get("word_class", existing_data["word_class"]),
            "chinese_translation": updated_data.get("chinese_translation", existing_data["chinese_translation"]),
            "word_description": updated_data.get("word_description", existing_data["word_description"]),
            "example_sentence": updated_data.get("example_sentence", existing_data["example_sentence"]),
            "example_sentence_translation": updated_data.get("example_sentence_translation",
                                                             existing_data["example_sentence_translation"]),
        }

        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''UPDATE Word SET word_class = ?, chinese_translation = ?, word_description = ?,
                            example_sentence = ?, example_sentence_translation = ? WHERE english_word = ?;''',
                        (updated_fields["word_class"], updated_fields["chinese_translation"],
                         updated_fields["word_description"], updated_fields["example_sentence"],
                         updated_fields["example_sentence_translation"], english_word))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ {english_word} 已更新！"]

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 更新資料時發生錯誤：{error}"]

        finally:
            conn.close()




class ArticleData:
    """
    ArticleData 類別負責操作文章資料表的 CRUD 操作。
    """
    @staticmethod
    def initialize_database(db: str) -> None:
        """
        初始化資料庫，建立文章資料表。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        """
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS Article (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            article_source TEXT NOT NULL UNIQUE,
                            article_content TEXT NOT NULL,
                            content_translation TEXT NOT NULL,
                            content_picture BLOB);''')
            conn.commit()
        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 初始資料庫時發生錯誤：{error}"]
        finally:
            conn.close()



    @staticmethod
    def insert_article(db: str, data: dict) -> List[str]:
        """
        新增文章資料。

        :param db: 資料庫檔案的路徑，型態為字串。
        :param data: 包含文章資料的字典，應包含以下 key:
                    - article_source (str): 文章來源
                    - article_content (str): 文章內容
                    - content_translation (str): 文章翻譯
                    - content_picture (bytes): 文章圖片
        :return: 狀態和訊息的列表，表示新增結果。
        """
        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''INSERT INTO Article (article_source, article_content, content_translation, content_picture)
                           VALUES (?, ?, ?, ?)''',
                        (data['article_source'], data['article_content'],
                         data['content_translation'], data.get('content_picture')))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ 文章 {data['article_source']} 已成功加入！"]

        except sqlite3.IntegrityError:
            return ["Error", f"ఠ_ఠ? 文章 {data['article_source']} 已存在，無法新增！"]

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 新增文章時發生錯誤：{error}"]

        finally:
            conn.close()


    @staticmethod
    def search_article(db: str, article_source: str) -> Union[Dict[str, Union[str, bytes]], None]:
        """
        查詢文章資料。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param article_source: 要查詢的文章來源。
        :return: 包含文章資料的字典，若無結果則返回 None。
        """
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute('''SELECT * FROM Article WHERE article_source = ?;''', (article_source,))
            row = cur.fetchone()
            if row:
                return dict(row)
            return None

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 查詢文章時發生錯誤：{error}"]

        finally:
            conn.close()



    @staticmethod
    def update_article(db: str, article_source: str, updated_data: Dict[str, Union[str, bytes]]) -> List[str]:
        """
        更新文章資料。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param article_source: 要更新的文章來源。
        :param updated_data: 包含更新內容的字典。
        :return: 狀態和訊息的列表，表示更新結果。
        """
        if not ArticleData.search_article(db, article_source):
            return ["Error", f"ఠ_ఠ? 找不到文章 {article_source}，無法更新！"]

        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''UPDATE Article
                           SET article_content = ?, content_translation = ?, content_picture = ?
                           WHERE article_source = ?;''',
                        (updated_data['article_content'], updated_data['content_translation'],
                         updated_data.get('content_picture'), article_source))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ 文章 {article_source} 已更新！"]
        except sqlite3.Error as error:
            return ["Error", f"更新文章時發生錯誤：{error}"]
        finally:
            conn.close()



    @staticmethod
    def delete_article(db: str, article_source: str) -> List[str]:
        """
        刪除文章資料。

        :param db: 資料庫檔案的路徑，型態為字串(str)。
        :param article_source: 要刪除的文章來源。
        :return: 狀態和訊息的列表，表示刪除結果。
        """
        if not ArticleData.search_article(db, article_source):
            return ["Error", f"ఠ_ఠ? 找不到文章 {article_source}，無法刪除！"]

        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute('''DELETE FROM Article WHERE article_source = ?;''', (article_source,))
            conn.commit()
            return ["Success", f"٩(⚙ᴗ⚙)۶ 文章 {article_source} 已刪除！"]

        except sqlite3.Error as error:
            return ["Error", f"ఠ_ఠ? 刪除文章時發生錯誤：{error}"]

        finally:
            conn.close()


class DataCrawl:
    """
    網頁爬蟲
    """
    def __init__(self, search_key):
        self.url = f"https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{search_key}"
        self.headword = None
        self.part_of_speech = None
        self.definitions = []
        self.examples_en = []
        self.examples_zh = []
        self.translations = []


    def crawl(self):
        headers = {'User-Agent': 'Mozilla/5.0'} #反爬蟲機制
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 爬取 <span class="hw dhw">headword</span>
        self.headword = soup.find('span', class_='hw dhw').text

        # 2. 爬取 <span class="pos dpos" title="A word that refers to a person, place, idea, event or thing.">noun</span>
        self.block = [block.text for block in soup.find_all('div', class_='pr entry-body__el')]

        # # 3. 遍歷所有定義區塊（每個定義和範例句子可能有多個）
        # for def_block in soup.find_all('div', class_='def ddef_d db'):
        #     # 抓取每個定義的文本
        #     definition_text = def_block.text.strip()
        #     self.definitions.append(definition_text)

        #     # 查找對應的英文範例句子
        #     example_block = def_block.find_next('div', class_='examp dexamp')  # 找到範例句子區塊
        #     if example_block:
        #         # 可能有多個範例句
        #         for example in example_block.find_all('span', class_='eg deg'):
        #             self.examples_en.append(example.text.strip())

        #     # 查找對應的中文範例句子
        #     chinese_example_block = def_block.find_next('div', class_='examp dexamp')  # 可能在同一個區塊
        #     if chinese_example_block:
        #         for example in chinese_example_block.find_all('span', class_='trans dtrans'):
        #             self.examples_zh.append(example.text.strip())

        # # 4. 爬取翻譯
        # for trans in soup.find_all('span', class_='dtrans'):
        #     self.translations.append(trans.text.strip())


        # ----------------------拋出josn測試----------------------------
        data = {'title': str(self.block)}
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        with open('output.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
        # --------------------------------------------------------------

        return

    def to_dict(self):
        """
        將爬取的資料轉換為字典格式
        """
        data = {
            'headword': self.headword,
            'part_of_speech': self.part_of_speech,
            'definitions': self.definitions,
            'examples': {
                'english': self.examples_en,
                'chinese': self.examples_zh
            },
            'translations': self.translations
        }
        return data