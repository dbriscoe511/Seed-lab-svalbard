%% RunPI_controller.m
%% Define motor parameters
Ra=1; % armaature resistance [Ohms]
Kt=1; % motor torque constant [Nm/A]
Ke=.5; % back emf constant [Vs/rad]
J=.05; % Load inertia [Nm^2]
b=.5; % damping [Nm/s]

%% Run a Simulation
% This simulation applies a rectifed sinusoidal voltage to a DC motor model,
% with the output as the angular position in radians
% open the block diagram so it appears in the documentation when published.
% Make sure the block diagram is closed before running the publish function

open_system("PI_controller")

out=sim("PI_controller");
%% A Plot of the results
% We see that the motor rotates in the positive direction, with some oscillations
% due to the varying input

figure

plot(out.Position)