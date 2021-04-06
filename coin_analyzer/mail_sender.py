import smtplib
from datetime import datetime


def send_mail_trackers(body):
    gmail_user = 'admin_mail_adress@gmail.com'
    gmail_password = '{MAIL_PASSWORD}'

    sent_from = gmail_user
    to = ['target_mail_adresses@gmail.com']
    subject = 'Please Check this Coins :)'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print('Something went wrong...', e)


def send_mail(high_rise_coin_predictions, low_rise_coin_predictions):
    print("############################# Predictions ##############################")
    print("high_rise_coin_predictions", high_rise_coin_predictions)
    print("------------------------------------------------------------")
    print("low_rise_coin_predictions", low_rise_coin_predictions)
    print("########################################################################")
    mail_body = prepare_mail_body(high_rise_coin_predictions, low_rise_coin_predictions)

    send_mail_trackers(mail_body)


def prepare_mail_body(high_rise_coin_predictions, low_rise_coin_predictions):
    high_rise_coin_predictions_to_string = prediction_to_string(high_rise_coin_predictions, True)
    low_rise_coin_predictions_to_string = prediction_to_string(low_rise_coin_predictions, False)

    mail_body = ''
    mail_body += 'Date :' + str(datetime.now()) + '\n\n---- high_rise_coin_predictions ----\n\n' + high_rise_coin_predictions_to_string
    mail_body += '\n\n---- low_rise_coin_predictions ----\n\n' + low_rise_coin_predictions_to_string

    return mail_body


def prediction_to_string(predictions, is_high_rise_coin):
    result_string = ''
    sign = ''

    if is_high_rise_coin is True:
        sign = '+'

    for prediction in predictions:
        result_string = result_string + str(prediction['symbol']) \
                        + ' price: ' + str(prediction['current_price']) \
                        + ' prediction: %' + sign + str(prediction['predicted_rise_percentage']) + '\n\n'

    return result_string
