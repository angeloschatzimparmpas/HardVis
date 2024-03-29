#!/usr/bin/env python
import sys
import pandas as pd
import pymongo
import json
import os


def import_content(filepath):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['mydb']
    collection_name = 'VehicleC' 
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.drop()
    db_cm.insert_many(data_json)

if __name__ == "__main__":
  filepath = './data/vehicle.csv'
  import_content(filepath)