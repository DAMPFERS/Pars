import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin, urlparse

# Crawler
class Crawler:
    def __init__(self):
        self.visited_urls = set()

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except requests.RequestException:
            return None

    def extract_links_and_text(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        links = set(urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True))
        return text, links

    def crawl(self, start_url, depth=2):
        to_crawl = {start_url}
        for _ in range(depth):
            new_urls = set()
            for url in to_crawl:
                if url not in self.visited_urls:
                    html = self.fetch_page(url)
                    if html:
                        text, links = self.extract_links_and_text(html, url)
                        Indexer().index_page(url, text)  # Index the page
                        new_urls.update(links)
                        self.visited_urls.add(url)
            to_crawl = new_urls

# Indexer
class Indexer:
    def __init__(self):
        self.conn = sqlite3.connect('search_index.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS word (
                                  id INTEGER PRIMARY KEY,
                                  word TEXT UNIQUE)''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS url (
                                  id INTEGER PRIMARY KEY,
                                  url TEXT UNIQUE)''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS word_index (
                                  word_id INTEGER,
                                  url_id INTEGER,
                                  position INTEGER,
                                  FOREIGN KEY (word_id) REFERENCES word(id),
                                  FOREIGN KEY (url_id) REFERENCES url(id))''')

    def index_page(self, url, text):
        url_id = self.get_or_create_url_id(url)
        words = text.split()
        for position, word in enumerate(words):
            word_id = self.get_or_create_word_id(word)
            self.index_word(word_id, url_id, position)

    def get_or_create_word_id(self, word):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM word WHERE word = ?', (word,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            cursor.execute('INSERT INTO word (word) VALUES (?)', (word,))
            return cursor.lastrowid

    def get_or_create_url_id(self, url):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM url WHERE url = ?', (url,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            cursor.execute('INSERT INTO url (url) VALUES (?)', (url,))
            return cursor.lastrowid

    def index_word(self, word_id, url_id, position):
        with self.conn:
            self.conn.execute('INSERT INTO word_index (word_id, url_id, position) VALUES (?, ?, ?)',
                              (word_id, url_id, position))







if __name__ == "__main__":
    start_url = "https://example.com"
    crawler = Crawler()
    crawler.crawl(start_url, depth=2)
    pass
