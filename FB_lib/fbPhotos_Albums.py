# -*- coding: utf-8 -*-
'''
File name       : fbPhoto_Albums.py
Author          : JasonChiuCC
Python Version  : 3.5.2
'''
# ====================================
# Standard Library
# ====================================
import html.parser
import os
import re
import time
import urllib.parse
from urllib.parse import urlparse, parse_qs

# ====================================
# Custom Library
# ====================================
from setting    import Config
from debug      import Debug

# ====================================
# Global var
# ====================================
AlbumsInfoList      = []
AlbumsPhotoInfoList = []

# ====================================
# Album Parm
# ====================================
class FBAlbumsParm:
    def __init__(self):
        self.token              = ''
        self.cursor             = ''
        self.profile_id         = ''
        self.user               = ''
        self.ajax_url           = ''

# ====================================
# Album name & link
# ====================================
class FBAlbumsInfo:
    def __init__(self, albums_name, albums_link):
        self.albums_name        = albums_name
        self.albums_link        = albums_link

# ====================================
# Photo Info
# ====================================
class FBAlbumsPhotoParm:
    def __init__(self):
        self.ajaxpipe_token     = ''
        self.last_fbid          = ''
        self.profile_id         = ''
        self.set                = ''
        self.user               = ''
        self.ajax_url           = ''

# ====================================
# Init album parm
# ====================================
def initAlbumsParm(fb_albums_parm, html_source):
    html_source_str = html_source.decode("utf-8")

    # token
    result  = re.findall(re.compile('"PhotoAlbumsAppCollectionPagelet".*?token:"(.*?)"', re.S), html_source_str)
    fb_albums_parm.token = result[0]
    # print('collection_token='+result[0])

    # cursor
    result  = re.findall(re.compile('"enableContentLoader",.*?,\"(.*?)\"\]', re.S), html_source_str)
    fb_albums_parm.cursor = result[0]
    # print('cursor='+result[0])

    # profile_id
    result  = re.findall(re.compile('{profileContextData:{profile_id:(.*?),', re.S), html_source_str)
    fb_albums_parm.profile_id = result[0]
    # print('profile_id='+result[0])

    # user
    result  = re.findall(re.compile('"USER_ID":"(.*?)"', re.S), html_source_str)
    fb_albums_parm.user = result[0]
    # print('__user='+result[0])

# ====================================
# Get album parm
# ====================================
def initAlbumsPhotoParm(fb_albums_photo_parm, html_source):
    html_source_str = html_source.decode("utf-8")

    # ajaxpipe_token
    result  = re.findall(re.compile('ajaxpipe_token":"(.*?)"', re.S), html_source_str)
    fb_albums_photo_parm.ajaxpipe_token = result[0]
    # print(result[0])

    # last_fbid
    result      = re.findall(re.compile('last_fbid.*?"(.*?)\\",', re.S), html_source_str)
    result_str  = result[0]
    result_str  = result_str.replace("\\","").replace("\"","").replace(":","")
    fb_albums_photo_parm.last_fbid = result_str
    # print(result_str)

    # profile_id
    result  = re.findall(re.compile('profile_id:(.*?),',re.S), html_source_str)
    fb_albums_photo_parm.profile_id = result[0]
    # print(result[0])

    # set
    result  = re.findall(re.compile('media_set.*?=(.*?)&amp', re.S), html_source_str)
    fb_albums_photo_parm.set = result[0]
    # print(result[0])

    # user
    result  = re.findall(re.compile('"USER_ID":"(.*?)"', re.S), html_source_str)
    fb_albums_photo_parm.user = result[0]
    # print(result[0])

# ====================================
# clean HTML Tag
# ====================================
def cleanhtml(raw_html):
    clean_html_pattern  = re.compile(b'<.*?>')
    cleantext           = re.sub(clean_html_pattern,b'', raw_html)
    cleantext           = cleantext.decode("utf-8")
    cleantext           = cleantext.replace("&lt;", "<")
    cleantext           = cleantext.replace("&gt;", ">")
    cleantext           = cleantext.replace("&amp;", "&")
    result_str          = 'result_str'
    result_str          = cleantext
    result_str          = result_str.replace("&amp;", "&")
    #print('result_str='+result_str)
    return result_str

