# Rubik's Cube Solver: Beginner's Method

"""
    Face Mapping Index:
    0: Up/Top
    1: Left
    2: Front
    3: Right
    4: Back
    5: Down/Bottom
"""


import moves

WHITE, GREEN, RED, BLUE, ORANGE, YELLOW = 'W', 'G', 'R', 'B', 'O', 'Y'

MOVE_FN = {
    'R': moves.turn_R, "R'": moves.turn_R_prime,
    'L': moves.turn_L, "L'": moves.turn_L_prime,
    'U': moves.turn_U, "U'": moves.turn_U_prime,
    'D': moves.turn_D, "D'": moves.turn_D_prime,
    'F': moves.turn_F, "F'": moves.turn_F_prime,
    'B': moves.turn_B, "B'": moves.turn_B_prime,
}

def copy_cube(cube):
    return [face[:] for face in cube]

def apply_moves_str(cube, move_str):
    for m in move_str.split():
        if m in MOVE_FN:
            MOVE_FN[m](cube)

def rotate_z2(cube):
    # Rotates the cube 180 degrees around the Z axis (Front-Back)
    # White layer is now on the bottom and the unsolved Yellow layer is on top 
    cube[0], cube[5] = cube[5][::-1], cube[0][::-1]
    cube[1], cube[3] = cube[3][::-1], cube[1][::-1]
    cube[2] = cube[2][::-1]
    cube[4] = cube[4][::-1]

def map_z2_moves(alg):
    # Maps moves performed on a Z2-rotated cube back to the unrotated cube
    m_map = {
        'U': 'D', "U'": "D'",
        'D': 'U', "D'": "U'",
        'F': 'F', "F'": "F'",
        'B': 'B', "B'": "B'",
        'L': 'R', "L'": "R'",
        'R': 'L', "R'": "L'"
    }
    return ' '.join(m_map[m] for m in alg.split())

def apply_z2_alg(cube, alg, all_sol):
    # Applies a standard algorithm to a Z2 rotated cube, mapping the output
    apply_moves_str(cube, alg)
    all_sol.append(map_z2_moves(alg))

def find_edge(cube, c1, c2):
    """
    Finds the location of an edge piece given its two colors.
    Returns: ((face1, index1), (face2, index2))
    """
    edges = [
        ((0,1),(4,1)), ((0,3),(1,1)), ((0,5),(3,1)), ((0,7),(2,1)),
        ((2,3),(1,5)), ((2,5),(3,3)), ((4,3),(3,5)), ((4,5),(1,3)),
        ((5,1),(2,7)), ((5,3),(1,7)), ((5,5),(3,7)), ((5,7),(4,7))
    ]
    for (f1,i1),(f2,i2) in edges:
        if (cube[f1][i1] == c1 and cube[f2][i2] == c2) or (cube[f1][i1] == c2 and cube[f2][i2] == c1):
            return ((f1,i1),(f2,i2))
    return None

def find_corner(cube, c1, c2, c3):
    """
    Finds the location of a corner piece given its three colors.
    Returns: ((face1, index1), (face2, index2), (face3, index3))
    """
    corners = [
        ((0,0),(4,2),(1,0)), ((0,2),(3,2),(4,0)), ((0,6),(1,2),(2,0)), ((0,8),(2,2),(3,0)),
        ((5,0),(2,6),(1,8)), ((5,2),(3,6),(2,8)), ((5,6),(1,6),(4,8)), ((5,8),(4,6),(3,8))
    ]
    target = {c1, c2, c3}
    for corner in corners:
        if {cube[f][i] for f,i in corner} == target:
            return corner
    return None

# Step 1: Solve White Cross on Top (face 0)

def white_edge_solved(cube, side_color):
    slot = {GREEN: ((0,7),(2,1)), RED: ((0,5),(3,1)),
            BLUE: ((0,1),(4,1)), ORANGE: ((0,3),(1,1))}
    (wf,wi),(sf,si) = slot[side_color]
    return cube[wf][wi] == WHITE and cube[sf][si] == side_color

