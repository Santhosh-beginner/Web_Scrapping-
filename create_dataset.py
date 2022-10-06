from requests_html import HTMLSession
import pandas as pd
#search link for product u can change it as your wish.
url = 'https://www.amazon.in/s?k=earbuds&crid=19ZUAAA3XTO3Q&sprefix=earbuds%2Caps%2C219&ref=nb_sb_noss_1'

s = HTMLSession()
r = s.get(url)
r.html.render(sleep=1)
items = r.html.find('div[data-asin]')

asins = []

for item in items:
    if item.attrs['data-asin'] != '':
        asins.append(item.attrs['data-asin'])
print(asins)

products = []

for asin in asins:
    url = f'https://www.amazon.in/dp/{asin}'
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    if(r.html.find('#productTitle', first=True)!= None):
      title = r.html.find('#productTitle', first=True).full_text.strip()
    else:
        title=" "
    if(r.html.find('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay', first=True)!=None):
        price = r.html.find('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay', first=True).full_text
    elif(r.html.find('#priceblock_ourprice', first=True)!=None):
        price = r.html.find('#priceblock_ourprice', first=True).full_text
    else :
        price=" "
    if(r.html.find('span.a-icon-alt', first=True)!=None):
        rating = r.html.find('span.a-icon-alt', first=True).full_text
    else:
        rating=" "
    if(r.html.find('#acrCustomerReviewText', first=True)!=None):
       reviews = r.html.find('#acrCustomerReviewText', first=True).full_text
    else :
        reviews=" "

    product = {
        'title': title,
        'price': price,
        'rating': rating,
        'reviews': reviews
        }
    products.append(product)
    print('Grabbed ASIN', asin)
df = pd.DataFrame(products)
df.to_csv('ssd.csv', index=False)
