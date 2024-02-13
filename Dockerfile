FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update 
RUN apt install -y mesa-vulkan-drivers \
        libxcursor1 \
        libxft2 \
        libxi6 \
        libxinerama1 \
        libxkbcommon0 \
        libxrandr2 \
        libxml2  
RUN apt install -y python3 python3-pip python3-tk
WORKDIR /app
COPY ./requirements.txt ./
RUN python3 -m pip install -r requirements.txt
COPY ./ ./
CMD python3 main.py
ENV XDG_RUNTIME_DIR=/tmp
ENV DISPLAY=host.docker.internal:0.0

