function J = f_IDFOM(xns, tnorm, ynorm, tin,flagtin,opp)
s=tf('s');
%:::::::::::::::::Prueba escalón:::::::::::::::::::::::::::::::::

    [z p k]=APC(xns(1),xns(2),0.001,1000);   %Aproximación de CRONE
    
    Gmm=zpk(z,p,k); 
    Gm0 = 1*exp((-(xns(3)+tin))*s)/(Gmm+1); 
    kadj2=1;
    if xns(2) < 1
    kadj2=1+dcgain(Gmm);   
    end
    Gm0 = kadj2*exp((-(xns(3)+tin))*s)/(Gmm+1); 
    yout=step(Gm0,tnorm);
    
    if opp==1
     for i=1:flagtin
      tinvec(i)=tnorm(i);
      ynorm2(i)=ynorm(i);
      yout2(i)=yout(i); 
     end
     J= trapz(tnorm,abs(yout-ynorm))-trapz(tinvec,abs(yout2-ynorm2));  %Función objetivo
    else
     J= trapz(tnorm,abs(yout-ynorm));
    end

%::::::::::::::::::::Función de costo::::::::::::::::::::::::::::

