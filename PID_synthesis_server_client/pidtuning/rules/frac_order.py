# Fractional order rule # TODO: include reference
# TODO: quitar los raise, colocarlos donde corresponde

import numpy as _np
from pidtuning.models.controller import Controller

valid_controllers = ('PID', 'PI')
valid_Ms          = ('1.4', '2.0')

PID_Ms_1_4 = {

    '1.0': {
        'a1' : 0.4305,
        'a2' : -1.0191,
        'a3' : 0.1934,
        'b1' : -0.1334,
        'b2' : 0.7935,
        'b3' : -1.6791,
        'b4' : 1.7563,
        'b5' : 0.3517,
        'c1' : 0,
        'c2' : 0,
        'c3' : 0.0145,
        'c4' : 0.3097,
        'c5' : 0.0034
    },
    '1.1': {
        'a1' : 0.4078,
        'a2' : -1.1165,
        'a3' : 0.1747,
        'b1' : -0.2472,
        'b2' : 1.3119,
        'b3' : -2.4638,
        'b4' : 2.0925,
        'b5' : 0.4297,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.0106,
        'c4' : 0.3934,
        'c5' : 0.0086
    },
    '1.2': {
        'a1' : 0.3690,
        'a2' : -1.2234,
        'a3' : 0.1594,
        'b1' : -0.1874,
        'b2' : 0.9888,
        'b3' : -1.7916,
        'b4' : 1.3695,
        'b5' : 0.7233,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.0488,
        'c4' : 0.5210,
        'c5' : 0.0097
    },
    '1.3': {
        'a1' : 0.3200,
        'a2' : -1.3277,
        'a3' : 0.1419,
        'b1' : -0.2985,
        'b2' : 1.4774,
        'b3' : -2.4395,
        'b4' : 1.4793,
        'b5' : 0.8265,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.0874,
        'c4' : 0.6697,
        'c5' : 0.0178
    },
    '1.4': {
        'a1' : 0.2707,
        'a2' : -1.4198,
        'a3' : 0.1167,
        'b1' : -0.3848,
        'b2' : 1.8259,
        'b3' : -2.8043,
        'b4' : 1.3769,
        'b5' : 0.9231,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.1642,
        'c4' : 0.9189,
        'c5' : 0.0192
    },
    '1.5': {
        'a1' : 0.2129,
        'a2' : -1.5247,
        'a3' : 0.0848,
        'b1' : -0.2933,
        'b2' : 1.2987,
        'b3' : -1.6063,
        'b4' : 0.0630,
        'b5' : 1.3279,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.2547,
        'c4' : 1.3056,
        'c5' : 0.0044
    },
    '1.6': {
        'a1' : 0.1560,
        'a2' : -1.6289,
        'a3' : 0.0443,
        'b1' : -0.0180,
        'b2' : -0.1716,
        'b3' : 1.1486,
        'b4' : -2.1477,
        'b5' : 1.7771,
        'c1' : 0.1511,
        'c2' : -0.5011,
        'c3' : 0.3403,
        'c4' : 1.5835,
        'c5' : 0.0274
    },
    '1.7': {
        'a1' : 0.0931,
        'a2' : -1.7754,
        'a3' : 0.0197,
        'b1' : 0.1862,
        'b2' : -1.1855,
        'b3' : 2.9074,
        'b4' : -3.3834,
        'b5' : 1.8803,
        'c1' : 0.0775,
        'c2' : 0.1769,
        'c3' : -1.0230,
        'c4' : 3.1938,
        'c5' : -0.0559
    },
    '1.8': {
        'a1' : 0.0329,
        'a2' : -2.0740,
        'a3' : 0.0293,
        'b1' : 0.2483,
        'b2' : -1.4872,
        'b3' : 3.3014,
        'b4' : -3.3244,
        'b5' : 1.6057,
        'c1' : -0.2495,
        'c2' : 2.1912,
        'c3' : -6.0176,
        'c4' : 7.1816,
        'c5' : -0.2569
    }
}

