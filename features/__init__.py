from aloe import *
from selenium import webdriver
import os

driver = webdriver.Firefox()
# driver.get('http://localhost:5000/')

@before.each_example
def navigate(*args):
    driver.get('http://localhost:5000/index.html')


@step('I have selected the file (\S+)')
def i_have_selected_the_file(step, filename):
    driver.find_element_by_id("advanced-settings").click()
    file_select_elem = driver.find_element_by_id('choose-file')
    path = os.getcwd() + '/music/' + filename
    path = "~/Diss/ocgen/app/music/" + filename
    file_select_elem.send_keys(path)


@step('I click on (\S+)')
def i_click_on_submit(step, button):
    driver.find_element_by_id(button).click()


@step('I see the loading animation appear')
def i_see_the_loading_animation_appear(step):
    driver.implicitly_wait(2)
    # Make sure animation is visible
    assert "" == driver.find_element_by_id('loading').get_attribute('style')


@step('I see the tabs appear after (\d+) seconds')
def i_see_the_tabs_appear(step, seconds):
    driver.implicitly_wait(seconds)
    assert driver.find_element_by_id("result") is not None

