# Maxwell Boltmann Particle Simulation in Python
This is Maxwell Boltzmann Particle Simulation implemented in Python using numpy.

Each particle only interacs with each other via elastic collision.

At the beginning, each particles are given velocity so the velocity distribution does not match the Maxwell Boltzmann distribution. 
As time passes, particles will collide with each other and the velocity distribution will change.
This velocity distribution wil then be compared with Maxwell Boltzmann distribution theory to confirm the Maxwell Botlmann Theory.

This is not a realtime simulation. Calculation will be done first and then the result will be presented as graph of particle position using Matplotlib animation.
Result can be also saved as video

# Result Example
![](https://media2.giphy.com/media/v83JXcoM1rTPD89X6d/giphy.gif)
