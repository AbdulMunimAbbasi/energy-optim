
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Simulate Energy ---
def simulate_energy(days):
    hours = days * 24
    data = []
    for h in range(hours):
        hour = h % 24
        occupancy = 1 if 8 <= hour <= 18 else 0
        temp = 20 + 5 * np.sin(hour * np.pi / 12)
        machine1 = 5 if occupancy else 2
        hvac = 3 if temp > 25 else 2
        lighting = 1.5 if 6 <= hour <= 18 else 2.5
        total = machine1 + hvac + lighting + 1
        data.append([h, occupancy, temp, machine1, hvac, lighting, total])

    df = pd.DataFrame(data, columns=['Hour', 'Occupancy', 'Temp', 'Machine1', 'HVAC', 'Lighting', 'Total_kWh'])
    return df

# --- Optimization ---
def optimize(df):
    df['Machine1_opt'] = df.apply(lambda row: row['Machine1'] - 2 if row['Occupancy'] == 0 else row['Machine1'], axis=1)
    df['HVAC_opt'] = df.apply(lambda row: row['HVAC'] - 1 if row['Temp'] < 22 else row['HVAC'], axis=1)
    df['Lighting_opt'] = df.apply(lambda row: row['Lighting'] - 0.5 if 6 <= row['Hour'] <= 18 else row['Lighting'], axis=1)

    df['Optimized_kWh'] = df['Machine1_opt'] + df['HVAC_opt'] + df['Lighting_opt'] + 1
    df['Savings'] = df['Total_kWh'] - df['Optimized_kWh']
    return df

# --- App Layout ---
st.title("🌱 AI-Based Energy Optimization Prototype")

days = st.slider("Select simulation duration (in days)", 1, 7, 2)
df = simulate_energy(days)
df = optimize(df)

st.subheader("📊 Energy Usage (First 10 Rows)")
st.dataframe(df[['Hour', 'Total_kWh', 'Optimized_kWh', 'Savings']].head(10))

st.subheader("📈 Energy Usage Comparison")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Hour'], df['Total_kWh'], label="Original")
ax.plot(df['Hour'], df['Optimized_kWh'], label="Optimized", linestyle="--")
ax.set_xlabel("Hour")
ax.set_ylabel("Energy (kWh)")
ax.set_title("Before vs After Optimization")
ax.legend()
st.pyplot(fig)

st.subheader("🔍 Summary")
total_orig = df['Total_kWh'].sum()
total_opt = df['Optimized_kWh'].sum()
savings = total_orig - total_opt
percent = (savings / total_orig) * 100

st.success(f"💡 Total Energy Saved: {savings:.2f} kWh ({percent:.2f}%)")
