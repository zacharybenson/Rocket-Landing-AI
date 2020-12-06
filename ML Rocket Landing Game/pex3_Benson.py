# ---------------------------------------------------------------------
# Rocket Landing Simulator
# Gate Check: 4
# Course: CS110Z, Spring 2020
# ---------------------------------------------------------------------
import pythonGraph, random, math, time
import pex3_ai_benson
import pex3_helper
# CONSTANTS
WINDOW_WIDTH  = 1800
WINDOW_HEIGHT = 800
# Performance Variables
fuel_consumed = 0
crashes = 0
landings = 0
score = 0
max_score  = 0
# Simulation Variables
time_elapsed = 0
AI_run_allowed = 5
AI_run_count = 0

# Terrain
ground_height = 0
ground_width = 0
water_height = 0
ground_heights = []
water_heights = []
# Rocket

Vrocket_x = 0
Vrocket_y = 0
rocket_height = 50
rocket_width = 50
rocket_boost = True
rocket_boost_up = 0.0
rocket_boost_right = 0.0
rocket_boost_left = 0.0
gravity = .08

rocket_x = 0
rocket_y = 0 + rocket_height
rocket_left_side = 0
rocket_right_side = 0
rocket_ref = rocket_y+rocket_height
        

# Boat (i.e., Landing Pad)
boat_x = 0
boat_y = 0
Vboat_x = 0
boat_width  = 120
boat_height = round(WINDOW_HEIGHT/20,0)
boat_max = int(WINDOW_WIDTH - boat_width  )
boat_left_side = 0
boat_right_side = 0

# --------------------------------------------------------------
# Initializes the Simulation
# --------------------------------------------------------------
def initialize_simulation(generate_new_scenario):
    global time_elapsed
   
    initialize_terrain(generate_new_scenario)
    initialize_boat(generate_new_scenario)
    initialize_rocket(generate_new_scenario)

# --------------------------------------------------------------
# Initializes the Terrain
# --------------------------------------------------------------
def initialize_terrain(generate_new_scenario):
    global ground_width, ground_height, water_height, terrain_height, SCREEN_WIDTH, SCREEN_HEIGHT
   
    terrain_height = []
    ground_heights.clear()
    water_heights.clear()
    
    #Creates random water and land height
    ground_width = random.randint(50, WINDOW_WIDTH * (.20))
    ground_height = random.randint(50,WINDOW_HEIGHT *(.30))
    water_height = random.randint(10, ground_height )
    for x in range(0,WINDOW_WIDTH):
        
        #Assigns the height dimmensions for the land within the land with
        if x in range(ground_width):
            ground_heights.append(ground_height)
            terrain_height.append(ground_height)
        
        #Assigns the height dimmensions for the water within the water width
        else:
            water_heights.append(water_height)
            terrain_height.append(ground_height)


# --------------------------------------------------------------
# Initializes the Boat
# --------------------------------------------------------------
def initialize_boat(generate_new_scenario):
    global boat_x ,boat_y,Vboat_x,boat_height,boat_width
    
    #Game play music
    pythonGraph.play_music('metroid03.mp3')
    time_elapsed = 0
    #Creates boat reference at bottom and right
    boat_x  =  random.randint(WINDOW_WIDTH - ground_width, WINDOW_WIDTH)-boat_width
    boat_y = WINDOW_HEIGHT - water_height - boat_height
    vlist = [-4,-3,-2,2,3,4]
    Vboat_x = random.choice(vlist)
# --------------------------------------------------------------
# Initializes the Rocket
# --------------------------------------------------------------
def initialize_rocket(generate_new_scenario):
     global rocket_boost,rocket_x,  rocket_y, Vrocket_x, Vrocket_y, rocket_height, rocket_width, ground_width, ground_height, water_height, terrain_height, SCREEN_WIDTH, SCREEN_HEIGHT
     rocket_x = (ground_width / 2) - rocket_width + rocket_width * .5
     rocket_y += WINDOW_HEIGHT - ground_height - rocket_y - rocket_y
     Vrocket_x = 0
     Vrocket_y = 0
     rocket_boost = True
     
