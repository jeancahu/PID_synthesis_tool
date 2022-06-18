# Django based Webapp for PID Control Tuning

A responsive website for PID controllers tuning using modern tuning techniques, fractional calculus and opensource software to run identiication routines for raw process data.
This project goal is to allow most of the mobile devices to approach controller parametes even with their default hardware limitations switching the computation load to the cloud,
this makes low stats computers able to display good aproximations and simulations anywhere they are needed.

The project includes the features below.
- Raw process data fractional order modeling by IDFOM identification rule (Guevara et al. 2015)
- Tune rule for PI/PID controller 0dol through FOMRoT method (Meneses et al. 2019)
- Close-loop simulations and ploting on Plotly library for Python
