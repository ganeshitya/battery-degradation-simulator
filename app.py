import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lithium Battery Life Simulator", layout="centered")

st.title("🔋 Lithium Battery Degradation Simulator")
st.write("Simulate how usable capacity of an LFP lithium-ion battery fades over cycles based on Depth of Discharge and End of Life assumptions.")

# User inputs
capacity_kWh = st.number_input("Battery Pack Capacity (kWh)", min_value=0.1, value=5.0, step=0.1)
dod_percent = st.slider("Depth of Discharge (%)", min_value=10, max_value=100, value=80)
eol_percent = st.slider("End of Life Threshold (%)", min_value=60, max_value=100, value=80)
cycles_input = st.slider("Max Cycle Count", min_value=1000, max_value=10000, step=500, value=6000)

def simulate_degradation(capacity_kWh, dod_percent, eol_percent, total_cycles):
    dod = dod_percent / 100
    eol = eol_percent / 100
    initial_soh = 1.05 # Initial State of Health (SOH) is 105%

    cycles = np.arange(0, total_cycles + 1)
    # Degradation model: SOH decreases from initial_soh to eol over total_cycles
    soh = initial_soh - (initial_soh - eol) * (cycles / total_cycles) ** 1.3
    usable_capacity = soh * capacity_kWh * dod
    return cycles, usable_capacity, soh

# Run the simulation
cycles, usable_cap, soh = simulate_degradation(capacity_kWh, dod_percent, eol_percent, cycles_input)

# ---
# Output Section
# ---
st.markdown("---") # Horizontal rule for separation
st.subheader("Output") # Using subheader for a clear heading

# Calculate and display usable capacity at start and end of life
# Usable capacity at start is the first value in the usable_cap array
initial_usable_capacity = usable_cap[0]
# Usable capacity at end of life is the last value in the usable_cap array
end_of_life_capacity = usable_cap[-1] 

st.write(f"**Usable Capacity at Start:** {initial_usable_capacity:.2f} kWh (based on {dod_percent}% DOD and 105% initial SOH)")
st.write(f"**End of Life Capacity:** {end_of_life_capacity:.2f} kWh (based on {eol_percent}% EOL threshold)")

# ---
# Capacity Degradation Graph Section
# ---
st.markdown("---") # Horizontal rule for separation
st.subheader("Capacity Degradation Graph") # Using subheader for a clear heading

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:green'
ax1.set_xlabel("Cycle Count")
ax1.set_ylabel("Usable Capacity (kWh)", color=color)
ax1.plot(cycles, usable_cap, label="Usable Capacity", color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.7)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel("State of Health (%)", color=color)
ax2.plot(cycles, soh * 100, '--', label="State of Health", color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Add title and legend
plt.title("Battery Usable Capacity and State of Health Over Cycles")
# Positioning the legend outside the plot to avoid overlap
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)


fig.tight_layout() # Adjust layout to prevent labels from overlapping
st.pyplot(fig)

st.caption("This simulation assumes a typical LFP cell degradation curve with slight overcapacity at start-of-life.")
