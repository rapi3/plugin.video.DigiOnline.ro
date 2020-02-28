#
#
#    Copyright (C) 2020  Alin Cretu
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os
import logging
# The cookielib module has been renamed to http.cookiejar in Python 3
import cookielib
# import http.cookiejar
import re

import vars


def init_AddonCookieJar(NAME, DATA_DIR):
  ####
  #
  # Initialize the vars.__CookieJar__ variable.
  #
  # Parameters:
  #      NAME: Logger name to use for sending the log messages
  #      DATA_DIR: The directory containing the cookies data file
  #
  ####

  logger = logging.getLogger(NAME)

  #global vars.__CookieJar__

  logger.debug('Enter function')

  # File containing the session cookies
  cookies_file = os.path.join(DATA_DIR, vars.__AddonCookiesFilename__)
  logger.debug('[ Addon cookies file ] cookies_file = ' + str(cookies_file))


  ### WARNING: The cookielib module has been renamed to http.cookiejar in Python 3
  vars.__AddonCookieJar__ = cookielib.MozillaCookieJar(cookies_file)
  #vars.__AddonCookieJar__ = http.cookiejar.MozillaCookieJar(cookies_file)

  # If it doesn't exist already, create a new file where the cookies should be saved
  if not os.path.exists(cookies_file):
    vars.__AddonCookieJar__.save()
    logger.info('[ Addon cookiefile ] Created cookiejar file: ' + str(cookies_file))
    logger.debug('[ Addon cookiefile ] Created cookiejar file: ' + str(cookies_file))

  # Load any cookies saved from the last run
  vars.__AddonCookieJar__.load()
  logger.debug('[ Addon cookiejar ] Loaded cookiejar from file: ' + str(cookies_file))



def get_cached_categories():
  ####
  #
  # Get the list of cached video categories.
  #
  # Return: The list of cached video categories
  #
  ####

  logger.debug('Enter function')

  _cached_data_filename_ = os.path.join(addon_data_dir, vars.__cache_dir__, 'categories.json')

  if os.path.exists(_cached_data_filename_) and os.path.getsize(file_path) != 0:
    # The data file with cached categories exists and is not empty.
    logger.info('Reading from data file: ' + _cached_data_filename_)
    logger.debug('Reading from data file: ' + _cached_data_filename_)
    _data_file_ = open(_cached_data_filename_, 'r')
    _cached_categories_ = json.load(_data_file_)
    _data_file_.close()
  else:
    # The data file with cached categories does not exist or it is empty.

    # First call the function to get the data from DigiOnline.ro and store it in the data file
    logger.info('Updating data file: ' + _cached_data_filename_)
    logger.debug('Updating data file: ' + _cached_data_filename_)
    get_categories()

    # Then read the freshly cached data
    logger.info('Reading from data file: ' + _cached_data_filename_)
    logger.debug('Reading from data file: ' + _cached_data_filename_)

    _data_file_ = open(_cached_data_filename_, 'r')
    _cached_categories_ = json.load(_data_file_)
    _data_file_.close()

  logger.debug('_cached_categories_ = ' + str(_cached_categories_))
  logger.debug('Exit function')

  return _cached_categories_


def get_cached_channels(category):
  ####
  #
  # Get the cached list of channels/streams.
  #
  # Parameters:
  #      category: Category name
  #
  # Return: The list of cached channels/streams in the given category
  #
  ####

  logger.debug('Enter function')

  logger.debug('Exit function')
  return _cached_channels_list_


def do_login(NAME, COOKIEJAR, SESSION):
  logger = logging.getLogger(NAME)

  logger.debug('Enter function')

  userAgent = vars.__userAgent__

  # Authentication to DigiOnline is done in two stages:
  # 1 - Send a GET request to https://www.digionline.ro/auth/login ('DOSESSV3PRI' session cookie will be set)
  # 2 - Send a PUT request to https://www.digionline.ro/auth/login with the credentials in the form-encoded data ('deviceId' cookie will be set)

  logger.debug('============== Stage 1: Start ==============')
  # Setup headers for the first request
  MyHeaders = {
    'Host': 'www.digionline.ro',
    'User-Agent': userAgent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US',
    'Accept-Encoding': 'identity',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
  }

  logger.debug('Cookies: ' + str(list(COOKIEJAR)))
  logger.debug('Headers: ' + str(MyHeaders))
  logger.debug('URL: https://www.digionline.ro/auth/login')
  logger.debug('Method: GET')

  # Send the GET request
  _request_ = SESSION.get('https://www.digionline.ro/auth/login', headers=MyHeaders)

  logger.debug('Received status code: ' + str(_request_.status_code))
  logger.debug('Received cookies: ' + str(list(COOKIEJAR)))
  logger.debug('Received headers: ' + str(_request_.headers))
  logger.debug('Received data: ' + str(_request_.content))
  logger.debug('============== Stage 1: End ==============')

  # Save cookies for later use.
  COOKIEJAR.save(ignore_discard=True)

  logger.debug('============== Stage 2: Start ==============')

  # Setup headers for second request
  MyHeaders = {
    'Host': 'www.digionline.ro',
    'Origin': 'https://www.digionline.ro',
    'Referer': 'https://www.digionline.ro/auth/login',
    'User-Agent': userAgent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US',
    'Accept-Encoding': 'identity',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
  }

  # Setup form data to be sent

  MyFormData = {
    'form-login-email': vars.__config_AccountUser__,
    'form-login-password': vars.__config_AccountPassword__
  }

  logger.debug('Cookies: ' + str(list(COOKIEJAR)))
  logger.debug('Headers: ' + str(MyHeaders))
  logger.debug('MyFormData: ' + str(MyFormData))
  logger.debug('URL: https://www.digionline.ro/auth/login')
  logger.debug('Method: POST')

  # Send the POST request
  _request_ = SESSION.post('https://www.digionline.ro/auth/login', headers=MyHeaders, data=MyFormData)

  logger.debug('Received status code: ' + str(_request_.status_code))
  logger.debug('Received cookies: ' + str(list(COOKIEJAR)))
  logger.debug('Received headers: ' + str(_request_.headers))
  logger.debug('Received data: ' + str(_request_.content))
  logger.debug('============== Stage 2: End ==============')

  # Authentication error.
  if re.search('<div class="form-error(.+?)>', _request_.content, re.IGNORECASE):
    logger.debug('\'form-error\' found.')

    _ERR_SECTION_ = re.findall('<div class="form-error(.+?)>\n(.+?)<\/div>', _request_.content, re.IGNORECASE|re.DOTALL)[0][1].strip()
    _auth_error_message_ = re.sub('&period;', '.', _ERR_SECTION_, flags=re.IGNORECASE)
    _auth_error_message_ = re.sub('&abreve;', 'a', _auth_error_message_, flags=re.IGNORECASE)

    logger.info('[Authentication error] => Error message: '+ _auth_error_message_)

    logger.debug('_ERR_SECTION_ = ' + str(_ERR_SECTION_))
    logger.debug('_auth_error_message_ = ' + _auth_error_message_)
    logger.debug('[Authentication error] => Error message: '+ _auth_error_message_)

    xbmcgui.Dialog().ok('[Authentication error message]', _auth_error_message_)

    logger.debug('Exit function')

    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")


  else:
    logger.debug('\'form-error\' not found.')

    logger.info('Authentication successfull')
    logger.debug('Authentication successfull')

    # Save cookies for later use.
    COOKIEJAR.save(ignore_discard=True)

    logger.debug('Exit function')





def test_function(ID):
  logger = logging.getLogger(ID)
  logger.debug('Enter function')
  logger.debug('Exit function')


