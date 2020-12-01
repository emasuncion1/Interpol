#!/usr/bin/env python3

__author__ = "Eleirold M. Asuncion"
__email__ = "emasuncion1@up.edu.ph"

# ----------------------------------------------------------------

# Package to be able to use RegEx
import re
import os
import math as m

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

    def io_operations(self, command):
        # command = convert_exp_to_value(command)
        keyword = command[0]

        for index, item in enumerate(command):
            if item in user_variables:
                command[index] = str(user_variables.get(item))

        if keyword == "PRINT":
            if command[1].startswith("[") and command[1].endswith("]"):
                print(self.print_user_input(command[1]))
            else:
                print(command[1])
        elif keyword == "PRINTLN":
            if command[1].startswith("[") and command[1].endswith("]"):
                print(self.print_user_input(command[1]) + "\n")
            else:
                print(command[1] + "\n")

    # def print_fn(self, user_input):
    #     try:
    #         array_word = user_input.split(' ', 1)
    #         print_keyword = array_word[0]
    #         word_string = array_word[1]
    #         if len(array_word) > 2 or len(array_word) == 1:
    #             syntax_incorrect()
    #         elif not(word_string.startswith('"') and word_string.endswith('"') and is_ascii(word_string)):
    #             syntax_incorrect()
    #         elif print_keyword == "PRINT":
    #             word = self.print_user_input(word_string)
    #             print(word)
    #         else:
    #             word = self.print_user_input(word_string)
    #             print(f"{word}\n")
    #     except:
    #         syntax_incorrect()

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
        counter_array = []
        number1 = 0
        number2 = 0
        number = 0

        # Get the index positions of adjacent keywords and store in a list
        for index, keyword in enumerate(array):
            if keyword in operator_keywords:
                counter_array.append(index)

        counter_array = list(dict.fromkeys(counter_array))

        try:
            # Substitute the variables to its equivalent value
            # if it is used as an expression
            for index, var in enumerate(array):
                if var in user_variables:
                    array[index] = str(user_variables.get(var))

            for index_of_keyword in reversed(counter_array):
                number1 = array[index_of_keyword + 1]
                number2 = array[index_of_keyword + 2]
                numbers_arr = array[index_of_keyword + 1:]

                if number1 in user_variables:
                    number1 = user_variables.get(number1)
                elif number2 in user_variables:
                    number2 = user_variables.get(number2)

                if array[index_of_keyword] == "MUL":
                    array[index_of_keyword] = self.multiply(number1, number2)
                elif array[index_of_keyword] == "DIV":
                    array[index_of_keyword] = self.divide(number1, number2)
                elif array[index_of_keyword] == "MOD":
                    array[index_of_keyword] = self.modulo(number1, number2)
                elif array[index_of_keyword] == "ADD":
                    array[index_of_keyword] = self.add(number1, number2)
                elif array[index_of_keyword] == "SUB":
                    array[index_of_keyword] = self.subtract(number1, number2)
                elif array[index_of_keyword] == "RAISE":
                    array[index_of_keyword] = self.math_raise(number1, number2)
                elif array[index_of_keyword] == "ROOT":
                    array[index_of_keyword] = self.root(number1, number2)
                elif array[index_of_keyword] == "MEAN":
                    array[index_of_keyword] = self.mean(numbers_arr)
                elif array[index_of_keyword] == "DIST":
                    if numbers_arr[2] == "AND":
                        numbers_arr.pop(2)
                    array[index_of_keyword] = self.dist(numbers_arr)

                number = array[index_of_keyword]

                if array[index_of_keyword + 1]:
                    array = self.pop_num_in_list(array, index_of_keyword)

            return int(number)
        except Exception:
            print("Invalid arithmetic operation")

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

    def math_raise(self, x, y):
        return int(x) ** int(y)

    def root(self, x, y):
        return int(y) ** (1 / int(x))

    def mean(self, numbers):
        numbers = [int(n) for n in numbers]
        return sum(numbers) / len(numbers)

    def dist(self, numbers):
        numbers = [int(n) for n in numbers]
        return int(m.sqrt(((numbers[0]-numbers[2])**2)
                      + ((numbers[1]-numbers[3])**2)))

    def pop_num_in_list(self, array, index):
        array_length = len(array)
        if array_length > 2:
            array.pop(index + 1)
            array.pop(index + 1)
        else:
            array.pop(index)

        return array

