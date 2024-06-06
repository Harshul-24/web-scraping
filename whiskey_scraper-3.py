#!/usr/bin/env python
# coding: utf-8

# In[41]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import smtplib
import re

baseurl = 'https://www.thewhiskyexchange.com'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15", 
    "X-Amzn-Trace-Id": "Root=1-642694de-52001da728637b6359ec78e9"}


# In[2]:


# page = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky', headers=headers)
# soup = BeautifulSoup(page.content, 'lxml')
# #print(soup)
# #productlist = soup.find_all('p', class_= "product-card__name")
# #<li class="product-grid__item"><a href="/p/2940/yamazaki-12-year-old" class="product-card" title="Yamazaki 12 Year Old" onclick="_gaq.push(['_trackEvent', 'JapaneseWhisky-GridView', 'click', '2940 : Yamazaki 12 Year Old'])"><div class="product-card__image-container"><img src="https://img.thewhiskyexchange.com/480/japan_yam1.jpg" alt="Yamazaki 12 Year Old" class="product-card__image" loading="lazy" width="3" height="4"></div><div class="product-card__content"><p class="product-card__name"> Yamazaki 12 Year Old </p><p class="product-card__meta"> 70cl / 43% </p></div><div class="product-card__data"><p class="product-card__price"> £145 </p><p class="product-card__unit-price"> (£207.14 per litre) </p></div></a></li>
# productlist = soup.find_all('li', class_='product-grid__item')
                             
# print(len(productlist))


# In[3]:


# productlinks = []
# #productlinks2 = []
# #c0 = 0
# for item in productlist:
#     #print(item)
#     c_url = item.find('a', href=True)['href']
#     #print(c_url)
#     productlinks.append(baseurl + c_url )
#     c0+=1
# #print(c0)
# print(len(productlinks))
# print(productlinks[0])

# # for item in productlist:
# #     for link in item.find_all('a', href=True):
# #         productlinks2.append (baseurl + link['href'])
        

# # print(len(productlinks2))
# # print(productlinks2[0])


# In[4]:


##
productlinks = []
for i in range(1,7):
    #page = requests.get('https://www.thewhiskyexchange.com/c/309/blended-malt-scotch-whisky', headers=headers)
    page = requests.get(f'https://www.thewhiskyexchange.com/c/309/blended-malt-scotch-whisky?pg={i}')
    soup = BeautifulSoup(page.content, 'lxml')
    
    #productlist = soup.find_all('p', class_= "product-card__name")
    #<li class="product-grid__item"><a href="/p/2940/yamazaki-12-year-old" class="product-card" title="Yamazaki 12 Year Old" onclick="_gaq.push(['_trackEvent', 'JapaneseWhisky-GridView', 'click', '2940 : Yamazaki 12 Year Old'])"><div class="product-card__image-container"><img src="https://img.thewhiskyexchange.com/480/japan_yam1.jpg" alt="Yamazaki 12 Year Old" class="product-card__image" loading="lazy" width="3" height="4"></div><div class="product-card__content"><p class="product-card__name"> Yamazaki 12 Year Old </p><p class="product-card__meta"> 70cl / 43% </p></div><div class="product-card__data"><p class="product-card__price"> £145 </p><p class="product-card__unit-price"> (£207.14 per litre) </p></div></a></li>
    productlist = soup.find_all('li', class_='product-grid__item')
    #print(len(productlist))
    
    #productlinks2 = []
    #c0 = 0
    for item in productlist:
        #print(item)
        c_url = item.find('a', href=True)['href']
        #print(c_url)
        productlinks.append(baseurl + c_url )
        #c0+=1
    #print(c0)
    #print(len(productlinks))
#print(productlinks)
print(len(productlinks))


# In[5]:


# <span class="review-overview__count">(46&nbsp;Reviews)
# </span>
# <p class="product-main__data">
# 70cl / 43%
# </p>

#<p class="product-action__stock-flag"><i class="product-action__stock-tick fas fa-check"></i> In Stock</p>

#<p class="product-facts__data">15 Year Old</p>
#<p class="product-facts__data">Scotland</p>
#<h3 class="product-facts__type">Country</h3>


# In[57]:


#testlink = 'https://www.thewhiskyexchange.com/queue/p/70869/april-fools-whisky-2023-the-gastronomy-selection-37-year-old'

#testlink = 'https://www.thewhiskyexchange.com/p/32602/johnnie-walker-green-label-15-year-old'

