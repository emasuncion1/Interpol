#!/usr/bin/env python3

__author__ = "Eleirold M. Asuncion"
__email__ = "emasuncion1@up.edu.ph"

# ----------------------------------------------------------------

# Package to be able to use RegEx
import re
import os
import sys
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
            sys.exit(1)
        except:
            print("Invalid file")
            sys.exit(1)

    def file_read(self, filename):
        with open(filename) as file:
            lines = file.readlines()

        for n, line in enumerate(lines, 1):
            line = re.sub(r'\#(?=([^\[\]]*\[[^\[\]]*\[)*[^\[\]]*$).+', '',  line).strip()
            commands.append(line)
            commands_copy.append(line)

        if not(commands[0] == "BEGIN"):
            syntax_incorrect()
        elif not(commands[-1] == "END"):
            print("Invalid end of file")

    def io_operations(self, command):
        keyword = command[0]

        try:
            if keyword == "INPUT":
                if (user_variables.get(command[1]) is int):
                    user_variables[command[1]] = int(self.input_fn())
                else:
                    user_variables[command[1]] = self.input_fn()
        except Exception:
            print(f"Invalid syntax")
            sys.exit(1)

        for index, item in enumerate(command):
            if item in user_variables:
                command[index] = str(user_variables.get(item))

        if keyword == "PRINT" or keyword == "PRINTLN":
            if command[1].startswith("[") and command[1].endswith("]"):
                print(self.print_user_input(command[1]))
            elif command[1] in operator_keywords:
                value_to_print = math.arithmetic(command[1:])
                print(str(value_to_print))
            elif (command[1] in reserved_keys) and (command[1] not in operator_keywords):
                raise Exception
            else:
                print(command[1])

    def input_fn(self):
        global is_first_run
        if is_first_run:
            user_input = input("Enter INTERPOL file (.ipol): ").strip()
            is_first_run = False
        else:
            user_input = input().strip()
            if not is_ascii(user_input):
                raise Exception
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
            print(f"Invalid arithmetic operation at line number [ {index + 2} ]")
            array = " ".join(str(e) for e in array)
            print(f"----> {array}")
            sys.exit(1)

    def add(self, x, y):
        return int(x) + int(y)

    def subtract(self, x, y):
        return int(x) - int(y)

    def multiply(self, x, y):
        return int(x) * int(y)

    def divide(self, x, y):
        try:
            if y == "0":
                pass
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
            if array[1] in user_variables:
                print(f"Duplicate variable declaration at line number [ {index + 2} ]")
                array = " ".join(str(e) for e in array)
                print(f"----> {array}")
                sys.exit(1)

            if array[0] == "VARSTR":
                if not is_ascii(array[1]):
                    print(f"Invalid syntax at line number [ {index + 2} ]")
                    array = " ".join(str(e) for e in array)
                    print(f"----> {array}")
                    sys.exit(1)

                if len(array) == 2:
                    user_variables[array[1]] = ""
                elif len(array) > 2:
                    if not array[3].startswith("["):
                        print(f"Invalid data type at line number [ {index + 2} ]")
                        array = " ".join(str(e) for e in array)
                        print(f"----> {str(array)}")
                        sys.exit(1)
                    elif is_ascii(array[3]):
                        user_variables[array[1]] = array[3]
                    else:
                        raise Exception
                elif (not (array[2] == "WITH")) and (len(array) > 2):
                    raise Exception
            elif array[0] == "VARINT":
                if len(array) == 2:
                    user_variables[array[1]] = 0
                elif len(array) > 2 and array[3].startswith("["):
                    raise Exception
                elif (not (array[2] == "WITH")) and (len(array) > 2):
                    raise Exception
                elif (len(array) > 2) and (array[3] in operator_keywords):
                    user_variables[array[1]] = math.arithmetic(array[3:])
                elif len(array) > 2:
                    if re.search(r'(?:\.\d+)', array[3]): # Check if there is a floating point number
                        print(f"Invalid data type at line number [ {index + 2} ]")
                        array = " ".join(str(e) for e in array)
                        print(f"----> {array}")
                        sys.exit(1)
                else:
                    user_variables[array[1]] = array[3]
        except Exception:
            print(f"Incompatible data type at line number [ {index + 2} ]")
            array = " ".join(str(e) for e in array)
            print(f"----> {array}")
            sys.exit(1)

class Assignment:
    def assign_operations(self, array, index):
        try:
            if array[1] in operator_keywords:
                value = array[1:]
                in_index = value.index("IN")
                user_variables[array[in_index + 2]] = math.arithmetic(array[1:in_index + 1])
            elif array[3] not in user_variables:
                print(f"Variable is not declared at line number [ {index + 2} ]")
                array = " ".join(str(e) for e in array)
                print(f"----> {array}")
                sys.exit(1)
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
            print(f"Invalid data type at line number [ {index + 2} ]")
            sys.exit(1)

        try:
            if array[1] in user_variables:
                array[1] = str(user_variables.get(array[1]))
        except Exception:
            print(f"Variable is not declared at line number [ {index + 2} ]")
            array = " ".join(str(e) for e in array)
            print(f"----> {array}")
            sys.exit(1)

