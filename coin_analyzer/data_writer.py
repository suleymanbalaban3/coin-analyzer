import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["coin"]
market_values = db["coin_analysis"]
coin_information_values = db["coin_information"]


def insert_market_values(all_market_data_hourly):
    market_values.insert_many(all_market_data_hourly)


def upsert_coin_informations(coin_informations):
    for coin_information in coin_informations:
        coin_information_count = find_coin_informartion(coin_information['coin_id'])
        if coin_information_count == 0:
            insert_coin_informartion(coin_information)


def insert_coin_informartion(coin_information):
    coin_information_values.insert_one(coin_information)


def find_coin_informartion(coin_id):
    return coin_information_values.count({'coin_id': coin_id})