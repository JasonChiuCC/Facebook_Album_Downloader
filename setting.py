# -*- coding: utf-8 -*-
'''
File name       : setting.py
Author          : JasonChiuCC
Python Version  : 3.5.2
'''
# ====================================
# Global var
# ====================================
class Config(object):
    # Screen setting
    Window_High         = 1024
    Window_Wight        = 768

    # Url setting
    Base_Url            = 'https://www.facebook.com/'
    Album_Url           = 'https://www.facebook.com/media/set/?set='
    Album_Pt_Url        = 'https://www.facebook.com/photo.php?'
    Category            = '/photos_albums'  # Select photos_of, photos_all, photos_albums
    Category_Famous     = '/photos'

    # Facebook setting
    Email               = 'YourFacebookAccount'
    Password            = 'YourFacebookPassword'
    Target_Name         = 'zuck'
    Target_Type         = 'Normal'          # Select Normal / Famous

    # Debug
    Debug_log           = False
    Debug_sc_shoot      = False

    # Download setting
    Folder_name         = 'Download'

    # Other setting
    Phantomjs_path      = r'D:\Your_Phantomjs_Path\phantomjs.exe'