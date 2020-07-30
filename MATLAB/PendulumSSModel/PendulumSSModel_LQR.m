  %{
Joseph Lupton
Inverted Pendulum
%}
clc 
clear
close all

mc = 2.15; %cart mass (kg)
mp = 0.0227; %pendulum mass (kg)
l = .04572; %Half rod length (m)
b = 0%.02548; %damping coeff/coeff of friction
g = 9.81; %gravity const
v = 14.7; %starting voltage
Kv = .0559; %(Conversion from Volts to Newtons)


I = mp*((2*l)^2)/3; %moment of intertia

p = I*(mc+mp)+mc*mp*l^2; %denominator for the A and B matrices

A = [0                 1                 0                 0;
     0          -(I+mp*l^2)*b/p    (mp^2*g*l^2)/p          0;
     0                 0                 0                 1;
     0            -(mp*l*b)/p      mp*g*l*(mc+mp)/p        0];
 
B = [        0;
       Kv*(I+mp*l^2)/p;
             0;
        Kv*mp*l/p];
    
C = [1 0 0 0;
     0 0 1 0];
 
D = [0;
     0];
 
states = {'x' 'x_dot' 'phi' 'phi_dot'};
inputs = {'u'};
outputs = {'x'; 'phi'};

sys_ss = ss(A,B,C,D,'statename',states,'inputname',inputs,'outputname',outputs);

%poles = eig(A)  %{0, 0, 3.0404, -3.0404}, Unstabe in open loop
%co = ctrb(sys_ss);
%controllability = rank(co) %Controllabiity = 4, system is controllable


%%% LQR %%%
Q = C'*C;
Q(1,1) = 100;
Q(3,3) = 500
R = 1;
K = lqr(A,B,Q,R)

Ac = [(A-B*K)];
Bc = [B];
Cc = [C];
Dc = [D];

states = {'x' 'x_dot' 'phi' 'phi_dot'};
inputs = {'r'};
outputs = {'x'; 'phi'};

sys_cl = ss(Ac,Bc,Cc,Dc,'statename',states,'inputname',inputs,'outputname',outputs);

t = 0:0.01:10;
r =zeros(size(t));

figure(1)
[y,t,x]=initial(sys_cl,[0,0,0.075,0],t);
[AX,H1,H2] = plotyy(t,y(:,1),t,y(:,2),'plot');
set(get(AX(1),'Ylabel'),'String','cart position (m)')
set(get(AX(2),'Ylabel'),'String','pendulum angle (radians)')
title('Step Response with LQR Control')

figure(2)
force = sum(K.*x,2);
plot(t,force)

save('sysModelLQR.mat', 'sys_ss', 'sys_ss')

