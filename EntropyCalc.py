# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 23:57:14 2025
#Password Entropy CBar Chart Security Testing
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
        size += 33  # ASCII Printable Characters 
        
    return size

# Entropy formula E = log2(RL)
def calculate_entropy(password):
    R = get_charset_size(password)
    L = len(password)
    if R == 0 or L == 0:
        return 0
    entropy = math.log2(R ** L)
    return entropy

# Calculating Strength based on bit size
def get_strength_label(entropy):
    if entropy < 28:
        return "Very Weak"
    elif entropy < 46:
        return "Weak"
    elif entropy < 80:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"

# Calculating Entropy based on entry on data input
def main():
    passwords = []
    entropies = []
    labels = []

    print("Enter 5 passwords:")
    for i in range(5):
        pwd = input(f"Password {i + 1}: ")
        passwords.append(pwd)
        entropy = calculate_entropy(pwd)
        entropies.append(entropy)
        labels.append(get_strength_label(entropy))

    #Barchart from data presented
    plt.figure(figsize=(10, 6))
    bars = plt.bar(passwords, entropies, color='skyblue')
    plt.title("Password Entropy (in bits)")
    plt.ylabel("Entropy (bits)")
    plt.ylim(0, max(entropies) + 10)

    # Add entropy and strength label in the barchart
    for bar, entropy, label in zip(bars, entropies, labels):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1,
                 f"{entropy:.2f} bits\n{label}", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()