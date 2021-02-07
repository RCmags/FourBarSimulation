# Four bar linkage Simulation
This is a simple 2D simulation of a four bar linkage. The lengths of the bars can be changed at the start of the program, as can the mass of the driving and driven bars. For simplicity, the intermiate bar that acts as a conrod is assumed to be massless. Other inputs are the initial angular velocity of the driving bar and a constant external torque acting on said bar. 

As the system reduces to a single degree freedom, only one variable is solved for, mainly, the angle of the driving bar with respect to the horizontal. The solution to the resulting differential equation is then used to control the angle of the input bar during the animation phase of the program. 

The output is a canvas animation of the linkage mechanism rotating under the absense damping forces (System energy is conserved). This animation can then be saved as a video that is created in the same location as the .py file. 

NOTE: This was written in Python 2. 
