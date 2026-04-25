import moves

def rotate_z2(cube):
    # Top <-> Bottom
    cube[0], cube[5] = cube[5][::-1], cube[0][::-1]
    
    # Left <-> Right
    cube[1], cube[3] = cube[3][::-1], cube[1][::-1]
    
    # Front rotates 180
    cube[2] = cube[2][::-1]
    
    # Back rotates 180
    cube[4] = cube[4][::-1]

def test_mapping(move_name, func, expected_faces_changed):
    c = moves.init_cube()
    rotate_z2(c)
    func(c)
    rotate_z2(c)
    
    c_orig = moves.init_cube()
    # Which function on c_orig produces the exact same state as c?
    funcs = [moves.turn_U, moves.turn_D, moves.turn_F, moves.turn_B, moves.turn_L, moves.turn_R,
             moves.turn_U_prime, moves.turn_D_prime, moves.turn_F_prime, moves.turn_B_prime, moves.turn_L_prime, moves.turn_R_prime]
    names = ['U', 'D', 'F', 'B', 'L', 'R', "U'", "D'", "F'", "B'", "L'", "R'"]
    
    for f, n in zip(funcs, names):
        c2 = moves.init_cube()
        f(c2)
        if c == c2:
            return n
    return "UNKNOWN"

mappings = {}
for n, f in zip(['U', 'D', 'F', 'B', 'L', 'R', "U'", "D'", "F'", "B'", "L'", "R'"],
                [moves.turn_U, moves.turn_D, moves.turn_F, moves.turn_B, moves.turn_L, moves.turn_R,
                 moves.turn_U_prime, moves.turn_D_prime, moves.turn_F_prime, moves.turn_B_prime, moves.turn_L_prime, moves.turn_R_prime]):
    mappings[n] = test_mapping(n, f, [])

print("Z2 Mapping:")
for k, v in mappings.items():
    print(f"Algorithm Move {k} -> Physical Move {v}")
