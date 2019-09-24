import os
import pickle

from ...config import *

class CacheHandler:

    def read_file_name_cache(self):
        if os.path.isfile(file_name_cache_path):
            with open(file_name_cache_path, 'r') as infile:
                file_name = infile.read()
        else:
            with open(file_name_cache_path_deployed_sys, 'r') as infile:
                file_name = infile.read()
        return file_name


    def write_file_name_cache(self, file_name):
        if os.path.isfile(file_name_cache_path):
            with open(file_name_cache_path, 'w') as outfile:
                outfile.truncate(0)
                outfile.write(file_name)
        else:
            with open(file_name_cache_path_deployed_sys, 'w') as outfile:
                outfile.truncate(0)
                outfile.write(file_name)
        return


    def dicts_to_cache(self, dicts):
        """
        Write the dictionary, that is used to form the word window when the user clicks a token, to the cache.
        :param dicts: Line dictionary and identifier line dictionary.
        :return: None; files are pickled and stored in cache.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'wb') as outfile:
            pickle.dump(dicts, outfile)
        return
        #__LOGGER__.debug(' Wrote file to {}'.format(path))


    def cache_to_dicts(self):
        """
        Read the dictionary, that is used to form the word window when the user clicks a token, from the cache.
        :return: Line dictionary and identifier line dictionary.
        """
        path = view_cache_path + 'dicts'
        with open(path, 'rb') as infile:
            dicts = pickle.load(infile)
        return dicts



