%El siguiente programa brinda la facilidad de generar los distintos
%elementos necesarios para la obtención del modelo fraccional, así como 
%el modelo final y un conjunto de figuras relacionadas a las simulaciones
%para obtener el modelo buscado.

file_id = fopen(output_path+"identool_results.m", "wt");

%::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
global To vo Lo Ko ynorm unorm tnorm long tin tmax tu     % se definen variables globales

%:::::::::::::::Carga de datos y asignaciones:::::::::::::::::   

carga=load(output_path+"step_response.txt"); % se cargan los datos del .txt
t=carga(:,1);            % se crean vectores con las columnas de
u=carga(:,2);            % de tiempo, señal de control y salida del .txt
y=carga(:,3);            % de la curva de reacción
long=length(t);          % se asigna a long la cantidad de datos del vector t

fprintf('\nEl modelo óptimo está siendo calculado, espere por favor...')

%:::::::::::::::::Obtención ganancia estática:::::::::::::::::::::::::::::::
inicio=tic;

% los valores del archivo de datos, debe tener t,y,u de la misma extensión
sample=7;                        %valor para trabajar los datos con ruido y sacar un promedio
Uo=mean(u(1:sample));            %se sacan los promedios para                          
Uf=mean(u(long-sample+1:long));  %obtener los valores para la ganancia
Yo=mean(y(1:sample));            % limpiando de ruido
Yf=mean(y(long-sample+1:long));            
Ko=(Yf-Yo)/(Uf-Uo);              % la fórmula común de ganancia

%::::::::::::%normalización de param::::::::::::::::::::

ynorm=(y-Yo)./(Yf-Yo);       %vector de salida normalizado
unorm=(u-Uo)./(Uf-Uo);       %vector de entrada (escalón) normalizado
tnorm=t-min(t);              %Normalización del tiempo (se hace así porq podría haber)
ymax=max(ynorm);             %empezado el muestreo en t!=0


%:::::::::Determinación del tiempo de escalón::::::::::::::::
cont=1;  
flagtin=0;
%hace la función de bandera
while cont<long
    if unorm(cont+1)>unorm(cont) || unorm(cont+1)<unorm(cont)
        tin=tnorm(cont);
        flagtin=cont;        %obtiene la posición de tin en el vector
        cont=long;
    else
        cont=1+cont;
    end
end


%:::::::::::::Obtención de los valores iniciales:::::::::::::::::::::::::
%::::::::::::::Datos para valor inicial de T y L:::::::::::::::::::::::::::::::

m1=1;            %inicialización de variable
while m1<long            
    if ynorm(m1)>0.632*ynorm(long)       %obtención del punto al 63.2% del yinf
        t63=tnorm(m1);            %Tiempo al 63.2% del valor máximo de y
        y63=ynorm(m1);
        m1=long;
    else
        m1=m1+1;
    end
end

m2=1;
while m2<long
    if ynorm(m2)>0.03*ynorm(long) && tnorm(m2)>tin       %obtención del punto al 63.2% del yinf
        t3=tnorm(m2);
        y3=ynorm(m2);             %Tiempo al 3% del valor máximo de y
        m2=long;
    else
        m2=m2+1;
    end
end

m3=1;
while m3<long
    if ynorm(m3)>0.9*ynorm(long)      %obtención del punto al 63.2% del yinf
        t90=tnorm(m3);            %Tiempo al 90% del valor máximo de y
        y90=ynorm(m3);
        m3=long;
    else
        m3=m3+1;
    end
end

