
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re



headers = headers = {
                'authority': 'www.amazon.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'device-memory': '8',
                'downlink': '6.9',
                'dpr': '1.25',
                'ect': '4g',
                'rtt': '50',
                'sec-ch-device-memory': '8',
                'sec-ch-dpr': '1.25',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-viewport-width': '680',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'viewport-width': '680'
                }



storeId = "AZC5JQHYF9AQY"
currentPage = 1
while True:
    url = "https://www.amazon.com/s?i=merchant-items&me=" + storeId + "&page=" + str(currentPage)
    response = requests.get(url, headers=headers)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.findAll('div', {'data-component-type': 's-search-result'})

    itemsList = []
    for item in element:
        title = item.find(class_="a-size-medium a-color-base a-text-normal").text
        price = item.find(class_ = "a-offscreen").text
        stock = item.find(class_ = "a-size-base a-color-price").text
        stock = int(re.findall(r'\d+\.?\d*', stock)[0])
        url = item.find("a").get("href").split("/")
        urlId = url[2]
        if urlId =="dp":
            asin = url[3]
        else:
            continue
            
        # extract numerical values using regex
        newUrl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_ALL_mbc?asin=" + asin + "&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain"
        response = requests.get(newUrl, headers=headers)
        
        parse_only = SoupStrainer(class_="a-offscreen")
        soup2 = BeautifulSoup(response.content, "html.parser", parse_only=parse_only)
        try:
            buyBox = soup2.find(class_="a-offscreen").text
        except:
            continue
        itemInfo = [title, price, buyBox, stock, asin]
        # itemsList.append(itemInfo)
        print("\n\n\n")
        print("title: ", title)
        print("price: ", price)
        print("buybox: ", buyBox)
        print("stock: ", stock)
        print("asin: ", asin)
        
    if itemsList == []:
        break
        
    currentPage +=1
        
        
        
# #sort itemsList by stock
# itemsList.sort(key=lambda x: x[2], reverse= True)

# print(itemsList)

        