PID_Ms_2_0 = {

    '1.0': {
        'a1' : 0.7749,
        'a2' : -1.0170,
        'a3' : 0.3424,
        'b1' : -0.0551,
        'b2' : 0.5530,
        'b3' : -1.6274,
        'b4' : 2.2994,
        'b5' : 0.1312,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.0043,
        'c4' : 0.2696,
        'c5' : 0.0127
    },
    '1.1': {
        'a1' : 0.7148,
        'a2' : -1.1381,
        'a3' : 0.3315,
        'b1' : -0.1484,
        'b2' : 0.8988,
        'b3' : -1.9398,
        'b4' : 2.1392,
        'b5' : 0.3638,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.0256,
        'c4' : 0.3680,
        'c5' : 0.0092
    },
    '1.2': {
        'a1' : 0.6473,
        'a2' : -1.2541,
        'a3' : 0.2973,
        'b1' : -0.1026,
        'b2' : 0.6228,
        'b3' : -1.3366,
        'b4' : 1.4780,
        'b5' : 0.6518,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.1413,
        'c4' : 0.5786,
        'c5' : -0.0090
    },
    '1.3': {
        'a1' : 0.5794,
        'a2' : -1.3572,
        'a3' : 0.2440,
        'b1' : -0.1981,
        'b2' : 1.0982,
        'b3' : -2.1250,
        'b4' : 1.8162,
        'b5' : 0.6983,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.2214,
        'c4' : 0.7685,
        'c5' : -0.0171
    },
    '1.4': {
        'a1' : 0.5374,
        'a2' : -1.4250,
        'a3' : 0.1421,
        'b1' : -0.1695,
        'b2' : 0.9569,
        'b3' : -1.9021,
        'b4' : 1.4605,
        'b5' : 0.8765,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.3584,
        'c4' : 1.0178,
        'c5' : -0.0228
    },
    '1.5': {
        'a1' : 0.4291,
        'a2' : -1.5417,
        'a3' : 0.0890,
        'b1' : -0.4515,
        'b2' : 2.2932,
        'b3' : -3.9744,
        'b4' : 2.4179,
        'b5' : 0.7907,
        'c1' : 0,
        'c2' : 0,
        'c3' : -0.3831,
        'c4' : 1.3265,
        'c5' : -0.0354
    },
    '1.6': {
        'a1' : 0.3200,
        'a2' : -1.6677,
        'a3' : 0.0459,
        'b1' : -0.2851,
        'b2' : 1.3978,
        'b3' : -2.1642,
        'b4' : 0.6622,
        'b5' : 1.2727,
        'c1' : -0.0428,
        'c2' : 0.3045,
        'c3' : -0.5825,
        'c4' : 1.7790,
        'c5' : -0.0507
    },
    '1.7': {
        'a1' : 0.2143,
        'a2' : -1.8137,
        'a3' : 0.0299,
        'b1' : -0.2368,
        'b2' : 1.0478,
        'b3' : -1.2715,
        'b4' : -0.3035,
        'b5' : 1.4685,
        'c1' : -0.0855,
        'c2' : 0.6214,
        'c3' : -1.1764,
        'c4' : 2.6044,
        'c5' : -0.0789
    },
    '1.8': {
        'a1' : 0.1209,
        'a2' : -1.9973,
        'a3' : 0.0307,
        'b1' : -0.0637,
        'b2' : 0.2404,
        'b3' : 0.0352,
        'b4' : -1.1707,
        'b5' : 1.5749,
        'c1' : -0.2948,
        'c2' : 1.7942,
        'c3' : -3.4048,
        'c4' : 4.2976,
        'c5' : -0.1570
    }
}

