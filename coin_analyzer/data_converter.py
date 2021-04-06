import math
import torch
from torch.autograd import Variable


def build_market_values(coin_id, time_series):
    market_data_hourly = {'coin_id': coin_id,
                          'price': time_series['close'],
                          'market_cap': time_series['market_cap'],
                          'reddit_posts': time_series['reddit_posts'],
                          'reddit_posts_score': time_series['reddit_posts_score'],
                          'reddit_comments': time_series['reddit_comments'],
                          'reddit_comments_score': time_series['reddit_comments_score'],
                          'tweets': time_series['tweets'],
                          'tweet_spam': time_series['tweet_spam'],
                          'tweet_followers': time_series['tweet_followers'],
                          'tweet_retweets': time_series['tweet_retweets'],
                          'tweet_replies': time_series['tweet_replies'],
                          'tweet_favorites': time_series['tweet_favorites'],
                          'tweet_sentiment_impact1': time_series['tweet_sentiment_impact1'],
                          'tweet_sentiment_impact2': time_series['tweet_sentiment_impact2'],
                          'tweet_sentiment_impact3': time_series['tweet_sentiment_impact3'],
                          'tweet_sentiment_impact4': time_series['tweet_sentiment_impact4'],
                          'tweet_sentiment_impact5': time_series['tweet_sentiment_impact5'],
                          'social_score': time_series['social_score'],
                          'average_sentiment': time_series['average_sentiment'],
                          'social_impact_score': time_series['social_impact_score'],
                          'correlation_rank': time_series['correlation_rank'],
                          'alt_rank_30d': time_series['alt_rank_30d'],
                          'social_contributors': time_series['social_contributors'],
                          'price_btc': time_series['price_btc']}

    return market_data_hourly


def calculate_price_change_rate(price, next_price):
    price_change_rate = ((next_price / price) * 100) - 100
    rounded_price_change_rate = round(price_change_rate / 5) * 5

    return rounded_price_change_rate


def get_x_values(doc):
    training_x_values = [
        doc['coin_id'],
        doc['price'],
        doc['market_cap'],
        doc['reddit_posts'],
        doc['reddit_posts_score'],
        doc['reddit_posts_score'],
        doc['reddit_comments'],
        doc['reddit_comments_score'],
        doc['tweets'],
        doc['tweet_spam'],
        doc['tweet_followers'],
        doc['tweet_retweets'],
        doc['tweet_replies'],
        doc['tweet_favorites'],
        doc['tweet_sentiment_impact1'],
        doc['tweet_sentiment_impact2'],
        doc['tweet_sentiment_impact3'],
        doc['tweet_sentiment_impact4'],
        doc['tweet_sentiment_impact5'],
        doc['social_score'],
        doc['average_sentiment'],
        doc['social_impact_score'],
        doc['correlation_rank'],
        doc['alt_rank_30d'],
        doc['social_contributors'],
        doc['price_btc']
    ]

    for index in range(len(training_x_values)):
        if training_x_values[index] is None:
            training_x_values[index] = 0
        else:
            normalized_item = training_x_values[index]
            if normalized_item < -1:
                training_x_values[index] = math.log10(normalized_item * -1) * -1
            elif normalized_item > 1:
                training_x_values[index] = math.log10(normalized_item)

    return training_x_values


def get_y_values(doc):
    training_y_values = [
        doc['price_change_rate']
    ]

    return training_y_values


def prepare_data_for_training(training_data):
    training_x_values_all = []
    training_y_values_all = []

    for doc in training_data:
        if doc['price_change_rate'] is not None:
            training_x_values = get_x_values(doc)
            training_y_values = get_y_values(doc)

            training_x_values_all.append(training_x_values)
            training_y_values_all.append(training_y_values)

    training_x = Variable(torch.Tensor(training_x_values_all))
    training_y = Variable(torch.Tensor(training_y_values_all))

    return training_x, training_y


def prepare_data_for_prediction(prediction_data):
    prediction_x_values_all = []

    for doc in prediction_data:
        training_x_values = get_x_values(doc)

        prediction_x_values_all.append(training_x_values)

    prediction_x = Variable(torch.Tensor(prediction_x_values_all))

    return prediction_x
