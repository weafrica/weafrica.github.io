#!/bin/bash
# filepath: /mnt/c/Users/saule/OneDrive/Documents/weafrica.github.io/deploy.sh

# Generate the static site
pelican content

# Move the generated files to the root directory
cp -r output/* .

# Add, commit, and push changes to GitHub
git add .
git commit -m "Deploy site"
git push origin main