
from bs4 import BeautifulSoup
import requests

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






url = "https://www.amazon.com/s?i=merchant-items&me=" + "A1UYWNXLVQQ3CL"

response = requests.request("GET", url, headers=headers)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")
element = soup.findAll('div', {'data-component-type': 's-search-result'})
for i in element:
    n = i.find(class_="a-size-medium a-color-base a-text-normal")
    s = i.find(class_ = "a-offscreen")
    p = i.find(class_ = "a-size-base a-color-price")
    print(n.text, s.text, p.text)

