import streamlit as st
import pymongo
from datetime import date
from plot import datetime_to_str


def retrieve_user_data(users):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Schedule']
    final_list = []
    for user in users:
        collection = db[user]
        data = collection.find()
        final_list.append(list(data))
    client.close()
    return final_list


def retrieve_tasks(task_collections):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Tasks']
    final_list = []
    for task_collection in task_collections:
        collection = db[task_collection]
        data = collection.find()
        final_list.append(list(data))
    client.close()
    return final_list


def update_tasks(task_collection, completed_status, dealine, participants_list, progress, task_name):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Tasks']
    collection = db[task_collection]
    collection.replace_one(
        {'name': task_name},
        {
          'name': task_name,
          'completed': completed_status,
          'participants': participants_list,
          'progress': progress,
        }
    )
    client.close()


def update_user(user, status, schedule):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Schedule']
    collection = db[user]
    collection.replace_one(
        {'name': user},
        {
            'name': user,
            'status': status,
            'schedule': schedule
            }
        )
    client.close()


def add_user(user, status, schedule):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Schedule']
    collection = db[user]
    collection.insert_one(
        {
            'name': user,
            'status': status,
            'schedule': schedule
            }
        )
    client.close()


# if st.button('update'):
#     add_user('V.Dang', 'Active', [[]])
