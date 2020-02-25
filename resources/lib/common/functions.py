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

import vars


def get_cached_categories():
    ####
    #
    # Get the list of cached video categories.
    #
    # Return: The list of cached video categories
    #
    ####

    logger.debug('Enter function')

    _cached_data_filename_ = os.path.join(addon_data_dir, vars.__cache_dir__ 'categories.json')

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





