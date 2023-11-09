# Readme

## Build

### Commands

#### Install Requirements

```bash
python3 -m pip install -r requirements.txt
```

#### Install Streamlit

```bash
python3 -m pip install streamlit
```

## Run

### Streamlit

```bash
export STREAMLIT_AIR_VISUAL_API_KEY=key
python3 -m pip streamlit run streamlit_server.py
```

## Instructions

- Set up the project:
  a. Install the required Python libraries, such as Streamlit, Requests, and Streamlit-folium. -- done
  b. Register for a free API key from AirVisual to access their API. -- done
- Build the Streamlit application:
  a. Create a new Python file and import the necessary libraries. -- done?
  b. Initialize the Streamlit application and set up the layout. -- done?
- Implement the 3 location selection methods:
  a. Create select box widgets for users to select a country, state, and city. When the user selects a location, fetch the corresponding data from the AirVisual API.
  b. The nearest city based on the user's IP address. To achieve this, make use of the IP geolocation endpoint provided by the AirVisual API.
  c. Provide two text input boxes for users to enter latitude and longitude information. When the user submits the coordinates, fetch the corresponding data from the AirVisual API.
- Display the weather and air quality information:
  a. Remember to parse and format the data retrieved from the API.
  b. Display the temperature, humidity, and air quality index using Streamlit widgets (a table is also accepted here).
  c. Integrate the Streamlit-folium library to display a map of the specified location (a function has been provided for this part).
