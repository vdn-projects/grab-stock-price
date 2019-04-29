from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime, timedelta
from pytz import timezone
import time
import config

download_path = os.getcwd() + "/data"


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)


def initialize():
    display = None
    if not config.local_test:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()

    url = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # prefs = {"download.default_directory": "/home/djangodeploy/download"}
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    return display, driver


def process(driver, ticker_code, from_date, to_date):
    elem = driver.find_element_by_css_selector('#symbolID')
    elem.send_keys(ticker_code)
    elem = driver.find_element_by_css_selector('#fHistoricalPrice_FromDate')
    elem.send_keys(from_date)
    elem = driver.find_element_by_css_selector('#fHistoricalPrice_ToDate')
    elem.send_keys(to_date)

    try:
        elem = driver.find_element_by_css_selector('#fHistoricalPrice_View')
        elem.click()

        elem = WebDriverWait(driver, 3, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#tab-1 > div.box_content_tktt > ul > li:nth-child(2) > div.row-time.noline')))

        elem = driver.find_element_by_css_selector(
            '#tab-1 > div.box_content_tktt > div > div > a > span.text')
        elem.click()

        # timeout 10 sec, polling 2 sec
        WebDriverWait(driver, 10, 2).until(every_downloads_chrome,
                                           f"Download complete for {ticker_code}.")

    except TimeoutError:
        print(ticker_code + " has no data.")


def quit(display, driver):
    driver.close()
    driver.quit()
    if not config.local_test:
        display.stop()


def main(n_days=4):
    """
    Download stock prices of last n day
    """
    time_zone = "Asia/Saigon"
    date_format = "%d/%m/%Y"

    from_date = (datetime.now(timezone(time_zone)) +
                 timedelta(days=-n_days)).strftime(date_format)

    to_date = (datetime.now(timezone(time_zone)) +
               timedelta(days=1)).strftime(date_format)

    tickers = pd.read_csv("./data/ticker_list.csv")
    for i, ticker in tickers.iterrows():
        try:
            display, driver = initialize()
            process(driver, ticker.TickerCode, from_date, to_date)
            quit(display, driver)
        except:
            quit(display, driver)


if __name__ == "__main__":
    main()
