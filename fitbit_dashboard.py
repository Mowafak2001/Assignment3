import fitbit_data
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# To run: streamlit run fitbit_dashboard.py

st.title("Mowafawk's Fitbit Dashboard")

'''
Figure 1:

Step count for a 30-day period
'''

# Use today's date as the default value
today = datetime.now().strftime('%Y-%m-%d')

# Construct date string and retrieve step count
df_steps = fitbit_data.get_user_steps(today)

if df_steps is not None:
    fig1 = plt.figure()
    ax = sns.barplot(x='Steps', y='Date', data=df_steps, orient='h', color='blue', alpha=0.6)
    avg_steps = df_steps['Steps'].mean()
    ax.axvline(x=avg_steps, linewidth=2, color='orange', ls=':')
    st.subheader('Step count from last 30 days')
    st.pyplot(fig1)

st.markdown('---')

'''
Figure 2:

Heart rate data for selected day
'''

# Allow user to pick a date
selected_day = st.date_input(label='Select a day:')
day_str = selected_day.strftime('%Y-%m-%d')

df_hr = fitbit_data.get_hr_per_min(day_str)
if df_hr is not None:
    df_hr['HR_10_min_avg'] = df_hr['HR'].rolling(window=10).mean()

    fig2 = plt.figure()
    st.subheader(f'Heart rate for {day_str} (10-minute average)')
    sns.set(font_scale=0.7)
    plot_ = sns.lineplot(data=df_hr, x='time', y='HR_10_min_avg')
    avg_hr = df_hr['HR_10_min_avg'].mean()
    plot_.axhline(y=avg_hr, linewidth=2, color='orange', ls=':')
    plt.xticks(rotation=90)
    st.pyplot(fig2)

st.markdown('---')

'''

# Figure 3:

# Zone minutes data for the past 30 days

'''
df_zone = fitbit_data.get_user_zone(today)
if df_zone is not None:
    st.subheader('Zone minutes from last 30 days')
    st.dataframe(df_zone)

    # Create plot for zone minutes
    fig3, ax = plt.subplots()
    df_zone.set_index('Date', inplace=True)
    
    # Plot each zone separately for better clarity
    df_zone.plot(ax=ax)
    plt.title('Zone minutes over the last 30 days')
    plt.xlabel('Date')
    plt.ylabel('Minutes in each zone')
    
    # Reduce the number of ticks and rotate labels for better readability
    ax.set_xticks(ax.get_xticks()[::3])  # Show every 3rd date
    plt.xticks(rotation=45, ha='right')  # Rotate and align labels

    st.pyplot(fig3)


