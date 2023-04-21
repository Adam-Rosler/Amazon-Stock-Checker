from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import random
import csv


class StockChecker():

    def __init__(self, storeId):
        # storeFront
        self.storeFront = None
        # grab all the asin elements from the store
        asinElements = self.scrapeAsinsFromStore(storeId)
        # grab the list of items and their corresponding data
        self.itemsList = self.parseAsin(asinElements)
        # sort items list by stock
        self.itemsList.sort(key=lambda x: x[3], reverse=True)
        # write to csv file
        self.writeToCsv(storeId)

    def generateHeader(self):
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

    def scrapeAsinsFromStore(self, storeId):
        # contains the elements of each product on a storefront
        itemElements = []

        # current page of the sellers store
        currentPage = 1

        # keep looping the pages
        while True:
            print("Checking store page: ", currentPage)
            url = "https://www.amazon.com/s?i=merchant-items&me=" + \
                storeId + "&page=" + str(currentPage)
            sellerPage = requests.get(url, headers=self.generateHeader())
            # Parse the HTML content of the page
            soup = BeautifulSoup(sellerPage.content, "html.parser")

            if currentPage == 1:
                # Find the storefront name and store it
                self.storeFront = soup.find('option').text

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

    def getTitle(self, element):
        title = element.find(
            class_="a-size-medium a-color-base a-text-normal").text
        return title

    def getPrice(self, element):
        price = element.find(class_="a-offscreen").text
        # remove the "$"
        price = price.replace("$", "")
        # convert to float
        price = float(price)

        return price

    def getStock(self, element):
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
            stock = 0
        return stock

    def getAsin(self, element):
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

    def getBuyBoxPrice(self, asin):
        # extract numerical values using regex
        newUrl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_ALL_mbc?asin=" + asin + \
            "&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain"
        # generate a header
        response = requests.get(newUrl, headers=self.generateHeader())
        # for speed, only parse this specific class containing the buybox
        parseOnly = SoupStrainer(class_="a-offscreen")
        soup2 = BeautifulSoup(
            response.content, "html.parser", parse_only=parseOnly)
        try:
            # grab the buybox price
            buyBox = soup2.find(class_="a-offscreen").text
            # remove the "$"
            buyBox = buyBox.replace("$", "")
            # convert to float
            buyBox = float(buyBox)
            return buyBox
        except:
            # if no buybox is found, it returns None
            return None

    def parseAsin(self, elements):
        # length of the elements
        itemsLength = len(elements)
        completed = 1
        # holds all the items information
        itemsList = []

        # loop through all the elements
        for element in elements:
            # print the status
            print("completed: ", str(completed) + "/" + str(itemsLength))
            # add to completed
            completed += 1
            # get the title
            title = self.getTitle(element)
            # get the price
            price = self.getPrice(element)
            # get the stock
            stock = self.getStock(element)
            # get the asin
            asin = self.getAsin(element)

            # check if asin is empty
            # continue if it is meaning no asin was found
            if asin == None:
                continue

            # gets the buybox
            buyBox = self.getBuyBoxPrice(asin)
            if buyBox == None:
                continue

            # check if the sellers price is within 5% of the buybox price
            upperBound = buyBox * 1.05
            if (price > upperBound):
                continue

            # create an item
            itemInfo = [title, price, buyBox, stock, asin]
            itemsList.append(itemInfo)

        return itemsList

    def writeToCsv(self, storeId):
        # Open a CSV file for writing
        with open(f'Store Front Data/{self.storeFront}-{storeId}.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(['Title', 'Price', 'Buy Box', 'Stock', 'ASIN'])

            # Write the data rows
            for item in self.itemsList:
                # Add the hyperlink formula to the Amazon URL column
                writer.writerow(item)


while True:
    storeId = input("Please enter a store ID: ")
    StockChecker(storeId)
