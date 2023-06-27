# set the Base Image from which your image will be built on
FROM nikolaik/python-nodejs:latest
# create a directory called beermoney in root. 
# This directory will contain the code which currently resides in

RUN apt-get update

RUN mkdir /beermoney

# make /beermoney the working directory
WORKDIR /beermoney

# copy your requirements file to the directory you just created
COPY Tests/requirements.txt /beermoney 

RUN pip install -r requirements.txt

# copy the current directory in you local machine to /beermoney in your image
COPY beermoney-app/package*.json ./

RUN npm ci --omit=dev

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