# --------------------------------------------------------------
# Draws all of the in game objects
# --------------------------------------------------------------
def erase_objects():
   pythonGraph.clear_window(pythonGraph.colors.BLACK)

# --------------------------------------------------------------
# Draws all of the in game objects
# --------------------------------------------------------------
def draw_objects():
    global time_elapsed
    
    time_elapsed += 1
    draw_terrain()
    draw_boat()
    draw_rocket()
    draw_hud()
    
# --------------------------------------------------------------
# Draws the Terrain
# --------------------------------------------------------------
def draw_terrain(): 
    for x in range(0,WINDOW_WIDTH):
        
        #Draws land
        if x in range(0, ground_width):
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - ground_heights[x], pythonGraph.colors.GREEN)
       
       #Draws water
        else:
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - water_heights[x-ground_width], pythonGraph.colors.BLUE)
            
# --------------------------------------------------------------
# Draws the Boat
# --------------------------------------------------------------
def draw_boat():
    global boat_x ,boat_y,Vboat_x,boat_height,boat_width
    pythonGraph.draw_image('boat.png',boat_x, boat_y,boat_width,boat_height)

# --------------------------------------------------------------
# Draws the Rocket (and Thrusters)
# --------------------------------------------------------------
def draw_rocket():
    global rocket_x, rocket_y,rocket_width,rocket_height,rocket_ref
    pythonGraph.draw_image('rocket.png',rocket_x, rocket_y,rocket_width,rocket_height)
    #Draws the appropiate thrusters to match input
    if rocket_boost_up >0.0:
        pythonGraph.draw_image('fired.png',rocket_x + rocket_width *.40 , rocket_y+rocket_height * .95 ,rocket_width*.25,rocket_height*.25)
    if rocket_boost_right > 0.0:
        pythonGraph.draw_image('firel.png',rocket_x, rocket_y + rocket_height * .85,rocket_width*.25,rocket_height*.25)
    if rocket_boost_left < 0.0:
        pythonGraph.draw_image('firer.png',rocket_x + rocket_width *.85 , rocket_y + rocket_height *.85 ,rocket_width*.25,rocket_height*.25)
    
# --------------------------------------------------------------
# Draws the On Screen Text
# --------------------------------------------------------------
def draw_hud():
   
   #Updates the Hud Display
    pythonGraph.draw_text("Max Score: " + str(round(max_score,2)), 0, 0, "WHITE", 20)
    pythonGraph.draw_text("Time Elapsed: " + str(round(time_elapsed,2)), 0, 20, "WHITE", 20)
    pythonGraph.draw_text("Fuel Consumed: " + str(round(fuel_consumed,2)), 0, 40, "WHITE", 20)
    pythonGraph.draw_text("X Velocity: " + str(round(Vrocket_x,2)), 0, 60, "WHITE", 20)
    pythonGraph.draw_text("Y Velocity: " + str(round(Vrocket_y,2)), 0, 80, "WHITE", 20)
    pythonGraph.draw_text("Crashes: " + str(crashes) + "  Landings: " + str(landings), 0, 100, "WHITE", 20)

# --------------------------------------------------------------
# Updates all animated objects
# --------------------------------------------------------------
def update_objects():
    update_rocket()
    update_boat()

# --------------------------------------------------------------
# Updates the Rocket
# --------------------------------------------------------------
def update_rocket():
    global  rocket_ref,rocket_left_side, fuel_consumed,rocket_x, rocket_y, Vrocket_x,Vrocket_y,rocket_boost_up ,rocket_boost_right,rocket_boost_left,gravity,rocket_boost
    
    if rocket_boost is True:
        rocket_boost_right = 0
        rocket_boost_left = 0
        rocket_boost_up = 0
        
        #Launch Phase
        if rocket_y >= WINDOW_HEIGHT /2 :   
            rocket_boost_up = .35
        
        else: 
            rocket_boost_right = .25
        
        if rocket_x >= ground_width:
            rocket_boost = False
    
    #Updates Rocket Velocity
    Vrocket_y  = Vrocket_y - rocket_boost_up + gravity 
    Vrocket_x  = Vrocket_x  + rocket_boost_right
    Vrocket_x  = Vrocket_x  + rocket_boost_left
 
     #Updates Rocket Position
    rocket_x += Vrocket_x
    rocket_y += Vrocket_y 

    #Updates the current amount of fuel burned
    fuel_consumed -= rocket_boost_left
    fuel_consumed += rocket_boost_right
    fuel_consumed += rocket_boost_up


    rocket_ref = rocket_y+rocket_height
