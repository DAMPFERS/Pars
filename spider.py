import requests
from bs4 import BeautifulSoup as BS


def _addrVerification(origin_url: str, addr: str) -> str:
    if "https://" in addr:
        prohibited_words = [".pdf", ".png", ".jpg", ".docx", ".xmls", "youtube", "tiktok", "rutube", "ok.ru", "t.me/", "zen.yandex.ru", "gosuslugi.", "vk.com"]  
        for i in prohibited_words: 
            if i in addr: return None
        return addr 
    elif addr[0] == '/': return str(origin_url) + addr
    else: return None


def getPage(url: str) -> dict:
    '''
    param url: словарь
    return: словарь из строки и списка, содержащий текс страницы по ключу "Text" и url адреса по ключу "Links"
    '''
    response = requests.get(url)
    soup = BS(response.content, "lxml")

    text = soup.get_text()

    urls = []
    for link in soup.find_all('a'):
        addr = link.get("href")
        res = _addrVerification(url, addr)
        if res != None: urls.append(res)
    return {"Text": text, "Links": urls}
        


def main():
    DEEP = 1
    current_URLs = ["https://www.nstu.ru/"]
    browsing_history = [] 
    for _ in range(DEEP):
        next_URLs = []
        for url in current_URLs:
            page = getPage(url)
            browsing_history.append(url)
            for link in page["Links"]:
                if link not in browsing_history: next_URLs.append(link)
        current_URLs = next_URLs
        


if __name__ == "__main__":
    main()