#!/usr/bin/env python3

import jinja2

jin_env = jinja2.Environment(loader=jinja2.FileSystemLoader('/var/www/templates'))
template = jin_env.get_template("ingress_page.html")

page_code = template.render()

print("Content-type:text/html\r\n\r\n")
print(page_code)

