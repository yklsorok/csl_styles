#!/usr/bin/python
# this script could be on Linux
# experiment at your own risk!
# please, backup database before running the script

# import modules
import sqlite3
import os
import fnmatch

# define finder function for database file
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# set full path to your database
# under Windows it is usually like
# "C:\Users\USER\AppData\Local\Mendeley Ltd\Mendeley Desktop\email@server.com@www.mendeley.com.sqlite"
# where USER is the name of your user, email@server.com is your email
# under Linux, it is usually like
# "/home/USER/.local/share/data/Mendeley Ltd./Mendeley Desktop/email@server.com@www.mendeley.com.sqlite"
# where USER is the name of your user, email@server.com is your email. 
# !!!note, there should be the full path, otherwise sqlite3 will throw an error

db_path = "/home/" + os.getlogin() + "/.local/share/data/Mendeley Ltd./Mendeley Desktop/"
db_filename = find('*mendeley.com.sqlite', db_path)
conn = sqlite3.connect(db_filename[1])

result = {}
fields = {}
c = conn.cursor()
# get max document id
c.execute('SELECT MAX(documentId) FROM DocumentContributors')
maxId = c.fetchone()
# count authors for every document
for i in range(maxId[0]):
    for row in c.execute('SELECT count(id) FROM documentContributors WHERE documentId=' + str(i)):
        result[i] = row[0]
# create a dictionary where documentId is associated with required field
for key in result.keys():
    a = result[key]
    if a == 1:
        fields[key] = "publisher"
    elif a == 2:
        fields[key] = "city"
    elif a == 3:
        fields[key] = "genre"

# update table "documents"
for key in fields.keys():
    b = fields[key]
    c.execute('UPDATE Documents SET ' + b + '=\'' + b + '\' WHERE id=' + str(key))
# save (commit) the changes
conn.commit()

# close connection
conn.close()
