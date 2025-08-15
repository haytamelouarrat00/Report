#!/bin/bash

# Check if commit message was provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"commit message\""
    exit 1
fi

git add .
git commit -m "$1"
git push -u origin master
