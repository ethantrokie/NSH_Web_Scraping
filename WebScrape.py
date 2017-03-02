
## requires requests, pandas and BeautifulSoup libraries

import requests
import pandas as pd
from bs4 import BeautifulSoup

counter = 1 # counts page number
anotherPage = True
           
## function which gets data for one page   
def getData (website):
    page = requests.get(website) # retrieves html from site
    
    soup = BeautifulSoup(page.content, 'html.parser') 
    productgrid = soup.find(class_="productgrid")
    products = productgrid.select(".product")
    name = [product.find(class_="name").get_text() for product in products] # gets lists of Product IDs
    price = [product.find(class_="price").get_text() for product in products] # gets lists of prices
    swatch1 = [product.find(class_="swatch").get_text() for product in products] 
    Brand = [justBrand[7:50] for justBrand in swatch1] # gets lists of Brands
    swatch2 = [(product.find_all(class_="swatch"))[1].get_text() for product in products] # gets lists of Product Descriptions
    nextPage = productgrid.select(".lbtn")

    ## Puts data into panda dataframe and then export it to a csv file
    dataThing = pd.DataFrame({
            "Price": price, 
            "Product Description": swatch2,
            "Brand": Brand,
            "Product ID":name
        })
    cols = dataThing.columns.tolist()
    cols = ['Product ID', 'Brand', 'Price', 'Product Description']
    dataThing = dataThing[cols]
    dataThing.to_csv('tshirtPage'+str(counter)+'.csv', index = False)
    return nextPage


## loops through pages and puts data in csv files
while anotherPage:
    anotherPage = getData("https://www.ssactivewear.com/ps/t_shirts-raglan?Page="+str(counter))
    counter = counter+1
