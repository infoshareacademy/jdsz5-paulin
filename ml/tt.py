from _init import rest_models

from _init import Dataset
import pandas as pd

if __name__ == "__main__":
    # data_set = Dataset()
    # df = data_set.df_set(preprocess=True)
    x_user = pd.DataFrame.from_dict({
        'area_total': [50.0], 'building_year': [2000], 'fixed_latitude': [50.00],
        'fixed_longitude': [20.00], 'apartment_room_number': [2.0], 'apartment_floor': [2.0],
        'location_province': [4.0]
    })
    print(x_user.shape)
    rm = rest_models(x_user, "", False)
    m = rm.load_ball(x_user)
    print(m)
    # mm = rm.load_model("regression", load_type="joblib")
    # print(mm)
