from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def gather_data(driver):
    counter = 1
    delay = 5
    selenium_dict_list = []
    for i in range(1, 2):
        place_dict = {}
        url = "https://kulturenvanteri.com/arastir/d/?_paged={}".format(i)
        driver.get(url)
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'button_filter')))
        tmp_click = driver.find_element_by_id("button_filter")
        tmp_click.click()
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='modal-link']")))
        # finds all elements under mainnav (about, downloads, documentation...)
        all_elems = driver.find_elements_by_xpath("//*[@class='modal-link']")

        for elem in all_elems:
            try:

                elem.click()
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='pt-3 mb-3 list-unstyled small']")))
            except ElementClickInterceptedException:
                try:
                    if counter % 2:
                        driver.execute_script("window.scrollTo(0, 0)")
                        WebDriverWait(driver, delay).until(EC.element_to_be_clickable(By.XPATH,))
                        elem.click()
                        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='pt-3 mb-3 list-unstyled small']")))
                    else:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        WebDriverWait(driver, delay).until(EC.element_to_be_clickable(elem))
                        elem.click()
                        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='pt-3 mb-3 list-unstyled small']")))
                except:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    WebDriverWait(driver, delay).until(EC.element_to_be_clickable(elem))
                    elem.click()
                    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='pt-3 mb-3 list-unstyled small']")))

            list_elements = elem.find_elements_by_xpath("//*[@class='pt-3 mb-3 list-unstyled small']")[0].text
            tmp = list_elements.split("\n")
            counter += 1
            for item in tmp:
                if "Grup" in item:
                    place_dict["group"] = item.split(":")[1]
                if "Tür" in item:
                    place_dict["theme"] = item.split(":")[1]
                if "Bölge" in item:
                    place_dict["area"] = item.split(":")[1]
                if "Kültür" in item:
                    place_dict["culture"] = item.split(":")[1]
                if "Yüzyıl" in item:
                    place_dict["century"] = item.split(":")[1]
            try:
                place_dict["description"] = driver.find_element_by_css_selector("p").text
            except:
                place_dict["description"] = " "
            try:
                place_dict["images"] = driver.find_element_by_xpath("//*[@class='figure-thumb']//img").get_attribute("src")
            except:
                place_dict["images"] = ""
            place_dict["name"] = driver.find_element_by_xpath("//*[@class='col-8 col-md-6 h3 px-0 pb-3 pt-0']/a").text
            place_dict["location"] = driver.find_elements_by_xpath("//*[@class='googlemap']/a")[1].get_attribute("href").split("/")[-1]
            selenium_dict_list.append(place_dict)

            # close_button.click()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            time.sleep(7)

    return selenium_dict_list


def get_address(browser, location_link):
    browser.get(location_link)
    time.sleep(6)
    #coordinates = location_link.split("/")[-1]
    coordinates = browser.find_element_by_xpath("//*[@class='7.x3AX1-LfntMc-header-title-ij8cu']")
    address = browser.find_element_by_xpath("//span[@class='lRsTH-Tswv1b-text']").text

    location = {"coordinates": coordinates, "address": address}
    return location


def all_adress(browser, dict_list):
    for i in dict_list:
        location_link = i["location"]
        i["location"] = get_address(browser, location_link)


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path="chromedriver.exe")

    selenium_dict_list = gather_data(driver)
    with open('selenium.txt', 'w') as f:
        for element in selenium_dict_list:
            f.write(str(element) + "\n")
        f.close()
    # selenium_dict_list = [{"location":"https://www.google.com/maps/place/41%C2%B003'20.3%22N+28%C2%B056'24.5%22E/@41.0556335,28.940134,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d41.0556335!4d28.940134"},{"location":"https://www.google.com/maps/place/41%C2%B003'20.3%22N+28%C2%B056'24.5%22E/@41.0556335,28.940134,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d41.0556335!4d28.940134"}]
    # all_adress(driver, selenium_dict_list)
