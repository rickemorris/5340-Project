# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 22:42:12 2025
Crack Time Calculator based on i7 6700HQ (2015 processor)
@author: ricke
"""

import math
import matplotlib.pyplot as plt

# Determine R (unique characters)
def get_charset_size(password):
    charsets = {
        'lower': False,
        'upper': False,
        'digits': False,
        'symbols': False
    }

    for char in password:
        if char.islower():
            charsets['lower'] = True
        elif char.isupper():
            charsets['upper'] = True
        elif char.isdigit():
            charsets['digits'] = True
        else:
            charsets['symbols'] = True

    size = 0
    if charsets['lower']:
        size += 26
    if charsets['upper']:
        size += 26
    if charsets['digits']:
        size += 10
    if charsets['symbols']:
        size += 33  # Assuming 33 printable symbols

    return size

# Entropy formula E = log2(R^L)
def calculate_entropy(password):
    R = get_charset_size(password)
    L = len(password)
    if R == 0 or L == 0:
        return 0
    entropy = math.log2(R ** L)
    return entropy

# Crack time in hours using:  2^entropy / 6552832 ops/sec / 3600
def calculate_crack_time_hours(entropy):
    if entropy == 0:
        return 0
    crack_time_seconds = (2 ** entropy) / 6552832
    return crack_time_seconds / 3600

# Strength calculated based on how fast it can be cracked (changed from original script)
def get_strength_label(crack_time_hours):
    if crack_time_hours < 1:
        return "Very Weak"
    elif crack_time_hours < 8760:  # < 1 year
        return "Weak"
    elif crack_time_hours < 52596:  # < 6 years
        return "Reasonable"
    elif crack_time_hours < 2000000:  # < ~228 years
        return "Strong"
    else:
        return "Very Strong"

# Color Strength on Barchart
def get_color_by_strength(strength):
    colors = {
        "Very Weak": "red",
        "Weak": "lightcoral",
        "Reasonable": "blue",
        "Strong": "lightgreen",
        "Very Strong": "green"
    }
    return colors.get(strength, "gray")

# User input and barchart details
def main():
    passwords = []
    crack_times_hours = []
    strength_labels = []
    bar_colors = []

    print("Enter 5 passwords:")
    for i in range(5):
        pwd = input(f"Password {i + 1}: ")
        entropy = calculate_entropy(pwd)
        crack_hours = calculate_crack_time_hours(entropy)
        strength = get_strength_label(crack_hours)
        color = get_color_by_strength(strength)
 
        passwords.append(pwd)
        crack_times_hours.append(crack_hours)
        strength_labels.append(strength)
        bar_colors.append(color)

    # Barchart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(passwords, crack_times_hours, color=bar_colors)
    plt.title("Estimated Hours to Crack Password")
    plt.ylabel("Crack Time")
    plt.yscale('log')
    plt.ylim(0.1, max(crack_times_hours) * 2)

    # Labels from Barchart
    for bar, time_hr, label in zip(bars, crack_times_hours, strength_labels):
        yval = bar.get_height()
        text = f"{time_hr:.2f} hrs\n{label}"
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval,
                 text, ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()