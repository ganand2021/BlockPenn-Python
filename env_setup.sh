#!/bin/bash

# Variables
PYTHON_VERSION="3.9"

# Define colors and icons
GREEN="\033[32m"
YELLOW="\033[33m"
RESET="\033[0m"
CHECK_MARK="✅"
WRENCH="🔧"
GEAR="⚙️"
HAM_AND_WRENCH="🛠️"

# Create a virtual environment
echo -e "${YELLOW}${WRENCH} Creating a virtual environment with Python $PYTHON_VERSION...${RESET}"
python3 -m venv venv --python=python$PYTHON_VERSION

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
echo -e "${YELLOW}${WRENCH} Installing the project requirements...${RESET}"
pip install -r requirements.txt

# Additional setup steps, if necessary (e.g., database setup, environment variables, etc.)
echo -e "${YELLOW}${WRENCH} Performing additional setup steps...${RESET}"
# Add your custom setup steps here

echo -e "${GREEN}${CHECK_MARK} Environment setup complete. Now, you can start working on your project.${RESET}"
