#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download a updated file from Dropbox.
This is an example app for API v2.
"""
import pdb
import sys
import os
import time
import logging
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Add OAuth2 access token here.
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
TOKEN = 'i_i************AJZql4Oi9vQY8Gwrccz7VIsqEitcEyemfH_C_PVFDiKzA'

LOCALFILE = 'C:/Users/ankur-kumar/Desktop/Oauth/ankur.txt'
DROPBOXPATH = ''
DROPBOXFILENAME = 'index.html'



# Uploads contents of LOCALFILE to Dropbox
def upload():
    with open(LOCALFILE, 'r') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + DROPBOXPATH + '/' + DROPBOXFILENAME + "...")
        try:
            dbx.files_upload(f, DROPBOXPATH + '/' + DROPBOXFILENAME, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
#check file exist or not
def file_Exist():
    try:
        res = dbx.files_list_folder(DROPBOXPATH)
    except dropbox.exceptions.ApiError as err:
        sys.exit('Folder listing failed for', DROPBOXPATH, '-- assumped empty:', err)
    for entry in res.entries:
        if entry.name == DROPBOXFILENAME:
            return "Success"

    sys.exit("ERROR: File not Found. Invalid file name or path")


# Download file to a latest revision
def download(rev=None):
    try:
        dbx.files_download_to_file(LOCALFILE, DROPBOXPATH + '/' + DROPBOXFILENAME, rev)
    except dropbox.exceptions.HttpError as err:
        sys.exit('*** HTTP error', err)


#Delete the file from dropbox
def delete(rev=None):
    try:
        dbx.files_delete(DROPBOXPATH + '/' + DROPBOXFILENAME)
    except dropbox.exceptions.HttpError as err:
        sys.exit('*** HTTP error', err)
		
		

#Create a new Folder
def create_folder(rev=None):
    try:
        dbx.files_create_folder(DROPBOXPATH + '/NewFolder')
    except dropbox.exceptions.HttpError as err:
        sys.exit('*** HTTP error', err)


def select_revision():
    # Get the revisions for a file and sort by the datetime object
    try:
        revisions = sorted(dbx.files_list_revisions(DROPBOXPATH + '/' + DROPBOXFILENAME, limit=50).entries,
                           key=lambda entry: entry.server_modified)
    except dropbox.exceptions.HttpError as err:
        sys.exit('*** HTTP error', err)

    # Return the latest revision (Last entry, because revisions was sorted oldest:newest)
    return revisions[len(revisions)-1].rev
if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")
    # Create an instance of a Dropbox class, which can make requests to the API.
    try:
        dbx = dropbox.Dropbox(TOKEN)
    except dropbox.exceptions.HttpError as err:
        sys.exit('*** HTTP error', err)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    #file_Exist()
    #delete()
    #upload()
    #create_folder()
    #select_revision()
    download()




#   EOFB
