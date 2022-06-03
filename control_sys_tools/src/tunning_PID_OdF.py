#!/bin/python3

#
# PID one-degree-of-freedom Tunning
#

import numpy as np
import sys

#

from common import common
from common import PID_Ms_2_0 as Ms_2_0
from common import PID_Ms_1_4 as Ms_1_4

# Args:
# * v,  Fractional order
# * T,  Time constant
# * K,  Proportional constant
# * L,  Dead time constant
# * Ms, maximum sensitivity

# Internal values
# * tao_o, Fractional normalized dead time

def main ():
    print("PID controller tunnig")    
    print(sys.argv)

    args = []
    values_dict = {}

    if len(sys.argv) != 6:
        raise ValueError('here are not enough values')
        sys.exit(1)

    print("There are whole necessary values")

    try:
        for num in sys.argv[1:]:
            print(type(num))
            print(num)
            if '.' in num:
                print("float type")
                args.append(float(num))
            else:
                print("int type")
                args.append(int(num))
    except Exception:
        raise ValueError('There are args that are not numbers')
        sys.exit(2)

    # Define model values
    v  = args[0]
    T  = args[1]
    K  = args[2]
    L  = args[3]
    Ms = args[4]
    
    # Verify v is in range

    if float(v) <= 1.8 and float(v) >= 1.0:
        print('Fractional order is in range [1.0, 1.8]')
    else:
        raise ValueError('Fractional order is not in range [1.0, 1.8]')
        sys.exit(3)

    # Calculate fractional normalized dead time
    tao_o = float(L)/(np.power(T,1/float(v)))
    print("fractional normalized dead time: ", tao_o)

    
    if tao_o <= 2.0 and tao_o >= 0.1:
        print('Fractional normalized dead time is in range [0.1, 2.0]')
    else:
        raise ValueError('Fractional normalized dead time is not in range [0.1, 2.0]')
        sys.exit(4)

    if Ms == 2.0:
        values_dict = Ms_2_0.PID_Ms_2_0
    elif Ms == 1.4:
        values_dict = Ms_1_4.PID_Ms_1_4
    else:
        raise ValueError('Maximum sensitivity is not in {1.4, 2.0}')
        sys.exit(5)
    print('Maximum sensitivity is in range {1.4, 2.0}')

    print('PID Tunning:')

    kappa_p = common.normalized_proportional_const(values_dict, v, tao_o)
    print('Normalized proportional value:', kappa_p)

    tao_i = common.normalized_integral_const(values_dict, v, tao_o)
    print('Normalized integral value:', tao_i)

    tao_d = common.normalized_differential_const(values_dict, v, tao_o)
    print('Normalized differential value:', tao_d)

    K_p = np.divide(kappa_p, K)
    print('Proportional value:', K_p)

    T_i = np.multiply(tao_i, np.power(T, np.divide(1,v)))
    print('Integral value:', T_i)

    T_d = np.multiply(tao_d, np.power(T, np.divide(1,v)))
    print('Differential value:', T_d)

    sys.exit(0)
    
    
main()
