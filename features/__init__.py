from aloe import *
from selenium import webdriver
import os

driver = webdriver.Firefox()
driver.get('http://localhost:5000/')

# Make sure animation is hidden
animation = driver.find_element_by_id('loading')
assert "display: none" in animation.get_attribute('style')


@step('I have selected the file (\S+)')
def i_have_selected_the_file(step, filename):
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
    # Make sure animamtion is visible
    assert "" == driver.find_element_by_id('loading').get_attribute('style')
