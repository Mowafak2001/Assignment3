import requests
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

headers = {'Authorization': f'Bearer {access_token}'}

# Fetches step count data from Fitbit API for a specified date range.
def get_user_steps(day):
    url = f"https://api.fitbit.com/1/user/-/activities/steps/date/{day}/30d.json"
    print(f'URL generated for step data retrieval:\n{url}')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        step = response.json()
        step_x_vals = []
        step_y_vals = []

        for i in step["activities-steps"]:
            step_x_vals.append(i["dateTime"])
            step_y_vals.append(int(i["value"]))

        steps_df = pd.DataFrame({'Date': step_x_vals, 'Steps': step_y_vals})
        return steps_df
    else:
        print(f"Error: {response.status_code}")
        return None

# New function to get user zone minutes for a 30-day period
def get_user_zone(day):
    url = f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{day}/30d.json"
    print(f'URL generated for zone minutes data retrieval:\n{url}')
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        zones = response.json()

        dates = []
        active_zone_minutes = []
        fat_burning_zone_minutes = []
        cardio_zone_minutes = []
        peak_zone_minutes = []

        for entry in zones["activities-active-zone-minutes"]:
            date = entry["dateTime"]
            minutes = entry["value"]

            active_minutes = minutes.get('activeZoneMinutes', 0)
            fat_burn = minutes.get('fatBurningZoneMinutes', 0)
            cardio = minutes.get('cardioActiveZoneMinutes', 0)
            peak = minutes.get('peakActiveZoneMinutes', 0)

            dates.append(date)
            active_zone_minutes.append(active_minutes)
            fat_burning_zone_minutes.append(fat_burn)
            cardio_zone_minutes.append(cardio)
            peak_zone_minutes.append(peak)

        df = pd.DataFrame({
            'Date': dates,
            'Active': active_zone_minutes,
            'Fat_Burning': fat_burning_zone_minutes,
            'Cardio': cardio_zone_minutes,
            'Peak': peak_zone_minutes
        })

        df.to_csv(f'zone_minutes_end_{day}.csv', index=False)
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

# Fetches heart rate per-minute data from Fitbit API for a given day.
def get_hr_per_min(day):
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{day}/1d/1min.json"
    print(f'URL generated for HR data retrieval:\n{url}')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        heart = response.json()
        heart_xvals = []
        heart_yvals = []

        for x in heart["activities-heart-intraday"]["dataset"]:
            heart_xvals.append(x["time"])
            heart_yvals.append(x["value"])

        df = pd.DataFrame({'time': heart_xvals, 'HR': heart_yvals})
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    day = input('Enter a date (yyyy-mm-dd): ')
    print()

    df_steps = get_user_steps(day)
    if df_steps is not None:
        df_steps.to_csv(f'steps-end-{day}.csv')
        print(f'Saving 30-day step data to steps-end-{day}.csv\n')
    else:
        print(f"No step data available for {day}")

    df_hr = get_hr_per_min(day)
    if df_hr is not None:
        df_hr.to_csv(f'hr-{day}.csv')
        print(f'Saving heart rate data for {day} to hr-{day}.csv\n')
    else:
        print(f"No heart rate data available for {day}")

    df_zone = get_user_zone(day)
    if df_zone is not None:
        df_zone.to_csv(f'zone_minutes_end_{day}.csv')
        print(f'Saving zone minutes data to zone_minutes_end_{day}.csv\n')
    else:
        print(f"No zone minutes data available for {day}")

if __name__ == '__main__':
    main()