# ====================================
# clean illegal fllder name
# ====================================
def cleanFolderName(raw_string):
    result_str          = raw_string
    result_str          = result_str.replace("\\", "")
    result_str          = result_str.replace("/", "")
    result_str          = result_str.replace(":", "")
    result_str          = result_str.replace("*", "")
    result_str          = result_str.replace("?", "")
    result_str          = result_str.replace("\"", "")
    result_str          = result_str.replace("<", "")
    result_str          = result_str.replace(">", "")
    result_str          = result_str.replace("|", "")
    #print('result_str='+result_str)
    return result_str

# ====================================
# Build album url
# ====================================
def buildAlbumsUrl(fbAP):
    fbAP.ajax_url = ('https://www.facebook.com/ajax/pagelet/generic.php/PhotoAlbumsAppCollectionPagelet?'
           'dpr=1&'
           'data={"collection_token":"' + fbAP.token + '",'
           '"cursor":"' + fbAP.cursor + '",'
           '"profile_id":' + fbAP.profile_id + ','
           '"tab_key":"photos","q":"q","overview":false,"ftid":null,"order":null,"sk":"photos","importer_state":null}&'
           '__user=' + fbAP.user + '&'
           '__a=1&__dyn=plop&__req=plop&__be=-1&__pc=PHASED:DEFAULT&__rev=2416784'
    )
    #print("Ajax_url = " + str(fbAP.ajax_url))
    return(fbAP.ajax_url)

# ====================================
# Build album photo url
# ====================================
def buildAlbumsPhotoUrl(fbAPP):
    fbAPP.ajax_url = ('https://www.facebook.com/ajax/pagelet/generic.php/TimelinePhotosAlbumPagelet?'
           'dpr=1&ajaxpipe=1&'
           'ajaxpipe_token='+fbAPP.ajaxpipe_token+'&'
           'no_script_path=1&'
           'data={"scroll_load":true,'
           '"last_fbid":"'+fbAPP.last_fbid+'",'
           '"fetch_size":32,'
           '"profile_id":'+fbAPP.profile_id+','
           '"tab_key":"media_set",'
           '"set":"'+fbAPP.set+'",'
           '"type":"3","dpr":"1","ajaxpipe":"1","ajaxpipe_token":"'+fbAPP.ajaxpipe_token+'",'
           '"quickling":{"version":"2419142;0;"},'
           '"__user":"'+fbAPP.user+'",'
           '"__a":"1","__dyn":"plop","__req":"jsonp_11","__be":"-1","__pc":"PHASED:DEFAULT","__rev":"2419142","__adt":"11",'
           '"vanity":"plop","sk":"photos","overview":false,"active_collection":69,'
           '"collection_token":"plop","cursor":0,"tab_id":"u_jsonp_11_f","order":null,"importer_state":null}&'
           '__user='+fbAPP.user+'&'
           '__a=1&__dyn=plop&__req=jsonp_12&__be=-1&__pc=PHASED:DEFAULT&__rev=2419142&__adt=12'
           )
    #print("Ajax_url = " + str(fbAPP.ajax_url))
    return(fbAPP.ajax_url)

# ====================================
# Build album photo origin url
# ====================================
def buildAlbumsPhotoOriUrl(photo_html_source,fbAPP, photo_dict):
    html_soruce_str = photo_html_source.decode("utf-8")

    # ssid = timestamp
    ssid = int(time.time())
    #print(ssid)

    photo_ori_url = ('https://www.facebook.com/ajax/pagelet/generic.php/PhotoViewerInitPagelet?'
            'dpr=1&'
            'ajaxpipe=1&'
            'ajaxpipe_token='+fbAPP.ajaxpipe_token+'&'
            'no_script_path=1&'
            'data={"fbid":"'+photo_dict['fbid'][0]+'",'
            '"set":"'+photo_dict['set'][0]+'","type":"3",'
            '"size":"'+photo_dict['size'][0]+'","theater":null,"source":"4",'
            '"ssid":'+str(ssid)+','
            '"av":"'+fbAPP.user+'"}&'
            '__user='+fbAPP.user+'&'
            '__a=1&'
            '__dyn=plop&'
            '__req=jsonp_6&'
            '__be=-1&'
            '__pc=PHASED:DEFAULT&'
            '__rev=2419142&'
            '__adt=6&'
           )
    #print("photo_ori_url = " + str(photo_ori_url))
    return(photo_ori_url)