def solve_white_cross(cube):
    c = copy_cube(cube)
    all_sol = []
    
    for sc in [GREEN, ORANGE, BLUE, RED]:
        if white_edge_solved(c, sc): continue
        
        edge = find_edge(c, WHITE, sc)
        (f1,i1), (f2,i2) = edge
        if f1 == 0 or f2 == 0:
            face = f1 if f2 == 0 else f2
            turn = {2:"F", 3:"R", 4:"B", 1:"L"}[face]
            seq = f"{turn} {turn}"
            apply_moves_str(c, seq); all_sol.append(seq)
            
        edge = find_edge(c, WHITE, sc)
        (f1,i1), (f2,i2) = edge
        if f1 in [1,2,3,4] and f2 in [1,2,3,4]:
            if (f1, i1) == (2,3) or (f2, i2) == (2,3): # F-L
                if f1 == 2 and c[f1][i1] == WHITE or f2 == 2 and c[f2][i2] == WHITE:
                    seq = "F' D F"
                else: seq = "L D' L'"
            elif (f1, i1) == (2,5) or (f2, i2) == (2,5): # F-R
                if f1 == 2 and c[f1][i1] == WHITE or f2 == 2 and c[f2][i2] == WHITE:
                    seq = "F D' F'"
                else: seq = "R' D R"
            elif (f1, i1) == (4,5) or (f2, i2) == (4,5): # B-L
                if f1 == 4 and c[f1][i1] == WHITE or f2 == 4 and c[f2][i2] == WHITE:
                    seq = "B D' B'"
                else: seq = "L' D L"
            elif (f1, i1) == (4,3) or (f2, i2) == (4,3): # B-R
                if f1 == 4 and c[f1][i1] == WHITE or f2 == 4 and c[f2][i2] == WHITE:
                    seq = "B' D B"
                else: seq = "R D' R'"
            apply_moves_str(c, seq); all_sol.append(seq)
                
        target_face = {GREEN:2, RED:3, BLUE:4, ORANGE:1}[sc]
        for _ in range(4):
            edge = find_edge(c, WHITE, sc)
            (f1,i1), (f2,i2) = edge
            w_face = f1 if c[f1][i1] == WHITE else f2
            s_face = f2 if c[f1][i1] == WHITE else f1
            
            if w_face == 5 and s_face == target_face:
                turn = {2:"F", 3:"R", 4:"B", 1:"L"}[target_face]
                seq = f"{turn} {turn}"
                apply_moves_str(c, seq); all_sol.append(seq)
                break
            elif s_face == 5 and w_face == target_face:
                if target_face == 2: seq = "F' U' R U"
                elif target_face == 3: seq = "R' U' B U"
                elif target_face == 4: seq = "B' U' L U"
                elif target_face == 1: seq = "L' U' F U"
                apply_moves_str(c, seq); all_sol.append(seq)
                break
            else:
                apply_moves_str(c, "D"); all_sol.append("D")
    
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Step 2: Solve White Corners on Top

def white_corner_solved(cube, s1, s2):
    slots = [
        ((0,6),(1,2),(2,0), ORANGE, GREEN),
        ((0,8),(2,2),(3,0), GREEN, RED),
        ((0,2),(3,2),(4,0), RED, BLUE),
        ((0,0),(4,2),(1,0), BLUE, ORANGE),
    ]
    for (uf,ui),(af,ai),(bf,bi), sa, sb in slots:
        if {s1,s2} == {sa,sb}:
            return (cube[uf][ui] == WHITE and
                    cube[af][ai] in {s1,s2} and cube[bf][bi] in {s1,s2})
    return False

def solve_white_corners(cube):
    c = copy_cube(cube)
    all_sol = []
    
    corners = [(GREEN, ORANGE), (RED, GREEN), (BLUE, RED), (ORANGE, BLUE)]
    
    for (s1, s2) in corners:
        if white_corner_solved(c, s1, s2): continue
        
        corner = find_corner(c, WHITE, s1, s2)
        faces = [f for f,i in corner]
        
        if 0 in faces:
            if 2 in faces and 3 in faces: seq = "R' D' R"
            elif 3 in faces and 4 in faces: seq = "B' D' B"
            elif 4 in faces and 1 in faces: seq = "L' D' L"
            elif 1 in faces and 2 in faces: seq = "F' D' F"
            apply_moves_str(c, seq); all_sol.append(seq)
            
        f_s1 = {GREEN:2, RED:3, BLUE:4, ORANGE:1}[s1]
        f_s2 = {GREEN:2, RED:3, BLUE:4, ORANGE:1}[s2]
        
        for _ in range(4):
            corner = find_corner(c, WHITE, s1, s2)
            faces = [f for f,i in corner]
            if f_s1 in faces and f_s2 in faces:
                break
            apply_moves_str(c, "D"); all_sol.append("D")
            
        if {f_s1, f_s2} == {2, 3}:
            while not white_corner_solved(c, s1, s2):
                seq = "R' D' R D"
                apply_moves_str(c, seq); all_sol.append(seq)
        elif {f_s1, f_s2} == {3, 4}:
            while not white_corner_solved(c, s1, s2):
                seq = "B' D' B D"
                apply_moves_str(c, seq); all_sol.append(seq)
        elif {f_s1, f_s2} == {4, 1}:
            while not white_corner_solved(c, s1, s2):
                seq = "L' D' L D"
                apply_moves_str(c, seq); all_sol.append(seq)
        elif {f_s1, f_s2} == {1, 2}:
            while not white_corner_solved(c, s1, s2):
                seq = "F' D' F D"
                apply_moves_str(c, seq); all_sol.append(seq)
    
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Step 3: Solve Middle Layer

