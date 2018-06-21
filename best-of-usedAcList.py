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

MDtab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#manuTab div:nth-of-type(13)")))
MDtab.click()

dc_9_10 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#acList div:nth-of-type(6) button"))
)
dc_9_10.click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "am-list-item")))
usedPlanes = driver.find_elements_by_tag_name("am-list-item")
best = []

for ac in usedPlanes:
    # wandering through acs
    ac.click()
    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, "lxml")

    cruiseSpeed = soup.find(id="acSpeed").string
    fuelUse = soup.find(id="acFuel").string
    score = float(cruiseSpeed) / float(fuelUse)

    if len(best) == 0:
        # ac info
        actives = soup.find_all(class_="active")
        regNum = actives[2]['data-reg']
        acRange = soup.find(id="acRange").string

        planeInfo = [regNum, score, acRange]

        best.append(planeInfo)
    # Checks current ac's score against worst of top 5
    elif score > best[len(best) - 1][1]:
        index = 0
        for plane in best:
            if score > plane[1]:
                # ac info
                actives = soup.find_all(class_="active")
                regNum = actives[2]['data-reg']
                acRange = soup.find(id="acRange").string

                planeInfo = [regNum, score, acRange]

                best.insert(index, planeInfo)

                if len(best) > 10:
                    del best[10]
                break
            index += 1


print('  Reg.  |  Score   |  Range ')
for plane in best:
    print('{0[0]:8}|{0[1]:^10.3f}|{0[2]:^8}'.format(plane))

driver.quit()