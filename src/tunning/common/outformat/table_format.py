def print_table_results (controller_type,
                         Ms, script_syntax,
                         kappa_p, tao_i, tao_d,
                         K_p, T_i, T_d):
    if script_syntax:
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
    else:
        print(controller_type, 'Tunning results, sensibility (Ms):', Ms )
        print('R:\tNormalized proportional value:\t', kappa_p)
        print('R:\tNormalized integral value:\t', tao_i)
        if controller_type == 'PID':
            print('R:\tNormalized differential value:\t', tao_d)
        print('R:\t__________ Proportional value:\t', K_p)
        print('R:\t__________ Integral value:\t', T_i)
        if controller_type == 'PID':
            print('R:\t__________ Differential value:\t', T_d)
        print('\n')
