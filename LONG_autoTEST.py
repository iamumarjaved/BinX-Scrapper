import time
import os
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException


#USER Credentials and Prefrences
#Credentials
global user_email 
global user_password
global perform_long_or_short 
global search_item


user_email = "example123@mail.com"
user_password = "1234"
perform_long_or_short = "short"
search_item = "bitcoin"


#Prefrences LONG
global long_margin
long_margin = "0"

global long_leverage
long_leverage = "50x"

global take_profit
take_profit = False

global stop_loss
stop_loss = True


#Prefrences SHORT
global short_margin
short_margin = "0"

global short_leverage
short_leverage = "100x"

global short_take_profit
short_take_profit = False

global short_stop_loss
short_stop_loss = True


# Function to save cookies
def save_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


# Function to load cookies
def load_from_pickle(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


# Inject cookies into selenium from saved file
def inject_cookies_to_driver(driver):
    cookies = load_from_pickle('session_cookies.pkl')
    if cookies:
        for cookie in cookies:
            if "expiry" in cookie:
                del cookie["expiry"]  # Selenium doesn't like the 'expiry' field when adding a cookie.
            driver.add_cookie(cookie)
        return True
    return False


#Perform LOGIN
def perform_login_with_selenium(driver):
    # LOGIN Credentials Input
    email_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'html body div#__nuxt div#__layout div.page-container div.user-layout div.user-layout-container div.login-block div.form_content_wrap div.form-input-wrapper.mt-20 div.input-wrapper div.el-input.el-input--suffix.form-input input.el-input__inner')))
    email_element.send_keys(user_email)
    password_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'html body div#__nuxt div#__layout div.page-container div.user-layout div.user-layout-container div.login-block div.form_content_wrap div.password-ct input.password-element.el-input__inner')))
    password_element.send_keys(user_password)
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'html body div#__nuxt div#__layout div.page-container div.user-layout div.user-layout-container div.login-block div.form_content_wrap button.btn')))
    login_button.click()
    time.sleep(60)
    save_to_pickle(driver.get_cookies(), 'session_cookies.pkl')


#Check LOGIN 
def is_user_logged_in(driver):
    try:
        account_icon = driver.find_element(By.CSS_SELECTOR, "html.pxtorem body div#__nuxt div#__layout div.page-container header.navigation.bx-fe-navigation.responsive.white-type nav.navigation-inner div.nav-right div.user-menus div.compatible-menu-scroll.menu-item.popover.account span.icon.account")
        # If the element is found, the user is logged in
        return True
    except NoSuchElementException:
        # If the account icon element is not found
        if os.path.exists('session_cookies.pkl'):
            os.remove('session_cookies.pkl')
        print("User is not logged in. Session file deleted due to error or Session expired. Account Icon not Found!")
        return False


# Disables Notifications
chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)


# Open Browser
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)


# Open the Page
driver.get("https://bingx.com/en-us/login/?redirect=https%3A%2F%2Fbingx.com%2Fen-us%2F")


# If we can't inject cookies, then perform the login
if not inject_cookies_to_driver(driver):
    perform_login_with_selenium(driver)
    wait = WebDriverWait(driver, 10)
    add_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close-png")))
    add_close.click()
    time.sleep(10)
    driver.quit()
    exit()


# Refresh after setting cookies or logging in
driver.refresh()

#Close First addvertisement
wait = WebDriverWait(driver, 10)
try:
    add_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close-png")))
    add_close.click()
    time.sleep(5)
except TimeoutException:
    print("The first Close Button not Found.")
    # If the first advertisement is not found, try to close the second one
    try:
        add_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-close")))
        add_close.click()
        time.sleep(5)
    except TimeoutException:
        print("The second Close Button not Found.")


