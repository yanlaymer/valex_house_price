import pandas as pd
import xgboost as xgb
from pydantic import BaseModel
from typing import List, Optional
from pickle import load

class HouseModel(BaseModel):
    city: str
    district: str
    street: str
    house_number: str
    rooms: int
    square: float
    material: str
    construction_year: float
    bathroom: str
    condition: str
    local_phone: str
    internet: str
    sewage: str
    water: str
    electricity: str
    heating_system: str
    gas_system: str
    security_system: str
    territory_area_m2: float
    level: int
    household_buildings: Optional[List[str]]
    household_number: int
    furniture: str


class HousePricePredictor:
    def __init__(self):
        self.house_model = load(open('weights/house_model.pkl', 'rb'))
        self.train_columns = load(open('weights/df_columns.pkl', 'rb'))
        self.numerics = ['territory_area_m2', 'level', 'square', 'construction_year', 'rooms']

    def predict_price(self, house_data: HouseModel) -> float:
        df = {k: 0 for k in self.train_columns}

        json_to_send = house_data.model_dump()

        temp = {}
        for i in ['city', 'district', 'street', 'house_number', 'household_buildings', 'household_number', 'furniture']:
            temp[i] = json_to_send.get(i)
            json_to_send.__delitem__(i)

        if temp.get('household_buildings'):
            if temp.get('household_buildings') in ['да', 'нет']:
                df.update({'household_buildings_{}'.format(temp.get('household_buildings')): 1})

        df.update({k: v for k, v in json_to_send.items() if k in self.numerics})
        df.update({k + '_' + str(v): 1 for k, v in json_to_send.items() if k not in self.numerics})

        df = pd.DataFrame(df, index=[0])
        
        self.price_per_square_meter = self.house_model.predict(xgb.DMatrix(df))[0]
        predicted_base_price = self.price_per_square_meter * df['square'].values[0]

        # Apply location-based multipliers
        predicted_base_price = self._apply_location_multipliers(temp, predicted_base_price)

        # Apply other multipliers
        if temp.get("household_number") > 1:
            predicted_base_price *= (0.98 - (0.05 * temp.get("household_number")))

        if temp.get("furniture") == "полностью":
            predicted_base_price *= 1.05

        if temp.get("furniture") == "частично":
            predicted_base_price *= 1.003

        if temp.get("household_buildings") == "да":
            predicted_base_price *= 1.03

        return predicted_base_price

    def _apply_location_multipliers(self, temp, base_price):
        if temp.get("city") == "Алматы":
            if temp.get("district") in ["Бостандыкский", "Медеуский", "Ауэзовский", "Алмалинский"]:
                return base_price
            elif temp.get("district") in ["Алатауский", "Турксибский", "Жетысуский", "Наурызбайский"]:
                return base_price * 0.9
            else:
                return base_price * 0.75
        elif temp.get("city") in ["Астана", "Шымкент"]:
            return base_price * 0.65
        elif "обл." in temp.get("city"):
            return base_price * 0.50
        else:
            return base_price * 0.6
