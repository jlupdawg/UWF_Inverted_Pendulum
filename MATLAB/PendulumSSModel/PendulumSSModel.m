  %{
Joseph Lupton
Inverted Pendulum
%}
clc 
clear
close all

mc = 4.425; %cart mass (lbs)
mp = 0.05; %pendulum mass (lbs)
l = 1.5; %Half rod length (ft)
b = 0.1; %damping coeff
g = 32.2; %gravity const
v = 16.8; %starting voltage


I = mp*((2*l)^2)/3; %moment of intertia

p = I*(mc+mp)+mc*mp*l^2; %denominator for the A and B matrices

A = [0      1              0           0;
     0 -(I+mp*l^2)*b/p  (mp^2*g*l^2)/p   0;
     0      0              0           1;
     0 -(mp*l*b)/p       mp*g*l*(mc+mp)/p  0];
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

save('sysModel.mat', 'sys_ss', 'sys_ss')