# ====================================
# Get ori photo url
# ====================================
def getAlbumsPhotoOriUrl(photo_html_source):
    html_soruce_str = photo_html_source.decode("utf-8")
    result = re.findall(re.compile('image.*?url":"(.*?)",', re.S), html_soruce_str)
    photo_url = result[0].replace("\/", "/").replace("&amp;", "&")
    #print(photo_url)
    return photo_url
# ====================================
# Get Cursor
# ====================================
def getAlbumsCursor(html_source):
    html_soruce_str = html_source.decode("utf-8")
    result  = re.findall(re.compile('"enableContentLoader",.*?,\"(.*?)\"\]',re.S), html_soruce_str)
    return result[0]

# ====================================
# Get LastFbid
# ====================================
def getLastFbid(html_source):
    html_soruce_str = html_source.decode("utf-8")
    #print(html_soruce_str)
    result          = re.findall(re.compile('last_fbid.*?"(.*?)\\",',re.S), html_soruce_str)
    result_str      = result[0]
    result_str      = result_str.replace("\\","").replace("\"","").replace(":","")
    return result_str

# ====================================
# Get album link
# ====================================    
def getAllAlbumsInfo(driver,html_source):
    albums_current_page     = 0
    albums_link  = re.findall(re.compile(b'albumThumbLink.*?href=".*?set=(.*?)"',re.S), html_source)
    albums_title = re.findall(re.compile(b'class="photoTextTitle".*?<strong>(.*?)<\/strong>',re.S), html_source)

    # Save info
    #print("==============================\n")
    for i in range(0, len(albums_link), 1) :
        #print( str(index) + " Album Link : " + cleanhtml(albums_link))
        # skip video
        Link    = cleanhtml(albums_link[i])
        Title   = cleanhtml(albums_title[i])
        if Link[0:2] == 'vb' or Link[0:2] == 'ft':
            continue

        AlbumsInfoList.append( FBAlbumsInfo(Title, Link))
    #print("==============================\n")

    fbAP = FBAlbumsParm()
    initAlbumsParm(fbAP,html_source)

    while True:
        time.sleep(1)
        #print 'Current album page = '+str(albums_current_page)
        driver.get( buildAlbumsUrl(fbAP) )
        ajax_html_source     = (driver.page_source).encode('utf-8')
        ajax_html_source_str = cleanhtml(ajax_html_source).encode('ascii').decode('unicode-escape')

        albums_link  = re.findall(re.compile(b'albumThumbLink.*?set=(.*?)\\"',re.S), ajax_html_source)
        albums_title = re.findall(re.compile('<strong>(.*?)<',re.S), ajax_html_source_str)

        #print("==============================\n")
        for i in range(0, len(albums_link), 1) :
            #print( str(index) + " Album Link : " + cleanhtml(albums_link) )
            AlbumsInfoList.append(FBAlbumsInfo(html.unescape(albums_title[i]), cleanhtml(albums_link[i])))
        #print("==============================\n")


        # Check next page
        pattern             = re.compile(b'"enableContentLoader"',re.S)
        lenCheck            = len(re.findall(pattern,ajax_html_source))
        if lenCheck == 0:
            print("Finish Page = %3d" % (albums_current_page))
            break
        else:
            fbAP.cursor         = getAlbumsCursor(ajax_html_source)
            albums_current_page = albums_current_page + 1

