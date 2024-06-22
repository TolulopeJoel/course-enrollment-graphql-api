#!/bin/bash

# Function to run a command and check its result
run_command() {
    echo "Running: $1"
    eval $1
    if [ $? -ne 0 ]; then
        echo "Error: Command failed - $1"
        exit 1
    fi
}

# Step 1: Modify your models (this step is manual and not included in the script)

# Step 2: Generate a new migration script
read -p "Enter a message for the migration: " migration_message
run_command "alembic revision --autogenerate -m \"$migration_message\""

# Step 3: Apply the migration
run_command "alembic upgrade head"

echo "Migration completed successfully."