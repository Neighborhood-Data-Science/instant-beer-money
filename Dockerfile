# set the Base Image from which your image will be built on
FROM nikolaik/python-nodejs:latest
# create a directory called beermoney in root. 
# This directory will contain the code which currently resides in
RUN mkdir /beermoney

# make /beermoney the working directory
WORKDIR /beermoney

# copy your requirements file to the directory you just created
COPY Tests/requirements.txt /beermoney 

RUN pip install -r requirements.txt

# copy the current directory in you local machine to /beermoney in your image
ADD . /beermoney

RUN cd beermoney-app

RUN npm install

RUN npm run build

RUN npm run preview

EXPOSE 5000

CMD python