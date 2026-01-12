import numpy as np

# Malaysian TOU Tariff
# Peak: 8:00 AM - 10:00 PM (0.35 RM) | Off-Peak: 10:00 PM - 8:00 AM (0.20 RM)
TARIFF = [0.20]*8 + [0.35]*14 + [0.20]*2

def calculate_metrics(particle_position, fixed_tasks, shiftable_tasks):
    total_cost = 0
    total_discomfort = 0
    hourly_load = np.zeros(24)
    
    # 1. Process Fixed Appliances
    for task in fixed_tasks:
        start = int(task['Preferred_Start_Hour'])
        duration = int(task['Duration_Hours'])
        power = task['Avg_Power_kW']
        for h in range(start, start + duration):
            hourly_load[h % 24] += power
            total_cost += power * TARIFF[h % 24]

    # 2. Process Shiftable Appliances (Position from PSO)
    for i, task in enumerate(shiftable_tasks):
        # Round the PSO position to the nearest hour
        start = int(round(particle_position[i])) % 24
        duration = int(task['Duration_Hours'])
        power = task['Avg_Power_kW']
        preferred = task['Preferred_Start_Hour']
        
        total_discomfort += abs(start - preferred)
        
        for h in range(start, start + duration):
            hourly_load[h % 24] += power
            total_cost += power * TARIFF[h % 24]

    # 3. Constraint: 5.0 kW Peak Power Limit
    penalty = 0
    peak_load = max(hourly_load)
    if peak_load > 5.0:
        # Penalize heavily if over 5.0 kW to force PSO to find a different time
        penalty = (peak_load - 5.0) * 10000 
    
    # Fitness = Cost + Weighted Discomfort + Penalty
    # We want to minimize this value
    fitness = total_cost + (total_discomfort * 0.1) + penalty
    
    return fitness, total_cost, total_discomfort, hourly_load
