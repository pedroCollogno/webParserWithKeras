from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains;
import time, base64, requests, os

def src_to_base64(src) :
    l = len(list(src))
    start = 0
    for i in range(l) :
        if src[i:i+6] == "base64" :
            start = i + 6
            break
    if start == 0 :
        return False
    return src[start:]

def src_to_image(src, count, dirName) :
    if src == None :
        print("None")
        return False
    if src[-4:] == ".png" :
        image_result = open("./data/" + dirName + "/image_" + str(count) + ".png", "wb")
    else :
        image_result = open("./data/" + dirName + "/image_" + str(count) + ".jpeg", "wb")
    if "https" in src :
        req = requests.get(src)
        data = req.content
    else :
        try :
            b_64 = src_to_base64(src)
            data = base64.b64decode(b_64)
        except :
            print(src)
    try :
        image_result.write(data)
    except :
        print("data : ")
        print(data)


classe = input()
if not os.path.exists("data/" + classe) :
    driver = webdriver.Chrome()
    driver.get("https://images.google.com/?hl=fr")

    os.makedirs("data/" + classe)

    searchbar = driver.find_element_by_xpath("//input[@title = 'Rechercher']")
    searchbar.send_keys(classe)
    searchbar.send_keys(Keys.ENTER)
    time.sleep(1)

    for i in range(10) :
        time.sleep(1)
        driver.execute_script('''els = document.querySelectorAll('img');
                        els[els.length - 11].parentElement.scrollIntoView();
                        inputs = document.querySelectorAll('input'); input = inputs[inputs.length - 1];
                        if(input.getAttribute('value')=='Plus de résultats'){input.click();}''')


    images = driver.find_elements_by_tag_name("img")

    list_images = []
    for img in images :
        src = img.get_attribute("src")
        if(src == None) :
            src = img.get_attribute("data-src")
        list_images.append(src)
    list_images.pop(0)
    L = len(list_images)
    print(L)
    for i in range(L) :
        if list_images[i] != "" :
            src_to_image(list_images[i], i, classe)

    driver.close()