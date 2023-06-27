# Stage 1: Initial build of the application

# set the Base Image from which your image will be built on
FROM nikolaik/python-nodejs:latest AS initialBuild

RUN apt-get update

# create a directory called beermoney in root. 
# This directory will contain the code which currently resides in our github repository
RUN mkdir /beermoney

# make /beermoney the working directory
WORKDIR /beermoney

# Install vite
RUN npm install -g vite

RUN npm install typescript@latest -g

# copy the current directory in you local machine to /beermoney in your image
COPY beermoney-app/package*.json ./

RUN npm ci

COPY . ./

WORKDIR /beermoney/beermoney-app

RUN npm run build

# # Stage 2: Production Stage
FROM nginx:stable-alpine

# Copy the built output from the builder stage to the Nginx default public folder
COPY --from=initialBuild /beermoney/beermoney-app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
