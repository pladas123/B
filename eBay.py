import re
import requests
import time
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import json
import pandas as pd
import csv

ebay_url = "https://www.ebay.co.uk/sch/i.html?_nkw=" # static

class URLs():
    def __init__(self, sku):
        self.target_ebay = ""
        self.URL_fixer(self.sku)
        
    def URL_fixer(self, sku):
        self.target_ebay = ebay_url + str(self.sku) + "&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=4000" # vary list returned

class eBay_request(): # finished
    
    def __init__(self, target_ebay):
        self.temp_price = ""
        self.offer_list = {'e1':"",'e2':"",'e3':"",'e4':"",'e5':""}
        self.target_ebay = target_ebay
        self.val_extract(self.target_ebay)
        
    def val_extract(self, url):
        output = requests.get(url, headers = {"User Agent" : user_agent})
        soup = BeautifulSoup(output.content, "lxml")
        self.body = soup.body

    def collect(self):
        counter = 0
        while counter <5: # get five most recent results
            entry_key = 'e' + str((counter+1))
            temp_price = self.body.findAll("span", {"class" : "bold bidsold"})
            self.trans_price = temp_price[counter].getText()
            self.price_reg = re.sub("[^0-9\.]", "", self.trans_price)
            self.offer_list[entry_key] = self.price_reg
            counter += 1
        #print("eBay : " + str(self.offer_list))
        return self.offer_list

if __name__ == "__main__":
    data_collect()
