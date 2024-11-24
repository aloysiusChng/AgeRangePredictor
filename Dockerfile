# # Start your image with a node base image
# FROM node:18-alpine

# # The /app directory should act as the main application directory
# WORKDIR /app

# # Copy the app package and package-lock.json file
# COPY package*.json ./

# # Copy local directories to the current local directory of our docker image (/app)
# COPY ./src ./src
# COPY ./public ./public

# # Install node packages, install serve, build the app, and remove dependencies at the end
# RUN npm install \
#     && npm install -g serve \
#     && npm run build \
#     && rm -fr node_modules

# EXPOSE 3000

# # Start the app using serve command
# CMD [ "serve", "-s", "build" ]



# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
