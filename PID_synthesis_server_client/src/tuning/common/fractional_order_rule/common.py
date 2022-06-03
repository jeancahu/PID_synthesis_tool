#!/bin/python3

import numpy as np

def normalized_proportional_const (values_dict, v, tao_o):
    # param: in:  Values dict
    # param: in:  Fractional order
    # param: in:  Normalized dead time
    # param: out: Normalized proportional const

    if str(v) in values_dict:
        table = values_dict[str(v)]
        a1 = table['a1']
        a2 = table['a2']
        a3 = table['a3']

    else:
        v_l = str(v)[:3]
        v_r = str(v+0.1)[:3]
        
        table_l = values_dict[v_l]
        table_r = values_dict[v_r]

        a1 = np.interp(v, [v_l, v_r], [table_l['a1'], table_r['a1']])
        a2 = np.interp(v, [v_l, v_r], [table_l['a2'], table_r['a2']])
        a3 = np.interp(v, [v_l, v_r], [table_l['a3'], table_r['a3']])
        
    result =  a1*np.power(tao_o, a2) + a3
    return result

def normalized_integral_const (values_dict, v, tao_o):
    # param: in:  Values dict
    # param: in:  Fractional order
    # param: in:  Normalized dead time
    # param: out: Normalized integral const

    if str(v) in values_dict:
        table = values_dict[str(v)]
        b1 = values_dict[str(v)]['b1']
        b2 = values_dict[str(v)]['b2']
        b3 = values_dict[str(v)]['b3']
        b4 = values_dict[str(v)]['b4']
        b5 = values_dict[str(v)]['b5']

    else:
        v_l = str(v)[:3]
        v_r = str(v+0.1)[:3]
        
        table_l = values_dict[v_l]
        table_r = values_dict[v_r]

        b1 = np.interp(v, [v_l, v_r], [table_l['b1'], table_r['b1']])
        b2 = np.interp(v, [v_l, v_r], [table_l['b2'], table_r['b2']])
        b3 = np.interp(v, [v_l, v_r], [table_l['b3'], table_r['b3']])
        b4 = np.interp(v, [v_l, v_r], [table_l['b4'], table_r['b4']])
        b5 = np.interp(v, [v_l, v_r], [table_l['b5'], table_r['b5']])
        
    result = b1*np.power(tao_o, 4)
    result += b2*np.power(tao_o, 3)
    result += b3*np.power(tao_o, 2)
    result += b4*tao_o
    result += b5
    return result

def normalized_differential_const (values_dict, v, tao_o):
    # param: in:  Values dict
    # param: in:  Fractional order
    # param: in:  Normalized dead time
    # param: out: Normalized differential const

    if str(v) in values_dict:
        table = values_dict[str(v)]
        c1 = values_dict[str(v)]['c1']
        c2 = values_dict[str(v)]['c2']
        c3 = values_dict[str(v)]['c3']
        c4 = values_dict[str(v)]['c4']
        c5 = values_dict[str(v)]['c5']

    else:
        v_l = str(v)[:3]
        v_r = str(v+0.1)[:3]
        
        table_l = values_dict[v_l]
        table_r = values_dict[v_r]

        c1 = np.interp(v, [v_l, v_r], [table_l['c1'], table_r['c1']])
        c2 = np.interp(v, [v_l, v_r], [table_l['c2'], table_r['c2']])
        c3 = np.interp(v, [v_l, v_r], [table_l['c3'], table_r['c3']])
        c4 = np.interp(v, [v_l, v_r], [table_l['c4'], table_r['c4']])
        c5 = np.interp(v, [v_l, v_r], [table_l['c5'], table_r['c5']])

    result = c1*np.power(tao_o, 4)
    result += c2*np.power(tao_o, 3)
    result += c3*np.power(tao_o, 2)
    result += c4*tao_o
    result += c5
    return result
