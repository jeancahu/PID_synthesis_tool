#!/bin/bash

mkdir /var/www/html/images
chmod 755 /var/www/html/images
cp ./client_cgi_python.py /var/www/cgi-bin/

cat <<EOF
server.modules = (
	       "mod_access",
	       "mod_cgi",
	       "mod_alias",
	       "mod_compress",
        "mod_redirect",
)

server.document-root        = "/var/www/html"
server.upload-dirs          = ( "/var/cache/lighttpd/uploads" )
server.errorlog             = "/var/log/lighttpd/error.log"
server.pid-file             = "/var/run/lighttpd.pid"
server.username             = "www-data"
server.groupname            = "www-data"
server.port                 = 80


index-file.names            = ( "index.php", "index.html", "index.lighttpd.html" )
url.access-deny             = ( "~", ".inc" )
static-file.exclude-extensions = ( ".php", ".pl", ".fcgi" )

compress.cache-dir          = "/var/cache/lighttpd/compress/"
compress.filetype           = ( "application/javascript", "text/css", "text/html", "text/plain" )

# default listening port for IPv6 falls back to the IPv4 port
include_shell "/usr/share/lighttpd/use-ipv6.pl " + server.port
include_shell "/usr/share/lighttpd/create-mime.assign.pl"
include_shell "/usr/share/lighttpd/include-conf-enabled.pl"


$HTTP["url"] =~ "^/interactive/" {
        alias.url += ( "/interactive/" => "/var/www/cgi-bin/" )
        cgi.assign = (
		   ".cgi" => "",
                ".py"  => "/usr/bin/python3",
                ".pl"  => "/usr/bin/perl",
                ".sh"  => "/bin/sh",
        )
}
EOF
#> /etc/lighttpd/lighttpd.conf
