from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from secrets import pw, cardNumber, cvc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lib import product_links, proxies
import random
import time

class Botly:

    # inititate browser and navigate to product page
    def __init__ (self, product, pw, cardNumber, cvc, proxies, attempts, success):

        self.product = product
        self.cardNumber = cardNumber
        self.cvc = cvc
        self.proxies = proxies
        self.success = success

        # PROXY = PROXY_LIST[4]
        
        # include credentials for chrome log in (gets all saved credentials for websites)
        options = webdriver.ChromeOptions() 
        options.add_argument(r"user-data-dir=C:\Users\sport\AppData\Local\Google\Chrome\User Data")
        
        # specify settings to reduce bot suspicion
        options.add_argument("--start-maximized")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        options.add_extension('path_to_extension')
        # specify headless browser mode
        # options.add_argument("headless")

        # add working user-agent
        userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        options.add_argument("user-agent="+userAgent)

        # add proxy
        # options.add_argument('--proxy-server=%s' % PROXY)

        # specify browser
        self.browser = webdriver.Chrome(r"C:\Projects\selenium\selenium drivers\chromedriver", options=options)
       
        # remove navigator webdriver flag for bot detection
        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # navigate to product page on website
        self.browser.get(product)
        self.delay()

        print("Settings loaded correctly..")

        # begin botting process
        self.inStock(attempts)

        # if successfully purchased products, then set success true
        if self.cartProduct():
            success = True
        else:
            success = False

    # set delays for flow protection
    def delay (self):
        time.sleep(random.randint(1,2))
        
    # check if item is in stock
    def inStock(self, attempts):

        print("Checking to see if in stock..")
        arr = self.browser.find_elements_by_xpath("//*[contains(text(), 'Ship it')]")
        
        self.delay()

        if len(arr) > 0:
            attempts = 0
            print("item is in stock.. going to cart product")
            self.cartProduct()

        else:
            attempts+=1
            print("item is not stock..refreshing page and trying again..")
            print("current attempts: "+str(attempts))

            # dependent on being Windows system
            self.browser.refresh()
            print("page refreshed..")
            self.inStock(attempts)

    # cart the product and place order
    def cartProduct(self):

        print("Specifying quantity..")

        # specify quantity of 3
        self.browser.find_element_by_xpath("//button[@data-test='custom-quantity-picker']")\
            .click()
        self.delay()
        self.browser.find_element_by_xpath("//ul[@id='options']/li[3]")\
            .click()

        print("Quantity of 3 specified..Attempting to add to cart..")
        self.delay()

        # add products to cart
        self.browser.find_element_by_xpath("//button[contains(text(), 'Ship it')]")\
            .click()
        self.delay()

        print("Current Page: Product Page")

        self.browser.find_element_by_xpath("//button[contains(text(), 'View cart & checkout')]")\
            .click()
        self.delay()

        print("Current Page: Product Page (Item-Added Popup)")
        self.browser.find_element_by_xpath("//button[contains(text(), 'check out')]")\
            .click()
        self.delay()

        print("Current Page: Final Checkout Page")
        self.browser.find_element_by_name("cvc").send_keys(cvc)
        self.browser.find_element_by_xpath("//button[contains(text(), 'Place your order')]")\
            .click()
        
        print("Order successfully placed..")
        return True



        # write function to show that order was completed 
        # assign number of successful orders to a counter
        # set a limit for how many orders we want

        # self.authenticateLogin()
        # check if credit card is saved
            # if card is saved, place order
            # if card is NOT saved, save card info then place order
        # self.browser.find_element_by_name("cardnumber").send_keys(cardNumber)
        # self.browser.find_element_by_xpath("//button[contains(text(), 'Confirm')]")\
        #     .click()
        # place order

