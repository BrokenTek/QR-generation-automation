#!/bin/bash

# Function to check if a program is in PATH
check_in_path() {
    local program=$1
    local path=$(which $program 2>/dev/null)
    [[ -n $path ]] && echo $path
}

# Check if Homebrew is installed
if [ -z "$(check_in_path brew)" ]; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Check if Homebrew is in PATH
if [ -z "$(check_in_path /opt/homebrew/bin/brew)" ]; then
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "Homebrew is already in PATH."
fi

# Install Python 3
echo "Installing Python 3..."
brew install python@3

# Check if Python 3 is in PATH
if [ -z "$(check_in_path /usr/local/opt/python@3/bin/python3)" ]; then
    echo 'export PATH="/usr/local/opt/python@3/bin:$PATH"' >> ~/.zprofile
    source ~/.zprofile
else
    echo "Python 3 is already in PATH."
fi

echo "Setup completed successfully!"
echo "Restart your Terminal session to ensure changes are completed."


echo "cd" >> pwd
