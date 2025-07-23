# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 23:10:06 2025
Heatmap on passwords
@author: ricke
"""

import math
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# PW Strength categories
strength_levels = ["Very Strong", "Strong", "Reasonable", "Weak", "Very Weak"]

# Color Code Stength
strength_to_color = {
    "Very Weak": "#ff4d4d",       # Red
    "Weak": "#ff9999",            # Light Red
    "Reasonable": "#66b3ff",      # Blue
    "Strong": "#b3ffb3",          # Light Green
    "Very Strong": "#33cc33"      # Green
}

# Crack time categorization
def classify_strength(hours):
    if hours < 1:
        return "Very Weak"
    elif hours < 8760:
        return "Weak"
    elif hours < 52596:
        return "Reasonable"
    elif hours < 2_000_000:
        return "Strong"
    else:
        return "Very Strong"

# Quantum crack time in hours
def quantum_crack_time(password):
    n = len(password)
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26
    if any(c.isupper() for c in password): pool_size += 26
    if any(c.isdigit() for c in password): pool_size += 10
    if any(not c.isalnum() for c in password): pool_size += 32

    if pool_size == 0:
        return 0  # if empty or only spaces

    total_combinations = pow(pool_size, n)
    quantum_combinations = math.sqrt(total_combinations)
    speed = 10_000_000_000  # 10 billion guesses/sec
    q_seconds = quantum_combinations / speed
    return q_seconds / 3600  # convert to hours

# ==== User Input ====
passwords = []
print("Enter 5 passwords to evaluate:")
for i in range(5):
    pw = input(f"Password {i+1}: ").strip()
    passwords.append(pw)

labels = passwords

# Prepare DataFrames
heatmap_values = pd.DataFrame("", index=strength_levels, columns=labels)
colors = pd.DataFrame("", index=strength_levels, columns=labels)

# Present data
for i, pw in enumerate(passwords):
    hours = quantum_crack_time(pw)
    strength = classify_strength(hours)

    # Formatting
    if hours >= 1_000_000:
        time_str = f"{hours/1_000_000:.1f}M h"
    elif hours >= 10_000:
        time_str = f"{hours/1000:.1f}K h"
    else:
        time_str = f"{hours:.1f} h"

    # Set values in the row corresponding to the strength
    heatmap_values.loc[strength, labels[i]] = time_str
    colors.loc[strength, labels[i]] = strength_to_color[strength]

# Heat Map for Data
plt.figure(figsize=(10, 6))
ax = sns.heatmap(
    heatmap_values.isin([""]) == False,
    annot=heatmap_values.values,
    fmt="",
    cbar=False,
    linewidths=0.5,
    linecolor='gray',
    cmap=["white"],
)

# Heatmap cell color
for y in range(heatmap_values.shape[0]):
    for x in range(heatmap_values.shape[1]):
        if heatmap_values.iloc[y, x] != "":
            color = colors.iloc[y, x]
            ax.add_patch(
                plt.Rectangle((x, y), 1, 1, fill=True, color=color, ec='gray', lw=0.5)
            )

# Final Heatmap Organization
plt.title("Quantum Crack Time by Password", fontsize=14)
plt.xlabel("Passwords Category")
plt.ylabel("Strength Category")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()