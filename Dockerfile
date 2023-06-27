# Stage 1: Initial build of the application

# set the Base Image from which your image will be built on
FROM nikolaik/python-nodejs:latest AS initialBuild

# Retrieve any updates
RUN apt-get update

# create a directory called beermoney in root. 
# This directory will contain the code which currently resides in our github repository
RUN mkdir /beermoney

# make /beermoney the working directory
WORKDIR /beermoney

# copy the current directory in you local machine to /beermoney in your image
COPY beermoney-app/package*.json ./

# Install all dependencies
RUN npm ci

# Copy source code to container
COPY . ./

# Make beermoney-app the working directory
WORKDIR /beermoney/beermoney-app

# Build the app
RUN npm run build

# # Stage 2: Production Stage
FROM nginx:stable-alpine AS prod

# Copy the built output from the builder stage to the Nginx default public folder
COPY --from=initialBuild /beermoney/beermoney-app/dist /usr/share/nginx/html

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

#Expose port 80 for access to the application
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
