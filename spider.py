import requests
from bs4 import BeautifulSoup as BS


def _addrVerification(origin_url: str, addr: str) -> str:
    '''
    param origin_url: базовый url адресс страницы, которая парситься 
    param addr: проверяемый url адресс
    return: url сайта в случае успеха, или None если адресс некорректный
    '''
    if "https://" in addr:
        prohibited_words = [".pdf", ".png", ".jpg", ".docx", ".xmls", "youtube", "tiktok", "rutube", "ok.ru", "t.me/", "zen.yandex.ru", "gosuslugi.", "vk.com"]  
        for i in prohibited_words: 
            if i in addr: return None
        return addr 
    elif addr[0] == '/': return str(origin_url) + addr
    else: return None


def getHTML(url: str) -> str:
    '''
    param url: URL адрес страницы
    return: текст HTML страницы в случае успеха или None в случае неудачи
    '''
    try:
        response = requests.get(url)
        if response.status_code() == 200: return response.text()
        else: return None
    except requests.RequestException:
        return None

def getPage(url: str, response: str) -> dict:
    '''
    param url: URL адрес страницы
    param response: текст HTML страницы
    return: словарь из строки и множества, содержащий текс страницы по ключу "Text" и url адреса по ключу "Links"
    '''
    soup = BS(response, "lxml")
    text = soup.get_text()

    urls = set()
    for link in soup.find_all('a'):
        addr = link.get("href")
        res = _addrVerification(url, addr)
        if res != None: urls.update(res)
    return {"Text": text, "Links": urls}
        

def main():
    DEEP = 1
    current_URLs = {"https://www.nstu.ru/"}
    browsing_history = set() 
    for _ in range(DEEP):
        next_URLs = set()
        for url in current_URLs:
            if url not in browsing_history:
                html = getHTML(url)
                if html:
                    page = getPage(url, html)
                    next_URLs.update(page["Links"])
                    browsing_history.add(url)
        current_URLs = next_URLs
        

if __name__ == "__main__":
    main()
    # help(BS.find_all)