def mid_edge_solved(cube, fa, ia, fb, ib):
    return cube[fa][ia] == cube[fa][4] and cube[fb][ib] == cube[fb][4]

def second_layer_solved(cube):
    return (mid_edge_solved(cube, 2,5,3,3) and mid_edge_solved(cube, 2,3,1,5) and
            mid_edge_solved(cube, 4,5,1,3) and mid_edge_solved(cube, 4,3,3,5))

def solve_second_layer(cube):
    c = copy_cube(cube)
    all_sol = []
    
    rotate_z2(c)
    
    right_alg = "U R U' R' U' F' U F"
    left_alg  = "U' L' U L U F U' F'"
    
    for _ in range(16):
        if second_layer_solved(c): break
        
        inserted = False
        for _ in range(4):
            top = c[0][7] # U-F edge
            front = c[2][1]
            if top != YELLOW and front != YELLOW:
                if front == c[2][4]:
                    if top == c[3][4]:
                        apply_z2_alg(c, right_alg, all_sol)
                        inserted = True; break
                    elif top == c[1][4]:
                        apply_z2_alg(c, left_alg, all_sol)
                        inserted = True; break
            
            back = c[4][1] # U-B edge
            top_b = c[0][1]
            if top_b != YELLOW and back != YELLOW:
                if back == c[4][4]:
                    if top_b == c[3][4]: # Insert U-B to B-R
                        alg = "U' R' U R U B U' B'"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                    elif top_b == c[1][4]: # Insert U-B to B-L
                        alg = "U L U' L' U' B' U B"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                        
            right = c[3][1] # U-R edge
            top_r = c[0][5]
            if top_r != YELLOW and right != YELLOW:
                if right == c[3][4]:
                    if top_r == c[2][4]: # Insert U-R to F-R
                        alg = "U' F' U F U R U' R'"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                    elif top_r == c[4][4]: # Insert U-R to B-R
                        alg = "U B U' B' U' R' U R"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                        
            left = c[1][1] # U-L edge
            top_l = c[0][3]
            if top_l != YELLOW and left != YELLOW:
                if left == c[1][4]:
                    if top_l == c[2][4]: # Insert U-L to F-L
                        alg = "U F U' F' U' L' U L"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                    elif top_l == c[4][4]: # Insert U-L to B-L
                        alg = "U' B' U B U L U' L'"
                        apply_z2_alg(c, alg, all_sol)
                        inserted = True; break
                        
            apply_z2_alg(c, "U", all_sol)
            
        if not inserted:
            mid_edges = [(2,5,3,3), (2,3,1,5), (4,5,1,3), (4,3,3,5)]
            for fa,ia,fb,ib in mid_edges:
                if not mid_edge_solved(c, fa, ia, fb, ib):
                    if fa == 2 and ia == 5:
                        apply_z2_alg(c, right_alg, all_sol)
                    elif fa == 2 and ia == 3:
                        apply_z2_alg(c, left_alg, all_sol)
                    elif fa == 4 and ia == 3:
                        apply_z2_alg(c, "U' R' U R U B U' B'", all_sol)
                    elif fa == 4 and ia == 5:
                        apply_z2_alg(c, "U L U' L' U' B' U B", all_sol)
                    break
                    
    rotate_z2(c)
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Step 4: Yellow Cross 

def yellow_cross(cube):
    return all(cube[0][i] == YELLOW for i in [1,3,5,7])

def solve_yellow_cross(cube):
    c = copy_cube(cube)
    all_sol = []
    rotate_z2(c)
    
    alg = "F R U R' U' F'"
    
    for _ in range(6):
        if yellow_cross(c): break
        
        e = {1: c[0][1]==YELLOW, 3: c[0][3]==YELLOW, 5: c[0][5]==YELLOW, 7: c[0][7]==YELLOW}
        yc = sum(e.values())
        
        if yc == 0:
            apply_z2_alg(c, alg, all_sol)
        elif yc == 2:
            if e[3] and e[5]: # Horizontal line
                apply_z2_alg(c, alg, all_sol)
            elif e[1] and e[7]: # Vertical line
                apply_z2_alg(c, "U", all_sol)
                apply_z2_alg(c, alg, all_sol)
            else: # L-shape
                while not (c[0][1]==YELLOW and c[0][3]==YELLOW):
                    apply_z2_alg(c, "U", all_sol)
                apply_z2_alg(c, alg, all_sol)
        else:
            apply_z2_alg(c, alg, all_sol)
            
    rotate_z2(c)
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Step 5: Solve Yellow Edge 

