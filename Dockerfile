#docker build -t python_folder_splitter:1.0.0 . --network=host
FROM python:3.8-bullseye
RUN apt-get update
RUN apt-get install -y tzdata && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean
RUN apt-get install -y python3-pip libgdal-dev locales
RUN echo 'alias python=python3' >> ~/.bashrc
RUN echo 'alias pip=pip3' >> ~/.bashrc
RUN pip3 install numpy
RUN pip3 install Pillow
RUN pip3 install python-magic
RUN mkdir -p /app
RUN mkdir -p /app/src
RUN mkdir -p /app/dst
WORKDIR /app
