# -*- coding: utf-8 -*-
'''
File name       : main.py
Author          : JasonChiuCC
Python Version  : 3.5.2
'''
# ====================================
# Standard Library
# ====================================
from selenium import webdriver

# ====================================
# Custom Library
# ====================================
from setting import Config
from debug   import Debug
from FB_lib  import fbPhotos_Albums as fbPA

# ====================================
# Login
# ====================================
driver = webdriver.PhantomJS(Config.Phantomjs_path)
driver.set_window_size(Config.Window_High, Config.Window_Wight)
driver.get(Config.Base_Url)
driver.find_element_by_id("email").clear()
driver.find_element_by_id("email").send_keys(Config.Email)
driver.find_element_by_id("pass").clear()
driver.find_element_by_id("pass").send_keys(Config.Password)
driver.find_element_by_id("loginbutton").click()
Debug.sc_shot(driver, '1-FB Index.png')

# Download Album
if Config.Target_Type == 'Normal':
    fbPA.startDownload(driver)
