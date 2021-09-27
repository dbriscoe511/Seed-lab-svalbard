%% Runmotorsim_SQ.m
%% Define motor parameters
Ra=1; % armaature resistance [Ohms]
Kt=.5; % motor torque constant [Nm/A]
Ke=.5; % back emf constant [Vs/rad]
J=.05; % Load inertia [Nm^2]
b=.5; % damping [Nm/s]
%% Run a Simulation
% This simulation applies a rectifed sinusoidal voltage to a DC motor model,
% with the output as the angular position in radians
% open the block diagram so it appears in the documentation when published.
% Make sure the block diagram is closed before running the publish function

open_system("motorsim_SQ")

% run the simulation

out=sim("motorsim_SQ");
%% A Plot of the results
% We see that the motor rotates in the positive direction, with some oscillations
% due to the varying input

figure
plot(out.simout)
plot(out.inputs)