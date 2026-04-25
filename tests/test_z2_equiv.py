import moves

def copy_cube(cube):
    return [face[:] for face in cube]

def rotate_z2(cube):
    cube[0], cube[5] = cube[5][::-1], cube[0][::-1]
    cube[1], cube[3] = cube[3][::-1], cube[1][::-1]
    cube[2] = cube[2][::-1]
    cube[4] = cube[4][::-1]

def map_z2_moves(alg):
    m_map = {
        'U': 'D', "U'": "D'",
        'D': 'U', "D'": "U'",
        'F': 'F', "F'": "F'",
        'B': 'B', "B'": "B'",
        'L': 'R', "L'": "R'",
        'R': 'L', "R'": "L'"
    }
    return ' '.join(m_map[m] for m in alg.split())

MOVE_FN = {
    'R': moves.turn_R, "R'": moves.turn_R_prime,
    'L': moves.turn_L, "L'": moves.turn_L_prime,
    'U': moves.turn_U, "U'": moves.turn_U_prime,
    'D': moves.turn_D, "D'": moves.turn_D_prime,
    'F': moves.turn_F, "F'": moves.turn_F_prime,
    'B': moves.turn_B, "B'": moves.turn_B_prime,
}

def apply_moves_str(cube, move_str):
    for m in move_str.split():
        if m in MOVE_FN:
            MOVE_FN[m](cube)

alg = "U R U' R' U' F' U F"

# Method 1: Z2 rotate, apply alg, Z2 rotate back
c1 = moves.init_cube()
rotate_z2(c1)
apply_moves_str(c1, alg)
rotate_z2(c1)

# Method 2: apply mapped alg
c2 = moves.init_cube()
mapped_alg = map_z2_moves(alg)
apply_moves_str(c2, mapped_alg)

print("C1 == C2:", c1 == c2)

if c1 != c2:
    for i in range(6):
        if c1[i] != c2[i]:
            print(f"Face {i} differs:")
            print("C1:", c1[i])
            print("C2:", c2[i])

