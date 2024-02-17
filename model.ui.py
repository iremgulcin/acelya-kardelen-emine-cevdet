import streamlit as st
import pandas as pd
import json
import joblib
import matplotlib.pyplot as plt
import plotly.express as px

# json dicti loadla
with open("line_map.json", "r") as f:
    line_data = json.load(f)
model = joblib.load("hist_model_tempsiz_tscv.joblib")  # model

veriler_2022 = pd.read_feather("final_set.feather")
veriler_2022 = veriler_2022.set_index('transition_date') # indexi tarih olarak ayarla
veriler_2022["month"] = veriler_2022.index.month
veriler_2022["day"] = veriler_2022.index.day

def create_input_df(selected_date, selected_hour, transfer, line):
    """
    Creates an input DataFrame from user input and line map data.

    Args:
        selected_date (str): kullanıcının seçtiği tarih (e.g., "2023-10-27").
        selected_hour (int): şeçilen saat (e.g., 4).
        transfer (str):  ("Normal" or "Aktarma").
        line (str): seçilen hat ismi

    Returns:
        pd.DataFrame: input_df, kullacınıın seçtikleri ve tarihten çıkarılan sütunlar
    """

    # date ten aldığımız şeyler
    date_obj = pd.to_datetime(selected_date, format="%Y-%m-%d")
    day = date_obj.dayofweek
    month = date_obj.month
    dayofyear = date_obj.dayofyear
    day_of_month = date_obj.day

    # jsondan aldım hat özelliklerini 
    line_info = line_data.get(line, {})
    transport_type_id = line_info.get("transport_type_id", 0)
    top_lines_indicator = line_info.get("top_lines_indicator", 0)
    line_encoded = line_info.get("line_encoded", None)

    # input_df oluştur
    input_data = pd.DataFrame({
        "date": [date_obj],  # date i sütun olarak ekle, sonra index yap
        "transition_hour": [selected_hour],
        "transport_type_id": [transport_type_id],
        "day": [day],
        "line_encoded": [line_encoded],
        "transfer_type_b": [1 if transfer == "Normal" else 0],
        "month": [month],
        "dayofyear": [dayofyear],
        "day_of_month": [day_of_month],
        "top_lines_indicator": [top_lines_indicator],
    })

    # indexi tarih yap, ismini de değiştirdim nolur nolmaz diye
    
    input_data = input_data.set_index("date")
    input_data.index.name = "transition_date"

    return input_data


# Streamlit app
st.title("Yolcu Yoğunluğu Tahmin Sistemine Hoş Geldiniz!")
st.markdown("Lütfen gerekli yerleri doldurunuz.")
page_icon="U+1F44B"
selected_date = st.date_input("Tarih seçiniz:")
time_options = [str(x) + ":00" for x in range(0, 24)]
selected_hour = st.selectbox('Saat seçiniz:', time_options)
selected_hour = int(selected_hour.split(":")[0])
#selected_hour = st.slider("Saat seçiniz:", 0, 23, 4)  # Use slider for hour selection
transfer = st.selectbox("Transfer türünü seçiniz:", ["Normal", "Aktarma"])
line = st.selectbox("Hat seçiniz:", list(line_data.keys()))

if st.button("Submit"):
    input_df = create_input_df(selected_date, selected_hour, transfer, line)
    print(input_df.dtypes)
    print("dataset: ",input_df)
    # Make prediction
    try:
        prediction = model.predict(input_df)  

        
        if len(prediction.shape) == 1:
            predicted_passengers = abs(prediction[0])  # single value
        
        else:
            predicted_passengers = abs(prediction)[0]  # first prediction
        st.write("Tahmin edilen yolcu yoğunluğu:", int(predicted_passengers))
        
        # plot number_of_passenger for the selected line on the same day in 2022
        selected_month = input_df['month'].iloc[0]
        selected_day = input_df['day_of_month'].iloc[0]
        line_same_day_data = veriler_2022[(veriler_2022['line'] == line) & (veriler_2022['month'] == selected_month) & (veriler_2022['day'] == selected_day)]
        
               
        fig = px.line(line_same_day_data, x='transition_hour', y='number_of_passenger', 
                    color='transfer_type',
                    labels={'number_of_passenger': 'Kullanım Sayısı'},
                    title=f"{line} Hattı İçin {selected_day}/{selected_month}/2022'deki Kullanım Dağılımı")

        # Add labels and legend
        fig.update_layout(
            xaxis_title='Saat',
            yaxis_title='Kullanım Sayısı',
            legend_title='Legend',
            showlegend=True,
            hovermode = "x"  
        )

        fig.update_traces(hovertemplate='Saat: %{x} <br> Kullanım Sayısı: %{y} <extra></extra>')

        st.plotly_chart(fig)


    except Exception as e:
        st.error(f"Error making prediction: {e}")

