# PID_synthesis_server_client
PID Synthesis software, Server and Client

## Project directory tree

    .
	├── bash
	│   ├── compute_request.sh
	│   ├── functions.sh
	│   ├── generate_all_dicts.sh
	│   ├── generate_python3_dicts.sh
	│   ├── g_PID_combinations.sh
	│   ├── matlab.sh
	│   ├── read_colm.sh
	│   ├── wait_and_list_images.sh
	│   ├── wait_and_send_model_comparison.sh
	│   ├── wait_and_send_vectors.sh
	│   └── wait_error_indexes.sh
	├── config
	├── data
	│   ├── PID_tables_data_Ms_1.4.txt
	│   ├── PID_tables_data_Ms_2.0.txt
	│   ├── PI_tables_data_Ms_1.4.txt
	│   └── PI_tables_data_Ms_2.0.txt
	├── LICENSE
	├── README.md
	└── src
	    ├── client
	    │   ├── desktop_client
	    │   │   ├── client.py
	    │   │   └── run.sh
	    │   └── webapp_client
	    │       ├── bash
	    │       │   └── setup_lighttpd.sh
	    │       ├── cgi-bin
	    │       │   ├── client_cgi_python.py
	    │       │   └── client_param_in.py
	    │       ├── html
	    │       │   ├── css
	    │       │   │   └── tool_style.css
	    │       │   └── js
	    │       └── templates
	    │           ├── iframe_plotly.html
	    │           ├── ingress_page.html
	    │           └── results_page.html
	    ├── identool
	    │   ├── lib
	    │   │   ├── APC.m
	    │   │   ├── f_IDFOM.m
	    │   │   ├── finish.m
	    │   │   ├── IDFOM.m
	    │   │   ├── set_variables.m
	    │   │   └── start.m
	    │   └── run.sh
	    ├── server
	    │   ├── common
	    │   │   ├── client_thread.py
	    │   ├── run.sh
	    │   └── server.py
	    ├── sketcher
	    │   ├── lib
	    │   │   ├── APC.m
	    │   │   ├── close_loop_ft.m
	    │   │   ├── crone_pm_aprox.m
	    │   │   ├── define_controllers.m
	    │   │   ├── error_indexes.m
	    │   │   ├── finish.m
	    │   │   ├── generate_plots.m
	    │   │   ├── parameters_preprocessing.m
	    │   │   └── start.m
	    │   ├── run.sh
	    │   ├── src
	    │   └── sys_response.m
	    └── tuning
	        ├── common
	        │   ├── fractional_order_rule
	        │   │   ├── common.py
	        │   │   ├── PID_Ms_1_4.py
	        │   │   ├── PID_Ms_2_0.py
	        │   │   ├── PI_Ms_1_4.py
	        │   │   └── PI_Ms_2_0.py
	        │   └── outformat
	        │       └── table_format.py
	        ├── run.sh
	        └── tuning.py
