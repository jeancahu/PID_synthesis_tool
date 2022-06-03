function [z p k] = APC(k, v, wl, wh)

% cronePadula2 construye la aproximación CRONE de la transformada de
% Laplace de un integrador o derivador fraccionario; en términos de z y p,
% vectores, y k, un escalar, que corresponden respectivamente a los ceros,
% polos y ganancia de la aproximación.
% 
% El argumento de la función está constituido por k, la ganancia deseada,
% v, el orden fraccionario, y los límites superior e inferior del intervalo
% de frecuencias donde la aproximación será válida, wh y wl,
% respectivamente.

% Ya que mientras menor sea el orden fraccionario será menor el error
% introducido por la aproximación, se le resta a v el entrero inferior más
% cercano f, y se obtiene vf = v - f valor que siempre será positivo y para
% el cual se construye la aproximación. Posterioremente la función de
% transferencia obtenida se multiplica por s^f y se consigue una
% aproximación del orden deseado que introduce una desviación mucho menor
% fuera del intervalo [wl wh].
%
% Bibliografía:
% Oustaloup, A., Levron, F., Mathieu, B. y Nanot, F.M. (2000) Frequency-
%      Band Complex Noninteger Differentiator: Characterization and
%      Synthesis. IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS,I: FUNDAMENTAL
%      THEORY AND APPLICATIONS, VOL.47, NO.1, pp.25-39.

if isreal(v)
    
    % Se expande el intervalo de frecuancias una década tanto hacia arriba
    % como hacia abajo con el fin de asegurar la validez de la aproximación
    % en el intervalo de interés.
    
    %wl = wl/10;
    %wh = wh*10;
    
    % Se define el orden de la aproximación (se utliza esta línea)
    %o se comenta para trabajar con 43)
    %n=18;
    n=8;
    % Apartir de los límites wl y wh se obtiene el orden de la
    % aproximación, en este caso se consideró de aceptable el minimo más 4.
    
    %n = ceil(log10(wh/wl));%+4% se haya en conclusiones de synthesis
    
    % Se determina el nuevo orden fraccionario para la aproximación.
    f = floor(v); %redondea al valor entero inferior
    vf = v - f;
    
    % Se declaran los vectores z y p.
    
    z = zeros(1,n);
    p = zeros(1,n);
    
    % Se inicializa la obtención recursiva de los polos y los ceros.

    alpha = (wh/wl)^(vf/n);
    eta = (wh/wl)^((1-vf)/n);

    z(1) = wl * sqrt(eta);
    p(1) = z(1) * alpha;
    
    % Se obtiene los polos y los ceros en cuestión.

    for i = 2:n
        
        z(i) = p(i-1)*eta;
        p(i) = z(i)*alpha;
        
    end
    
    % Se determina la ganancia de la aproximación de forma tal que sea
    % equivalente a la ganancia deseada k.
    
    C = zpk(-z, -p, 1); % se definen los polos con parte real negativa   
    k1 = k / dcgain(C); % 
    C= k1*C;
    
    wm = sqrt(wl*wh);% sale de synthesis en la pag 4 del pdf    
    k2=(k*wm^vf)/bode(C,wm);
    k=k2*k1; % aproximación tenga ganancia unitaria, para así mantener la ganancia que se desea
             % se define la nueva k que permite obtener ganancia deseada en wm
    
    % Se agregan los polos o ceros necesarios para obtener la proximación
    % del orden deseado v.
    
    if v>0

    z = -[z zeros(1,f)];
    p = -p;
    
    else
    z = -z;       
    p = -[p zeros(1,-f)];
    
    end
    
else

   error('v es complejo')
   %G=zpk(z,p,);
   %step(G)

end
