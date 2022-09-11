import os, sys
# import getpass

def encrypt(string):
    encrypted = ""
    for character in string:
        encrypted += chr(ord(character) + 5)
    return encrypted

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"

login_information = open(directory + "Login Information.txt", "w")
# login_information.write(encrypt(getpass.getpass("Student ID: ", stream = None)) + "\n")
# login_information.write(encrypt(getpass.getpass("Password: ", stream = None)))
login_information.write(encrypt(input("Student ID: ")) + "\n")
login_information.write(encrypt(input("Password: ")))
login_information.close()