# ====================================
# Get photo
# ====================================
def getAllAlbumsPhoto(driver, html_source, folder_path):
    albums_pt_current_page     = 0
    albums_pt_num              = 0
    albums_pt_link  = re.findall(re.compile(b'uiMediaThumbMedium.*?photo.php\?(.*?)"',re.S), html_source)
    fbAPP = FBAlbumsPhotoParm()
    initAlbumsPhotoParm(fbAPP,html_source)

    #print("==============================\n")
    for index, res in enumerate(albums_pt_link):
        photo_link = Config.Album_Pt_Url + urllib.parse.unquote(cleanhtml(res))
        photo_dict = parse_qs(urlparse(photo_link).query)
        #print( str(index) + " Photo Link : " + photo_link )
        print(photo_dict)
        #print('photo_link='+photo_link)
        #print("[%d]"%(index))

        # (1) Get Photo Ajax
        driver.get(photo_link)
        photo_html_source   = (driver.page_source).encode('utf-8')
        photoOriUrl = buildAlbumsPhotoOriUrl(photo_html_source,fbAPP,photo_dict)

        # (2) Parse Ori photo url
        driver.get(photoOriUrl)
        photo_html_source = (driver.page_source).encode('utf-8')
        photo_ori_url = getAlbumsPhotoOriUrl(photo_html_source)

        # (3) Download photo
        driver.get(photo_ori_url)
        driver.save_screenshot(folder_path + '/' + str(albums_pt_num) + '_' + photo_dict['fbid'][0] + '.png')
        albums_pt_num += 1
    #print("==============================\n")

    while True:
        time.sleep(0.3)
        #print 'Current album page = '+str(albums_current_page)
        driver.get( buildAlbumsPhotoUrl(fbAPP) )
        ajax_html_source     = (driver.page_source).encode('utf-8')
        ajax_html_source_str = cleanhtml(ajax_html_source).encode('ascii').decode('unicode-escape')
        #print(ajax_html_source_str)


        albums_pt_link  = re.findall(re.compile('uiMediaThumbMedium.*?photo.php\?(.*?)"',re.S), ajax_html_source_str)
        #print("==============================\n")
        for index, res in enumerate(albums_pt_link):
            photo_link = Config.Album_Pt_Url + urllib.parse.unquote(res)
            photo_dict = parse_qs(urlparse(photo_link).query)
            #print("[%d]"%(index))
            #print(photo_dict)
            #print(photo_link)

            # (1) Get Photo Ajax
            driver.get(photo_link)
            photo_html_source   = (driver.page_source).encode('utf-8')
            photoOriUrl = buildAlbumsPhotoOriUrl(photo_html_source,fbAPP,photo_dict)

            # (2) Parse Ori photo url
            driver.get(photoOriUrl)
            photo_html_source = (driver.page_source).encode('utf-8')
            photo_ori_url = getAlbumsPhotoOriUrl(photo_html_source)

            # (3) Download photo
            driver.get(photo_ori_url)
            driver.save_screenshot(folder_path + '/' + str(albums_pt_num) + '_' + photo_dict['fbid'][0] + '.png')
            albums_pt_num += 1
        #print("==============================\n")

        # Check next page
        pattern             = re.compile(b'last_fbid',re.S)
        lenCheck            = len(re.findall(pattern,ajax_html_source))
        if lenCheck == 0:
            print("Finish Page = %3d" % (albums_pt_current_page))
            break
        else:
            fbAPP.last_fbid         = getLastFbid(ajax_html_source)
            albums_pt_current_page  = albums_pt_current_page + 1


# ====================================
# Album Name
# ====================================
def getAllAlbumsTitle(driver,html_source):
    # Get album name
    albums_title_pattern    = re.compile(b'class="photoTextTitle".*?<strong>(.*?)<\/strong>',re.S)
    albums_title            = re.findall(albums_title_pattern, html_source)
    print("\n")
    for index, res in enumerate(albums_title):
        print( str(index) + " Album Name : " + cleanhtml(res))


# ====================================
# Enter every album
# ====================================
def startDownloadAlbumsPhoto(driver):
    for index, item in enumerate(AlbumsInfoList):
        driver.get( Config.Base_Url + Config.Target_Name + '/media_set?set=' + AlbumsInfoList[index].albums_link)
        Debug.sc_shot(driver,'3-AlbumsPhoto.png')
        html_source = (driver.page_source).encode('utf-8')

        # Create folder
        folder_path = r'./' + Config.Folder_name + '/' + cleanFolderName(item.albums_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        getAllAlbumsPhoto(driver, html_source, folder_path)
        break

# ====================================
# Download photo
# ====================================
def startDownload(driver):
    driver.get( Config.Base_Url + Config.Target_Name + Config.Category)
    Debug.log('fbPA:'+ Config.Base_Url + Config.Target_Name + Config.Category)
    Debug.sc_shot(driver,'2-Albums Index.png')
    html_source = (driver.page_source).encode('utf-8')

    getAllAlbumsInfo(driver, html_source)
    startDownloadAlbumsPhoto(driver)