%::::::::::::::Valor inicial de v:::::::::::::::::::::::::::::::
v=0;
tt=t63/t90;
Mp=(ymax-ynorm(long))/ynorm(long);   %sobrepico máximo para el caso de respuesta subamortiguada
if (ymax>ynorm(long))        %parte del código para encontrar el punto inicial de v en base a resultados previos
    syms v;
    v1 = (1.4182+sqrt( (-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    v2 = (1.4182-sqrt( (-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    if isreal(v1) && isreal(v2)
        if (v1>=1 && v1<=3)
            v0=v1;
        else
            v0=v2;
        end
    end
elseif (tt>=0 && tt<=0.45)
    open('t63t90.fig');
    fprintf('\nIntroduzca el valor de v para t63/t90= %1.4d\n',tt);
    v0=input('\nv=');
    %v0=-P(2)/(3*P(1))-(((-P(2)^2+3*P(1)*P(3))*2^(1/3))/(3*P(1)*(-2*P(2)^3+9*P(1)*P(2)*P(3)-27*P(1)^2*P(4)+sqrt(4*(-P(2)^2+3*P(1)*P(3))^3+(-2*P(2)^3+9*P(1)*P(2)*P(3)-27*P(1)^2*P(4))^2)^(1/3))))+(-2*P(2)^3+9*P(1)*P(2)*P(3)-27*P(1)^2*P(4)+sqrt(4*(-P(2)^2+3*P(1)*P(4))^3+(-2*P(2)^3+9*P(1)*P(2)*P(3)-27*P(1)^2*P(4))))^(1/3)/(32^(1/3)*P(1));
else
    v0=1;  %PARA CONSTANTES DE TIEMPO MUYY GRANDES, EL SISTEMA NO FUNCIONA
end

%::::::::::::Determino la cantidad de cruces por 1::::::::::
if v0>1.3       %este dato solo se calcula si se introduce un FT o un MVE
    cont3=1;
    totalosc=0;
    while cont3<long
        if ynorm(cont3)<1 && ynorm(cont3+1)>1
            totalosc=totalosc+1;
            cont3=cont3+1;
        else
            cont3=cont3+1;
        end
    end
end
%:::::::::::::::::::::Asignación de L0:::::::::::::::::::::::
L0=t3-tin;
%::::::::::::Algoritmo para valor inicial de T0::::::::::::::::::

%::::::::::::Cálculo del tiempo de ascentamiento:::::::::::  
if v0>=1.1525
    ma=long;
    while ma>1
        if (ynorm(ma)>=1.05 || ynorm(ma)<=0.95)   
            ta=tnorm(ma);                         %Tiempo de ascentamiento
            ya=ynorm(ma);
            ma=1;
        else
            ma=ma-1;
        end
    end
end

if v0>=1.4349 && totalosc>=2
    %::::::::::::::::Tiempo de oscilación:::::::::::::::::::
    
    os=1;     %tiempo de oscilación para que esto aplique, debe ser mayor a 1
    while os<long
        if ynorm(os)>=1  
            tu1=tnorm(os);            
            yu1=ynorm(os);
            temp1=os;
            os=long;
        else
            os=os+1;
        end
    end
    
    os=temp1;
    while os<long       
        if ynorm(os)<=1  
            tu2=tnorm(os);            
            yu2=ynorm(os);
            os=long;
        else
            os=os+1;
        end
    end
    
    tu=tu2-tu1;         %obtención del medio periodo

    %::::::::::::::Condiciones para la asignación de T0::::::::::
    diff=0.05;
    tuT0=0;
    while tuT0<tu
        [zT0 pT0 kT0] =APC(1, v0, 0.001, 1000);
        MT0=zpk(zT0,pT0,kT0);         
        MMT0=1/(diff*MT0+1);
        [yT0,tT0]=step(MMT0,tnorm); 
        longT0=length(yT0);

        %Cálculo de tuT0
        os=1; 
        while os<longT0
            if yT0(os)>=1  
                tu1T0=t(os);            
                yu1T0=y(os);
                temp1=os;
                os=longT0;
            else
                os=os+1;
            end
        end
        
        os=temp1;
        while os<longT0      
            if yT0(os)<=1  
                tu2T0=t(os);            
                yu2T0=y(os);
                os=longT0;
            else
                os=os+1;
            end
        end
        
        tuT0=tu2T0-tu1T0;%obtención del medio periodo
        
        %condición de verificación 
        if tu<=tuT0
            T0=diff;     %asignación del valor de T0
        else
            diff=0.05+diff;
        end
    end

else
    T0=(t63-(tin+L0))^v0;
end

%:::::::Fase de obtención de modelo inicial::::::::::::::::::

%Modelo a utilizar
[z0 p0 k0]=APC(T0,v0,0.001,1000);  %se realiza la aproximación
Gmm=zpk(z0,p0,k0);                   %respecto a los valores iniciales
Gm0 = 1*exp(-(L0+tin)*s)/(Gmm+1);             %Se defini el modelo inicial para 
ym0=step(Gm0,tnorm);                            % establecer las tolerancias en la  
Tolf=trapz(tnorm,abs(ym0-ynorm))*1e-7;          %optimización (Tolx y Tolf).
Tolx=norm([T0 v0 L0])*1e-7;   

%::::::::::::::::::::Optimización:::::::::::::::::::::::::::

%se establecen las opciones para llevar a cabo la optiización
options=optimset('MaxIter',200, 'MaxFunEvals',1000,'Algorithm','active-set','TolFun',Tolf,'TolX',Tolx,'Display','off');

x0=[T0 v0 L0];      %Parámetros iniciales y comando de optimización con el rango de evaluación
costfun = @(xns)f_IDFOM(xns, tnorm,ynorm, tin,flagtin,1);
[xns,IAEns]=fmincon(costfun,x0,[],[],[],[], x0*(1-0.9),x0*(1+0.9),[],options);

To=xns(1);       %Constante de tiempo 
vo=xns(2);       %Orden fraccional
Lo=xns(3);       %Tiempo muerto


%::::::::Ajuste de ganancia estática para v<1::::::::::::::::
if vo<1
    [zo po koo]=APC(To,vo,0.001,1000);
    G= zpk(zo,po,koo);
    kadj=1+dcgain(G);
    Ko1=kadj*Ko;
    Ka=Ko;        %así queda guardado Ko 
end
%::::::::::Se forma el modelo final:::::::::::::::::::::::::
tmax=max(tnorm);
[zo po koo]=APC(To,vo,0.001,1000);
Gm= zpk(zo,po,koo);
if vo<1
    Gmo=Ko1*exp(-(Lo+tin)*s)/(Gm+1);
else
    Gmo=Ko*exp(-(Lo+tin)*s)/(Gm+1);
end
ym=step(Gmo,tnorm);

%::::::Cálculo del error con el modelo completo::::::::::::::::::
tuin=Yo/Ko;
ttfin=2*tmax;
if length(zo)==8                   %caso para un modelo con v<1
    zo(9)=0;
    po(9)=0;
    kpp=koo;
else
    po(9)=-1000;              %caso en el cual el modelo tiene un 1<=v<=2
    kpp=koo/0.001;
end

Delta_t=t(2)-t(1);

opt=simset('solver','ode45','SrcWorkspace','Current'); %se establecen los datos necesarios para la simulación
%se da el comando de simulación y se asignan los vectores según el mdl
[ttout,xxout,yyout]=sim('symulink_identool_error_model',(0:Delta_t:ttfin),opt);

ln=length(ttout);
for i=1:ln
    if ttout(i)==tmax-tin
        pos=i;                  
        for i=1:long
            ynew(i)=yyout(pos);
            tnew(i)=ttout(pos)-tmax+tin;
            pos=pos+1;
        end
        break
    end
end

%Corrección del vector debido a errores de redondeo (se introduce offset)
offset=ynew(1)-Yo;
for i=1:long
    ynew(i)=ynew(i)-offset;
end

ynew=transpose(ynew);
tnew=transpose(tnew);

%   Cálculo del error utilizando aproximación trapezoidal
%Señales originales
IAEns2=0;
for i=flagtin:1:long-1%Variable flag_tin se define en línea 90;
    IAEns2=IAEns2+((abs(ynew(i)-y(i))+abs(ynew(i+1)-y(i+1)))*Delta_t/2);   %ynorm          
end

%Señales normalizadas
error=0;
for i=flagtin:1:long-1%Variable flag_tin se define en línea 90;
    error=error+((abs(ym(i)/Ko-ynorm(i))+abs(ym(i+1)/Ko-ynorm(i+1)))*Delta_t/2);   %ynorm          
end
%:::::::::::::::::::Muestra de resultados::::::::::::::::::::::::::::
%:::::::Plot con los parámetros iniciales::::::::::::::::
[zin pin kin]=APC(T0,v0,0.001,1000);
Gin= zpk(zin,pin,kin);
if v0 < 1
    K01=1+dcgain(Gin);    
    Gin0=K01*Ko*exp(-(L0+tin)*s)/(Gin+1);
else
    Gin0=Ko*exp(-(L0+tin)*s)/(Gin+1);    
end
yin=step(Gin0,tnorm);

for i=1:flagtin
    tinvec(i)=tnorm(i);
    ynorm2(i)=ynorm(i);
    yin2(i)=yin(i); 
end
Scr0= trapz(tnorm,abs(yin/Ko-ynorm))-trapz(tinvec,abs(yin2/Ko-ynorm2));  %Función objetivo

%:::::::::Impresión de parámetros:::::::::::::::::::::::::::::::::

fprintf('\nParámetros del modelo inicial:\n\n')
if vo < 1
    if (Ko1/floor(Ko1))~=1
        fprintf('  K0\t= %4.2d\n',Ko1)
    else
        fprintf('  K0\t= %4.1d\n',Ko1) 
    end
else
    if (Ko/floor(Ko))~=1
        fprintf('  K0\t= %4.2d\n',Ko)
    else
        fprintf('  K0\t= %4.1d\n',Ko) 
    end
end
if (L0/floor(L0))~=1
    fprintf('  L0\t= %1.2d\n',L0)
else
    fprintf('  L0\t= %1.1d\n',L0) 
end
if v0==1
    fprintf('  v0\t= %1.1d\n',v0)    
else
    fprintf('  v0\t= %1.2d\n',v0)
end
if (T0/floor(T0))~=1
    fprintf('  T0\t= %1.2d\n',T0)
else
    fprintf('  T0\t= %1.1d\n',T0) 
end
fprintf('  Jla0\t= %1.2d\n',Scr0)

%% Modelo encontrado, parámetros óptimos:

fprintf(file_id,'v=%.20f;',vo)
fprintf(file_id,'T=%.20f;',To)
if vo < 1
    fprintf(file_id,'K=%.20f;',Ko1)
else
    fprintf(file_id,'K=%.20f;',Ko)
end
fprintf(file_id,'L=%.20f;',Lo) 
fprintf(file_id,'  %% model_calculated_values\n')
