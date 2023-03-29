import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

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
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        self.wait = WebDriverWait(self.driver, 300)
        self.login(user,pwd)
        for fileName in fileNames:
            self.uploadFiles(spotPath,fileName)
            os.remove(os.path.join(spotPath,fileName))
            print(f"{fileName} Published")

    def login(self,user,pwd):
        
        self.driver.get("https://podcasters.spotify.com/pod/login")

        username = self.wait.until(EC.presence_of_element_located((By.NAME,"email")))
        password = self.driver.find_element(By.NAME,"password")

        username.send_keys(user)
        password.send_keys(pwd)
        username.submit()        # Submit Login

    def uploadFiles(self,spotPath,fileName):
        
        uploadepisode = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="file"]')))
        uploadepisode.send_keys(os.path.join(spotPath,fileName))

        publish = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/form/div[1]/div[2]/button[2]')))

        title = self.driver.find_element(By.ID,"title")
        title.send_keys(fileName[:-4])
 
        textbox = self.driver.find_element(By.XPATH,'//*[@id="app-content"]/div/form/div[4]/div[2]/div/div[1]/div[2]')
        textbox.send_keys("Christian weekly devotionals from Abundant Life Family Church, Singapore")

        publish.click()

        xBut = self.wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/reach-portal/div[2]/div/div/div/div[1]/button')))
        xBut.click()
