#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Setup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdb


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': 'C:/Users/Graham/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False) 


# In[3]:


# Visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text',wait_time=1)


# In[4]:


# Create HTML object of the page
html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div',class_='content_title')


# In[5]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div',class_='content_title').get_text()
print(news_title)


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
print(news_p)


# In[7]:


# ### Featured Images


# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the 'full image' button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')
print(img_soup)


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')
print(img_url_rel)


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
print(img_url)


# In[ ]:





# In[13]:


# ## Mars Facts


# In[14]:


## Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars','Earth']
df.set_index('description',inplace=True)
print(df)


# In[15]:


df.to_html()


# In[ ]:





# In[ ]:





# In[ ]:





# In[16]:


# ## Hemisphere Scraping


# In[17]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles
hemisphere_image_urls = []


# In[19]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with BeautifulSoup


# In[20]:


for i in range(4):
    hemispheres = {}
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.find_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# In[ ]:





# In[ ]:





# In[21]:


print(hemisphere_image_urls)


# In[22]:


# End session
browser.quit()

