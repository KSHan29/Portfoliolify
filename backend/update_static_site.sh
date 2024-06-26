#!/bin/bash

# Navigate to the project root
cd /path/to/your/django/project

# Collect static files
python manage.py collectstatic --noinput

# Generate static site files
python manage.py distill-local output

# Navigate to the output directory
cd output

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
  git init
  git remote add origin https://github.com/your-username/your-repo-name.git
fi

# Checkout gh-pages branch
git checkout -b gh-pages

# Add and commit changes
git add .
git commit -m "Update static site with latest data"

# Push changes to gh-pages branch
git push origin gh-pages --force