whisky_list = []
#print(testlink)
for link in productlinks:
    print(link)
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    #<h1 class="product-main__name">
    # 

    date = datetime.date.today()
    #print(date)

    try:
        name = soup.find('h1', class_='product-main__name').contents[0].text.strip()
    except:
        name = link.split('/')[-1]

    try:
        rating = soup.find('span', class_='review-overview__rating star-rating star-rating--45').text.strip()
    except:
        rating = None

    try:
        price = soup.find('p', class_="product-action__price").text.strip().strip('£')
        #print(price)
    except:
        price = None

    try:
        reviews = soup.find('span', class_="review-overview__count").text.strip().strip('()')
        reviews = reviews.strip("Reviews")
        #print(reviews)
    
    except:
        reviews = None

    try:
        details = soup.find('p', class_="product-main__data").text.strip()
        #print(details)
    except:
        details = None

    try:
        available_flag = soup.find('p', class_="product-action__stock-flag").text.strip()
        available = "Yes" if available_flag =='In Stock' else "No"
        #print(available)
    except:
        available = None

    un_list = soup.find('ul', class_="product-facts")
    #print(un_list)

    try:
        age_tag = un_list.find('h3', text='Age')  # find h3 tag with text 'Age'
        wine_age = age_tag.find_next_sibling('p').text  # find the next sibling p tag and get its text
        #print(wine_age)
        age = re.findall(r'\d+', wine_age)
        age = int(age[0])
        #print(age)
    except:
        age = None

    try:
        country_tag = un_list.find('h3', text='Country')
        country = country_tag.find_next_sibling('p').text.strip()
        #print(country)

    except:
        country = None
        
    whisky = {"Name": name,
              "Details": details,
              "Price": price,
              "Date": date,
              "Available": available,
              "Reviews": reviews,
              "Age": age,
              "Country" : country}

    whisky_list.append(whisky)
    print(f"{name} : SUCCESS")

print('GRAND SUCCESS')
df = pd.DataFrame(whisky_list)


# In[58]:


df.head(20)


# In[60]:


df.to_csv('whisky-databse.csv', index=False)


# In[59]:


# #testlink = 'https://www.thewhiskyexchange.com/queue/p/70869/april-fools-whisky-2023-the-gastronomy-selection-37-year-old'

# #testlink = 'https://www.thewhiskyexchange.com/p/32602/johnnie-walker-green-label-15-year-old'

# whisky_list = []
# for link in productlinks:
#     print(link)
#     page = requests.get(productlinks[i], headers=headers)
#     soup = BeautifulSoup(page.content, 'lxml')
#     #<h1 class="product-main__name">
#     # 

#     date = datetime.date.today()
#     #print(date)

#     name = soup.find('h1', class_='product-main__name').contents[0].text.strip()

#     try:
#         rating = soup.find('span', class_='review-overview__rating star-rating star-rating--45').text.strip()

#     except:
#         rating = None

#     price = soup.find('p', class_="product-action__price").text.strip().strip('£')
#     #print(price)

#     reviews = soup.find('span', class_="review-overview__count").text.strip().strip('()')
#     reviews = reviews.strip("Reviews")
#     #print(reviews)

#     details = soup.find('p', class_="product-main__data").text.strip()
#     #print(details)

#     available_flag = soup.find('p', class_="product-action__stock-flag").text.strip()
#     available = "Yes" if available_flag =='In Stock' else "No"
#     #print(available)

# #     age_text = soup.find('p', class_="product-facts__data").text.strip()
# #     print(age_text)
# #     age = re.findall(r'\d+', age_text)
# #     age = int(age[0])
# #     print(age)

#     un_list = soup.find_all('li', class_="product-facts__item")
#     print(len(un_list))

# #     age_text = un_list.find_all('li')[0]
# #     age_text = age_text.find('p', class_="product-facts__data").text.strip()
# #     print(age_text)
# #     age = re.findall(r'\d+', age_text)
# #     age = int(age[0])
# #     #print(age)

#     country = un_list.find_all('li')[1].find('p', class_="product-facts__data").text.strip()
#     #print(country)
#     whisky = {"Name": name,
#               "Details": details,
#               "Price": price,
#               "Date": date,
#               "Available": available,
#               "Reviews": reviews,
#               "Age": age,
#               "Country" : country}

#     whisky_list.append(whisky)
    
    
# df = pd.DataFrame(whisky_list)


# In[ ]:


df.head(10)


# In[87]:





# In[ ]:




