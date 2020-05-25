#!/usr/bin/env bash
# Step 1:
# Build image and add a descriptive tag
docker build -f Dockerfile . -t jupyter --label jupyter
# Step 2: 
# List docker images
docker image ls --filter label=jupyter
# Step 3: 
# Run flask app
docker run -it -p 8888:8888 jupyter

