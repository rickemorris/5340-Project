# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 03:31:21 2025
Python conversion of script - https://github.com/ali-alwan99/Quantum-Password-Cracking/tree/main
@author: ricke
"""

import math
import time

def print_time(seconds):
    if seconds < 1:
        print("Instantly")
    elif seconds > 31536000:
        years = seconds / 31536000
        if years > 1_000_000_000:
            print(f"{round(years / 1_000_000_000)} billion years")
        elif years > 1_000_000:
            print(f"{round(years / 1_000_000)} million years")
        elif years > 1_000:
            print(f"{round(years / 1_000)} thousand years")
        else:
            print(f"{round(years)} years")
    elif seconds > 86400:
        print(f"{round(seconds / 86400)} days")
    elif seconds > 3600:
        print(f"{round(seconds / 3600)} hours")
    elif seconds > 60:
        print(f"{round(seconds / 60)} minutes")
    else:
        print(f"{round(seconds)} seconds")

def check_word(search, dictionary_path="E:/PythonClass/rockyou.txt"):
    try:
        with open(dictionary_path, "r", encoding="latin1") as file:
            for line in file:
                if search == line.strip():
                    return True
    except FileNotFoundError:
        print(f"Dictionary file '{dictionary_path}' not found.")
    return False

def print_strength(password):
    n = len(password)
    pool_size = 0
    normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c not in normal_chars for c in password)

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32

    speed = 10_000_000_000  # 10 billion attempts/sec

    total_combinations = math.pow(pool_size, n)
    quantum_combinations = math.sqrt(total_combinations)

    entropy = math.floor(math.log2(total_combinations)) + 1
    quantum_entropy = math.floor(math.log2(quantum_combinations)) + 1

    seconds = total_combinations / speed
    qseconds = quantum_combinations / speed

    if check_word(password):
        seconds = qseconds = 0

    print("A Classical Computer will break this password in:")
    print_time(seconds)
    print(f"Password Entropy: {entropy} bits\n")

    print("A Quantum Computer will break this password in:")
    print_time(qseconds)
    print(f"Quantum Entropy: {quantum_entropy} bits")

def main():
    print("Welcome to The Post-Quantum Password Cracker!")
    while True:
        password = input("Please enter a password (or type '1' to exit): ").strip()
        if password == "1":
            break
        print()
        print_strength(password)
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()