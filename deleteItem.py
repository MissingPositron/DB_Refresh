import pymongo
import os, re
import datetime
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017")
# database
mydb = myclient['MT_checkout_list']
# collection
mycol = mydb['lists']
# query
myquery = {"MT_stage": "MT2", "package": "tb_123__SLC_PRG_2ch_cst_firmware_scr1477p0__nvcc"}

print("delete begin...")
for x in mycol.find(myquery):
    print(x)

del_status = mycol.delete_many(myquery)
print(del_status.deleted_count, " records has been deleted")
    