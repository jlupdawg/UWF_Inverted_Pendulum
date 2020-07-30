  %{
Brendon Ortolano
Inverted Pendulum - Metric Units
7/23/2020
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


I = mp*((2*l)^2)/3; %moment of intertia

p = I*(mc+mp)+mc*mp*l^2; %denominator for the A and B matrices

A = [0                 1                 0                 0;
     0          -(I+mp*l^2)*b/p    (mp^2*g*l^2)/p          0;
     0                 0                 0                 1;
     0            -(mp*l*b)/p      mp*g*l*(mc+mp)/p        0]
 
B = [     0;
     (I+mp*l^2)/p;
          0;
        mp*l/p];
    
C = [1 0 0 0;
     0 0 1 0];
 
D = [0;
     0];
 
states = {'x' 'x_dot' 'phi' 'phi_dot'};
inputs = {'u'};
outputs = {'x';'phi'};

sys_ss = ss(A,B,C,D,'statename',states,'inputname',inputs,'outputname',outputs);

save('sysModelPID.mat', 'sys_ss', 'sys_ss')

tspan = 0:.1:10;
y0 = [0; 0; 0; 5];
[t,y] = ode45(@(t,y)cartpend(y,m,M,L,g,d,0),tspan,y0);

for k=1:length(t)
    drawcartpend(y(k,:),m,M,L);
end