# ----------------------------------------------------------------
# Methods
def greet_user():
    print("=======   INTERPOL INTERPRETER STARTED   =======")

def is_ascii(str):
    return all(ord(c) < 128 for c in str)

def syntax_incorrect():
    print("Invalid syntax")

def tokens_table(commands):
    print("\n========= INTERPOL LEXEMES/TOKENS TABLE =========")
    print ("{:<12} {:<30} {:<40}".format('LINE NO.','TOKENS','LEXEMES'))

    for index, command in enumerate(commands):
        # print(command, index)
        for i, cmd in enumerate(command):
            # print(command)
            token_val = reserved_keys.get(cmd, "")
            if cmd.startswith("["):
                cmd = cmd[1:-1]
                token_val = "STRING"
            elif re.search(r'-?\d+', cmd):
                token_val = "NUMBER"
            elif cmd in special_keys:
                token_val = special_keys.get(cmd)
            elif token_val == "":
                token_val = "IDENTIFIER"
            print("{:<12} {:<30} {:<40}".format(index + 1, token_val, cmd))

        if command[0] == "END":
            print("{:<12} {:<30} {:<40}".format(index + 1, "END_OF_FILE", "EOF"))
        else:
            print("{:<12} {:<30} {:<40}".format(index + 1, "END_OF_STATEMENT", "EOS"))

def symbols_table(variables):
    print("\n================= SYMBOLS TABLE =================")
    print ("{:<15} {:<20} {:<20}".format('VARIABLE NAME','TYPE','VALUE'))

    for var in variables:
        try:
            if re.search(r'-?\d+', variables[var]):
                variables[var] = int(variables[var])
        except Exception:
            pass

        if type(variables[var]) is str:
            print("{:<15} {:<20} {:<20}".format(var, "STRING", variables[var][1:-1]))
        else:
            print("{:<15} {:<20} {:<20}".format(var, "INTEGER", variables[var]))

# ----------------------------------------------------------------
# Variable Dictionaries
# Variable Declarations
var_declaration_keywords = {
    "VARSTR": "DECLARATION_STRING",
    "VARINT": "DECLARATION_INT",
    "WITH": "DECLARATION_ASSIGN_WITH_KEY"
}
# Assignment
assignment_keyword = {
    "STORE": "ASSIGN_KEY",
    "IN": "ASSIGN_VAR_KEY"
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

program_keywords = {
    "BEGIN": "PROGRAM_BEGIN",
    "END": "PROGRAM_END"
}

special_keys = {
    "AND": "DISTANCE_SEPARATOR"
}

is_first_run = True
is_compiler_started = False
user_input = ""
commands = []
commands_copy = []
token_commands = []
user_variables =  {}
reserved_keys = {**program_keywords, **var_declaration_keywords, **assignment_keyword, **io_keywords, **operator_keywords}

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

# Clean the command list
commands = [x for x in commands if x]

for index, command in enumerate(commands):
    keyword = re.split('\\s+(?![^\\[]*\\])', command)

    try:
        if ((keyword[1] in reserved_keys)
            and not (keyword[0] in io_keywords)
            and not (keyword[0] in assignment_keyword)):
            raise Exception
        else:
            if keyword[0] in var_declaration_keywords: # VARSTR and VARINT keyword
                variable.var_declaration(keyword)
            elif keyword[0] in assignment_keyword: # STORE keyword
                assignment.assign_operations(keyword, index)
            elif keyword[0] in io_keywords: # INPUT/PRINT/PRINTLN keywords
                user.io_operations(keyword)
            elif keyword[0].startswith("\#"):
                pass
            elif keyword[0] in program_keywords:
                pass
            else:
                print(f"Invalid syntax at line number [ {index + 2} ]")
                keyword = " ".join(str(e) for e in keyword)
                print(f"----> {str(keyword)}")
                sys.exit(1)
    except Exception:
        print(f"Invalid expression at line number [ {index + 2} ]")
        keyword = " ".join(str(e) for e in keyword)
        print(f"----> {str(keyword)}")
        sys.exit(1)

print("<------   OUTPUT END   ----------\n")

# Output the lexemes/tokens table
for command in commands_copy:
    keyword = re.split('\\s+(?![^\\[]*\\])', command)
    token_commands.append(keyword)

tokens_table(token_commands)

# Output symbols table
symbols_table(user_variables)

print("\n========  INTERPOL INTERPRETER TERMINATED  ========")
