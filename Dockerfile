FROM nginx:1.25.3 AS build

RUN apt-get update

RUN apt-get install -y build-essential \
                       wget \
                       git \
                       libpcre3 libpcre3-dev \
                       zlib1g zlib1g-dev \
                       openssl libssl-dev \ 
                       procps

RUN mkdir src

WORKDIR /src/

RUN wget http://nginx.org/download/nginx-1.25.3.tar.gz

RUN tar -xzvf nginx-1.25.3.tar.gz

RUN git clone https://github.com/evanmiller/mod_zip.git

#RUN git clone --branch=patch-1 https://github.com/dvershinin/nginx-unzip-module.git

# * Zip module.
RUN cd nginx-1.25.3/ && ./configure --with-compat --add-dynamic-module=../mod_zip

RUN cd nginx-1.25.3 && make modules

RUN cd nginx-1.25.3 && cp objs/ngx_http_zip_module.so  /etc/nginx/modules


#* Development stage. 
FROM nginx:1.25.3

COPY --from=build /etc/nginx/modules/ngx_http_zip_module.so /etc/nginx/modules

# prepend load module to config
RUN sed -i -e "1i load_module /etc/nginx/modules/ngx_http_zip_module.so;" /etc/nginx/nginx.conf
