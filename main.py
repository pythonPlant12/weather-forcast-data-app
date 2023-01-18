import streamlit as st
import plotly.express as px
from backend import get_data


st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days.")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        filtered_data = get_data(place, days, option)

        if option == "Temperature":
            temperatures = [data["main"]["temp"] / 10 for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=temperatures,
                             labels={"x": "Date", "y": "Temperature (ºC)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Snow": "images/snow.png", "Rain": "images/rain.png", "Clouds": "images/cloud.png",
                      "Clear": "images/clear.png"}
            sky_conditions = [data["weather"][0]["main"] for data in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            print(sky_conditions)
            st.image(image_paths, width=115)
    except KeyError:
        st.warning(body="This city doesn't exist.", icon="⚠")
