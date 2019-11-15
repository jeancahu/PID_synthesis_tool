#!/usr/bin/env python3

import socket, re
import cgi
import jinja2
#import sys
from json import loads as json_to_python

## Global Vars
server_URL = "163.178.124.156"
server_port = 8494
images_path = '../html/images/'
plotly_iframe_disable_button='true'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Se crea el socket
try:
    client.connect((server_URL, server_port))
except:
    # print("No fue posible ingresar por el puerto ", server_port, server_URL)
    pass

form_data = cgi.FieldStorage()
model_parameters = "no_images,simulation_vectors,json_format,error_indexes"

if "form_input" in form_data.keys():
    step_resp = form_data.getvalue('textcontent')
    step_resp = re.sub('^ *$' ,'' ,step_resp)
    if step_resp:
        model_type="model_file,model_parameters,model_comparison"
        in_frac_order = "-"
        in_time_const = "-"
        in_prop_const = "-"
        in_dtime_const = "-"

    else:
        model_type="model_fotf"
        in_frac_order = form_data.getvalue('in_frac')
        in_time_const = form_data.getvalue('in_time')
        in_prop_const = form_data.getvalue('in_prop')
        in_dtime_const = form_data.getvalue('in_dtime')

else:
    model_type="model_fotf"
    in_frac_order = str(form_data["v"].value)
    in_time_const = str(form_data["T"].value)
    in_prop_const = str(form_data["K"].value)
    in_dtime_const = str(form_data["L"].value)

# Send model type
model_type=model_type+','+model_parameters
client.send(model_type.encode())
response = client.recv(512)

# Send models parameters
if 'model_fotf' in model_type:
    parameters = in_frac_order+","+in_time_const+","+\
        in_prop_const+","+in_dtime_const
    client.send(parameters.encode())
else:
    parameters = step_resp+'\nEOF'
    client.sendall(parameters.encode())

controller_params = client.recv(2048).decode()

## Receive simulation vectors
result = ""
while not 'EOF' in result:
    # Recibe 512 bytes del cliente; data len
    result += client.recv(512).decode('utf-8')
vectors_result = result.replace("\nEOF\n",'')
client.send("vectors_received_confirmation".encode('utf-8'))

in_model_iae = '-'
if "model_parameters" in model_type:
    ## Receive model parameters
    model_parameters_json = client.recv(2048).decode()
    client.send("model_received_confirmation".encode('utf-8'))
    model_parameters_dict = json_to_python(model_parameters_json)
    in_frac_order = model_parameters_dict['v']
    in_time_const = model_parameters_dict['T']
    in_prop_const = model_parameters_dict['K']
    in_dtime_const = model_parameters_dict['L']
    in_model_iae = model_parameters_dict['IAE']

## Receive error indexes
error_indexes_json = client.recv(2048).decode()
client.send("error_indexes_received_confirmation".encode('utf-8'))

if "model_comparison" in model_type:
    ## Receive model vectors
    result = ""
    while not 'EOF' in result:
        # Recibe 512 bytes del cliente; data len
        result += client.recv(512).decode('utf-8')
    model_comparison_vects = result.replace("\nEOF\n",'')
    client.send("model_comparison_received_confirmation".encode('utf-8'))

# Close socket
client.close()

## Generate plotly iframe for close-loop
signal_template = jinja2.Template("""
	var {{vect}} = {
	    x: vect_{{vect}}_t,
	    y: vect_{{vect}},
	    type: 'scatter',
	    name: '{{name}}'
	};
""")

close_loop_signals_define = []
vects = ('X1', 'X2', 'X3', 'X4', 'R', 'D')
vects_names = ("PI, Ms=1.4", "PI, Ms=2.0", "PID, Ms=1.4", "PID, Ms=2.0", "r(s)", "d(s)")
for vect, name in zip(vects, vects_names):
    close_loop_signals_define.append(signal_template.render(
        vect=vect,
        name=name
    ))

if "model_comparison" in model_type:
    ## Generate plotly iframe for model comparison
    signal_template = jinja2.Template("""
            var {{vect}} = {
                x: vect_tnorm,
                y: vect_{{vect}},
                type: 'scatter',
                name: '{{name}}'
            };
    """)

    model_comparison_signals_define = []
    vects = ('unorm', 'ynorm', 'ym')
    vects_names = ("u(s)", "y(s)", "ym(s)")
    for vect, name in zip(vects, vects_names):
        model_comparison_signals_define.append(signal_template.render(
            vect=vect,
            name=name
        ))

## Controllers params parsing
controller_params = controller_params.replace('EOF', '')
controller_params = re.sub('[\t ]','', controller_params)
controller_params = controller_params.replace('}\n{', '},{')

jin_env = jinja2.Environment(loader=jinja2.FileSystemLoader('/var/www/templates'))

template = jin_env.get_template("results_page.html")
template_plotly = jin_env.get_template("iframe_plotly.html")

iframe_plotly_close_loop = template_plotly.render(vectors_define=vectors_result,
                                                  signals_define=close_loop_signals_define,
                                                  data="[X1, X2, X3, X4, R, D]",
                                                  title="Closed-loop System Responses"
)
if "model_comparison" in model_type:
    iframe_plotly_model_comparison = template_plotly.render(
        vectors_define=model_comparison_vects,
        signals_define=model_comparison_signals_define,
        data="[unorm, ynorm, ym]",
        title="Model Comparison"
    )

hash_dir = float(in_frac_order)+float(in_time_const)+float(in_prop_const)+float(in_dtime_const)
hash_dir = str(hash_dir)
hash_dir = hash_dir.replace('.','p')

plotly_page_file_link_close_loop = "/tmp/close_loop_"+hash_dir+"_plotly.html"
plotly_page_file_link_model_comparison = "/tmp/model_comparison_"+hash_dir+"_plotly.html"
plotly_page_file = open('../html'+plotly_page_file_link_close_loop, "w+")
plotly_page_file.write(iframe_plotly_close_loop)
plotly_page_file.close()

if "model_comparison" in model_type:
    plotly_iframe_disable_button='false'
    plotly_page_file = open('../html'+plotly_page_file_link_model_comparison, "w+")
    plotly_page_file.write(iframe_plotly_model_comparison)
    plotly_page_file.close()


page_code = template.render(v_param=in_frac_order,
                            T_param=in_time_const,
                            K_param=in_prop_const,
                            L_param=in_dtime_const,
                            model_IAE=in_model_iae,
                            controller_params=controller_params,
                            error_indexes=error_indexes_json,
                            iframe_plotly_close_loop=plotly_page_file_link_close_loop,
                            iframe_plotly_model_comparison=plotly_page_file_link_model_comparison,
                            button_disable=plotly_iframe_disable_button
)

print("Content-type:text/html\r\n\r\n")
print(page_code)

