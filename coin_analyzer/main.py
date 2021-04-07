import operator
import schedule
import time

from data_writer import insert_market_values, upsert_coin_informations
from linear_regression import train, predict
from coin_api import read_current_market_values, read_specified_hour_market_values
from data_reader import read_market_values, get_document_count
from mail_sender import send_mail


def create_new_model():
    hour_interval_count = 25
    document_count = get_document_count()

    if document_count == 0:
        hour_interval_count = 125

    market_data, coin_informations = read_specified_hour_market_values(hour_interval_count)
    insert_market_values(market_data)
    upsert_coin_informations(coin_informations)

    market_data_for_training = read_market_values()
    train(market_data_for_training)


def send_predictions():
    current_market_data_for_prediction, coin_informations = read_current_market_values()
    upsert_coin_informations(coin_informations)

    try:
        predictions = predict(current_market_data_for_prediction)

        high_rise_coin_predictions = []
        low_rise_coin_predictions = []

        for prediction in predictions:
            if prediction['predicted_rise_percentage'] >= 8.0:
                high_rise_coin_predictions.append(prediction)
            elif prediction['predicted_rise_percentage'] <= -10.0:
                low_rise_coin_predictions.append(prediction)

        high_rise_coin_predictions.sort(key=operator.itemgetter('predicted_rise_percentage'), reverse=True)
        low_rise_coin_predictions.sort(key=operator.itemgetter('predicted_rise_percentage'))

        high_rise_coin_prediction_count = len(high_rise_coin_predictions)
        low_rise_coin_prediction_count = len(low_rise_coin_predictions)

        if high_rise_coin_prediction_count > 0 or low_rise_coin_prediction_count > 0:
            send_mail(high_rise_coin_predictions, low_rise_coin_predictions)

    except Exception as err:
        print(f'Prediction was failed : {err}')


if __name__ == '__main__':

    #create_new_model()
    #send_predictions()

    schedule.every().day.at("00:01").do(create_new_model)
    schedule.every().hour.at(":10").do(send_predictions)

    while True:
        schedule.run_pending()
        time.sleep(1)
