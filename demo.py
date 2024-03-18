import streamlit as st
from src.predictor import HouseModel, HousePricePredictor
from pickle import load

predictor = HousePricePredictor()

st.title('House Price Prediction Valex')

# Create form for user input
with st.form("house_input_form"):
    city = st.text_input('City')
    district = st.text_input('District')
    street = st.text_input('Street')
    house_number = st.text_input('House Number')
    rooms = st.number_input('Rooms', value=1)
    square = st.number_input('Square Meters', value=50.0)
    material = st.selectbox('Material', ['деревянный', 'иное', 'каркасно-камышитовый', 'каркасно-щитовой', 'кирпичный', 'монолитный', 'панельный', 'пеноблочный', 'сэндвич-панели', 'шлакоблочный'])
    construction_year = st.number_input('Construction Year', min_value=1900, max_value=2024, value=2000)
    bathroom = st.selectbox('Bathroom', ['2 с/у и более', 'во дворе', 'раздельный', 'совмещенный'])
    condition = st.selectbox('Condition', ['свободная планировка', 'среднее', 'требует ремонта', 'хорошее', 'черновая отделка'])
    local_phone = st.selectbox('Local Phone', ['есть', 'есть возможность подключение', 'нет'])
    internet = st.selectbox('Internet', ['ADSL', 'нет', 'оптика', 'проводной'])
    sewage = st.selectbox('Sewage', ['есть возможность подведения', 'нет', 'септик', 'центральная'])
    water = st.selectbox('Water', ['есть возможность подведения', 'нет', 'скважина', 'центральная'])
    electricity = st.selectbox('Electricity', ['есть', 'есть возможность подключения', 'нет'])
    heating_system = st.selectbox('Heating System', ['без отопления', 'на газе', 'на жидком топливе', 'на твердом топливе', 'смешанное', 'центральное'])
    gas_system = st.selectbox('Gas System', ['автономный', 'есть возможность подключения', 'магистральный', 'нет'])
    security_system = st.selectbox('Security System', ['да', 'нет'])
    territory_area_m2 = st.number_input('Territory Area (m2)', value=0.0)
    level = st.number_input('Level', value=1)
    household_buildings = st.multiselect('Household Buildings', ['да', 'нет'])
    household_number = st.number_input('Household Number', value=0)
    furniture = st.selectbox('Furniture', ['полностью', 'частично', 'нет'])

    submitted = st.form_submit_button("Predict Price")

if submitted:
    house_data = HouseModel(
        city=city,
        district=district,
        street=street,
        house_number=house_number,
        rooms=rooms,
        square=square,
        material=material,
        construction_year=construction_year,
        bathroom=bathroom,
        condition=condition,
        local_phone=local_phone,
        internet=internet,
        sewage=sewage,
        water=water,
        electricity=electricity,
        heating_system=heating_system,
        gas_system=gas_system,
        security_system=security_system,
        territory_area_m2=territory_area_m2,
        level=level,
        household_buildings=household_buildings,
        household_number=household_number,
        furniture=furniture
    )
    
    # Predict the house price
    predicted_price = predictor.predict_price(house_data)
    st.write(f"Predicted House Price: {predicted_price}")