PI_Ms_1_4 = {

    '1.0': {
        'a1' : 0.2621,
        'a2' : -1.1413,
        'a3' : 0.1132,
        'b1' : -0.2666,
        'b2' : 1.2603,
        'b3' : -1.9851,
        'b4' : 1.3775,
        'b5' : 0.5972
    },
    '1.1': {
        'a1' : 0.2023,
        'a2' : -1.2344,
        'a3' : 0.1119,
        'b1' : -0.0954,
        'b2' : 0.3558,
        'b3' : -0.3412,
        'b4' : 0.1462,
        'b5' : 0.9010
    },
    '1.2': {
        'a1' : 0.1358,
        'a2' : -1.3665,
        'a3' : 0.1165,
        'b1' : 0.1333,
        'b2' : -0.7729,
        'b3' : 1.6547,
        'b4' : -1.4179,
        'b5' : 1.3350
    },
    '1.3': {
        'a1' : 0.1051,
        'a2' : -1.3136,
        'a3' : 0.0931,
        'b1' : 0.2416,
        'b2' : -1.2558,
        'b3' : 2.4481,
        'b4' : -2.0880,
        'b5' : 1.5180
    },
    '1.4': {
        'a1' : 0.0972,
        'a2' : -1.1049,
        'a3' : 0.0547,
        'b1' : 0.2855,
        'b2' : -1.4640,
        'b3' : 2.8237,
        'b4' : -2.4983,
        'b5' : 1.6207
    },
    '1.5': {
        'a1' : 0.0862,
        'a2' : -0.8906,
        'a3' : 0.0128,
        'b1' : 0.3200,
        'b2' : -1.6858,
        'b3' : 3.2676,
        'b4' : -2.9136,
        'b5' : 1.6093
    },
    '1.6': {
        'a1' : 0.1079,
        'a2' : -0.5234,
        'a3' : -0.0534,
        'b1' : 0.0146,
        'b2' : -0.2634,
        'b3' : 1.0072,
        'b4' : -1.5748,
        'b5' : 1.1806
    }
}

PI_Ms_2_0 = {

    '1.0': {
        'a1' : 0.5014,
        'a2' : -1.1083,
        'a3' : 0.3307,
        'b1' : -0.0141,
        'b2' : 0.0858,
        'b3' : -0.2800,
        'b4' : 0.9342,
        'b5' : 0.5898
    },
    '1.1': {
        'a1' : 0.4347,
        'a2' : -1.1948,
        'a3' : 0.3038,
        'b1' : -0.0528,
        'b2' : 0.3605,
        'b3' : -0.8891,
        'b4' : 1.3041,
        'b5' : 0.6466
    },
    '1.2': {
        'a1' : 0.3388,
        'a2' : -1.3011,
        'a3' : 0.2888,
        'b1' : -0.2333,
        'b2' : 1.1647,
        'b3' : -2.0467,
        'b4' : 1.7190,
        'b5' : 0.7622
    },
    '1.3': {
        'a1' : 0.2640,
        'a2' : -1.3624,
        'a3' : 0.2487,
        'b1' : -0.1832,
        'b2' : 0.9213,
        'b3' : -1.5512,
        'b4' : 1.0636,
        'b5' : 1.0745
    },
    '1.4': {
        'a1' : 0.1954,
        'a2' : -1.3740,
        'a3' : 0.2010,
        'b1' : -0.0763,
        'b2' : 0.3398,
        'b3' : -0.2939,
        'b4' : -0.3389,
        'b5' : 1.5752
    },
    '1.5': {
        'a1' : 0.1720,
        'a2' : -1.1931,
        'a3' : 0.1081,
        'b1' : 0.1898,
        'b2' : -1.1150,
        'b3' : 2.5040,
        'b4' : -2.6974,
        'b5' : 2.1084
    },
    '1.6': {
        'a1' : 0.2614,
        'a2' : -0.7171,
        'a3' : -0.0889,
        'b1' : 0.1405,
        'b2' : -0.8445,
        'b3' : 2.0568,
        'b4' : -2.7520,
        'b5' : 2.1243
    }
}

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

        a1 = _np.interp(v, [v_l, v_r], [table_l['a1'], table_r['a1']])
        a2 = _np.interp(v, [v_l, v_r], [table_l['a2'], table_r['a2']])
        a3 = _np.interp(v, [v_l, v_r], [table_l['a3'], table_r['a3']])

    result =  a1*_np.power(tao_o, a2) + a3
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

        b1 = _np.interp(v, [v_l, v_r], [table_l['b1'], table_r['b1']])
        b2 = _np.interp(v, [v_l, v_r], [table_l['b2'], table_r['b2']])
        b3 = _np.interp(v, [v_l, v_r], [table_l['b3'], table_r['b3']])
        b4 = _np.interp(v, [v_l, v_r], [table_l['b4'], table_r['b4']])
        b5 = _np.interp(v, [v_l, v_r], [table_l['b5'], table_r['b5']])

    result = b1*_np.power(tao_o, 4)
    result += b2*_np.power(tao_o, 3)
    result += b3*_np.power(tao_o, 2)
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

        c1 = _np.interp(v, [v_l, v_r], [table_l['c1'], table_r['c1']])
        c2 = _np.interp(v, [v_l, v_r], [table_l['c2'], table_r['c2']])
        c3 = _np.interp(v, [v_l, v_r], [table_l['c3'], table_r['c3']])
        c4 = _np.interp(v, [v_l, v_r], [table_l['c4'], table_r['c4']])
        c5 = _np.interp(v, [v_l, v_r], [table_l['c5'], table_r['c5']])

    result = c1*_np.power(tao_o, 4)
    result += c2*_np.power(tao_o, 3)
    result += c3*_np.power(tao_o, 2)
    result += c4*tao_o
    result += c5
    return result


