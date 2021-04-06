import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["coin"]
market_values = db["coin_analysis"]
coin_information_values = db["coin_information"]


def read_market_values():
    query = {}

    return market_values.find(query)


def find_coin_informartion(coin_id):
    return coin_information_values.find_one({'coin_id': coin_id})


def get_document_count():
    return market_values.find().count()
