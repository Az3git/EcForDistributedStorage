import os

def nodes_create(n, storage):
    for i in range(n):
        try:
            os.mkdir(storage + '/' + 'disk' + str(i))
        except:
            pass


