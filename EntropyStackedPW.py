# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 23:00:26 2025
Stacked Bar Chart 
@author: ricke
"""

import math
import matplotlib.pyplot as plt

# Known weak passwords (expandable)
dictionary_weak_passwords = {
    "123456", "password", "12345678", "qwerty", "abc123",
    "password1", "123456789", "12345", "letmein", "admin",
    "welcome", "monkey", "dragon", "football", "iloveyou"
}

# Strength cats and levels
strength_levels = {
    "Very Weak": 1,
    "Weak": 2,
    "Reasonable": 3,
    "Strong": 4,
    "Very Strong": 5
}

def get_color_by_strength(strength):
    return {
        "Very Weak": "red",
        "Weak": "lightcoral",
        "Reasonable": "blue",
        "Strong": "lightgreen",
        "Very Strong": "green"
    }.get(strength, "gray")

def get_strength_label(crack_time_hours, password):
    if password.lower() in dictionary_weak_passwords:
        return "Instant"
    if crack_time_hours < 1:
        return "Very Weak"
    elif crack_time_hours < 8760:
        return "Weak"
    elif crack_time_hours < 52596:
        return "Reasonable"
    elif crack_time_hours < 2000000:
        return "Strong"
    else:
        return "Very Strong"

def calculate_crack_time_hours(entropy):
    return (2 ** entropy) / 10_000_000_000 / 3600 if entropy > 0 else 0

def calculate_entropy(password):
    R = get_charset_size(password)
    L = len(password)
    return math.log2(R ** L) if R > 0 and L > 0 else 0

def get_charset_size(password):
    charsets = {'lower': False, 'upper': False, 'digits': False, 'symbols': False}
    for char in password:
        if char.islower(): charsets['lower'] = True
        elif char.isupper(): charsets['upper'] = True
        elif char.isdigit(): charsets['digits'] = True
        else: charsets['symbols'] = True
    size = 0
    if charsets['lower']: size += 26
    if charsets['upper']: size += 26
    if charsets['digits']: size += 10
    if charsets['symbols']: size += 33
    return size

def main():
    test_labels = []
    lower_strengths = []
    upper_strengths = []
    lower_colors = []
    upper_colors = []
    lower_passwords = []
    upper_passwords = []

    print("Enter 5 password pairs (Password 1, then Password 2):")
    for i in range(5):
        print(f"\n--- Test Pair {i + 1} ")
        pwd1 = input("Original Password: ").strip()
        pwd2 = input("Modified Password: ").strip()

        # Analyze Password 1
        entropy1 = calculate_entropy(pwd1)
        crack1 = calculate_crack_time_hours(entropy1)
        label1 = get_strength_label(crack1, pwd1)
        level1 = strength_levels[label1]
        color1 = get_color_by_strength(label1)

        # Analyze Password 2
        entropy2 = calculate_entropy(pwd2)
        crack2 = calculate_crack_time_hours(entropy2)
        label2 = get_strength_label(crack2, pwd2)
        level2 = strength_levels[label2]
        color2 = get_color_by_strength(label2)

        # Decide stacking order: stronger password on bottom
        if level1 >= level2:
            lower_strengths.append(level1)
            upper_strengths.append(level2)
            lower_colors.append(color1)
            upper_colors.append(color2)
            lower_passwords.append(f"{pwd1} ({label1})")
            upper_passwords.append(f"{pwd2} ({label2})")
        else:
            lower_strengths.append(level2)
            upper_strengths.append(level1)
            lower_colors.append(color2)
            upper_colors.append(color1)
            lower_passwords.append(f"{pwd2} ({label2})")
            upper_passwords.append(f"{pwd1} ({label1})")

        test_labels.append(f"Password Group {i + 1}")

    # Plotting
    plt.figure(figsize=(12, 6))

    #Stronger segment (low)
    bars_lower = plt.bar(test_labels, lower_strengths, color=lower_colors, label="Stronger Password")

    # Higher segment (high)
    bars_upper = plt.bar(test_labels, upper_strengths, bottom=lower_strengths, color=upper_colors, label="Weaker Password")

    # Remove Y-axis since we do not nee dit (graphically didn't look good)
    plt.gca().axes.get_yaxis().set_visible(False)

    # Clean up rest of chart
    plt.title("Password Strength Comparison (Stacked by Strength Category)")
    plt.legend()

    # Add password + strength text inside bars
    for i in range(5):
        plt.text(i, lower_strengths[i] / 2,
                 lower_passwords[i], ha='center', va='center', fontsize=8, color='black', rotation=90)
        if upper_strengths[i] > 0:
            plt.text(i, lower_strengths[i] + upper_strengths[i] / 2,
                     upper_passwords[i], ha='center', va='center', fontsize=8, color='white', rotation=90)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()