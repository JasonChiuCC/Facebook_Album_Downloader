# -*- coding: utf-8 -*-
'''
File name       : debug.py
Author          : JasonChiuCC
Python Version  : 3.5.2
'''
# ====================================
# Global var
# ====================================
from setting import Config

class Debug(object):
    @staticmethod
    def log(debug_message):
        if Config.Debug_log is True:
            print(debug_message)



    @staticmethod
    def sc_shot(driver, screenshot_name):
        if Config.Debug_sc_shoot is True:
            driver.save_screenshot(screenshot_name)

