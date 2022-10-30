
# Setup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': 'C:/Users/Graham/chromedriver.exe'}
    browser = Browser('chrome', executable_path="C:/Users/Graham/chromedriver.exe", headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store their results into a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data 

def mars_news(browser):
    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    # Create HTML object of the page
    html = browser.html
    news_soup = soup(html,'html.parser')

    # Add try/except for error handling
    try:
        
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div',class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the 'full image' button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Try/except for attribute errors
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:   
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set the index of our dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description',inplace=True)

    # Convert dataframe into HTML format and add bootstrap
    return df.to_html(classes='table table-striped')

def hemispheres(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Empty list to hold hemisphere images and titles
    hemisphere_image_urls = []

    # Retrieve image urls and titles
    for i in range(4):
        browser.find_by_css('a.product-item h3')[i].click()
        hemisphere_data = scrape_hemispheres(browser.html)
        hemisphere_image_urls.append(hemisphere_data)
        browser.back()
    return hemisphere_image_urls


def scrape_hemispheres(html_text):
    hemisphere_soup = soup(html_text, 'html.parser')
    try:
        title_elem = hemisphere_soup.find('h2',class_='title').get_text()
        sample_elem = hemisphere_soup.find('a',text='Sample').get('href')
    except AttributeError:
        title_elem = None
        sample_elem = None
    hemispheres = {
        'title': title_elem,
        'img_url':sample_elem
    }
    return hemispheres

if __name__ == '__main__':

    # If running as script, print scraped data
    print(scrape_all())