def yellow_edges_done(cube):
    return all(cube[f][1] == cube[f][4] for f in [1,2,3,4])

def solve_yellow_edges(cube):
    c = copy_cube(cube)
    all_sol = []
    rotate_z2(c)
    
    alg = "R U R' U R U U R'"
    
    for _ in range(12):
        if yellow_edges_done(c): break
        
        matches = [f for f in [1,2,3,4] if c[f][1] == c[f][4]]
        
        if len(matches) == 1:
            rot = {2:0, 3:1, 4:2, 1:3}[matches[0]]
            for _ in range(rot): apply_z2_alg(c, "U", all_sol)
            apply_z2_alg(c, alg, all_sol)
            for _ in range((4 - rot) % 4): apply_z2_alg(c, "U", all_sol)
        elif len(matches) == 0:
            apply_z2_alg(c, alg, all_sol)
        else:
            apply_z2_alg(c, "U", all_sol)
            
    rotate_z2(c)
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Step 6: Solve Yellow Corners

def corner_set(cube, positions):
    return {cube[f][i] for f,i in positions}

def corners_positioned(cube):
    slots = [
        ([(0,0),(4,2),(1,0)], 0, 4, 1),
        ([(0,2),(3,2),(4,0)], 0, 4, 3),
        ([(0,6),(1,2),(2,0)], 0, 2, 1),
        ([(0,8),(2,2),(3,0)], 0, 2, 3),
    ]
    return all(corner_set(cube, p) == {cube[f1][4], cube[f2][4], cube[f3][4]} for p, f1, f2, f3 in slots)

def solve_yellow_corners(cube):
    c = copy_cube(cube)
    all_sol = []
    rotate_z2(c)
    
    place = "U R U' L' U R' U' L"
    
    for _ in range(20):
        if corners_positioned(c): break
        
        c_pos = -1
        if corner_set(c, [(0,8),(2,2),(3,0)]) == {c[0][4], c[2][4], c[3][4]}: c_pos = 0
        elif corner_set(c, [(0,2),(3,2),(4,0)]) == {c[0][4], c[3][4], c[4][4]}: c_pos = 1
        elif corner_set(c, [(0,0),(4,2),(1,0)]) == {c[0][4], c[4][4], c[1][4]}: c_pos = 2
        elif corner_set(c, [(0,6),(1,2),(2,0)]) == {c[0][4], c[1][4], c[2][4]}: c_pos = 3
            
        if c_pos != -1:
            for _ in range(c_pos): apply_z2_alg(c, "U", all_sol)
            apply_z2_alg(c, place, all_sol)
            for _ in range((4 - c_pos) % 4): apply_z2_alg(c, "U", all_sol)
        else:
            apply_z2_alg(c, place, all_sol)
        
    orient = "R' D' R D"
    
    for _ in range(4):
        for __ in range(3):
            if c[0][8] == YELLOW: break
            apply_z2_alg(c, orient, all_sol)
            apply_z2_alg(c, orient, all_sol)
        apply_z2_alg(c, "U", all_sol)
        
    rotate_z2(c)
    for i in range(6): cube[i] = c[i]
    return ' '.join(all_sol)


# Main Solver

def solve_cube_logic(cube):
    # Returns the simplified final string of moves to solve the cube
    c = copy_cube(cube)
    parts = []
    
    s = solve_white_cross(c)
    if s.strip(): parts.append(s)
    
    s = solve_white_corners(c)
    if s.strip(): parts.append(s)
    
    s = solve_second_layer(c)
    if s.strip(): parts.append(s)
    
    s = solve_yellow_cross(c)
    if s.strip(): parts.append(s)
    
    s = solve_yellow_edges(c)
    if s.strip(): parts.append(s)
    
    s = solve_yellow_corners(c)
    if s.strip(): parts.append(s)
    
    sol_str = ' '.join(parts)
    return simplify_moves(sol_str)

# Reduce moves by simplifying redundant moves

def simplify_moves(move_str):
    if not move_str: return ""
    
    moves_list = move_str.split()
    stack = []
    
    for m in moves_list:
        face = m[0]
        val = -1 if "'" in m else 1
        
        if stack and stack[-1][0] == face:
            prev_face, prev_val = stack.pop()
            new_val = (prev_val + val) % 4
            if new_val != 0:
                stack.append((face, new_val))
        else:
            stack.append((face, val % 4))
            
    res = []
    for face, val in stack:
        if val == 1: res.append(face)
        elif val == 2: res.extend([face, face])
        elif val == 3: res.append(face + "'")
        
    return " ".join(res)