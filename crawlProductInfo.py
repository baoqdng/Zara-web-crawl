#!/usr/bin/python
#import librabry
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

def soup(url):
    """
    This function is create request with requests lib.
    """
    headers = {
    'user-agent': 'Mozilla/5.0',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    request = requests.get(url, headers=headers)
    return BeautifulSoup(request.text, "html.parser") #create soup request



def findProductInfo(soup):
    """
    This function is use for find html product information
    """
    return soup.find("div", class_="product-detail-info")

def productInfoCrawl(findProductInfo):
    """
    This function is use for crawl product information
    """
    #product_name
    name = findProductInfo.find("h1", class_="product-detail-info__header-name").text
    #product_color
    color = findProductInfo.find("p", class_="product-detail-selected-color product-detail-info__color").text.split("|")[0]
    #product_price
    price = findProductInfo.find("span", class_="money-amount__main").text
    #Get product_size
    size = findProductInfo.find("ul", class_="product-detail-size-selector__size-list").text#.split(' " ')[:1]
    #Get product_describe
    describe = findProductInfo.find("div", class_="product-detail-description").find("p").text
    return [name, color, price, size, describe]

def findProductImg(soup):
    """
    This function is use for find product image
    """
    img = soup.find("div", class_="layout__content").find("script")
    return img.text

def productImageCrawl(findProductImg):
    """
    This function is use for crawl product image
    """
    # source = findProductImg
    # image = source[0]["image"]
    source = findProductImg[1:-1]
    source = json.loads(source)
    image = source["image"]
    return image

def productData(url):
    """
    This function is use for combine product information and product's image link
    """
    s = soup(url)
    pinfo = productInfoCrawl(findProductInfo(s))
    pimg = productImageCrawl(findProductImg(s))
    pinfo.append(pimg) #add list of image link to list contain product information
    #pdata = pd.DataFrame([pinfo], columns=["name", "color", "price", "size", "describe", "img_link"]) #[pinfo] make pandas understand pinfo is a row
    return pinfo


url = "https://www.zara.com/us/en/silver-metal-tray-p44535102.html?v1=187171624&v2=2124401"

data = productData(url)
df = pd.DataFrame([data], columns=["name", "color", "price", "size", "describe", "img_link"])
#df = df.append(productData(url))
print(df)

