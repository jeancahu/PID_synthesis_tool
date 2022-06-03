function J = f_IDFOM(xns, tnorm, ynorm, tin, flagtin, opp)
s=tf('s');

% Step test
if xns(2)<1
    [z p k]=APC(1,-xns(2),0.001,1000);  %CRONE approximation
    Gmm=1/zpk(z,p,k);
else
    [z p k]=APC(1,xns(2),0.001,1000);   %CRONE approximation
    Gmm=zpk(z,p,k);
end

Gm0 = 1*exp((-(xns(3)+tin))*s)/(xns(1)*Gmm+1);
yout=step(Gm0,tnorm);

if opp==1
    for i=1:flagtin
        tinvec(i)=tnorm(i);
        ynorm2(i)=ynorm(i);
        yout2(i)=yout(i);
    end
    J= trapz(tnorm,abs(yout-ynorm))-trapz(tinvec, abs(yout2-ynorm2));
else
    J= trapz(tnorm,abs(yout-ynorm));
end
% Cost function
