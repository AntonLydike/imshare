def gen_nginx_conf():
    print("""

proxy_cache_path /data/nginx/cache keys_zone=mycache:10m;

server {
    root /var/www/imshare/;

    location / {
    }
          
    location /images {          
        sendfile           on;
        sendfile_max_chunk 1m;
        tcp_nopush on;
        tcp_nodelay       on;
        keepalive_timeout 65;
        
        expires max;
    }


}

""")