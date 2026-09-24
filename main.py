from collections import Counter
from statistics import mean, median, pvariance
import random
import getpass
import psycopg2


data = {
    "Monday": [
        "GREEN", "YELLOW", "GREEN", "BROWN", "BLUE",
        "PINK", "BLUE", "YELLOW", "ORANGE", "CREAM",
        "ORANGE", "RED", "WHITE", "BLUE", "WHITE",
        "BLUE", "BLUE", "BLUE", "GREEN"
    ],

    "Tuesday": [
        "ARSH", "BROWN", "GREEN", "BROWN", "BLUE",
        "BLUE", "BLEW", "PINK", "PINK", "ORANGE",
        "ORANGE", "RED", "WHITE", "BLUE", "WHITE",
        "WHITE", "BLUE", "BLUE", "BLUE"
    ],

    "Wednesday": [
        "GREEN", "YELLOW", "GREEN", "BROWN", "BLUE",
        "PINK", "RED", "YELLOW", "ORANGE", "RED",
        "ORANGE", "RED", "BLUE", "BLUE", "WHITE",
        "BLUE", "BLUE", "WHITE", "WHITE"
    ],

    "Thursday": [
        "BLUE", "BLUE", "GREEN", "WHITE", "BLUE",
        "BROWN", "PINK", "YELLOW", "ORANGE", "CREAM",
        "ORANGE", "RED", "WHITE", "BLUE", "WHITE",
        "BLUE", "BLUE", "BLUE", "GREEN"
    ],

    "Friday": [
        "GREEN", "WHITE", "GREEN", "BROWN", "BLUE",
        "BLUE", "BLACK", "WHITE", "ORANGE", "RED",
        "RED", "RED", "WHITE", "BLUE", "WHITE",
        "BLUE", "BLUE", "BLUE", "WHITE"
    ]
}


colours = []

for day in data:
    for colour in data[day]:
        if colour == "BLEW":
            colour = "BLUE"
        colours.append(colour)


frequency = Counter(colours)

print("COLOUR FREQUENCIES")
print("------------------")

for colour, count in frequency.items():
    print(colour, ":", count)


frequencies = list(frequency.values())

print("\nMEAN")
print("Mean frequency:", mean(frequencies))


most_common = frequency.most_common(1)[0]

print("\nMOST FREQUENT COLOUR")
print("Colour:", most_common[0])
print("Frequency:", most_common[1])


print("\nMEDIAN")
print("Median frequency:", median(frequencies))


print("\nVARIANCE")
print("Variance:", pvariance(frequencies))


red = frequency["RED"]
total = len(colours)

print("\nPROBABILITY OF RED")
print("RED:", red)
print("Total:", total)
print("Probability:", red / total)
print("Percentage:", (red / total) * 100, "%")


print("\nPOSTGRESQL")

try:
    password = getpass.getpass("Enter your PostgreSQL password: ")

    connection = psycopg2.connect(
        host="localhost",
        database="bincom",
        user="postgres",
        password=password,
        port="5432"
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colour_frequencies (
            id SERIAL PRIMARY KEY,
            colour VARCHAR(50) UNIQUE,
            frequency INTEGER
        )
    """)

    for colour, count in frequency.items():
        cursor.execute("""
            INSERT INTO colour_frequencies (colour, frequency)
            VALUES (%s, %s)
            ON CONFLICT (colour)
            DO UPDATE SET frequency = EXCLUDED.frequency
        """, (colour, count))

    connection.commit()

    cursor.close()
    connection.close()

    print("Data saved successfully.")

except Exception as e:
    print("PostgreSQL error:", e)


def search(numbers, target, index=0):

    if index == len(numbers):
        return False

    if numbers[index] == target:
        return True

    return search(numbers, target, index + 1)


numbers = [10, 20, 30, 40, 50]
target = 30

print("\nRECURSIVE SEARCH")

if search(numbers, target):
    print(target, "was found")
else:
    print(target, "was not found")


binary = ""

for i in range(4):
    binary += str(random.randint(0, 1))

decimal = 0

for digit in binary:
    decimal = decimal * 2 + int(digit)

print("\nRANDOM 4-BIT BINARY")
print("Binary:", binary)
print("Decimal:", decimal)


def fibonacci_sum(n):

    a = 0
    b = 1
    total = 0

    for i in range(n):
        total += a
        a, b = b, a + b

    return total


print("\nFIBONACCI")
print("Sum of first 50:", fibonacci_sum(50))


def check_sequence(sequence):

    result = ""

    for i in range(len(sequence)):

        if sequence[i:i + 3] == "111":
            result += "1"
        else:
            result += "0"

    return result


sequence = "0101101011101011011101101000111"

print("\n111 SEQUENCE")
print("Input:", sequence)
print("Output:", check_sequence(sequence))
