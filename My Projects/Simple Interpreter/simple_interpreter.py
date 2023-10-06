import os
import re
import sys

filename = "hello.py" #input("Input filename: ")
keywords = ["print", "input", "def", "class", "import", "pass", "for", "while"]

variables = {}

def Variable(text, line):
    variables_name_pattern = "^[A-Za-z0-9_-]*$"

    if text[0] not in keywords:
        if text[0][0].isnumeric():
            print("Syntax error! Variable cannot start with a number.")
            sys.exit()
        elif bool(re.match(variables_name_pattern, text[0])):
            # check variable type
            # if variable is number
            if text[2].isnumeric():
                if len(text) > 3:
                    match text[3]:
                        case "+": variables[text[0]] = f'{int(text[2]) + int(text[4])}'
                        case "-": variables[text[0]] = f'{int(text[2]) - int(text[4])}'
                        case "*": variables[text[0]] = f'{int(text[2]) * int(text[4])}'
                        case "/":
                            if text[4] == "0":
                                print("Zero Division Error!")
                                sys.exit()
                            variables[text[0]] = f'{int(text[2]) / int(text[4])}'
                else:
                    variables[text[0]] = text[2]
            # if variable is string
            elif text[2][0] == "\"" or text[2][0] == "\'":
                str = ""
                for i in range(2, len(text)):
                    str += text[i]
                    if text[i][-1] == "\"" or text[i][-1] == "\'":
                        break
                    str += " "
                variables[text[0]] = str

            # if variable is boolean
            elif text[2] == "True" or text[2] == "False":
                variables[text[0]] = text[2]
            # if variable is not number, string or boolean
            else:
                print(f"----------"
                      f"\nFile: {filename}, Line: {line}\n{text[2]} \nInvalid Syntax!"
                      f"\n----------")
                sys.exit()


def Print(text, line):
    print_text = ""
    for i in range(text.find("print(") + 6, text.find(")")):
        print_text += text[i]

    size = len(print_text)

    if print_text == "": print()
    else:
        # print number
        if print_text.isnumeric():
            print(print_text)
        # print string
        elif print_text[0] == "\'":
            if print_text[size - 1] != "\'":
                print("Syntax error! Closing quote not found.")
                sys.exit()
            else:
                for i in range(1, len(print_text) - 1):
                    print(print_text[i], end="")
                print()
        elif print_text[0] == "\"":
            if print_text[size - 1] != "\"":
                print("Syntax error! Closing quote not found.")
                sys.exit()
            else:
                for i in range(1, len(print_text) - 1):
                    print(print_text[i], end="")
                print()
        # print boolean
        elif print_text == "True" or print_text == "False":
            print(print_text)
        # print variable value
        elif print_text in variables:
            text = variables[print_text]
            for i in range(len(text)):
                if text[i] != "\'" and text[i] != "\"":
                    print(text[i], end="")
            print()
        else:
            print("Error. Variable name is not defined.")
            sys.exit()


def main():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            row = file.readline()
            line = 1
            while row:
                if row == "\n":
                    row = file.readline()
                    line += 1
                    continue

                split_text = row.split()

                # check if variable
                Variable(split_text, line)

                # check if print
                for n in split_text:
                    if keywords[0] in n:
                        Print(n, line)

                row = file.readline()
                line += 1
    else:
        print("File don't find.")


main()
print(variables)