"""
Roland Locke
1/31/2024

Required python modules:
Jupyter

"""
import os
import sys
import subprocess

#argparse is python's argument parser module
import argparse

#argument Parser
argParser = argparse.ArgumentParser(prog='documentHandler')

#command-line arguments
argParser.add_argument('inputFile', type=str, help='Path to the input file')
argParser.add_argument('-rb', '--remove_blank_space', action='store_true', help='Removes lines in a python file where two lines of blank_space are repeated')
argParser.add_argument('-py', '--convert_ipynb_to_py', action='store_true', help='Converts an .ipynb file to a .py file')

args = argParser.parse_args()

#place provided file in the inputFile variable
inputFile = args.inputFile

#eventually this will be used to string arguments together in the given order.
def get_argument_order():

    #get all arguments passed to the file
    args = sys.argv[1:]

    argumentOrder = []

    for arg in args:
        if arg.startswith('-'):
            argumentOrder.append(arg)

    return argumentOrder

#Converts ipynb (jupyter notebook) files to python files
def convert_ipynb_to_py(file):

    if os.path.splitext(file)[1] != '.ipynb':
        raise Exception("File is not an .ipynb file")
        return

    #edit the name of the given file to have the .py file type
    fileNamePy = file.split(".")[0] + '.py'

    #call to system to check if the file already exists (prevents overwriting an existing version)
    checkFileExists = 'IF EXIST ' + fileNamePy + ' echo exists'

    #Check if echo from previous call returns 'exists'
    result = subprocess.check_output(checkFileExists, shell=True)
    if 'exists' in result.decode('utf-8'):
        raise Exception('Failed: File already exists in the given files location')
        return
    else:
        #call to system so for jupyter notebook convert
        os.system('jupyter nbconvert --to script --no-prompt ' + file)

        return fileNamePy

#removes blankspace from python files
def remove_blank_space(file):

    if os.path.splitext(file)[1] != '.py':
        raise Exception("File is not an .py file")
        return

    #open the file
    f = open(file, 'rb')

    #call readlines()
    fileLines = f.readlines()

    #length of file by # of lines
    lengthOfFile = len(fileLines)-1

    #iterate through lines removing whitespace where needed
    for i in range(0, lengthOfFile, 1):
        if i+1 < lengthOfFile and fileLines[i] == fileLines[i+1]:
            fileLines.pop(i)
            lengthOfFile -= 1

    #close file
    f.close()

    #delete the contents of the file and re-write with the new lines
    f = open(file, 'wb')
    f.writelines(fileLines)

    #close file
    f.close()

    return file

if __name__ == "__main__":

    #get user arguments
    argsInput = get_argument_order()

    if args.remove_blank_space:
        remove_blank_space(inputFile)

    if args.convert_ipynb_to_py:
        convert_ipynb_to_py(inputFile)

    print("Complete")