#default libraries added by Ty
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from secrets import pw, cardNumber
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import random
import pdb;


#recaptcha libraries
import speech_recognition as sr
# import ffmpy
import requests
import urllib
import pydub

#system libraries
import os
import random
import time

#selenium libraries

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException



class InstaBot:

    # inititate browser and navigate to product page
    def __init__ (self, username, itemToPurchase, pw, cardNumber):
        self.itemToPurchase = itemToPurchase
        self.cardNumber = cardNumber

        # specify proxies
        PROXY_LIST = [
            "158.227.106.21:80", "27.255.52.230:8080", "136.233.215.142:80",
            "167.172.29.206:8080", "51.158.68.68:8811", "157.230.254.120:8080",
            "51.75.147.43:3128", "187.44.1.167:8080", "165.22.115.179:8080",
            "200.73.129.128:8080", "213.14.105.167:8080", "110.168.212.229:8080",
            "139.99.105.5:80", "159.89.175.163:3128", "142.93.150.156:8080",
            "175.141.69.203:80", "46.8.247.3:50967", "209.126.4.134:3128",
            "111.92.164.246:56871", "58.152.94.85:8080", "132.145.18.53:8080",
            "178.128.208.247:8080", "190.14.254.182:999", "201.91.82.155:3128",
            "200.41.150.83:54958"
        ]

        # set initial proxy
        PROXY = random.choice(PROXY_LIST)
        
        # include credentials for chrome log in (gets all saved credentials for websites)
        options = webdriver.ChromeOptions() 
        options.add_argument(r"user-data-dir=C:\Users\sport\AppData\Local\Google\Chrome\User Data")

        # other chrome options
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-plugins-discovery")

        # add working user-agent
        userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        options.add_argument("user-agent="+userAgent)

        # add previously set proxy
        options.add_argument('--proxy-server=%s' % PROXY)

        # specify browser
        self.browser = webdriver.Chrome(r"C:\Projects\selenium\selenium drivers\chromedriver", options=options)
       
        # navigate to product page on website

        checkUserAgent = self.browser.execute_script("return navigator.userAgent;")
        
        print("User Agent: "+checkUserAgent)
        print("Current PROXY: "+PROXY)

        try:

            self.delay()

            #go to website
            self.browser.get(itemToPurchase)
            
        except:
            print("[-] Please update the chromeself.browser.exe in the webdriver folder according to your chrome version:https://chromeself.browser.chromium.org/downloads")

        self.delay()
        self.checkCaptcha()
        self.inStock()
        

    def checkCaptcha(self):
        #check to see if there is recaptcha on screen
        arr = self.browser.find_elements_by_xpath("//*[contains(text(), 'Verify your identity')]")
        
        if len(arr) > 0:
            print("Recaptcha is present.. bypassing captcha..")
            self.verifyCaptcha()

        else:
            print("No Captcha present..")

    #verify captcha
    def verifyCaptcha(self):

        #switch to recaptcha frame
        frames=self.browser.find_elements_by_tag_name("iframe")
        self.browser.switch_to.frame(frames[0])
        self.delay()

        #click on checkbox to activate recaptcha
        self.browser.find_element_by_class_name("recaptcha-checkbox-border").click()

        #switch to recaptcha audio control frame
        self.browser.switch_to.default_content()
        frames=self.browser.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
        self.browser.switch_to.frame(frames[0])
        self.delay()

        #click on audio challenge
        self.browser.find_element_by_id("recaptcha-audio-button").click()

        #switch to recaptcha audio challenge frame
        self.browser.switch_to.default_content()
        frames= self.browser.find_elements_by_tag_name("iframe")
        self.browser.switch_to.frame(frames[-1])
        self.delay()

        #click on the play button
        self.browser.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

        #get the mp3 audio file
        src = self.browser.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s"%src)

        #download the mp3 audio file from the source
        urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")

        sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
        
        #breaks here
        sound.export(os.getcwd()+"\\sample.mp3", format="mp3")

        sample_audio = sr.AudioFile(os.getcwd()+"\\sample.mp3")


        r= sr.Recognizer()

        with sample_audio as source:
            audio = r.record(source)

        #translate audio to text with google voice recognition
        key=r.recognize_google(audio)
        print("[INFO] Recaptcha Passcode: %s"%key)

        #key in results and submit
        self.browser.find_element_by_id("audio-response").send_keys(key.lower())
        self.browser.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        self.browser.switch_to.default_content()
        self.delay()
        self.browser.find_element_by_id("recaptcha-demo-submit").click()
        self.delay()

    def delay (self):
        time.sleep(random.randint(2,3))

    # check if item is in stock
    def inStock(self):

        arr = self.browser.find_elements_by_xpath("//*[contains(text(), 'Add to cart')]")
        
        if len(arr) > 0:
            print("item is in stock..")
            self.cartProduct()

        else:
            print("item is not stock..refreshing page and trying again..")
            # dependent on being Windows system
            self.browser.refresh()
            print("page refreshed..")
            self.inStock()

    # cart the product and place order
    def cartProduct(self):
        # specify quantity (3)

        # add products to cart
        self.browser.find_element_by_xpath("//span[contains(text(), 'Add to cart')]")\
            .click()
        self.delay()
        self.browser.find_element_by_xpath("//span[contains(text(), 'Check out')]")\
            .click()
        self.delay()
        self.browser.find_element_by_xpath("//span[contains(text(), 'Continue')]")\
            .click()
        self.delay()
        self.browser.find_element_by_xpath("//span[contains(text(), 'Continue')]")\
            .click()
        self.delay()
        self.browser.find_element_by_name("cvv").send_keys("230")
        self.delay()
        self.browser.find_element_by_xpath("//span[contains(text(), 'Review your order')]")\
            .click()
        self.delay()



        # self.authenticateLogin()
        # check if credit card is saved
            # if card is saved, place order
            # if card is NOT saved, save card info then place order
        # place order

    
    # def login(self):


    def authenticateLogin(self):
        arr = self.browser.find_element_by_xpath("//form[input/@name='username']")

        if len(arr) > 0:
            print("logging in..")
            #fire function to login

        else:
            print("already logged in.. proceeding check out")
        
        
        #fire function to place order

    
        #find if fields for user name and password exist
        #if they exist, send username and password keys
        #otherwise proceed with code 

        #may need to incorporate boolean

username = "6039133103"


itemToPurchase = "https://www.walmart.com/ip/20-21-PANINI-DONRUSS-FOOTBALL-FAT-PACK/268999426"

# itemToPurchase = "http://httpbin.org/ip"


my_bot = InstaBot(username, itemToPurchase, pw, cardNumber)

