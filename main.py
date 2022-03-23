from botlyTarget import Botly
from secrets import pw, cardNumber, cvc
from lib import product_links, proxies

attempts = 0
product_links = product_links.links
proxies = proxies.proxies
# product = list(product_links.values())[0]
product="https://www.target.com/p/2021-nba-panini-prizm-basketball-trading-cards-multipack-box-of-12/-/A-83446160"
tasks = 0
quantityPurchased = 0
success = False

class Main:

    def __init__ (self, tasks, quantityPurchased, success):

        self.tasks = tasks
        self.quantityPurchased = quantityPurchased
        self.success = success

        while tasks <= 25 and quantityPurchased <= 3:
            try:
                botly = Botly(product, pw, cardNumber, cvc, proxies, attempts, success)     
                
                if (success):
                    quantityPurchased+=3
                    print("Current Quantiy: "+ quantityPurchased)

                else:
                    print("Quantiy remained the same..")
                    print("Current Quantiy: "+ quantityPurchased)

            except Exception as e:
                print("There was an issue:")
                print(e)
                tasks+=1

                print("Running next task")
        
        print(str(tasks)+" tasks complete!")
        print("Number of units purchased: "+str(quantityPurchased))

main = Main(tasks, quantityPurchased, success)
    

