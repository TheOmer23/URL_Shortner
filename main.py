import asyncio
from req import *
from pymongo import MongoClient
from urllib.parse import urlparse
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import string
import random

uri = "mongodb+srv://omer3199:miniMini6060@url.tp7zm.mongodb.net/?retryWrites=true&w=majority&appName=URL"


def connect_to_db():
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['URLs']
        return db
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def get_url_input():
    try:
        url = input("Please enter URL - ")
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return url
        else:
            print("The entered URL is not valid.")
            return await get_url_input()
    except Exception as e:
        print(f"An error occurred: {e}")
    
async def create_short_url(n=5):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + \
        string.digits) for _ in range(n)
    )

async def save_to_db(collection_name='URL'):
    try:
        url= await get_url_input()
        short_url= await create_short_url()

        db = connect_to_db()
        collection = db[collection_name]
        if not collection.find_one({"original_url": url}):
            document = {"original_url": url, "short_url": short_url}
            insert_doc = collection.insert_one(document)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def find_short_in_db(url, collection_name='URL'):
    try:
        db = connect_to_db()
        collection = db[collection_name]
        obj = collection.find_one({"short_url": url})
        return obj["original_url"] if obj else None
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 

async def find_long_in_db(url, collection_name='URL'):
    try:
        db = connect_to_db()
        collection = db[collection_name]
        obj = collection.find_one({"original_url": url})
        return obj["short_url"] if obj else None
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 


if __name__ == "__main__":
    asyncio.run(save_to_db())
    # print(asyncio.run(find_short_in_db("https://short04Hbf")))