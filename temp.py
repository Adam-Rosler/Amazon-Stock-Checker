import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/cart?a=B001T4UMM2&colid=&coliid=&ctaDeviceType=desktop&ctaPageType=detail&quantity=99999"

headers = {
  'authority': 'www.amazon.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'application/x-www-form-urlencoded',
  'dnt': '1',
  'referer': 'https://www.amazon.com/gp/aw/d/B001T4UMM2/',
  'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

print(soup.text)