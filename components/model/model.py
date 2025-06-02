import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model


def predict_tomorrow(loc_code, data_type):
    sequence_length = 30
    csv_file_bui = 'data/daily_average_water_bui.csv'
    csv_file_temp = 'data/daily_average_water_temp.csv'

    model = load_model('components/model/lstm_model_2012_2024.h5') # 모델 불러오기
    
    if data_type == 'tideObsRecent':
        data = pd.read_csv(csv_file_temp)
    else:
        data = pd.read_csv(csv_file_bui)

    input = data[data['obs_post_id'] == loc_code]['water_temp'].to_numpy()

    # 오늘 예측
    input_sequence = input.reshape((1, sequence_length, 1))
    predicted_temp_day1 = model.predict(input_sequence, verbose=0)[0][0]

    # 내일 예측
    new_sequence = np.append(input[1:], predicted_temp_day1).reshape((1, sequence_length, 1))
    predicted_temp_day2 = model.predict(new_sequence, verbose=0)[0][0]

    return predicted_temp_day2

if __name__ == "__main__":
    print(predict_tomorrow('HB_0001', 'buObsRecent'))