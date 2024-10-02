import sqlite3



def initialDataBase(addr):
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


def getOrCreateUrlId(cursor, url):
    cursor.execute('SELECT id FROM url WHERE url = ?', (url,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO url (url) VALUES (?)', (url,))
        return cursor.lastrowid


def getOrCreateWordId(cursor, word):
    cursor.execute('SELECT id FROM word WHERE word = ?', (word,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO word (word) VALUES (?)', (word,))
        return cursor.lastrowid


def indexWord(cursor, word_id, url_id, position):
        cursor.execute('INSERT INTO word_index (word_id, url_id, position) VALUES (?, ?, ?)',
                          (word_id, url_id, position))


def indexРage(url, text):
    conn = initialDataBase("C:\\PROGRAMS\\Python\\parsing\\Pars\\search_index.db")
    cur = conn.cursor()
    with conn:
        url_id = getOrCreateUrlId(cur, url)
        words = text.split()
        for position, word in enumerate(words):
            word_id = getOrCreateWordId(cur, text)
            indexWord(cur, word_id, url_id, position)


def main():
    a = "qwe\nrty     qazxsw\n         zxcvv"
    pass
    
   
        
        
        
        

if __name__ == "__main__":
    main()