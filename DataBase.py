import sqlite3



def initialDataBase(addr: str):
    """
    param addr:
    return: 
    """
    conn = sqlite3.connect(addr)
    cur = conn.cursor()
    with conn:
        cur.execute('''CREATE TABLE IF NOT EXISTS word (
                        id INTEGER PRIMARY KEY,
                        word TEXT UNIQUE)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS url (
                        id INTEGER PRIMARY KEY,
                        url TEXT UNIQUE)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS word_index (
                        word_id INTEGER,
                        url_id INTEGER,
                        position INTEGER,
                        FOREIGN KEY (word_id) REFERENCES word(id),
                        FOREIGN KEY (url_id) REFERENCES url(id))''')
        return conn
    return None


def getOrCreateUrlId(cursor, url: str) -> int:
    """
    param cursor:
    param url:
    return:
    """
    cursor.execute('SELECT id FROM url WHERE url = ?', (url,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO url (url) VALUES (?)', (url,))
        return cursor.lastrowid


def getOrCreateWordId(cursor, word:str) -> int:
    """
    param cursor:
    param url:
    return:
    """
    cursor.execute('SELECT id FROM word WHERE word = ?', (word,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO word (word) VALUES (?)', (word,))
        return cursor.lastrowid


def indexWord(cursor, word_id: int, url_id: int, position: int) -> None:
    """
    param cursor:
    param word_id:
    param url_id:
    param position:
    return: None
    """    
    cursor.execute('INSERT INTO word_index (word_id, url_id, position) VALUES (?, ?, ?)',
                          (word_id, url_id, position))
    return None


def indexРage(url: str, text: str) -> bool:
    """
    param text:
    param url:
    return: 
    """
    conn = initialDataBase("C:\\PROGRAMS\\Python\\parsing\\Pars\\search_index.db")
    if conn == None: return False
    cur = conn.cursor()
    with conn:
        url_id = getOrCreateUrlId(cur, url)
        words = text.split()
        for position, word in enumerate(words):
            word_id = getOrCreateWordId(cur, text)
            indexWord(cur, word_id, url_id, position)
    return True


def filterEnglishWords(word: str) -> bool:
    for char in word:
        if ('a' <= char <= 'z' or 'A' <= char <= 'Z'): return False
    return True

def main():
    a = "1234"
    print(filterEnglishWords(a))
    
   
        
        
        
        

if __name__ == "__main__":
    main()