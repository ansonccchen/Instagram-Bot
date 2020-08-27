from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com")
        self.login()

    def login(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            user = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            passw = wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            user.send_keys(self.username)
            passw.send_keys(self.password)
            self.driver.find_element_by_xpath('//button[@type="submit"]').click()
            self.driver.implicitly_wait(4)
            self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
            self.driver.implicitly_wait(4)
            self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        except:
            self.driver.quit()

    def nav_profile(self):
        self.driver.find_element_by_xpath(f'//img[@alt="{self.username}\'s profile picture"]').click()

    def get_usernames(self):
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        prev_height, curr_height = 0, 1
        while prev_height != curr_height:
            prev_height = curr_height
            time.sleep(1)
            curr_height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        follow_names = scroll_box.find_elements_by_tag_name('a')
        names = {}
        for name in follow_names:
            if name.text != '':
                names[name.text] = 1
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return names

    def check_unfollowers(self):
        self.driver.find_element_by_xpath(f'//a[@href="/{self.username}/following/"]').click()
        following = self.get_usernames()
        self.driver.find_element_by_xpath(f'//a[@href="/{self.username}/followers/"]').click()
        followers = self.get_usernames()
        not_fol_back = []
        for user in following:
            if user not in followers:
                not_fol_back.append(user)
        not_fol_back = sorted(not_fol_back)
        print(f"not following back: {not_fol_back}")
        self.driver.quit()

if __name__ == "__main__":
    ig_bot = InstaBot('u','p') # replace "u" with your username and "p" with your password
    ig_bot.nav_profile()
    ig_bot.check_unfollowers()