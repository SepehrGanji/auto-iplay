FROM istream_server_nginx_image

RUN apt-get update && \
    apt-get install iproute2 iputils-ping -y

COPY ./video/ /usr/local/nginx/html/

