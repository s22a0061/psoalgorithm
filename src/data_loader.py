import pandas as pd

def load_data(filepath="project_benchmark_data.csv"):
    df = pd.read_csv(filepath)
    # Split into fixed and shiftable for easier processing
    fixed_tasks = df[df['Is_Shiftable'] == False].to_dict('records')
    shiftable_tasks = df[df['Is_Shiftable'] == True].to_dict('records')
    return fixed_tasks, shiftable_tasks

def get_malaysian_tariff():
    # Peak (8 AM - 10 PM): 0.35 RM
    # Off-Peak (10 PM - 8 AM): 0.20 RM
    # Represented as a list of 24 values (one for each hour)
    tariff = [0.20] * 8 + [0.35] * 14 + [0.20] * 2
    return tariff
