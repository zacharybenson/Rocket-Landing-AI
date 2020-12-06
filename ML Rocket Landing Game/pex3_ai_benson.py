# ---------------------------------------------------------------------
# PEX 3 Rocket AI
# Author:  YOUR NAME GOES HERE
# Course: CS110Z, Spring 2020
# ---------------------------------------------------------------------
import pythonGraph, random, pex3_helper

# --------------------------------------------------------------
# This line starts the genetic algorithm
# Parameters (in order)
#   1.  Number of "AIs" that can survive each generation
#   2.  Number of children AIs that can be produced
#   3.  Max horizontal velocity
#   4.  Max vertical velocity
# --------------------------------------------------------------
pex3_helper.initialize_genetic_algorithm(2, 1, 10.0, 10.0)

# --------------------------------------------------------------
# This line sets the AI you want to submit to the competition
# When you are done with the PEX, uncomment this line and
# replace the parameters with the values of your "best" AI
# --------------------------------------------------------------
pex3_helper.use_ai_configuration(.18, .02, 4.57, .09)


# --------------------------------------------------------------
# Returns the Name of the Student
# --------------------------------------------------------------
def get_student_name():
    return "Zachary Benson"


# --------------------------------------------------------------
# Runs the AI
# --------------------------------------------------------------
def run_autopilot(WINDOW_WIDTH,run_number, rocket_x, rocket_y, Vrocket_x, Vrocket_y, rocket_width, boat_x, boat_y, boat_width):
   
   #Gets the parameters from the genetic algorithm
    ai_parameters = pex3_helper.get_ai(run_number)
   
    #Sets variables to return values
    Max_Y_Velocity = ai_parameters[3]
    Thrust_Amount_Y = ai_parameters[1]
    Max_X_Velocity = ai_parameters[2]
    Thrust_Amount_Y = ai_parameters[0]
   
   # This tuple tells your simulation which thrusters to fire
    # The first number is the left thruster, the second is the right, and the third is up
    Vrocket_y_max = 7
    Vrocket_y_amount = -.5
    
    Vrocket_x_max = 9
    Vrocket_x_min = -10
    Vrocket_x_amount = .5
        
    rocket_boost_right = 0
    rocket_boost_left = 0
    rocket_boost_up = 0
    
    Max_fuel = 500

    
    if Vrocket_y >= Vrocket_y_max:
        rocket_boost_up = .8
        
    if rocket_x < boat_x:
        if Vrocket_x < Vrocket_x_max:
            rocket_boost_right = .6
        else:
            rocket_boost_left = -.3
   
    if rocket_x > boat_x:
        if Vrocket_x > Vrocket_x_min:
            rocket_boost_left = -.6
        else:
            rocket_boost_right = .3
            
    if rocket_y > boat_y - 100:
        if rocket_x < boat_x - 50 or rocket_x > boat_x + 50 :
            rocket_boost_up = 1

    
    
    return (rocket_boost_left,  rocket_boost_right, rocket_boost_up)