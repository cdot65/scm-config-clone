#!/bin/bash

# Script to run tests with coverage reporting

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE} SCM Config Clone Test Runner ${NC}"
echo -e "${BLUE}======================================${NC}"

# Check if poetry is installed
if ! command -v poetry &> /dev/null
then
    echo -e "${RED}Error: Poetry is not installed.${NC}"
    echo "Please install poetry from https://python-poetry.org/docs/#installation"
    exit 1
fi

# Install dependencies if needed
echo -e "${YELLOW}Checking dependencies...${NC}"
poetry install

# Run specific test type based on argument
if [ "$1" = "unit" ]; then
    echo -e "${GREEN}Running unit tests...${NC}"
    poetry run pytest tests/unit/test_utilities_direct.py tests/unit/test_settings.py tests/unit/test_network_direct.py -v
elif [ "$1" = "integration" ]; then
    echo -e "${GREEN}Running integration tests...${NC}"
    poetry run pytest tests/integration -v
elif [ "$1" = "utils" ]; then
    echo -e "${GREEN}Running utility tests only...${NC}"
    poetry run pytest tests/unit/test_utilities_direct.py -v
elif [ "$1" = "settings" ]; then
    echo -e "${GREEN}Running settings tests only...${NC}"
    poetry run pytest tests/unit/test_settings.py -v
elif [ "$1" = "network" ]; then
    echo -e "${GREEN}Running network module tests...${NC}"
    poetry run pytest tests/unit/test_network_direct.py -v
elif [ "$1" = "fast" ]; then
    echo -e "${GREEN}Running fast tests (no coverage)...${NC}"
    poetry run pytest tests/unit/test_utilities_direct.py tests/unit/test_settings.py -v
else
    # Run all tests by default
    echo -e "${GREEN}Running all tests...${NC}"
    poetry run pytest tests/unit/test_utilities_direct.py tests/unit/test_settings.py tests/unit/test_network_direct.py -v
fi

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE} Tests completed ${NC}"
echo -e "${BLUE}======================================${NC}"