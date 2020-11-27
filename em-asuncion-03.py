#!/usr/bin/env python3

__author__ = "Eleirold M. Asuncion"
__email__ = "emasuncion1@up.edu.ph"

# ----------------------------------------------------------------

# Package to be able to use RegEx
import re
import os

# Define classes, methods, and variables
# ----------------------------------------------------------------
# Classes
class UserIO:
    def __init__(self, user_input):
        self.user_input = user_input

    # This function will handle the file input operation only
    def file_input(self):
        filename = self.input_fn()

        try:
            # Check if filename does not end with .ipol (e.g. text.ipol)
            if not(filename[-5:] == ".ipol"):
                print("Invalid file")
            elif os.stat(filename).st_size == 0:
                print("File is empty")
            else:
                # This is a valid .ipol file
                # Check file
                self.file_read(filename)
                # Remove BEGIN and END
                commands.pop(0)
                commands.pop(-1)
                return
        except FileNotFoundError:
            print("File not found")
        except:
            print("Invalid file")

    def file_read(self, filename):
        with open(filename) as file:
            lines = file.readlines()

        for n, line in enumerate(lines, 1):
            commands.append(line.rstrip())

        if not(commands[0] == "BEGIN"):
            syntax_incorrect()
        elif not(commands[-1] == "END"):
            print("Invalid end of file")

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
        global is_first_run
        if is_first_run:
            user_input = input("Enter INTERPOL file (.ipol): ").strip()
            is_first_run = False
        else:
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
                if array[0] == "MUL":
                    return self.multiply(number1, number2)
                elif array[0] == "DIV":
                    return self.divide(number1, number2)
                elif array[0] == "MOD":
                    return self.modulo(number1, number2)
                elif array[0] == "ADD":
                    return self.add(number1, number2)
                elif array[0] == "SUB":
                    return self.subtract(number1, number2)
            else:
                syntax_incorrect()
        except:
            syntax_incorrect()

    def add(self, x, y):
        return int(x) + int(y)

    def subtract(self, x, y):
        return int(x) - int(y)

    def multiply(self, x, y):
        return int(x) * int(y)

    def divide(self, x, y):
        try:
            if y == "0":
                print("Error: Division by zero.")
            else:
                return int(x) / int(y)
        except:
            syntax_incorrect()

    def modulo(self, x, y):
        return int(x) % int(y)

class Declaration:
    def var_declaration(self, array):
        if array[0] == "VARSTR":
            if len(array) > 2:
                user_variables[array[1]] = array[3]
            else:
                user_variables[array[1]] = ""
        elif array[0] == "VARINT":
            if len(array) == 2:
                user_variables[array[1]] = 0
            elif (len(array) > 2) and (array[3] in operator_keywords):
                math_array = [array[3], array[4], array[5]]
                user_variables[array[1]] = math.arithmetic(math_array)
            else:
                user_variables[array[1]] = 0

# ----------------------------------------------------------------
# Methods
def greet_user():
    print("=======   INTERPOL INTERPRETER STARTED   =======")

def is_ascii(str):
    return all(ord(c) < 128 for c in str)

def syntax_incorrect():
    print("The syntax is incorrect.")
# ----------------------------------------------------------------
# Variable Dictionaries
# Variable Declarations
var_declaration_keywords = {
    "VARSTR": "DECLARATION_STRING",
    "VARINT": "DECLARATION_INT"
}
# Assignment
assignment_keywords = {
    "STORE": "ASSIGN_KEY"
}
# User IO
io_keywords = {
    "INPUT": "INPUT",
    "PRINT": "PRINT",
    "PRINTLN": "OUTPUT_WITH_LINE"
}
# Operations
operator_keywords = {
    "ADD": "BASIC_OPERATOR_ADD",
    "SUB": "BASIC_OPERATOR_SUB",
    "MUL": "BASIC_OPERATOR_MUL",
    "DIV": "BASIC_OPERATOR_DIV",
    "MOD": "BASIC_OPERATOR_MOD",
    "RAISE": "ADVANCED_OPERATOR_RAISE",
    "ROOT": "ADVANCED_OPERATOR_ROOT",
    "MEAN": "ADVANCED_OPERATOR_MEAN",
    "DIST": "ADVANCED_OPERATOR_DIST"
}
is_first_run = True
is_compiler_started = False
user_input = ""
commands = []
user_variables =  {}

# Start of the program
greet_user()
user = UserIO("")
math = Math()
variable = Declaration()

# Accept the IPOL file
# ipol_file = user.file_input()
user.file_input()

print("\n=======   INTERPOL OUTPUT   =======")
print("\n-------   OUTPUT START   --------->")

for command in commands:
    keyword = re.split('\\s+(?![^\\[]*\\])', command)
    # print(keyword)
    if keyword[0] in var_declaration_keywords:
        variable.var_declaration(keyword)

print(user_variables)

print("<------   OUTPUT END   ----------\n")

# This will remove all comments (starting with #) from user input
# anywhere on the input except if enclosed on double quotes
# stripped_input = re.sub(r'\#(?=([^\"]*\"[^\"]*\")*[^\"]*$).+', '',  user_input).strip()

# if stripped_input == "END":
#     print("Ending program.")
# elif is_first_run and stripped_input == "BEGIN":
#     print("Starting program.")
#     is_first_run = False
#     is_compiler_started = True
# elif stripped_input == "BEGIN":
#     # Do nothing if BEGIN is entered again
#     pass
# elif is_compiler_started:
#     keyword = " ".join(stripped_input.split())
#     keyword = keyword.split(' ')
#     if keyword[0] in io_keywords:
#         stripped_input = " ".join(stripped_input.split())
#         user.print_fn(stripped_input)
#     elif keyword[0] in operator_keywords:
#         math.arithmetic(keyword)
#     elif user_input and user_input[0] == "#":
#         pass
#     else:
#         syntax_incorrect()
# else:
#     greet_user()
