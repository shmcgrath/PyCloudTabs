# -*- coding: UTF-8 -*-

import os
import datetime
import sqlite3
from sqlite3 import Error
import logging
import sys
from collections import Mapping
from pathlib import Path

def get_today_string():
    today = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
    return today

def create_bookmark_file(home):
    today = get_today_string()
    bookmarksFile = home + '/' + today + '-iCloudTabs.html'
    print('Creating cloudTabs file at ' + bookmarksFile)
    cloudTabsBookmarks = open(bookmarksFile, 'w')
    cloudTabsBookmarks.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
    cloudTabsBookmarks.write('    <!--This is an automatically generated file.\n')
    cloudTabsBookmarks.write('    It will be read and overwritten.\n')
    cloudTabsBookmarks.write('    Do Not Edit! -->\n')
    cloudTabsBookmarks.write('    <Title>Bookmarks</Title>\n')
    cloudTabsBookmarks.write('    <H1>Bookmarks</H1>\n')
    cloudTabsBookmarks.write('    <DL>')

    return cloudTabsBookmarks

def write_bookmark_footer(cloudTabsBookmarks):
    cloudTabsBookmarks.write('\n    </DL>')
    cloudTabsBookmarks.close()

def gather_cloud_tabs(conn, cloudTabsBookmarks):
    cloudTabsSql = 'SELECT cloud_tabs.title title, cloud_tabs.url url FROM cloud_tabs'
    c = conn.cursor()
    for row in c.execute(cloudTabsSql):
        title = row[0]
        url = row[1]
        bookmark = '\n      <DT><A HREF="' + url + '">' + title + '</A>'
        cloudTabsBookmarks.write(bookmark)

def create_connection(db_file):
    # create a database connection to the SQLite database
    # specified by the db_file
    # :param db_file: database file
    # :return: connection object or None
    # http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def main():
    home = str(Path.home())
    cloudTabsLocation = home + '/Library/Safari/CloudTabs.db'
    cloudTabsBookmarks = create_bookmark_file(home)

    conn = create_connection(cloudTabsLocation)
    with conn:
        gather_cloud_tabs(conn, cloudTabsBookmarks)

    write_bookmark_footer(cloudTabsBookmarks)


if __name__ == '__main__':
    main()
