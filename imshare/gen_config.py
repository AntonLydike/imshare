from .misc import mkdir


def gen_nginx_conf():
    return """proxy_cache_path /data/nginx/cache keys_zone=mycache:10m;

server {
    # change this to reflect the system:
    listen 80;
    server_name example.org;
    root /var/www/imshare/;

    # make use of the custom 404 page:
    error_page 404 /404.html;

    # gzip directives are not included as all non-image files sent are 
    # already small. Adding a compression/decompression steps seems unnecessary.
    # Some testing indicates that file sizes will stay at or below 2kib.
    # Gzipping jpegs yields no additional benefit as they are pretty much 
    # incompressible anyways.

    # optimize how images are serverd:
    location /images {          
        sendfile            on;
        sendfile_max_chunk  1m;
        tcp_nopush          on;
        tcp_nodelay         on;
        keepalive_timeout   65;
        # very aggressive caching, images are content-addressed
        # so they will never change.
        expires             max;
        add_header Cache-Control "public";
        add_header Cache-Control "immutable";
    }

    # cache stylesheet and scripts less agressively
    # they aren't big anyway
    location /static {
        expires             1d;
        add_header Cache-Control "public";
    }

}"""


def print_nginx_conf():
    print(gen_nginx_conf())
