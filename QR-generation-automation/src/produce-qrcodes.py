# This script will take a txt file with a URL on each line and produce a directory
#   with .png files for each URL, each containing a qrcode for that url
# Help: python qrcodes-auto.py -h   (python3 qrcodes-auto.py -h) *On Unix
# For: Bbot Workflow
# Author: Carson
# SPAGETTI PROCEDURAL CODE because its a very simple script.

import os
import subprocess
import sys

def main():
    # Check for '-h' or '--help' argument and output directions if passed
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        
        help_txt = '''
    HELP TEXT:
    
    This script is used to automate the process of creating QR codes (with or without specified sizes)
    for each URL in a .txt file, then places each QR code (saved as .png files) inside a directory (choice of name or default name).
    
    Users can use this program, passing in 0, 1, 2, or 3 arguments when calling the script with 'python3 produce-qrcodes.py'.
    
    Options:
        1) 0 arguments passed:
            When no arguments are passed, the script will search for a .txt file within the same directory (folder) as the script
            itself. This default .txt file name is 'links.txt'. If this file does not exist, the program will halt and not produce
            any QR codes as it will not know where the list of QR codes is. If 'links.txt' exists, the program will use default
            values for both the directory of QR codes name and the size of the QR codes. The default directory name where the QR
            codes will be held would be created (if it exists, the program will just use the existing directory) will be called
            'qrcodes' and the default size will be '3' (87x87 pixels). 
            * For reference: 
            - A size of '6' produces dimensions of 174x174 pixels.
            - A size of '10' produces dimensions of 290x290 pixels.
            - A size of '15' produces dimensions of 435x435 pixels.
        
        2) 1 argument passed that is an integer (whole number) that is also positive in value:
            When only one argument is passed that is a valid and positive integer, the same default values will be used as described
            in the 0 arguments version, but the QR code's will have a square size based on the integer argument that is passed. The 
            default value is '3', but likely values that would be passed in place would be somewhere between 5-15 (low-end to high-end).
            With this method, the program searches for 'links.txt' (halts if not found) and creates QR codes with the given size as .png
            files and saves them all in a directory called 'qrcodes'.
        
        3) 2 arguments passed (must be .txt file with links name or path and desired directory name for .png files):
            Argument 1 -> Name of .txt file (including the .txt suffix, and in quotes (" ") if there are spaces in the
            filename).
            Argument 2 -> Name of the directory (folder) desired for storing the QR code .png files (in quotes (" ") if using spaces).  
            The default size value of '3' is used for QR code generation.          
            
        4) 3 arguments passed:
            Argument 1 -> Name of .txt file (including the .txt suffix, and in quotes (" ") if there are spaces in the
            filename).
            Argument 2 -> Name of the directory (folder) desired for storing the QR code .png files (in quotes (" ") if using spaces).
            Argument 3 -> Positive integer desired for size of each QR code that will be saved in the directory named from the second
            argument as .png files. Default is 3, typical values passed would be around 5-15.
        '''
        
        print(f"\n{help_txt}")
        
        input("Press ENTER to exit...")
        return
    
    
    
    # If both arguments for input file name and output directory name are passed, assign them
    #   otherwise, use default values for each and tell user.   
    try:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
        args_passed = True  # Arguments passed (first 2)
    except IndexError:
        # Absence of both args, input file name and output direcotry name defaults defined
        input_file = "links.txt"
        output_dir = "qrcodes"
        args_passed = False   # Arguments not passed (both first 2)
        # Warn user of default usage
        print(f"\nWarning! Expected 2 Arguments specifying: 'input file name' and 'output directory name'.\nDefaulting \
to input file name of '{input_file}' and output directory name '{output_dir}'.\n*v(This can be ignored) *\n")
            
    # Check for and define size + default size in absence of third argument (3 is default for func call with no args)
    # All three arguments passed
    if args_passed and len(sys.argv) == 4:
        try:
            size = int(sys.argv[3])
            if size < 1:
                print("\nThe value passed for size must be greater than 0.\n")
                print("Exiting...")
                return
            print(f"\nQR code .png size set to {size}.\n")
        except ValueError:
            size = 3
            print(f"\nInvalid size (3rd) argument: '{sys.argv[3]}' (Must be an integer).\nDefaulting to {size}.\n")
    # Only size argument (1) passed
    elif not args_passed and len(sys.argv) == 2:
        try:
            size = int(sys.argv[1])
            if size < 1:
                print("\nThe value passed for size must be greater than 0.\n")
                print("Exiting...")
                return
            print(f"\nSize set to {size}.ONLY ARG\n")
        except ValueError:
            size = 3
            print(f"\nInvalid size (1st) argument: '{sys.argv[1]}' (Must be an integer).\nDefaulting to {size}.\n")
    # More than three arguments passed
    elif len(sys.argv) > 4:
        print("\nArguments passed invalid. Only 1 or 3 arguments allowed.\n\nExiting...")
        return
    # Invalid arguments passed
    else:
        size = 3
        print(f"\nThird argument not passed.\nDefaulting to {size}.")

    # Check for existence of directory by given name (or default name) and warn user
    #   creates directory if non-existent, uses directory that exists if it exists
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        print(f"\nDirectory '{output_dir}' already exists. Files will be added to this directory if they \
do not already exist by name.\nExisting files will be overwritten but won't change unless a new size is \
passed.\n* (This can be ignored) *\n")
    else:
        os.makedirs(output_dir, exist_ok=True)
        
    # Check for the existence of the given/default input file by name
    #   if the file does not exist, execution should halt
    if os.path.exists(input_file) and os.path.isfile(input_file):
        # Continue execution
        pass
    else:
        print("\nInput file by the given name does not exist.\n\nExiting...")
        return
    
    print(("---------------------------------------------------------"))
        
    # Parse input file of URL's
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            link = line.strip()
            if link:
                filename = ''.join([c if c.isalnum() else '_' for c in link])
                output_path = os.path.join(output_dir, f"{filename}.png")
                subprocess.run(['qrencode', '-o', output_path, '-s', str(size), link], check=False)
                print(f"Generated QR code for: {link}")

    print("---------------------------------------------------------")
    print(f"\nSucess! All QR codes generated and saved in the '{output_dir}' directory!")   

if __name__ == "__main__":
    main()
    