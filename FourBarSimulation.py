# Program Description:
# Simulate and animate the motion of four-bar linkage.
# The animation can also be stored as a video.

#--- Libraries 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint # Bring in the differential equation solver


#--- Mechanism Parameters: [constants]

# Bar lengths
A_HEIGHT = 1
C_LENGTH = 1
r_INPUT = 0.5
R_OUTPUT = 0.8

# Initial conditions [of bar r]  -Note: not all values are stable
r_ANG_INIT = 0.0
r_VEL_INIT = 0.2
r_TORQUE = 0.0
# Inertia of bars
INERTIA_r = 60
INERTIA_R = 10

#---- Simuation Parameters:

# Time interval
TIME_FINAL = 100
TIME_STEPS = 400

# Animation figures
BAR_WIDTH = 3
PIN_RADIUS = 0.05

#Plot bounds
X_BOUND = 1.5
Y_BOUND = 1.1

# Save animation as .gif 
SAVE_FIGURE = False         # True or False

#--- Output angle function:

# Position parameter [ determined whether rotation is possible ]
def sine_input( r_ang ):
   #Variables for output calculation
   h_length = np.sqrt( A_HEIGHT**2 + r_INPUT**2 
                      -2*A_HEIGHT*r_INPUT*np.sin(r_ang) )
     
   sine_term = ( ( R_OUTPUT**2 - C_LENGTH**2 + h_length**2 )/
               ( 2*R_OUTPUT*h_length ) )                     
   return sine_term


#   Global variable [angle at which bars lock]
g_lock_ang = 0
g_lock_switch = 0

#Function to calculate angle of bar R 
def output_angle( r_ang ):
 
   sine_term = sine_input(r_ang)

   if np.abs(sine_term) <= 1: 
       #Variables for output calculation   
       a_angle = np.arcsin( sine_term )

       l_angle = np.arctan( np.cos(r_ang)*r_INPUT / 
                           ( A_HEIGHT - r_INPUT*np.sin(r_ang) ) )
       #Output calculation:
       output = l_angle - a_angle
       
       #saving last non-locked angle
       global g_lock_ang
       g_lock_ang = r_ang
     
       return output
   else: 
       #Declaring bars are locked       
       global g_lock_switch
       g_lock_switch = 1
       
       return output_angle(g_lock_ang)
   #- End of function
    
#Function to limit angle of bar r if bar R is locked
def input_filter( r_ang ):
    if np.abs( sine_input(r_ang) ) > 1:
        return g_lock_ang
    else:
        return r_ang
    #- End of function


#--- Coordinates of pins:
origin = (0,0)
point_A = (0, A_HEIGHT)

def point_r(r_ang):
    x = np.cos(r_ang)*r_INPUT
    y = np.sin(r_ang)*r_INPUT
    return (x, y)

def point_R(r_ang):
    R_ang = output_angle(r_ang)
    x = np.cos(R_ang)*R_OUTPUT
    y = np.sin(R_ang)*R_OUTPUT + A_HEIGHT
    return (x, y)


#--- Linkage arrays:
link_A = [ origin, point_A ]

def link_r(r_ang):
    return [ origin, point_r(r_ang) ]

def link_R(r_ang):
    return [ point_A, point_R(r_ang) ]

def link_C(r_ang):
    return [ point_r(r_ang), point_R(r_ang) ] 


#--- Motion functions

#Mechanical advantage between bar r and bar R    
def mech_ratio(r_ang):
    R_ang = output_angle(r_ang)
    
    factor = r_INPUT*R_OUTPUT*np.sin(R_ang - r_ang)
    ratio = (A_HEIGHT*r_INPUT*np.cos(r_ang) + factor)/(
            A_HEIGHT*R_OUTPUT*np.cos(R_ang) + factor)
    
    return ratio

#Derivatives of output_angle:
def deriv_1( r_ang ):
    dx = 1e-5
    return ( output_angle(r_ang+dx) - output_angle(r_ang-dx) )/(2*dx)    

def deriv_2(r_ang):
    dx= 1e-5
    return ( output_angle(r_ang+dx) + output_angle(r_ang-dx)
            - 2*output_angle(r_ang) )/(dx**2)


#--- Solution to bar motion

