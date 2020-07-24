  %{
Joseph Lupton
Inverted Pendulum
%}
clc 
clear
close all

i_phi = .5; %initial angle in degrees
i_x = 0;

Stall_T = 20; %IN-OZ
Nom_V = 12; %V 12
Wheel_R = 2; %in
v = 16.8; %starting voltage
convFact = (100*Nom_V*Wheel_R*16)/(v*Stall_T); %conversion factor from input to duty cycle(%)
maxSig = 145; %Change input saturation

load('sysModel.mat');

[A, B, C, D] = ssdata(sys_ss);
%[poleVec,poles] = eig(A);

co = ctrb(sys_ss);
if (rank(co) ~= max(size(A)))
    fprinf('System is not controllable');
    return;
end

Q = C'*C;
Q(1,1) = 1; %Weight on cart position
Q(3,3) = 1; %Weight on rod angle
R = 1000; %Weight on Controls
[K] = lqr(A,B,Q,R);
%disp(K);
[controlPoleVec,Controlpoles] = eig(A-B*K);
%disp(controlPoleVec);

i_phi = i_phi/360*2*pi();

ic = [i_x, 0, i_phi, 0]'; %for simulink

sim('SysModel')

%extract data
t = sim_X.time;
x = sim_X.signals.values(:,1);
x_dot = sim_X.signals.values(:,2);
phi = sim_X.signals.values(:,3);
phi_dot = sim_X.signals.values(:,4);
u1 = sim_U.signals.values(:,1);
DC = u1.*convFact; %Conversion to dutycycle from force

%All Plots
%{
figure
subplot(5,1,1)
plot(t, x, 'LineWidth', 3)
title('System Response')
grid on
legend('x')

subplot(5,1,2)
plot(t, x_dot, 'LineWidth', 3)
grid on
legend('x dot')

subplot(5,1,3)
plot(t, phi, 'LineWidth', 3)
grid on
legend('phi')

subplot(5,1,4)
plot(t, phi_dot, 'LineWidth', 3)
grid on
legend('phi dot')

subplot(5,1,5)
plot(t, DC, 'LineWidth', 3)
grid on
legend('Input')
%}

%Position Plots
%%{
figure
subplot(3,1,1)
plot(t, x, 'LineWidth', 3)
title('System Response')
grid on
legend('x')

subplot(3,1,2)
plot(t, phi, 'LineWidth', 3)
grid on
legend('phi')

subplot(3,1,3)
plot(t, DC, 'LineWidth', 3)
grid on
legend('Duty Cycle')
%}












