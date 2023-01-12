#!/usr/bin/env python3

import sys
import pygsheets

import httplib2

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from helper.logger import *
from helper.gsheet.gsheet_reader import *

class GsheetHelper(object):

    __instance = None

    ''' class constructor
    '''
    def __new__(cls):
        # we only need one singeton instance of this class
        if GsheetHelper.__instance is None:
            GsheetHelper.__instance = object.__new__(cls)

        return GsheetHelper.__instance


    ''' initialize the helper
    '''
    def init(self, config):
        # as we go further we put everything inside a single dict _context
        self._context = {}

        info(f"authorizing with Google")

        _G = pygsheets.authorize(service_account_file=config['files']['google-cred'])
        self._context['_G'] = _G

        credentials = ServiceAccountCredentials.from_json_keyfile_name(config['files']['google-cred'], scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
        credentials.authorize(httplib2.Http())

        self._context['service'] = discovery.build('sheets', 'v4', credentials=credentials)

        gauth = GoogleAuth()
        gauth.credentials = credentials

        self._context['gsheet-read-wait-seconds'] = config['gsheet-read-wait-seconds']
        self._context['gsheet-read-try-count'] = config['gsheet-read-try-count']

        self.current_document_index = -1

        info(f"authorized with Google")


    ''' read the gsheet
    '''
    def read_gsheet(self, gsheet_name, worksheet_name):
        wait_for = self._context['gsheet-read-wait-seconds']
        try_count = self._context['gsheet-read-try-count']
        gsheet = None
        data = None
        for i in range(0, try_count):
            try:
                info(f"opening gsheet : {gsheet_name}")
                gsheet = self._context['_G'].open(gsheet_name)
                info(f"opened  gsheet : {gsheet_name}")

                break

            except Exception as e:
                print(e)
                warn(f"gsheet {gsheet_name} read request (attempt {i}) failed, waiting for {wait_for} seconds before trying again")
                time.sleep(float(wait_for))

        if gsheet is None:
            error('gsheet read request failed, quiting')
            sys.exit(1)

        # process the worksheet
        info(f"reading gsheet : [{gsheet_name}] worksheet : [{worksheet_name}]")
        data = process_gsheet(gsheet=gsheet, worksheet_name=worksheet_name)
        info(f"read    gsheet : [{gsheet_name}] worksheet : [{worksheet_name}]")

        return data