#Check If the user is login or not if not the session may be expire or errors occured remove the sessions
wait = WebDriverWait(driver, 10)
if is_user_logged_in(driver):
    print("User is logged in.")
    # Your logic after ensuring you are logged in:
    # Navbar ItemClick
    wait = WebDriverWait(driver, 10)
    try:
        click_navbar_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "html.pxtorem body div#__nuxt div#__layout div.page-container header.navigation.bx-fe-navigation.responsive.white-type nav.navigation-inner div.nav-left ul.nav-list li.nav-item.route.white-type a.nav-item-link span.trigger-name")))
        click_navbar_item.click()
        time.sleep(5)
    except TimeoutException:
        print("Navbar Markets item Not Found.")

    # Search Item
    wait = WebDriverWait(driver, 10)
    try:
        click_search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "html body div#__nuxt div#__layout div.page-container div.market-container div.market-content div.module-list-wrapper div.header div.search-box-wrapper div.bx-input-light-wrap div.ti-outer-wrap div.ti-wrap-left input.tl-input-inner")))
        click_search_box.send_keys(search_item)
        click_search_box.click()
        time.sleep(5)
    except TimeoutException:
        print("Search Bar item Not Found.")

    # SELECT Bitcoin Element
    wait = WebDriverWait(driver, 10)
    try:
        bitcoin_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.table-row:nth-child(1) > div:nth-child(8) > span:nth-child(2)")))
        bitcoin_element.click()
        time.sleep(10)
    except TimeoutException:
        print("Bitcoin item Not Found.")
    
    # Confirm OK Guideline Element
    wait = WebDriverWait(driver, 10)
    try:
        guideline_ok_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div:nth-child(2) > div.favorite-symbol-wrapper.vue-draggable-handle > div.tool-wrap > div.symbol-switch-guide-wrapper.newUser.with-icon > div > button")))
        guideline_ok_element.click()
        time.sleep(10)
    except TimeoutException:
        print("Guideline  OK element Not Found.")
    
    
    #IF Perform Task is LONG this will work.
    if perform_long_or_short.lower() == "long":
        #LONG LEVERAGE Settings
        if long_leverage == "5x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(1)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("5x leverage element Not Found.")
        elif long_leverage == "10x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(2)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("10x leverage element Not Found.")
        elif long_leverage == "20x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(3)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("20x leverage element Not Found.")
        elif long_leverage == "50x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(4)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("50x leverage element Not Found.")
        elif long_leverage == "100x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(5)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("100x leverage element Not Found.")
        elif long_leverage == "150x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(6)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("150x leverage element Not Found.")

        #TAke Profit
        wait = WebDriverWait(driver, 10)
        try:
            take_profit_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.futures-base-item-wrap > li:nth-child(8) > ul > div > span")))
            if take_profit==True:
                take_profit_toggle.click()
                time.sleep(10)
            else:
                pass
        except TimeoutException:
            print("Take Profit Button element Not Found.") 


        #Stop Loss
        wait = WebDriverWait(driver, 10)
        try:
            stop_profit_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.futures-base-item-wrap > li:nth-child(9) > ul > div > span")))
            if stop_loss==True:
                stop_profit_toggle.click()
                time.sleep(10)
            else:
                pass
        except TimeoutException:
            print("Stop Loss Button element Not Found.") 
    
    
    #IF PERFORM TASK IS SHORT this will work
    elif perform_long_or_short.lower() == "short":
        wait = WebDriverWait(driver, 10)
        try:
            short_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.trade-tab-item:nth-child(2) > span:nth-child(1)")))
            short_button.click()
            time.sleep(10)
        except TimeoutException:
            print("Short Button element Not Found.") 
        #SHORT leverage
        if short_leverage == "5x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(1)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 5x leverage element Not Found.")
        elif short_leverage == "10x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(2)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 10x leverage element Not Found.")
        elif short_leverage == "20x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(3)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 20x leverage element Not Found.")
        elif short_leverage == "50x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(4)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 50x leverage element Not Found.")
        elif short_leverage == "100x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(5)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 100x leverage element Not Found.")
        elif short_leverage == "150x":
            wait = WebDriverWait(driver, 10)
            try:
                leverage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.lever_item:nth-child(6)")))
                leverage.click()
                time.sleep(10)
            except TimeoutException:
                print("Short 150x leverage element Not Found.")

        #TAke Profit
        wait = WebDriverWait(driver, 10)
        try:
            take_profit_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.futures-base-item-wrap > li:nth-child(8) > ul > div > span")))
            if  short_take_profit==True:
                take_profit_toggle.click()
                time.sleep(10)
            else:
                pass
        except TimeoutException:
            print("Short Take Profit Button element Not Found.") 

        #Stop Loss
        wait = WebDriverWait(driver, 10)
        try:
            stop_profit_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.futures-base-item-wrap > li:nth-child(9) > ul > div > span")))
            if  short_stop_loss==True:
                stop_profit_toggle.click()
                time.sleep(10)
            else:
                pass
        except TimeoutException:
            print("Short Stop Loss Button element Not Found.") 
    
    
    
    """
        
    
    #SELECT and Enter Margin in LONG
    wait = WebDriverWait(driver, 10)
    try:
        Margin_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.futures-base-item-wrap > li:nth-child(8) > ul > div > span")))
        if Margin_element:
            Margin_element.send_keys(long_margin)
        time.sleep(10)
    except TimeoutException:
        print("Long Margin item Not Found.")
    
    """
#IF user is not Logged in or errors
else:
    print("User is not logged in, Try Logging in again to store the session.")

# Your logic after long or short :
wait = WebDriverWait(driver, 10)
try:
    Activate_trade = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div > div.content-container > div > div > div.vue-grid-item.vue-resizable.order-panel > div > div.footer > a")))
    Activate_trade.click()
    time.sleep(10)
except TimeoutException:
    print("Activate trade button item Not Found.")
# [ ... Rest of your code ... ]
time.sleep(10)
driver.quit()
