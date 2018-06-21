from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

email = "airlinemanager3scraping@gmail.com"
passwd = "123qwerty!"

# Opens facebook in firefox
driver = webdriver.Firefox()
url = "https://www.facebook.com/"
driver.get(url)

# Login
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("pass").send_keys(passwd, Keys.ENTER)

gameLinkElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "navItem_191389561439811")))
gameLinkElement.click()

# switch to the right game-screen
driver.switch_to.frame("iframe_canvas_fb_https")
driver.find_element_by_id("mainMenuFleet").click()
orderAcBtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "subTab2")))
orderAcBtn.click()

driver.implicitly_wait(1) # seconds
planeFactories = driver.find_elements_by_class_name("manu-div")

with open('Flydata AM3.csv', 'w') as f:
    columnHeaders = "Flytype, Nypris, Kan fås brugt, Kan fås ny, Hastighed, Rækkevidde, Antal sæder, Lbs/km\n"
    f.write(columnHeaders)

    for factory in planeFactories:
        factory.click()
        innerHTML = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(innerHTML, "lxml")
        
        factoryName = soup.find(id="manuName").string
        
        # array of div-elements containing ac items
        ACs = soup(class_="used-ac-item")
        for ac in ACs:
            # plane data extraction
            capacity = ac["data-capacity"]
            speed = ac["data-speed"]
            range_ = ac["data-range"]
            price = ac["data-price"]
            infoWrap = ac.find(class_="item-info-wrap")
            flightModel = infoWrap.previous_sibling.div.string
            fullPlaneName = factoryName + " " + flightModel
            fuelEfficiency = infoWrap.contents[1].contents[0].contents[2].string

            availableUsed = "Ja"
            availableNew = "Ja"

            if len(infoWrap.next_sibling.contents[0].contents) == 0:
                availableUsed = "Nej"

            if len(infoWrap.next_sibling.contents[1].contents) == 0:
                availableNew = "Nej"

            f.write(fullPlaneName + ", " + price + ", " + availableUsed + ", " + availableNew + ", "
                    + speed + ", " + range_ + ", " + capacity + ", " + fuelEfficiency + "\n")

driver.quit()