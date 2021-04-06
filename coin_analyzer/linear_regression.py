import torch
from datetime import datetime
from data_converter import prepare_data_for_training, prepare_data_for_prediction
from data_reader import find_coin_informartion

PATH = "..\\coin-analyzer\\models\\coin_model.pt"


class LinearRegressionModel(torch.nn.Module):

    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(26, 1) 

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred


def train(marketing_data):
    x_data, y_data = prepare_data_for_training(marketing_data)

    coin_model = LinearRegressionModel()

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(coin_model.parameters(), lr=0.001)

    print('Training Model...', datetime.now())

    for epoch in range(50000):
        optimizer.zero_grad()

        outputs = coin_model(x_data)

        loss = criterion(outputs, y_data)
        loss.backward()

        optimizer.step()

    save_model(coin_model)


def predict(prediction_data):
    x_data = prepare_data_for_prediction(prediction_data)
    coin_model = load_model()
    predictions = []

    for coefficient_index in range(len(x_data)):
        predicted_price_change_rate = round(float(coin_model(x_data[coefficient_index]).data.numpy()) * 10, 2)

        coin_information = find_coin_informartion(prediction_data[coefficient_index]['coin_id'])
        symbol = coin_information['symbol']

        current_price = round(float(prediction_data[coefficient_index]['price']), 4)

        predictions.append(
            {
                'symbol': symbol,
                'current_price': current_price,
                'predicted_rise_percentage': predicted_price_change_rate
            }
        )

    return predictions


def save_model(coin_model):
    torch.save(coin_model, PATH)
    print("New Model Created and saved...", datetime.now())


def load_model():
    coin_model = torch.load(PATH)
    coin_model.eval()

    print("Model Loaded...", datetime.now())

    return coin_model