# --------------------------------------------------------------
# Updates the Landing Pad / Boat
# --------------------------------------------------------------
def update_boat():
    global boat_x ,Vboat_x,ground_width, WINDOW_WIDTH,boat_max,boat_left_side,boat_right_side
    boat_x = boat_x + Vboat_x
    if not boat_x in range(ground_width , boat_max):
        Vboat_x *= -1
        
# --------------------------------------------------------------
# Checks for Manual (or eventually) AI Input
# --------------------------------------------------------------
def get_input():
    global  WINDOW_WIDTH,AI_run_count,rocket_boost_up , rocket_boost_right , rocket_boost_left, rocket_boost,Vrocket_x ,Vrocket_y, rocket_x,rocket_y,boat_x, boat_y, boat_width
    rocket_boost_up = 0
    rocket_boost_left = 0
    rocket_boost_right = 0
    
    if rocket_boost is False:
        ai_decision = pex3_ai_benson.run_autopilot(WINDOW_WIDTH,AI_run_count, rocket_x, rocket_y, Vrocket_x, Vrocket_y, rocket_width, boat_x, boat_y, boat_width)
        rocket_boost_left =  ai_decision[0]
        rocket_boost_right =  ai_decision[1]
        rocket_boost_up =  ai_decision[2]
   
   
   # if rocket_boost is False:
       #Primary Keyboard
        #if pythonGraph.key_down('left'):
            #rocket_boost_left =  -.3
        #if pythonGraph.key_down('right'):
            #rocket_boost_right =  .3
        #if pythonGraph.key_down('up'):
           # rocket_boost_up =  .3
      
      #Alternate keyboard      
       # if pythonGraph.key_down('a'):
            #rocket_boost_left =  -.3
       # if pythonGraph.key_down('d'):
          #  rocket_boost_right =  .3
       # if pythonGraph.key_down('w'):
           # rocket_boost_up =  .3

# --------------------------------------------------------------
# Detects if the Rocket has hit the ground or a boundry
# --------------------------------------------------------------
def is_simulation_over():
    global rocket_ref,rocket_control, rocket_x, rocket_y,rocket_width,rocket_left_side,rocket_right_side, WINDOW_WIDTH,rocket_boost,boat_x,boat_left_side,boat_right_side
    
    if rocket_boost is True:
        return False
    
    if rocket_boost is False:
        rocket_left_side = rocket_x
        rocket_right_side = rocket_x + rocket_width
        boat_left_side = boat_x 
        boat_right_side = boat_x + boat_width
        
        #Checks to see if rocket has flown past the right side of the screen. 
        if rocket_right_side >= WINDOW_WIDTH:
           return True
           rocket_boost = True      
       #Checks to see if rocket has flown past the left side of the screen. 
        if rocket_left_side <= 0:
            return True
            rocket_boost = True  
       #Checks to see if rocket has intersected land.          
        if rocket_x <= ground_width and rocket_y >= WINDOW_HEIGHT - ground_height - rocket_height :
            return True
            rocket_boost = True
        #Checks to see if rocket has intersected the water. 
        if rocket_x >= ground_width and rocket_y >= WINDOW_HEIGHT - water_height - rocket_height :
            return True
            rocket_boost = True
    
        else:
            return False

