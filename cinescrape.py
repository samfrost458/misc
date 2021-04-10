# web scraper for checking new films on cinema listing

import time
import pync
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from apscheduler.schedulers.blocking import BlockingScheduler

newVueTitles, newOdeonTitles = [], []
newVueLinks, newOdeonLinks = [], []

def scrape():

    # simulate chrome headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="/Users/samfrost/Downloads/chromedriver", options=chrome_options)
    
    ## TODO: REMOVE MANUAL DELAYS AND REPLACE WITH WAIT UNTILS
    
    def scroll_down():
        # get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # wait to load page
            time.sleep(0.5)
        
            # calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
    
    ### VUE
    def vue():
        # load site
        driver.get("https://www.myvue.com/cinema/manchester-printworks/whats-on")
        
        # if cookie accept bar exists then accept
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//*[@id=\"onetrust-accept-btn-handler\"]").click()
        except: pass
        
        # select all times
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"filmlist__filters\"]/li[8]/label").click()
        
        # scroll down until all films are loaded
        scroll_down()
        
        # find all film titles
        titles = [elem.get_attribute("innerHTML") for elem in driver.find_elements_by_xpath("//span[@rv-text='item.title']")]
        links  = [elem.get_attribute("href") for elem in driver.find_elements_by_xpath("//a[@class='subtitle h3']")]

        return titles, links
    
    
    ### ODEON
    def odeon():
        # load site
        driver.get("https://beta.odeon.co.uk/cinemas/manchester-great-northern/")
        
        # if cookie accept bar exists then accept
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id=\"onetrust-accept-btn-handler\"]").click()
        driver.execute_script('arguments[0].click();',driver.find_element_by_xpath("//*[@id=\"cookie-modal-container\"]/div/span"))
        
        # # select all times
        driver.execute_script('arguments[0].click();',driver.find_element_by_xpath("//*[@id=\"vista-cinema-showtime-picker-856\"]/div/div[2]/label/div[1]"))
        
        # find all film titles
        time.sleep(1)
        titles = [elem.get_attribute("innerHTML") for elem in driver.find_elements_by_xpath("//h3[@class='v-film-title__title']")]
        links  = [elem.get_attribute("href") for elem in driver.find_elements_by_xpath("//a[@class='v-link v-showtime-picker-film-details__film-link']")]
        
        return titles, links


    global newVueTitles, newOdeonTitles, newVueLinks, newOdeonLinks
    
    # copy out old data
    oldVueTitles = newVueTitles
    oldOdeonTitles = newOdeonTitles
    
    # replace with new data
    newVueTitles, newVueLinks = vue()
    newOdeonTitles, newOdeonLinks = odeon()
    
    # notify of changes
    for film, link in zip(newVueTitles, newVueLinks):
        if film not in oldVueTitles:
            pync.notify(film, title="New at Vue", open=link)
    for film, link in zip(newOdeonTitles, newOdeonLinks):
        if film not in oldOdeonTitles:
            if film not in newVueTitles:
                pync.notify(film, title="New at Odeon", open=link)
    
    driver.quit()

scrape()

# schedule data to update itself in the background periodically
scheduler = BlockingScheduler()
scheduler.add_job(func=scrape, trigger='cron', day='*', hour=18)
scheduler.start()






