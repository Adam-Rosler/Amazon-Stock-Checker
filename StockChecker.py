from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import random


# generate a header
def generateHeader():
    # generate a random number
    randomNumber = str(random.randint(0, 9999999999))

    # create the header
    headers = {
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
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/' + randomNumber,
                    'viewport-width': '680'
    }

    return headers


# grabs all the asins off a given storefront
def scrapeAsinsFromStore(storeId):
    # contains the elements of each product on a storefront
    itemElements = []

    # current page of the sellers store
    currentPage = 1

    # keep looping the pages
    while True:
        print("Checking store page: ", currentPage)
        url = "https://www.amazon.com/s?i=merchant-items&me=" + \
            storeId + "&page=" + str(currentPage)
        sellerPage = requests.get(url, headers=generateHeader())
        # Parse the HTML content of the page
        soup = BeautifulSoup(sellerPage.content, "html.parser")
        itemElement = soup.findAll(
            'div', {'data-component-type': 's-search-result'})

        # check if it is empty
        # if it is, it is done scraping the catalog
        if itemElement == []:
            break
        # combine with the main elements list
        itemElements.extend(itemElement)

        # continue onto the next page
        currentPage += 1
    return itemElements


def getTitle(element):
    title = element.find(
        class_="a-size-medium a-color-base a-text-normal").text
    return title


def getPrice(element):
    price = element.find(class_="a-offscreen").text
    return price


def getStock(element):
    # try catch in case there does not exist a stock value
    # occurs when stock value is high
    try:
        # find the stock text
        stock = element.find(class_="a-size-base a-color-price").text
        # grab the numerical number
        stock = re.findall(r'\d+\.?\d*', stock)[0]
        # convert to an integer
        stock = int(stock)
    except:
        # if the stock is unknown/ not found
        stock = "unknown"
    return stock


def getAsin(element):
    # find the urls and splits them
    url = element.find("a").get("href").split("/")
    # this is to check if the url contains dp or gp, we only want dp
    urlId = url[2]
    if urlId == "dp":
        asin = url[3]
        return asin
    else:
        # return None if nothing is found
        return None


def getBuyBoxPrice(asin):
    # extract numerical values using regex
    newUrl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_ALL_mbc?asin=" + asin + \
        "&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain"
    # generate a header
    response = requests.get(newUrl, headers=generateHeader())
    # for speed, only parse this specific class containing the buybox
    parseOnly = SoupStrainer(class_="a-offscreen")
    soup2 = BeautifulSoup(
        response.content, "html.parser", parse_only=parseOnly)
    try:
        # grab the buybox price
        buyBox = soup2.find(class_="a-offscreen").text
        return buyBox
    except:
        # if no buybox is found, it returns None
        return None


# parses asin content given a asin elements list


def parseAsin(elements):
    # loop through all the elements
    for element in elements:
        # get the title
        title = getTitle(element)
        # get the price
        price = getPrice(element)
        # get the stock
        stock = getStock(element)
        # get the asin
        asin = getAsin(element)

        # check if asin is empty
        # continue if it is meaning no asin was found
        if asin == None:
            continue

        # gets the buybox
        buyBox = getBuyBoxPrice(asin)
        if buyBox == None:
            continue

        # create an item
        itemInfo = [title, price, buyBox, stock, asin]
        # itemsList.append(itemInfo)
        print("\n\n\n")
        print("title: ", title)
        print("price: ", price)
        print("buybox: ", buyBox)
        print("stock: ", stock)
        print("asin: ", asin)


storeId = input("Please enter the storeID: ")
asinElement = scrapeAsinsFromStore(storeId)
parseAsin(asinElement)


# #sort itemsList by stock
# itemsList.sort(key=lambda x: x[2], reverse= True)

# print(itemsList)
