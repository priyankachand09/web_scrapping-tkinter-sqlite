from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
main_urls = "http://books.toscrape.com/index.html"
result = requests.get(main_urls)
soup = BeautifulSoup(result.text, "html.parser")
main_url = "http://books.toscrape.com/"


def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

# extracting category url for pages


categories_urls = [main_url +x.get('href') for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
categories_urls = categories_urls[1:]
print(categories_urls)

# extracting page url
pages_urls = []
new_page = "http://books.toscrape.com/catalogue/page-1.html"
while requests.get(new_page).status_code == 200:
    pages_urls.append(new_page)
    new_page = pages_urls[-1].split("-")[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"

def getBooksURLs(url):
    soup = getAndParseURL(url)
    # remove the index.html part of the base url before returning the results
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])

# extracting books url
booksURLs = []
for page in pages_urls:
    booksURLs.extend(getBooksURLs(page))
# declaring list that are used
names = []
prices = []
nb_in_stock = []
img_urls = []
categories = []
ratings = []
book_number = []
i = 1
# scrape data for every book URL
for url in booksURLs:

    soup = getAndParseURL(url)

    # product name
    names.append(soup.find("div", class_=re.compile("product_main")).h1.text)
    # product price
    prices.append(soup.find("p", class_="price_color").text[2:])  # get rid of the pound sign
    # number of available products
    nb_in_stock.append(
        re.sub("[^0-9]", "", soup.find("p", class_="instock availability").text))  # get rid of non numerical characters
    # image url
    img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
    # product category
    categories.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])
    # ratings
    ratings.append(soup.find("p", class_=re.compile("star-rating")).get("class")[1])
    book_number.append(i)
    i = i + 1
##converting data to dataframe
new_data = pd.DataFrame(
    {'BOOK_ID': book_number, 'NAME': names, 'PRICE': prices, 'NB_IN_STOCK': nb_in_stock, "URL_IMG": img_urls,
     "PRODUCT_CATEGORY": categories,"RATING": ratings})
new_data = new_data.set_index('BOOK_ID')
print(new_data.head())
# saving data in csv file
new_data.to_csv("books_data.csv")

