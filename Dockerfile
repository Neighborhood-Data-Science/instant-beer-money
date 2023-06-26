# set the Base Image from which your image will be built on
FROM python:3.11.1
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

RUN wget https://nodejs.org/dist/v20.1.0/node-v20.1.0.tar.gz && \
    tar -xzvf node-v20.1.0.tar.gz && \
    rm node-v20.1.0.tar.gz && \
    cd node-v20.1.0 && \
    ./configure && \
    make -j4 && \
    make install && \
    cd .. && \
    rm -r node-v20.1.0

RUN cd beermoney-app

RUN npm install

RUN npm run build

RUN npm run preview

EXPOSE 5000

CMD python