%{
Script for Processing Inverted Pendulum Encoder Data
%}

%%Variables
wheelRadius = 2 * 25.4; %Wheel radius in mm

%%Read data
fid = fopen("../Data/EncoderData.txt",'rt');
data = textscan(fopen, '%f');

angle = data(1:2:end,:);
time = data(2:2:end,:);

position = wheelRadius * angle;

velocity = zeroes(size(position),1);
acceleration = zeroes(size(position),1);

%%Centered Difference derivative calculations
for i=1:1:size(position)-1
    velocity(i) = (position(i+1) - position(i-1)) / (time(i+1) - time(i-1));
    acceleration(i) = (position(i+1) - 2*position(i) + position(i-1)) / ((time(i+1) - time(i)) * (time(i) - time (i-1)));
end
    
%%Plot data
figure 1:
plot(time, position);
title('Cart Position');
xlabel('Time (s)');
ylabel('Position(m)');

figure 2:
plot(time, velocity);
title('Cart Velocity (Centered)');
xlabel('Time (s)');
ylabel('Velocity(m/s)');

figure 3:
plot(time, acceleration);
title('Cart Acceleration (Centered)');
xlabel('Time (s)');
ylabel('Acceleration(m/s^2)');

figure 4:
plot(velocity, acceleration);
title('Cart Velocity vs Acceleration (Centered)');
xlabel('Time (s)');
ylabel('Velocity(m/s)');