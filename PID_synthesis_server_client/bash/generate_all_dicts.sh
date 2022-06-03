#!/bin/bash

bash ./bash/generate_python3_dicts.sh data/PID_tables_data_Ms_1.4.txt  > src/common/PID_Ms_1_4.py
bash ./bash/generate_python3_dicts.sh data/PID_tables_data_Ms_2.0.txt  > src/common/PID_Ms_2_0.py
bash ./bash/generate_python3_dicts.sh data/PI_tables_data_Ms_1.4.txt  > src/common/PI_Ms_1_4.py
bash ./bash/generate_python3_dicts.sh data/PI_tables_data_Ms_2.0.txt  > src/common/PI_Ms_2_0.py

exit 0
