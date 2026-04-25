from ursina import *
import moves
import time
from threading import Thread
import solver

app = Ursina()
window.color = color.black
EditorCamera(move_speed = 0)  # Allows rotation with right-click drag
camera.world_position = (0, 0, -10)
camera.look_at((0,0,0))

logic_cube = moves.init_cube()

color_map = {
    'W' : color.white, 'O' : color.orange, 'G' : color.green,
    'R' : color.red, 'B' : color.blue, 'Y' : color.yellow
}
move_map = {
    'R': moves.turn_R, 'L': moves.turn_L, 'U': moves.turn_U,
    'D': moves.turn_D, 'F': moves.turn_F, 'B': moves.turn_B
}

prime_map = {
    "R'": moves.turn_R_prime, "L'": moves.turn_L_prime, "U'": moves.turn_U_prime,
    "D'": moves.turn_D_prime, "F'": moves.turn_F_prime, "B'": moves.turn_B_prime
}
move_count = 0
counter_text = Text(text = 'Moves : 0', position = (-0.8, 0.45), scale = 2, color = color.white)

def solve_cube():
    print("Solver started...")
    
    # Create a copy of the cube state so we don't mess up visuals immediately
    cube_copy = [face[:] for face in logic_cube]
    
    # Run the solver logic on the copy
    solution_str = solver.solve_cube_logic(cube_copy)
    
    print(f"Solution: {solution_str}")
    
    if not solution_str:
        print("No solution found or cube already solved.")
        return

    moves_list = solution_str.split()
    
    # Function to run animation in background
    def run_animation():
        global move_count
        for move in moves_list:
            if held_keys['q']: break
            
            # Check for Prime moves
            if move in prime_map:
                prime_map[move](logic_cube)
                move_count += 1
            # Check for Standard moves
            elif move in move_map:
                move_map[move](logic_cube)
                move_count += 1
            
            update_visuals()
            time.sleep(0.3) 
            
    # Start the thread exactly once
    t = Thread(target=run_animation)
    t.start()

# Auto-Solver button    
solve_b = Button(
    text='AUTO SOLVE', 
    color=color.azure, 
    position=(0.7, -0.4), 
    scale=(0.2, 0.05), 
    on_click=solve_cube
)

visual_faces = []

def create_face(rotation_deg):

    temp_face = []
    parent = Entity(rotation = rotation_deg) # Invisible parent serves as an anchor

    for y in [1, 0, -1]:
        for x in [-1, 0, 1]:
            element = Entity(
                parent = parent,
                model = 'quad', # Flat square
                color = color.gray,
                scale = 0.92, # Black border visibility
                position = (x, y, -1.5) # To make it pop out
            )
            temp_face.append(element)
    visual_faces.append(temp_face)

# 0 : Up face
create_face((90, 0, 0))

# 1 : Left face
create_face((0, 90, 0))

# 2 : Front face
create_face((0, 0, 0))

# 3 : Right face
create_face((0, -90, 0))

# 4 : Back face
create_face((0, 180, 0))

# 5 : Down face
create_face((-90, 0, 0))

def update_visuals():
    global move_count
    for face_index in range(6):
        face = logic_cube[face_index] # Get face from initialised cube
        _3d_element_list = visual_faces[face_index]

        for i in range(9):
            color_code = face[i]
            if color_code in color_map:
                _3d_element_list[i].color = color_map[color_code]

    counter_text.text = f"Moves: {move_count}"

update_visuals()

def input(key):
    global move_count
    
    if key == 'q': app.quit()

    if key == 's':
        move_count = 0
        moves.scramble(logic_cube, 20)
        update_visuals()
    
    if key == 't':
        move_count = 0
        fresh = moves.init_cube()
        for i in range(6): logic_cube[i] = fresh[i]
        update_visuals()

    if key in ['r', 'l', 'u', 'd', 'f', 'b']:
        move_code = key.upper()
        
        if held_keys['shift']:
            move_str = move_code + "'"
            if move_str in prime_map:
                prime_map[move_str](logic_cube)
                print(f"Turned {move_str}")
                move_count += 1
        else:
            if move_code in move_map:
                move_map[move_code](logic_cube)
                print(f"Turned {move_code}")
                move_count += 1
                
        update_visuals()

app.run()