def stateVector_deriv( stateVector, t ):
    #Angle of bar r
    r_ang = stateVector[0];
    
    #checking if bars locked
    if g_lock_switch == 0:
        
        #Angular velocity of bar r
        r_ang_vel = stateVector[1];
    
        #Acceleration of bar r
        r_ang_accel = ( r_TORQUE - INERTIA_R*(r_ang_vel**2)*deriv_2(r_ang)*
                       mech_ratio(r_ang) )/(INERTIA_r + INERTIA_R*
                                 deriv_1(r_ang)*mech_ratio(r_ang) )
    
    #Setting motion to zero when bars locked
    else: 
        r_ang = g_lock_ang
        r_ang_vel = 0
        r_ang_accel = 0
    
    #U[0] = position ; U[1] = velocity
    #dU[0] = velocity ; dU[1] = acceleration
    return [ r_ang_vel, r_ang_accel ]

#Defining time interval
time_array = np.linspace(0, TIME_FINAL, TIME_STEPS)

#Solving state vector
stateVector_initial = [ r_ANG_INIT, r_VEL_INIT ]
stateVector_solution = odeint(stateVector_deriv, stateVector_initial, time_array)


#--- Creating figure for plot
figure = plt.figure() 
axes = plt.axes( xlim=(-X_BOUND, X_BOUND), ylim=( -Y_BOUND + A_HEIGHT*0.5,
                                                Y_BOUND + A_HEIGHT*0.5 ) )
plt.xlabel("X position")
plt.ylabel("Y position")
plt.title("Four bar linkage")



#--- Creating patch objects [ animation figures ]:
    
    #Linkages:
bar_A = plt.Polygon( link_A , closed = None, 
                    fill = None, ec = 'blue', lw = BAR_WIDTH )

bar_r = plt.Polygon( link_r(r_ANG_INIT), closed = None, 
                    fill = None, ec = 'red', lw = BAR_WIDTH )

bar_R = plt.Polygon( link_R(r_ANG_INIT), closed = None, 
                    fill = None, ec = 'gray', lw = BAR_WIDTH )

bar_C = plt.Polygon( link_C(r_ANG_INIT), closed = None,
                    fill = None, ec = 'purple', lw = BAR_WIDTH )

    #Pins:
pin_origin = plt.Circle( origin, PIN_RADIUS, fc = 'yellow' )
pin_A = plt.Circle( point_A, PIN_RADIUS, fc = 'yellow' )
pin_r = plt.Circle( point_r(r_ANG_INIT), PIN_RADIUS, fc = 'yellow' )
pin_R = plt.Circle( point_R(r_ANG_INIT), PIN_RADIUS, fc = 'yellow' )


#--- Animation functions:
def initial_plot():

    #Linkages:
    axes.add_patch( bar_A )
    axes.add_patch( bar_r )
    axes.add_patch( bar_R )

    #Pins:
    axes.add_patch( pin_origin )
    axes.add_patch( pin_A )

    #Layering bar C before rotating pins [r and R]
    axes.add_patch( bar_C )
    axes.add_patch( pin_r )
    axes.add_patch( pin_R )
    
    return bar_A, bar_r, pin_origin, bar_R, pin_A, bar_C, pin_R, pin_r
    #Note: return order is order of image layers
 
def animate_index(i):
    #output angle
    r_ang = stateVector_solution[i,0]
    #   Filtering input if bar R is locked
    r_ang = input_filter(r_ang)

    #Linkages:
    bar_r.set_xy( link_r(r_ang) )
    bar_R.set_xy( link_R(r_ang) )
    bar_C.set_xy( link_C(r_ang) )

    #pins
    pin_r.center = point_r(r_ang) 
    pin_R.center = point_R(r_ang) 

    return bar_A, bar_r, pin_origin, bar_R, pin_A, bar_C, pin_R, pin_r
    #Note: return order is order of image layers


#--- Generating animation
anim = animation.FuncAnimation( figure, animate_index, init_func = initial_plot,
                                 frames = TIME_STEPS, interval = 40, blit = True )                             

#--- Saving animation [Remove comment to enable]
if SAVE_FIGURE:
	anim.save("fourbar.gif", writer=animation.PillowWriter(fps=5), dpi=75)  

# display
plt.show()
