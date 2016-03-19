#!/usr/bin/python
# this script could be on Linux
# experiment at your own risk!
# please, backup database before running the script

# import modules
import sqlite3
from getpass import getuser
from fnmatch import fnmatch
import os

# define finder function for database file
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# set full path to your database
# under Windows it is usually like
# "C:\Users\USER\AppData\Local\Mendeley Ltd\Mendeley Desktop\email@server.com@www.mendeley.com.sqlite"
# where USER is the name of your user, email@server.com is your email
# under Linux, it is usually like
# "/home/USER/.local/share/data/Mendeley Ltd./Mendeley Desktop/email@server.com@www.mendeley.com.sqlite"
# where USER is the name of your user, email@server.com is your email.
# !!!note, the path should be full, otherwise sqlite3 will throw an error

# setup connection
db_path = os.getenv("SystemDrive") + "\\Users\\" + getuser() + "\\AppData\\Local\\Mendeley Ltd\\Mendeley Desktop\\"
db_filename = find('*mendeley.com.sqlite', db_path)
os.system("echo Found Mendeley Database at " + db_filename[0])
conn = sqlite3.connect(db_filename[0])
c = conn.cursor()
# initialize variables
result = {}
doctype = {}
fields = {}
pages = {}
page_update_count = 0

# get max document id
c.execute('SELECT MAX(documentId) FROM DocumentContributors')
maxId = c.fetchone()
# count authors for every document
for i in range(maxId[0]):
    for row in c.execute('SELECT count(id) FROM documentContributors WHERE documentId=' + str(i)):
        result[i] = row[0]
    for row2 in c.execute('SELECT type FROM Documents WHERE id=' + str(i)):
        doctype[i] = row2[0]
# create a dictionary where documentId is associated with required field

for key in result.keys():
    a = result[key]
    if a == 0:
        b = ""
    else:
        b = doctype[key]
    if b == "JournalArticle":
        if a==1:
            fields[key] = "publisher"
        elif a == 2:
            fields[key] = "city"
        elif a == 3:
            fields[key] = "genre"

# update pages fields if they are in short format
for row in c.execute('SELECT id, pages FROM Documents'):
    try:
        pages_list = row[1].split("-")
        # if two pages given
        if len(pages_list) == 2:
            first_page = pages_list[0]
            last_page = pages_list[1]
            # if page format is short
            if int(last_page) < int(first_page):
                last_page_upd = first_page[:-len(last_page)] + last_page
                pages[row[0]] = first_page + "-" + last_page_upd
                page_update_count += 1
    except:
        # if smth went wrong, i.e. pages are in P111 format
        pass

# drop publisher/city/genre fields
c.execute('UPDATE Documents SET publisher=NULL, city=NULL, genre=NULL WHERE type=\'JournalArticle\'')
# save (commit) the changes
conn.commit()

# update table Documents by setting publisher/city/genre fields
for key in fields.keys():
    b = fields[key]
    c.execute('UPDATE Documents SET ' + b + '=\'' + b + '\' WHERE id=' + str(key))
# save (commit) the changes
conn.commit()

# update pages field in table Documents
for key in pages.keys():
    p = pages[key]
    c.execute('UPDATE Documents SET pages=\'' + p + '\' WHERE id=' + str(key))
# save (commit) the changes
conn.commit()

# print results independently of Python 2 or 3 installed
os.system("echo "+ str(page_update_count) + " page fields updated")
os.system("echo Publisher/City/Genre fields in " + str(len(fields.keys())) + " article records updated")
os.system("echo Press any key to exit...")
# close connection
conn.close()