class Declaration:
    def var_declaration(self, array):
        try:
            if array[0] == "VARSTR":
                if len(array) == 2:
                    user_variables[array[1]] = ""
                elif len(array) > 2:
                    if not array[3].startswith("["):
                        raise Exception
                    user_variables[array[1]] = array[3]
                elif (not (array[2] == "WITH")) and (len(array) > 2):
                    raise Exception
            elif array[0] == "VARINT":
                if len(array) == 2:
                    user_variables[array[1]] = 0
                elif (not (array[2] == "WITH")) and (len(array) > 2):
                    raise Exception
                elif (len(array) > 2) and (array[3] in operator_keywords):
                    user_variables[array[1]] = math.arithmetic(array[3:])
                elif len(array) > 2:
                    if (not type(array[3]) is int):
                        raise Exception
                    user_variables[array[1]] = array[3]
        except Exception:
            print(f"Invalid expression at line number [ {index + 2} ]")

class Assignment:
    def assign_operations(self, array, index):
        try:
            if array[1] in user_variables:
                array[1] = str(user_variables.get(array[1]))
        except Exception:
            print(f"Variable is not declared at line number {index + 2}")

        try:
            if len(array) > 4:
                syntax_incorrect()
            elif array[3] not in user_variables:
                print(f"Variable is not declared at line number {index + 2}")
            elif (re.search(r'-?\d+', array[1]) and
                type(user_variables.get(array[3])) is int):
                if (array[1].startswith("[") or array[1].startswith("\"")
                        or array[1].startswith("\'")):
                    raise Exception
                user_variables[array[3]] = int(array[1])
            elif type(user_variables.get(array[3])) is str:
                if not array[1].startswith("["):
                    raise Exception
                user_variables[array[3]] = array[1]
            else:
                raise Exception
        except Exception:
            print(f"Incompatible data type at line number {index + 2}")

# ----------------------------------------------------------------
# Methods
def greet_user():
    print("=======   INTERPOL INTERPRETER STARTED   =======")

def is_ascii(str):
    return all(ord(c) < 128 for c in str)

def syntax_incorrect():
    print("The syntax is incorrect.")

def convert_exp_to_value(array):
    for index, item in enumerate(array):
        if item in user_variables:
            array[index] = str(user_variables.get(item))

    return array
# ----------------------------------------------------------------
# Variable Dictionaries
# Variable Declarations
var_declaration_keywords = {
    "VARSTR": "DECLARATION_STRING",
    "VARINT": "DECLARATION_INT"
}
# Assignment
assignment_keyword = {
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
reserved_keys = {**var_declaration_keywords, **assignment_keyword, **io_keywords, **operator_keywords}

# Start of the program
greet_user()
user = UserIO("")
math = Math()
variable = Declaration()
assignment = Assignment()

# Accept the IPOL file
# ipol_file = user.file_input()
user.file_input()

print("\n========   INTERPOL OUTPUT   ========")
print("\n-------   OUTPUT START   --------->")

for index, command in enumerate(commands):
    keyword = re.split('\\s+(?![^\\[]*\\])', command)
    try:
        if keyword[1] in reserved_keys:
            raise Exception
        else:
            if keyword[0] in var_declaration_keywords: # VARSTR and VARINT keyword
                variable.var_declaration(keyword)
            elif keyword[0] in assignment_keyword: # STORE keyword
                assignment.assign_operations(keyword, index)
            elif keyword[0] in io_keywords: # INPUT/PRINT/PRINTLN keywords
                user.io_operations(keyword)
    except Exception:
        print(f"Invalid expression at line number [ {index} ]")

# print(f"user_variables: {user_variables}")

print("<------   OUTPUT END   ----------\n")
print("\n========  INTERPOL INTERPRETER TERMINATED  ========")

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
