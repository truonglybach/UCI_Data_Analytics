
# coding: utf-8

# In[1]:
def scrape():

    # Import necessary dependencies to scrape
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import requests


    # Took out locate chromedriver because that was a jupyter notebook method,
    # so leaving it in the code would mess up the Python function.

    # In[3]:


    # Create a path for browser function
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)


    # In[4]:


    # Store a url as a string and visit the site with browser
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    # In[5]:


    # Grab .html link and parse info
    nasa_news_html = browser.html
    soup = bs(nasa_news_html, "html.parser")
    # Scrape desired content and store
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text


    # In[6]:


    # Store next website's url as string and visit with the browser function
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


    # In[7]:


    # Store the .html link and parse info
    jpl_html = browser.html
    soup = bs(jpl_html, "html.parser")
    # Grab base_url and endpoint
    base_url = "https://www.jpl.nasa.gov/"
    endpoint_url = soup.find("article", class_="carousel_item")["style"].split()[1].strip("""
    url() "" '' ;
    """)
    # Concatenate strings and visit the url
    url = (base_url + endpoint_url)
    browser.visit(url)


    # In[8]:


    # Grab the .html link of the page and parse the info
    img_html = browser.html
    soup = bs(img_html, "html.parser")
    # Store the image url accordingly
    featured_image_url = soup.find("img")["src"]


    # In[10]:


    # Store the url of the next website as a string and visit the url
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)


    # In[11]:


    # Store the .html link and parse
    twit_html = browser.html
    soup = bs(twit_html, "html.parser")
    # Store the latest tweet
    mars_weather = soup.find("p", class_="TweetTextSize").text


    # In[12]:


    # Store the next url as a string and use pandas to read the table data
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)


    # In[14]:


    # Store the next url as a string and visit the website
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)


    # In[15]:


    # Store the .html link and parse the info
    usgs_html = browser.html
    soup = bs(usgs_html, "html.parser")


    # In[16]:


    # Store the results
    results = soup.find_all("div", class_="description")


    # In[17]:


    # For every record, grab link
    taglink_list = []
    for result in results:
        taglink_list.append(result.a["href"])


    # In[19]:


    # Store base url as string
    base_url = "https://astrogeology.usgs.gov"


    # In[20]:


    # For every page, grab the title and img endpoint url
    title_list = []
    endpoint_url_list = []
    for i in taglink_list:
        url = (base_url + i)
        browser.visit(url)
        link_html = browser.html
        # Grab title
        soup = bs(link_html, "html.parser")
        title_list.append(soup.find("h2", class_="title").text)
        # Grab img endpoint url
        endpoint_url_list.append(soup.find("img", class_="wide-image")["src"])


    # In[21]:


    # For every endpoint url, concatenate with base url
    full_url_list = []
    for i in endpoint_url_list:
        full_url_list.append(base_url + i)


    # In[22]:


    # Replace unnecessary words accordingly
    title_list = [i.replace(" Enhanced", "").strip() for i in title_list]


    # In[23]:


    # Store the titles and urls of each instance as a dictionary
    hemi_list = []
    for i in title_list:
        entry = {"title": i, "img_url": full_url_list[title_list.index(i)]}
        hemi_list.append(entry)

    # Make the var table into a df and use .to_dict("records")
    # to make the df into a parsable dict for MongoDB

    table_df = table[0].rename(columns={0: "Mars Stats", 1: "Data"})
    table_dict = table_df.to_dict("records")

    # In[30]:


    # Combine all scraped data into one dictionary
    scraped_data = {"NASA Mars News Article": news_title, "Short Summary": news_p, "JPL Featured Space Image URL": featured_image_url, "Mars Weather Twitter Account (Latest Tweet)": mars_weather, "Table of Facts about Mars": table_dict, "List of Mars Hemispheres and their Image URLs": hemi_list}

    return scraped_data
