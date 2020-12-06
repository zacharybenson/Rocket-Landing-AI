# ---------------------------------------------------------------------
# PEX 3 Helper
# Implements a Simple Genetic Algorithm to Help Train a Rocket AI
# Course: CS110Z, Spring 2020
# ---------------------------------------------------------------------
import random

# Configuration Parameters
population_size = -1
num_parents = 1
num_children = 0
max_thrust_x = 1.0
max_thrust_y = 1.0

# The Population of AI Agents
population = []

# The Current Run
current_run = -1

# Flag that determines if we are generating new AIs
freeze_values = False
final_thrust_x_amount = 0.0
final_thrust_y_amount = 0.0
final_max_thrust_x = 0.0
final_max_thrust_y = 0.0

# --------------------------------------------------------------
# Sets Up the GA
# --------------------------------------------------------------
def initialize_genetic_algorithm(parents, children, x_max, y_max):
    global num_parents, num_children, max_thrust_x, max_thrust_y
    num_parents = parents
    num_children = children
    max_thrust_x = x_max
    max_thrust_y = y_max

  
# --------------------------------------------------------------
# Retrieves an AI (or generates a new one)
# --------------------------------------------------------------
def get_ai(run_number):
    global current_run, population_size, first_generation
       
    if run_number == 0 and current_run != run_number and len(population) > 0:
        create_population()
    elif current_run != run_number and population_size <= run_number:
        population_size = run_number + 1
        ai = create_ai()
        print(ai)
        print("  AI #%d (Alive: %d Gen):  Score: %0.2f, Horiz Thrust: %0.2f (%0.2f MAX), Vert Thust: %0.2f (%0.2f MAX)" % (run_number, ai[6], ai[0], ai[1], ai[3], ai[2], ai[4]))
        population.append(ai)

    current_run = run_number
    ai = population[run_number]

    return (ai[1], ai[2], ai[3], ai[4])


# --------------------------------------------------------------
# This function tells the GA to only produce the specified AI
# This effectively stops all learning.
# --------------------------------------------------------------
def use_ai_configuration(thrust_x_amount, thrust_y_amount, max_thrust_x, max_thrust_y):
    global freeze_values, population, population_size, current_run, final_thrust_x_amount, final_thrust_y_amount, final_max_thrust_x, final_max_thrust_y
    freeze_values = True
    population = []
    population_size = -1
    current_run = -1
    final_thrust_x_amount = thrust_x_amount
    final_thrust_y_amount = thrust_y_amount
    final_max_thrust_x = max_thrust_x
    final_max_thrust_y = max_thrust_y
    

# --------------------------------------------------------------
# Creates a New (RANDOM) AI
# Will Create a FIXED AI
# --------------------------------------------------------------
def create_ai():
    if freeze_values == True:
        return [0.0, final_thrust_x_amount, final_thrust_y_amount, final_max_thrust_x, final_max_thrust_y, 0.0, 1]
    else:
        score = 0.0
        max_vx = round(random.random() * max_thrust_x, 5)
        max_vy = round(random.random() * max_thrust_y, 5)
        vx = round(random.random() * 0.5 * max_vx, 5)
        vy = round(random.random() * 0.5 * max_vy, 5)
        total_score = 0
        lifespan = 1
        return [score, vx, vy, max_vx, max_vy, total_score, lifespan]


# --------------------------------------------------------------
# Generates an AI with characteristics from its parents
# --------------------------------------------------------------
def create_offspring(parent1, parent2):
    offspring = [0, 0, 0, 0, 0, 0, 1]
    
    # Parameter 3 - Max X
    if random.random() > 0.5:
        offspring[3] = parent1[3]
    else:
        offspring[3] = parent2[3]
    
    # Parameter 4 - Max Y
    if random.random() > 0.5:
        offspring[4] = parent1[4]
    else:
        offspring[4] = parent2[4]
    
    # Parameter 1 and 2 - x/y thrust
    offspring[1] = random.random() * 0.5 * offspring[3]
    offspring[2] = random.random() * 0.5 * offspring[4]
    
    print("P1:", parent1, " + P2:", parent2, "-->", offspring)
    
    return offspring


# --------------------------------------------------------------
# Creates a Population of AIs
# --------------------------------------------------------------
def create_population():
    global population
    
    new_population = []
    
    if freeze_values == True:
        print("AI Frozen")
        for i in range(0, population_size):
            new_population.append([0, final_thrust_x_amount, final_thrust_x_amount, final_max_thrust_x, final_max_thrust_y, 0, 1])
    
    elif len(population) > 0:
        print("Results from Previous Generation")
        population.sort(reverse=True)
        print_population()
        print()
        
        for i in range(0, min(len(population), num_parents)):
            population[i][6] += 1
            new_population.append(population[i])
        
        print("Creating Offspring (%d parents --> %d new offspring)" % (num_parents, num_children))
        for i in range(num_parents, min(len(population), num_parents + num_children)):
            parent1 = new_population[random.randint(0, num_parents-1)]
            parent2 = new_population[random.randint(0, num_parents-1)]
            attempts = 0
            
            while parent2 == parent1:
                parent2 = population[random.randint(0, num_parents)]
            
            offspring = create_offspring(parent1, parent2)
            
            while offspring in new_population and attempts < 10:
                offspring = create_offspring(parent1, parent2)
                attempts += 1
            
            if offspring not in new_population:
                new_population.append(offspring)
            else:
                new_population.append(create_ai())
        print()
        
        for i in range(num_parents + num_children, population_size):
            new_population.append(create_ai())
            
        print("New Generation")
        
    else:
        print("Creating Initial Population")
        for i in range(population_size):
            new_population.append(create_ai())
    
    population = new_population
    print_population()
                                  

# --------------------------------------------------------------
# Prints out the population to the console
# --------------------------------------------------------------
def print_population():
    for i in range(0, len(population)):
        ai = population[i]
        print("  AI #%d (Alive: %d Gen):  Score: %0.2f, Horiz Thrust: %0.2f (%0.2f MAX), Vert Thust: %0.2f (%0.2f MAX)" % (i, ai[6], ai[0], ai[1], ai[3], ai[2], ai[4]))


# --------------------------------------------------------------
# Assigns a Score to a Specific AI
# --------------------------------------------------------------
def score_ai(run_number, score):
    if freeze_values == False:
        old_score = population[run_number][0]
            
        # Adds Score to the Total
        population[run_number][5] += score
            
        # Calculates a New Weighted Score
        population[run_number][0] = population[run_number][5] / population[run_number][6]
        
        print("  Updating Score for AI %d (%0.2f): %0.2f --> %0.2f" % (run_number, score, old_score, population[run_number][0]))
    else:
        print("  Score for AI %d = (%0.2f)" % (run_number, score))

