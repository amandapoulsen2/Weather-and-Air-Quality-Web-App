import streamlit as st
import requests
import os
from datetime import date

api_key = os.environ["STREAMLIT_AIR_VISUAL_API_KEY"]

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

# Using object notation
category = st.sidebar.selectbox(
    "Choose a category?",
    (
        "By City, State, and Country",
        "By Nearest City (IP Address)",
        "By Latitude and Longitude",
    ),
    index=0,
)

today = date.today()


@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)


@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict


@st.cache_data
def generate_list_of_states(country_selected):
    states_url = (
        f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    )
    states_dict = requests.get(states_url).json()
    return states_dict


@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict


# {
#         "ts": "2017-02-01T03:00:00.000Z",  //timestamp
#         "aqius": 21, //AQI value based on US EPA standard
#         "aqicn": 7, //AQI value based on China MEP standard
#         "tp": 8, //temperature in Celsius
#         "tp_min": 6, //minimum temperature in Celsius
#         "pr": 976,  //atmospheric pressure in hPa
#         "hu": 100, //humidity %
#         "ws": 3, //wind speed (m/s)
#         "wd": 313, //wind direction, as an angle of 360° (N=0, E=90, S=180, W=270)
#         "ic": "10n" //weather icon code, see below for icon index
# },


def generate_info(data):
    location = data["location"]
    latitude = location["coordinates"][1]
    longitude = location["coordinates"][0]

    city = data["city"]

    current = data["current"]

    weather = current["weather"]
    cel = weather["tp"] / 1.0
    far = cel * (9 / 5) + 32

    pollution = current["pollution"]

    map_creator(latitude, longitude)

    st.markdown("Today is **" + today.strftime("%Y-%m-%d") + "**")

    st.markdown(
        "Temperature in {city} is **{cel}\N{DEGREE SIGN}C/{far}\N{DEGREE SIGN}F**".format(
            city=city, cel=round(cel, 1), far=round(far, 1)
        ),
        unsafe_allow_html=True,
    )
    st.markdown("Humidity is **{}**".format(weather["hu"]))

    st.markdown("The air quality index is currently **{}**".format(pollution["aqius"]))


if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = []
        for i in countries_dict["data"]:
            countries_list.append(i["country"])
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=countries_list)

        if country_selected:
            # TODO: Generate the list of states, and add a select box for the user to choose the state
            states_dic = generate_list_of_states(country_selected)
            if states_dic["status"] == "success":
                states_list = []
                for i in states_dic["data"]:
                    states_list.append(i["state"])
                states_list.insert(0, "")

                state_selected = st.selectbox("Select a state", options=states_list)

                if state_selected:
                    # TODO: Generate the list of cities, and add a select box for the user to choose the city
                    cities_dic = generate_list_of_cities(
                        state_selected, country_selected
                    )
                    if cities_dic["status"] == "success":
                        cities_list = []
                        for i in cities_dic["data"]:
                            cities_list.append(i["city"])
                        cities_list.insert(0, "")

                        city_selected = st.selectbox(
                            "Select a city", options=cities_list
                        )

                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()

                            if aqi_data_dict["status"] == "success":
                                # TODO: Display the weather and air quality data as shown in the video and description of the assignment
                                data = aqi_data_dict["data"]

                                generate_info(data)
                            else:
                                st.warning("No data available for this location.")
                        else:
                            st.warning(
                                "No stations available, please select another city"
                            )
                else:
                    st.warning("No stations available, please select another state")
        else:
            st.warning("No stations available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")
elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
        # TODO: Display the weather and air quality data as shown in the video and
        # description of the assignment
        data = aqi_data_dict["data"]

        generate_info(data)
    else:
        st.warning("No data available for this location.")
elif category == "By Latitude and Longitude":
    # TODO: Add two text input boxes for the user to enter the latitude and longitude information
    latitude = st.text_input("latitude, e.g. 37.76", key="latitude", placeholder=37.76)
    longitude = st.text_input(
        "longitude, e.g. -122.4", key="longitude", placeholder=-122.4
    )

    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
            # TODO: Display the weather and air quality data as shown in the video and description of the assignment
            data = aqi_data_dict["data"]

            generate_info(data)
        else:
            st.warning("No data available for this location.")
