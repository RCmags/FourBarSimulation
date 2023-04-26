# Four bar linkage Simulation :chart_with_upwards_trend: :triangular_ruler:
This is a simple 2D simulation of a four bar linkage written in __python 3__. 

## What it simulates
The lengths of the bars can be changed at the start of the program, as can the mass of the driving and driven bars. For simplicity, the intermediate bar that acts as a conrod is assumed to be massless. Other inputs are the initial angular velocity of the driving bar and a constant external torque acting on said bar. 

As the system reduces to a single degree of freedom, only one variable is solved for, mainly, the angle of the driving bar with respect to the horizontal. The solution to the resulting differential equation is then used to control the angle of the input bar during the animation phase of the program.

__Note__: For more information on how the program works, see the attached PDF. It explains the code and physics in much greater detail. 

## Animation
The output is an animation of the linkage mechanism rotating in the absence of damping forces (system energy is conserved). This animation can then be saved as a video that is created in the same location as the .py file. 

## Dependencies
The script requires the following libraries:

- [numpy](https://numpy.org/)
- [scipy](https://scipy.org/)
- [matplotlib](https://matplotlib.org/)

## Output
Here are examples of the output:

<p align="center">
<img src = "/images/short_bar_anim.gif" width = "35%" height = "35%"> <img src = "/images/short_graph.png" width = "35%" height = "35%">
</p>

<p align="center">
<img src = "/images/long_bar_anim.gif" width = "35%" height = "35%"> <img src = "/images/long_graph.png" width = "35%" height = "35%">
</p>
