# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 18:33:36 2022

@author: SRY
"""

#page_scraper for pakwheels.com

#importing required libraries
import requests as req
import time
#importing Beautiful Soup library to get readable data from raw HTML code
from bs4 import BeautifulSoup as soup
#importing Pandas library in order to store the derivated data (data derived from scrape)
import pandas as pd


def main():
    
    #main URL
    #we are interested to find the used car data in Islamabad only 
    base_url = 'https://www.pakwheels.com/used-cars/islamabad/24856?page='

    #our tickers
    #storing all the page numbers (~477) available in the base url, in a array.
    #The total count of vehicles will be (~11900)
    cars = []
    pages = range(1,2)
    for x in pages:
        cars.append(str(x))
    
    # a typical request would look like req.METHOD(url)   ; method = get or post
    res = req.get(base_url)
    
    #creating empty lists of our desired variables to use it for storing the output.
    price_list = []
    year_list = []
    capacity_list = []
    company_list = []
    variant_list = []
    
    #status code tells whether our request is succeeded or not
    # 200 - Succeess
    # 404 - Page not found
    # 400 - Generic error
    # 302 - Redirected
    print(f'[-] Status Code: {res.status_code}')
   
    #finding the desired variable values for each page (ticker)
    for ticker in cars:
        
        # making request for each page
        carpage = req.get(base_url+ticker)
        print(f'[-] Status Code: {carpage.status_code}')
        
        if carpage.status_code == 200:
            #we succeeded!
            
            # we are storing the page source upon which we will be working further
            # .text is that raw HTML code from the page that we will be using to find our desired data
            source = carpage.text
            
            # creating a beautiful sourp object, passing the raw text of our page aka source here
            # then we are using an html.parser out of many other parsers that beautiful soup has
            parsedpage = soup(source, 'html.parser')
            #print(parsedpage) 
            
            # now finding the exact location of our desired data
            # .text will actually find the text in that class and div
            
            #first we will find the desired broad region where all of our interested data lies
            subsource = parsedpage.find('div', class_='col-md-9 search-listing pull-right')
            #print(subsource)
            
            #now further shringking our scope to the base ROI (template)  aka base_source, where our data lies in a group. 
            base_source = subsource.find_all('div', class_='col-md-9 grid-style')
            
            #This base ROI is repeated multiple times (36X) per page containing data of various cars
            #Now iterating over all the base ROI existances and finding the desired variable values for each instance of base ROI
            for j in base_source[:36]:
                #now extracting the desired variables from the page
                
                #extracting make and model of car for example; (Suzuki Alto  2020 VXR for Sale)
                make_model = j.find('h3').text
                print(make_model)
                
                #extracting price of car
                car_price = j.find('div', class_='price-details generic-dark-grey').text
                print(car_price)
                
                #extracting model year and engine volume along with several un necesssary features
                info = j.find('ul', class_='list-unstyled search-vehicle-info-2 fs13').text
                print(info)

                #slicing for car price
                car_price = car_price.replace("\t", "")
                car_price = car_price.replace("\n", "")
                car_price = car_price.replace("PKR ", "")
                car_price = car_price.replace(" ", "")
                car_price = car_price.replace("lacs", "")
              
                #slicing of features in info 
                info = info.split('\n')
                info[4] = info[4].replace(' cc', "")

                make_model = j.find('h3').text
                model = make_model.split(' ')
                make_model = make_model.replace(info[1] + " ", "")
                make_model = make_model.replace(model[0] + " ", "")
                make_model_variant = make_model.replace(" for Sale", "")

                capacity_list.append(info[4])
                year_list.append(info[1])
                variant_list.append(make_model_variant)
                company_list.append(model[0])
                
                #updating our empty to store all output data in it
                price_list.append(car_price)
                
            #prints the url of each ticker/ page
            print(f'\t[-] {base_url+ticker}')
                                   
        else:
            # we failed!
            print(f'[x] Request to page {base_url+ticker} failed, status code: {carpage.status_code}')
        
        # wait for one second before putting a next request
        time.sleep(1)
    
    #printing out list values
    print(price_list)
    print(year_list)
    print(variant_list)
    print(company_list)
    print(capacity_list)
    
    #storing all of our variables array values into a csv file.    
    df = pd.DataFrame({ "Make":company_list, "Model":variant_list, "Year":year_list, "Engine":capacity_list, "Price":price_list})
    df.to_csv("scrap2.csv", index=False)
    
    return

if __name__=='__main__':
    main()
