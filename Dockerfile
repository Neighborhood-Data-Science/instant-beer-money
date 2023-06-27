# Stage 1: Initial build of the application

# set the Base Image from which your image will be built on
FROM nikolaik/python-nodejs:latest AS initialBuild

RUN apt-get update

# create a directory called beermoney in root. 
# This directory will contain the code which currently resides in our github repository
RUN mkdir /beermoney

# make /beermoney the working directory
WORKDIR /beermoney

# copy your requirements file to the directory you just created
COPY Tests/requirements.txt /beermoney 

RUN pip install -r requirements.txt

# Install vite
RUN npm install -g vite

RUN npm install typescript@latest -g

# copy the current directory in you local machine to /beermoney in your image
COPY beermoney-app/package*.json ./

RUN npm ci

COPY . ./

RUN npm run build

# Stage 2: Production Stage
FROM nginx:stable-alpine

# Copy the built output from the builder stage to the Nginx default public folder
COPY --from=initialBuild /beermoney/dist /usr/share/nginx/html

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
