#!/usr/bin/env python3

__author__ = "Eleirold M. Asuncion"
__email__ = "emasuncion1@up.edu.ph"

# ----------------------------------------------------------------

# Package to be able to use RegEx
import re

# Define classes, methods, and variables
# ----------------------------------------------------------------
# Classes
class UserIO:
    def __init__(self, user_input):
        self.user_input = user_input

    def print_fn(self, user_input):
        try:
            array_word = user_input.split(' ', 1)
            print_keyword = array_word[0]
            word_string = array_word[1]
            if len(array_word) > 2 or len(array_word) == 1:
                syntax_incorrect()
            elif not(word_string.startswith('"') and word_string.endswith('"') and is_ascii(word_string)):
                syntax_incorrect()
            elif print_keyword == "PRINT":
                word = self.print_user_input(word_string)
                print(word)
            else:
                word = self.print_user_input(word_string)
                print(f"{word}\n")
        except:
            syntax_incorrect()

    def input_fn(self):
        user_input = input().strip()
        return user_input

    def print_user_input(self, user_input):
        # Removes the first and last character of the string
        return user_input[1:-1].strip()

class Math:
    def arithmetic(self, array):
        try:
            number1 = array[1]
            number2 = array[2]
            if len(array) > 3 or len(array) == 1:
                syntax_incorrect()
            elif number1 and number2: # Make sure number1 and number2 are not null
                if keyword[0] == "ADD":
                    self.add(number1, number2)
                elif keyword[0] == "SUB":
                    self.subtract(number1, number2)
                elif keyword[0] == "MUL":
                    self.multiply(number1, number2)
                elif keyword[0] == "DIV":
                    self.divide(number1, number2)
                elif keyword[0] == "MOD":
                    self.modulo(number1, number2)
            else:
                syntax_incorrect()
        except:
            syntax_incorrect()

    def add(self, x, y):
        print(int(x) + int(y))

    def subtract(self, x, y):
        print(int(x) - int(y))

    def multiply(self, x, y):
        print(int(x) * int(y))

    def divide(self, x, y):
        try:
            if y == "0":
                print("Error: Division by zero.")
            else:
                print(int(x) / int(y))
        except:
            syntax_incorrect()

    def modulo(self, x, y):
        print(int(x) % int(y))
# ----------------------------------------------------------------
# Methods
def greet_user():
    print("INTERPOL Compiler")
    print("Input BEGIN to begin. Input END to end.")

def is_ascii(str):
    return all(ord(c) < 128 for c in str)

def syntax_incorrect():
    print("The syntax is incorrect.")
# ----------------------------------------------------------------
# Variables
print_keywords = ["PRINT", "PRINTLN"]
operator_keywords = ["ADD", "SUB", "MUL", "DIV", "MOD"]
is_first_run = True
is_compiler_started = False
user_input = ""

# Start of the program
greet_user()
user = UserIO("")
math = Math()

while user_input != "END":
    user_input = user.input_fn()
    # This will remove all comments (starting with #) from user input
    # anywhere on the input except if enclosed on double quotes
    stripped_input = re.sub(r'\#(?=([^\"]*\"[^\"]*\")*[^\"]*$).+', '',  user_input).strip()

    if stripped_input == "END":
        print("Ending program.")
    elif is_first_run and stripped_input == "BEGIN":
        print("Starting program.")
        is_first_run = False
        is_compiler_started = True
    elif stripped_input == "BEGIN":
        # Do nothing if BEGIN is entered again
        pass
    elif is_compiler_started:
        keyword = " ".join(stripped_input.split())
        keyword = keyword.split(' ')
        if keyword[0] in print_keywords:
            stripped_input = " ".join(stripped_input.split())
            user.print_fn(stripped_input)
        elif keyword[0] in operator_keywords:
            math.arithmetic(keyword)
        elif user_input and user_input[0] == "#":
            pass
        else:
            syntax_incorrect()
    else:
        greet_user()