# --------------------------------------------------------------
# Analyzes the Results of the Simulation
# --------------------------------------------------------------
def analyze_results():
    global time_elapsed,rocket_y,score,landings, crashes, max_score,boat_left_side,boat_right_side,rocket_right_side,rocket_left_side,fuel_consumed,AI_run_count
    
    rocket_left_side = rocket_x
    rocket_right_side = rocket_x + rocket_width
    boat_left_side = boat_x 
    boat_right_side = boat_x +boat_width
    #End Screen Music
    pythonGraph.play_music('metroid16.mp3')
    #Score Calc
    if boat_left_side <= rocket_left_side and rocket_right_side < boat_right_side:
        score = 10000 - fuel_consumed - time_elapsed - Vrocket_x - Vrocket_y
        landings += 1
        fuel_consumed = 0
    
    else:
        score = 5000 - fuel_consumed - time_elapsed - Vrocket_x - Vrocket_y
        crashes += 1
        fuel_consumed = 0
    
    #Passes Score to Ai
    pex3_helper.score_ai(AI_run_count,score)
    
    #New highscore screen
    if score > max_score:
        max_score = score
        
        #Landing
        if boat_left_side <= rocket_left_side and rocket_right_side <= boat_right_side:
            pythonGraph.draw_image('win.png',0, 0,WINDOW_WIDTH,WINDOW_HEIGHT)
            pythonGraph.draw_text("THE ROCKET HAS LANDED SAFELY!", WINDOW_WIDTH/8, WINDOW_HEIGHT*2/3-50, "WHITE", 100)
            pythonGraph.draw_text("NEW HIGHSCORE: "+ str(round(score,2)), WINDOW_WIDTH/4, WINDOW_HEIGHT*2/3+100, "WHITE", 100)
            pythonGraph.update_window()
            time.sleep(8.6)
        
        #Crash
        else:
            pythonGraph.draw_image('win.png',0, 0,WINDOW_WIDTH,WINDOW_HEIGHT)
            pythonGraph.draw_text("THE ROCKET HAS CRASHED!", WINDOW_WIDTH/5, WINDOW_HEIGHT*2/3-50, "WHITE", 100)
            pythonGraph.draw_text("NEW HIGHSCORE: "+ str(round(score,2)), WINDOW_WIDTH/4, WINDOW_HEIGHT*2/3+100, "WHITE", 100)
            pythonGraph.update_window()
            time.sleep(8.6)
    
    #Score screen if it is not a new highscore
    else:
        #Landing
        if boat_left_side <= rocket_left_side and rocket_right_side <= boat_right_side:
            pythonGraph.draw_image('win.png',0, 0,WINDOW_WIDTH,WINDOW_HEIGHT)
            pythonGraph.draw_text("THE ROCKET HAS LANDED SAFELY!", WINDOW_WIDTH/8, WINDOW_HEIGHT*2/3-50, "WHITE", 100)
            pythonGraph.draw_text("SCORE: "+ str(round(score,2)), WINDOW_WIDTH/3, WINDOW_HEIGHT*2/3+100, "WHITE", 100)
            pythonGraph.update_window()
            time.sleep(8.6)
        
        #Crash
        else:
            pythonGraph.draw_image('win.png',0, 0,WINDOW_WIDTH,WINDOW_HEIGHT)
            pythonGraph.draw_text("THE ROCKET HAS CRASHED!", WINDOW_WIDTH/5, WINDOW_HEIGHT*2/3-50, "WHITE", 100)
            pythonGraph.draw_text("SCORE: "+ str(round(score,2)), WINDOW_WIDTH/3, WINDOW_HEIGHT*2/3+100, "WHITE", 100)
            pythonGraph.update_window()
            time.sleep(8.5)
    score = 0
    time_elapsed = 0
    rocket_y = rocket_height

# -----------------------------------------------------
# "Main Program"
# -----------------------------------------------------
pythonGraph.open_window(WINDOW_WIDTH, WINDOW_HEIGHT)
pythonGraph.set_window_title("CS110Z (S20) Rocket Simulator - Zachary Benson")

# --------------------------------------------------------------
#
# Initializes the Simulation At Least Once
initialize_simulation(True)

# Main "Game Loop"
while pythonGraph.window_not_closed():
    if is_simulation_over() == False:
        erase_objects()
        draw_objects()
        get_input()
        update_objects()
    else:
        analyze_results()
        AI_run_allowed = 5
        if AI_run_count < AI_run_allowed:
            initialize_boat(True)
            initialize_rocket(True)
            draw_objects()
            AI_run_count  += 1     
        if AI_run_count == AI_run_allowed:            
            initialize_simulation(True)
            draw_objects()    
            AI_run_count  = 0
    pythonGraph.update_window()
