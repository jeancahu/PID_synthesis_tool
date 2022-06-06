%% IDFOM for Octave variation, uses padé delay approximation instead exp()


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

try
  if (version_info.Name=="MATLAB")
    Gm0 = 1*exp((-(xns(3)+tin))*s)/(xns(1)*Gmm+1); % Define the tf for MATLAB
  end
catch ME
  %% Octave PADE delay approximation
  [pade_num, pade_den] = padecoef((xns(3)+tin),18);
  pade_delay=tf(pade_num,pade_den);
  Gm0 = 1*pade_delay/(xns(1)*Gmm+1);
end

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