def tuning(alpha, T, K, L, Ms, ctype):
    """
    PI/PID Tunning rule for fractional order models
    # TODO: add tuning rule paper reference

    Args:
    param: in: alpha     Fractional order
    param: in: T         Time constant
    param: in: K         Proportional constant
    param: in: L         Dead time constant
    param: in: Ms        Maximum sensitivity
    param: in: ctype     Controler type ['PI','PID']

    Internal values
    * tao_o, Fractional normalized dead time
    """

    if ctype == 'PID' or ctype == 'PI':
        pass
    else:
        raise ValueError("Unknown controller")
        return False

    try:
        alpha    = float(alpha)
        # T        = T
        K        = abs(K)
        # L        = L
        # Ms       = Ms

    except Exception:
        raise ValueError("Wrong input value, tuning input error")
        return False

    # Verify alpha is in range
    if ctype == 'PI':
        alpha_range = (1.6,1.0)
    elif ctype == 'PID':
        alpha_range = (1.8,1.0)

    if alpha <= alpha_range[0] and alpha >= alpha_range[1]:
        pass
    else:
        raise ValueError(
            'Fractional order is not in range [', alpha_range[1],', ', alpha_range[0],']')
        return False

    # Calculate fractional normalized dead time
    tao_o = float(L)/(_np.power(T,1/alpha))

    if tao_o <= 2.0 and tao_o >= 0.1:
        pass
    else:
        raise ValueError('Fractional normalized dead time is not in range [0.1, 2.0]')
        return False

    if Ms == '2.0':
        if ctype == 'PID':
            values_dict = PID_Ms_2_0
        elif ctype == 'PI':
            values_dict = PI_Ms_2_0
    elif Ms == '1.4':
        if ctype == 'PID':
            values_dict = PID_Ms_1_4
        elif ctype == 'PI':
            values_dict = PI_Ms_1_4
    else:
        raise ValueError('Maximum sensitivity is not in {1.4, 2.0}')
        return False

    # Calculate results:
    kappa_p = normalized_proportional_const(values_dict, alpha, tao_o)
    tao_i = normalized_integral_const(values_dict, alpha, tao_o)
    if ctype == 'PID':
        tao_d = normalized_differential_const(values_dict, alpha, tao_o)
    else:
        tao_d = 0
    K_p = _np.divide(kappa_p, K)
    T_i = _np.multiply(tao_i, _np.power(T, _np.divide(1, alpha)))
    if ctype == 'PID':
        T_d = _np.multiply(tao_d, _np.power(T, _np.divide(1, alpha)))
    else:
        T_d = 0

    return Controller(
        ctype,   # Controller type
        Ms,      # Controller-plant sensivity
        kappa_p, # Normalized proportional constant
        tao_i,   # Normalized integral constant
        tao_d,   # Normalized differential constant
        K_p,     # Proportional constant
        T_i,     # Integral constant
        T_d,     # Differential constant
    )
