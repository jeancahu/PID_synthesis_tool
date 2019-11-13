#!/bin/python3

#
# PI/PID Tunning
#

# Args:
# * v,     Fractional order
# * T,     Time constant
# * K,     Proportional constant
# * L,     Dead time constant
# * Ms,    maximum sensitivity
# * synx,  syntax string
# * CType, Controler type ['PI','PID']

# Internal values
# * tao_o, Fractional normalized dead time

import numpy as np
from sys import exit
from sys import argv

#

from common.fractional_order_rule import common
from common.outformat import table_format

# Define controller type
Type = argv[-1]
if Type == 'PID':
    from common.fractional_order_rule import PID_Ms_2_0 as Ms_2_0
    from common.fractional_order_rule import PID_Ms_1_4 as Ms_1_4
elif Type == 'PI':
    from common.fractional_order_rule import PI_Ms_2_0 as Ms_2_0
    from common.fractional_order_rule import PI_Ms_1_4 as Ms_1_4
else:
    print("Error, unknown controller")
    exit(6)

# Define syntax
if type(argv[-2]) == str:
    syntx = argv[-2].lower()
else:
    syntx = "none"

def main ():
    #print(Type, "controller tunnig")
    #print(argv)

    args = []
    values_dict = {}

    if len(argv) != 8:
        raise ValueError('here are not enough values')
        exit(1)

    #print("There are whole necessary values")

    try:
        args = [ float(x) for x in argv[1:-2] ]
    except Exception:
        raise ValueError('There are args that are not numbers')
        exit(2)

    # Define model values
    v    = float(args[0])
    T    = args[1]
    K    = args[2]
    L    = args[3]
    Ms   = args[4]
    
    # Verify v is in range
    if Type == 'PI':
        v_range = (1.6,1.0)
    elif Type == 'PID':
        v_range = (1.8,1.0)

    if v <= v_range[0] and v >= v_range[1]:
        # print('Fractional order is in range [', v_range[1],', ', v_range[0],']')
        pass
    else:
        raise ValueError(
            'Fractional order is not in range [', v_range[1],', ', v_range[0],']')
        exit(3)

    # Calculate fractional normalized dead time
    tao_o = float(L)/(np.power(T,1/v))
    # print("fractional normalized dead time: ", tao_o)

    
    if tao_o <= 2.0 and tao_o >= 0.1:
        # print('Fractional normalized dead time is in range [0.1, 2.0]')
        pass
    else:
        raise ValueError('Fractional normalized dead time is not in range [0.1, 2.0]')
        exit(4)

    if Ms == 2.0:
        if Type == 'PID':
            values_dict = Ms_2_0.PID_Ms_2_0
        elif Type == 'PI':
            values_dict = Ms_2_0.PI_Ms_2_0
    elif Ms == 1.4:
        if Type == 'PID':
            values_dict = Ms_1_4.PID_Ms_1_4
        elif Type == 'PI':
            values_dict = Ms_1_4.PI_Ms_1_4
    else:
        raise ValueError('Maximum sensitivity is not in {1.4, 2.0}')
        exit(5)
    # print('Maximum sensitivity is in range {1.4, 2.0}')

    # Calculate results:
    kappa_p = common.normalized_proportional_const(values_dict, v, tao_o)    
    tao_i = common.normalized_integral_const(values_dict, v, tao_o)
    if Type == 'PID':
        tao_d = common.normalized_differential_const(values_dict, v, tao_o)
    else:
        tao_d = 0
    K_p = np.divide(kappa_p, K)
    T_i = np.multiply(tao_i, np.power(T, np.divide(1,v)))
    if Type == 'PID':
        T_d = np.multiply(tao_d, np.power(T, np.divide(1,v)))
    else:
        T_d = 0

    table_format.print_table_results(Type, Ms, syntx,
        kappa_p, tao_i, tao_d, K_p, T_i, T_d)

if __name__ == "__main__": 
  main()
  exit(0)
