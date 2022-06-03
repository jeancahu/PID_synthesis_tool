% Using CRONE Oustaloup to define Pm

fprintf("Running CRONE Oustaloup module\n")

if v<1
    [zz, pp, kk]=APC(1,-v,wl,wh); 
    mod=1/zpk(zz,pp,kk);
else
    [zz, pp, kk]=APC(1,v,wl,wh); 
    mod=zpk(zz,pp,kk);
end       
Pm=K*exp(-L*s)/(T*mod+1);

clear zz
clear pp
clear kk
clear mod
