import streamlit as st
import pymongo
from datetime import date
from plot import convert_date_to_string



def retrieve_user_data(user):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])
    db = client['Schedule']
    collection = db[user]
    data = list(collection.find())
    client.close()
    return data


def update_tasks():
    return None


def update_user(user, status, schedule):
    client = pymongo.MongoClient(st.secrets['mongo']['uri'])

    db = client['Schedule']
    collection = db[user]
    collection.replace_one(
        {'name': user},
        {
        'name': user,
        'status': status,
        'schedule': convert_date_to_string(schedule)
        }
        )
    client.close()

st.write(retrieve_user_data('Dank'))
if st.button('update'):
    update_user('Dank', 'Busy', [["2024-01-01", '2024-01-02']])