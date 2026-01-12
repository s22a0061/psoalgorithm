import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data_loader import load_data
from src.pso_engine import PSOOptimizer
from src.metrics import calculate_metrics

st.set_page_config(page_title="Smart Home Energy Optimizer", layout="wide")

st.title("⚡ Smart Home Energy Optimization using PSO")
st.write("Optimizing appliance schedules to minimize cost and respect the 5.0 kW limit.")

# Sidebar for PSO Parameters
st.sidebar.header("PSO Settings")
swarm_size = st.sidebar.slider("Swarm Size", 10, 100, 30)
iters = st.sidebar.slider("Iterations", 10, 200, 50)
w = st.sidebar.slider("Inertia (w)", 0.1, 1.0, 0.5)

# Load Data
fixed, shiftable = load_data("data/project_benchmark_data.csv")

if st.button("Run Optimization"):
    optimizer = PSOOptimizer(fixed, shiftable, swarm_size=swarm_size, w=w)
    best_start_times, history = optimizer.optimize(iterations=iters)
    
    # Calculate final results
    fit, cost, discomfort, load = calculate_metrics(best_start_times, fixed, shiftable)
    
    # UI Layout: Results
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"RM {cost:.2f}")
    col2.metric("Discomfort", f"{discomfort:.2f} Hours")
    col3.metric("Peak Load", f"{max(load):.2f} kW")

    # Plotting Load Profile
    st.subheader("24-Hour Power Usage Profile")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(24), load, color='skyblue', label='Total Load')
    ax.axhline(y=5.0, color='r', linestyle='--', label='5.0 kW Limit')
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Power (kW)")
    ax.legend()
    st.pyplot(fig)

    # Plotting Convergence
    st.subheader("PSO Convergence (Fitness over Iterations)")
    st.line_chart(history)
    
    st.subheader("Performance Summary")

    # 1. Calculate Baseline (using Preferred_Start_Hour from CSV)
    baseline_positions = [task['Preferred_Start_Hour'] for task in shiftable]
    _, base_cost, base_discomfort, _ = calculate_metrics(baseline_positions, fixed, shiftable)
    
    # 2. Compare with Optimized
    savings = base_cost - cost
    improvement = (savings / base_cost) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Money Saved", f"RM {savings:.2f}")
    col2.metric("Efficiency Gain", f"{improvement:.1f}%")
    
