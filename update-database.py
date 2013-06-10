# !!! this script should be run under Windows!!!
# experiment at your own risk!
# do not forget to backup database before running the script

# import modules
import sqlite3

# set full path to your database
# under Windows it is usually like
# C:\Users\USER\AppData\Local\Mendeley Ltd\Mendeley Desktop\email@server.com@www.mendeley.com.sqlite
# where USER is the name of your user, email@server.com is your email
conn = sqlite3.connect('yourdatabase.sqlite')

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

# update table documents
for key in fields.keys():
    b = fields[key]
    c.execute('UPDATE Documents SET ' + b + '=\'' + b + '\' WHERE id=' + str(key))
# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
