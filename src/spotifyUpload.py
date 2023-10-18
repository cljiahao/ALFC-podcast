import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class spotifyUpload():
    def __init__(self,lang,srcPath,fileNames):

        load_dotenv()
        user = os.getenv(f"{lang}USER")
        pwd = os.getenv(f"{lang}PASS")

        spotPath = os.path.join(os.getcwd(),srcPath,lang)

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.binary_location = '/usr/bin/google-chrome'
        chrome_options.headless = True
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 100)
        self.login(user,pwd)
        for fileName in fileNames:
            self.uploadFiles(spotPath,fileName)
            os.remove(os.path.join(spotPath,fileName))
            print(f"{fileName} Published")

    def login(self,user,pwd):
        
        self.driver.get("https://podcasters.spotify.com/pod/dashboard/episode/wizard")

        self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div[3]/div/button[1]').click()

        username = self.wait.until(EC.presence_of_element_located((By.NAME,"email")))
        password = self.driver.find_element(By.NAME,"password")

        username.send_keys(user)
        password.send_keys(pwd)
        username.submit()        # Submit Login

    def uploadFiles(self,spotPath,fileName,refresh=True):
        try:
            uploadepisode = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="file"]')))
            uploadepisode.send_keys(os.path.join(spotPath,fileName))
        except: 
            if refresh:
                print("Refreshed Browser")
                self.driver.refresh()
                self.uploadFiles(spotPath,fileName,False)
            else: 
                # self.driver.save_screenshot("image.png")
                raise TimeoutError('Browser not responsive.')

        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app-content"]/div/div/footer/div/div[3]/div/span'),'Preview ready!'))

        title = self.driver.find_element(By.NAME,"title")
        title.send_keys(fileName[:-4])
 
        textbox = self.driver.find_element(By.NAME,'description')
        textbox.send_keys("Christian weekly devotionals from Abundant Life Family Church, Singapore")

        publishRadio = self.driver.find_element(By.ID,'publish-date-now')
        self.driver.execute_script("arguments[0].checked = true;", publishRadio)

        explicitRadio = self.driver.find_element(By.ID,'no-explicit-content')
        self.driver.execute_script("arguments[0].checked = true;", explicitRadio)

        nextButton1 = self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div/footer/div/div[4]/button')
        self.driver.execute_script("arguments[0].click();", nextButton1)
        time.sleep(3)
        nextButton2 = self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div/footer/div/div[4]/button')
        self.driver.execute_script("arguments[0].click();", nextButton2)
        time.sleep(3)
        publishBut = self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/div/footer/div/div[4]/button')
        self.driver.execute_script("arguments[0].click();", publishBut)

        self.driver.get("https://podcasters.spotify.com/pod/dashboard/episode/wizard")