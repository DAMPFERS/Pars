import requests
from bs4 import BeautifulSoup as BS



#link_elements = soup.select("a[href]")

# urls = []
# for link_element in link_elements:
#     url = link_element["href"]
#     if "https:" in url:
#         urls.append(url)

# print(urls)






# print(soup.find("div", class_ = "main-events__grid js-main-events-grid").get_text())
# print()

# print(response.status_code)
# print(response.text)





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
    DEEP = 2
    current_URLs = ["https://www.nstu.ru/"]
    url_history = []
    for _ in range(DEEP):
        next_URLs = []
        for url in current_URLs:
            page = getPage(url)
            for link in page["Links"]:
                if link not in url_history: 
                    url_history.append(link)
                    next_URLs.append(link)
        current_URLs = next_URLs
        


if __name__ == "__main__":
    a = ["qwe"]
    b = ["qax", "qwe"]
    print(a[0] in b)
    # main()