#!/bin/bash

# Define variables
REPO_NAME="working-patterns-replication-package"
ZIP_FILE="${REPO_NAME}.zip"

# Create the zip file
echo "Creating zip file: ${ZIP_FILE}"
zip -r "${ZIP_FILE}" . -x "*.git*" "*.zip" "*.DS_Store"

# Check if the zip file was created successfully
if [ -f "${ZIP_FILE}" ]; then
    echo "Zip file created successfully: ${ZIP_FILE}"
else
    echo "Failed to create zip file"
    exit 1
fi