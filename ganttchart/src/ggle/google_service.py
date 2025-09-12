#!/usr/bin/env python

import gspread

from googleapiclient.discovery import build
from google.oauth2 import service_account
from apiclient import errors
from googleapiclient.errors import HttpError

from ggle.google_sheet import GoogleSheet

from helper.logger import *

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


''' Google service wrapper
'''
class GoogleService(object):

    ''' constructor
    '''
    def __init__(self, service_account_json_path):

        # get credentials for service-account
        credentials = service_account.Credentials.from_service_account_file(service_account_json_path)
        scoped_credentials = credentials.with_scopes(SCOPES)

        # the gsheet service
        self.gsheet_service = build('sheets', 'v4', credentials=credentials)

        # the drive service
        self.drive_service = build('drive', 'v3', credentials=credentials)

        # using gspread for proxying the gsheet API's
        self.gspread = gspread.authorize(scoped_credentials)

        # authed_session = AuthorizedSession(credentials)
        # response = authed_session.get('https://www.googleapis.com/storage/v1/b')

        # authed_http = AuthorizedHttp(credentials)
        # response = authed_http.request('GET', 'https://www.googleapis.com/storage/v1/b')


    ''' open a gsheet
    '''
    def open(self, gsheet_name, try_for=3):
        gspread_sheet = None
        wait_for = 30
        for try_count in range(1, try_for+1):
            try:
                gspread_sheet = self.gspread.open(gsheet_name)
                break

            except Exception as e:
                print(e)
                if try_count < try_for:
                    warn(f"open gsheet failed in [{try_count}] try, trying again in {wait_for} seconds", nesting_level=1)
                    time.sleep(wait_for)
                else:
                    warn(f"open gsheet failed in [{try_count}] try", nesting_level=1)

        if gspread_sheet:
            return GoogleSheet(google_service=self, gspread_sheet=gspread_sheet)
        else:
            return None


    ''' get a drive file
    '''
    def get_drive_file(self, drive_file_name):
        try:
            files = []
            page_token = None
            while True:
                q = f"name = '{drive_file_name}'"
                response = self.drive_service.files().list(q=q,
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, webViewLink)',
                                                pageToken=page_token).execute()

                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            if len(files) > 0:
                return files[0]

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None



    ''' copy a file
    '''
    def copy_file(self, source_file_id, target_folder_id, target_file_title):
        copied_file = {'name': target_file_title, 'parents' : [target_folder_id]}
        try:
            response = self.drive_service.files().copy(fileId=source_file_id, fields='id', body=copied_file).execute()
            print(response)
            return response
        except Exception as error:
            print(error)
            return None


    ''' share a file

        Args:
            service: Drive API service instance.
            file_id: ID of the file to insert permission for.
            value: User or group e-mail address, domain name or None for 'default'
                    type.
            perm_type: The value 'user', 'group', 'domain' or 'default'.
            role: The value 'owner', 'writer' or 'reader'.
        Returns:
            The inserted permission if successful, None otherwise.
    '''
    def share(self, file_id, email, perm_type, role):
        new_permission = {
            'emailAddress': email,
            'type': perm_type,
            'role': role
        }
        try:
            return self.drive_service.permissions().create(fileId=file_id, moveToNewOwnersRoot=True, transferOwnership=True, body=new_permission).execute()

        except Exception as error:
            print(error)

        return None
