import os
import time
import subprocess
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

urlnewrelic='givemeurl' #newrelic url

def init_newrelic():
    option = webdriver.ChromeOptions()
    option.add_argument("window-size=960,1080")
    option.add_argument("window-position=960,0")
    # option.headless = True
    browser = webdriver.Chrome(options=option)
    browser.get(urlnewrelic)
    element = browser.find_elements(By.CSS_SELECTOR, 'input')
    element[1].send_keys('email@mail.com')  #your login newrelic
    element[1].submit()
    element = browser.find_elements(By.CSS_SELECTOR, 'input')
    element[3].send_keys('Password')      #your password newrelic
    element[3].submit()
    time.sleep(5)
    return browser


def init_pingdom():
    option = webdriver.ChromeOptions()
    option.add_argument("window-size=960,1080")
    option.add_argument("window-position=0,0")
    # option.headless = True
    browser = webdriver.Chrome(options=option)
    browser.get('https://my.pingdom.com/app/newchecks/checks')
    element = browser.find_elements(By.CSS_SELECTOR, 'input')
    element[0].send_keys('email@email.com')       #your login pingdom
    element[1].send_keys('Password')      #your password pingdom
    element[1].submit()
    time.sleep(5)
    return browser


def newrelic(browser):
    relic_list = []
    browser.get(urlnewrelic)
    time.sleep(10)
    while browser.title != "New Relic Explorer < New Relic One":
        browser.get(urlnewrelic)
        time.sleep(10)
    element = browser.find_element(By.CSS_SELECTOR, '#root > div')
    newrelic_class = element.get_attribute("class").split("-")[0]
    element = browser.find_elements(By.CSS_SELECTOR,
                                    '.' + newrelic_class + '-wnd-EntityTitleTableRowCell-status--critical')
    num_elem = len(element)
    # print("Down on New Relic:", num_elem)
    # print()
    element = browser.find_elements(By.CSS_SELECTOR, '.' + newrelic_class + '-wnd-TableCell-content')
    for i in range(num_elem):
        # print(element[i * 8 + 1].text)
        relic_list.append(element[i * 8 + 1].text)
    return browser, relic_list


def pingdom(browser):
    ping_list = []
    browser.get('https://my.pingdom.com/app/newchecks/checks')
    # wait = WebDriverWait(browser, 10)
    # wait.until(ec.title_contains('Uptime Checks'))
    time.sleep(10)
    while browser.title != "Uptime Checks":
        browser.get('https://my.pingdom.com/app/newchecks/checks')
        time.sleep(10)
    browser.switch_to.frame(0)
    element = browser.find_elements(By.CSS_SELECTOR, 'tr')
    # print("Down on Pingdom:", len(browser.find_elements(By.CSS_SELECTOR, '.pd-check-status-down')))
    # print()
    for i in element:
        if i.find_elements(By.CSS_SELECTOR, '.pd-check-status-down'):
            i = i.find_element(By.CSS_SELECTOR, 'strong')
            # print(i.text)
            ping_list.append(i.text)
    return browser, ping_list


def alarm(ignore_list, service):
    with subprocess.Popen(["afplay", "audio.mp3"]) as proc:
        print("^ that service down. Please, send any symbol for stopping alarm: ")
        input()
        proc.terminate()
        print("OK! Stopping. Add that service in ignore list? Send 'y' for accept or any for decline (service not "
              "call alarm on 5 min) :")
        a = input()
        if a == "y":
            ignore_list.append(service)


def check(ignore_list, warning_list, service):
    if not ignore_list.count(service):
        if not warning_list.count(service):
            warning_list.append(service)
            warning_list.append(1)
        elif warning_list[warning_list.count(service)] < 5:
            warning_list[warning_list.count(service)] += 1
        else:
            alarm(ignore_list, service)
            pos = warning_list.count(service)
            warning_list.pop(pos)
            warning_list.pop(pos - 1)


def main():
    ignore_list = ["awv-staging-cluster"]
    warning_list = []
    ping_browser = init_pingdom()
    newrelic_browser = init_newrelic()
    while 1:
        ping_browser, ping_list = pingdom(ping_browser)
        newrelic_browser, relic_list = newrelic(newrelic_browser)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Last update:", datetime.datetime.now())
        print("Ignore list:", ignore_list)
        print()
        print("Warning list:")
        for i in range(0, len(warning_list) - 1, 2):
            print(warning_list[i], warning_list[i + 1], "min")
        print()
        print("Down on New Relic:", len(relic_list))
        for i in relic_list:
            print(i)
            check(ignore_list, warning_list, i)
        print()
        print("Down on Pingdom:", len(ping_list))
        for i in ping_list:
            print(i)
            check(ignore_list, warning_list, i)

        time.sleep(35)

    # browser.quit()


main()
