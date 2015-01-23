#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import sys
import os
import urllib
import urllib2
import getpass

## Class for managing external resources, whether they are located via local
## path or URL.
class ResourceManager:
  ## @var manager
  # An instance of urllib2.HTTPPasswordMgrWithDefaultRealm.
  ## @var opener
  # An instance of urllib2.OpenerDirector.
  
  ## Initialize an empty ResourceManager object.
  # @param self The object pointer.
  def __init__(self):
    self.manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    handler = urllib2.HTTPBasicAuthHandler(self.manager)
    self.opener = urllib2.build_opener(handler)
  
  ## Adds a new URL / login / password to self.manager.
  # @param self The object pointer.
  # @param url A valid URL.
  # @param login Login for the input URL (default None).
  # @param password Password for the input login (default None).
  def add_password(self, url, login=None, password=None):
    self.manager.add_password(None, url, login, password)
  
  ## Returns the resource stored at the input URL.
  # @param self The object pointer.
  # @param url A valid URL.
  # @return A resource file.
  def get_resource(self, url):
    # Try to open as a local path
    try:
      handle = urllib.urlopen(urllib.pathname2url(url))
      return handle
    except IOError as e:
      pass
    # Case where input URL is not a local path
    try:
      handle = self.opener.open(url)
      return handle
    except IOError as e:
      pass
    if not hasattr(e, 'code') or e.code != 401:
      print("Error " + str(e.errno) + ": " + str(e.strerror))
      sys.exit(1)
    # Case where login / password are unknown
    else:
      username = str(raw_input("Username for " + url + ": "))
      password = getpass.getpass()
      self.manager.add_password(None, url, username, password)
      try:
        handle = self.opener.open(url)
        return handle
      except IOError as e:
        print("Error " + str(e.errno) + ": " + str(e.strerror))
        sys.exit(1)
  
  ## For testing purposes; install self.opener.
  # @param self The object pointer.
  def install_opener(self):
    urllib2.install_opener(self.opener)
