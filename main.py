import requests
import smtplib

api_key = ""  # API key from OpenWeatherMap
endpoint = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = "0.0000"  # Your latitude (float)
MY_LONG = "0.0000"  # Your longitude (float)

# Email account that sends the message
EMAIL_SENDER = "email@gmail.com"
EMAIL_SENDER_PASSWORD = "password"

# Email account that receives the message
EMAIL_RECEIVER = "email@gmail.com"

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_data_next_12_hours = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_data_next_12_hours:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 600:  # Codes less than 600 mean rain
        will_rain = True

if will_rain:
    # Assumes the sender is using a gmail account
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
    connection.sendmail(
        from_addr=EMAIL_SENDER,
        to_addrs=EMAIL_RECEIVER,
        msg="Subject:Rain Alert\n\nThere will be rain in the next 12 hours!"
    )
