def print_table_results (controller_type,
                         Ms, script_syntax,
                         kappa_p, tao_i, tao_d,
                         K_p, T_i, T_d):
    if script_syntax == 'm_code':
        controller = \
            str(controller_type)+'_Ms_'+str(Ms).replace('.','_')
        print(controller+'_kappa_p='+str(kappa_p)+';')
        print(controller+'_tao_i='+str(tao_i)+';')
        if controller_type == 'PID':
            print(controller+'_tao_d='+str(tao_d)+';')
        print(controller+'_K_p='+str(K_p)+';')
        print(controller+'_T_i='+str(T_i)+';')
        if controller_type == 'PID':
            print(controller+'_T_d='+str(T_d)+';')

    elif script_syntax == 'json':
        print("{\n\t'type':",'"'+controller_type+'",',
              "\n\t'ms':",'"'+str(Ms)+'",',
              "\n\t'n_kp':", str(kappa_p)+',',
              "\n\t'n_ti':", str(tao_i)+',',
              "\n\t'n_td':", str(tao_d)+',',
              "\n\t'kp':", str(K_p)+',',
              "\n\t'ti':", str(T_i)+',',
              "\n\t'td':", str(T_d),
              "\n}"
        )

    elif script_syntax == 'human_readable':
        print(controller_type, 'Tunning results, sensibility (Ms):', Ms,
              '\nR:\tNormalized proportional value:\t', kappa_p,
              '\nR:\tNormalized integral value:\t', tao_i)
        if controller_type == 'PID':
            print('R:\tNormalized differential value:\t', tao_d)
        print('R:\t__________ Proportional value:\t', K_p,
              '\nR:\t__________ Integral value:\t', T_i)
        if controller_type == 'PID':
            print('R:\t__________ Differential value:\t', T_d)
        print('\n')

    else:
        print(controller_type)
        print(Ms)
        print(kappa_p)
        print(tao_i)
        print(tao_d)
        print(K_p)
        print(T_i)
        print(T_d)
