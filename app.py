import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Lithium Battery Life Simulator", layout="centered")

# Title
st.title("🔋 Lithium Battery Degradation Simulator")
st.write("Simulate how usable capacity of an LFP lithium-ion battery fades over cycles based on Depth of Discharge and End of Life assumptions.")

# Inputs
capacity_kWh = st.number_input("Battery Pack Capacity (kWh)", min_value=0.1, value=5.0, step=0.1)
dod_percent = st.slider("Depth of Discharge (%)", min_value=10, max_value=100, value=80)
eol_percent = st.slider("End of Life Threshold (%)", min_value=60, max_value=100, value=80)
cycles_input = st.slider("Max Cycle Count", min_value=1000, max_value=10000, step=500, value=6000)

# Simulation function
def simulate_degradation(capacity_kWh, dod_percent, eol_percent, total_cycles):
    dod = dod_percent / 100
    eol = eol_percent / 100
    initial_soh = 1.05
    cycles = np.arange(0, total_cycles + 1)
    soh = initial_soh - (initial_soh - eol) * (cycles / total_cycles) ** 1.3
    usable_capacity = soh * capacity_kWh * dod
    return cycles, usable_capacity, soh

# Run simulation
cycles, usable_cap, soh = simulate_degradation(capacity_kWh, dod_percent, eol_percent, cycles_input)

initial_usable_capacity = usable_cap[0]
end_of_life_capacity = usable_cap[-1]

# ---
# Card-style Output Section
# ---
st.markdown("---")
st.subheader("📊 Simulation Summary")

# Custom CSS for cards
st.markdown("""
<style>
.card-container {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    gap: 20px;
}
.card {
    flex: 1;
    background-color: #f1f3f6;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    text-align: center;
}
.card h3 {
    font-size: 1.2rem;
    color: #444;
}
.card .icon {
    font-size: 2rem;
}
.card .value {
    font-size: 1.8rem;
    font-weight: bold;
    margin: 10px 0;
    color: #0a58ca;
}
.card .subtitle {
    font-size: 0.9rem;
    color: #777;
}
</style>
""", unsafe_allow_html=True)

# Output as cards
st.markdown(f"""
<div class="card-container">
    <div class="card">
        <div class="icon">🔋</div>
        <h3>Usable Capacity at Start</h3>
        <div class="value">{initial_usable_capacity:.2f} kWh</div>
        <div class="subtitle">Based on 105% SOH</div>
    </div>
    <div class="card">
        <div class="icon">⚠️</div>
        <h3>End of Life Capacity</h3>
        <div class="value">{end_of_life_capacity:.2f} kWh</div>
        <div class="subtitle">Threshold: {eol_percent}% EOL</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---
# Plotting Section
# ---
st.markdown("---")
st.subheader("📉 Capacity Degradation Graph")

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

fig.tight_layout()
st.pyplot(fig, clear_figure=True)

st.caption("This simulation assumes a typical LFP cell degradation curve with slight overcapacity at start-of-life.")
