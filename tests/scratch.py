import moves

def rotate_x2(cube):
    # Pitch 180 degrees (rotate around X axis? No, Left/Right axis is X. So pitch forward).
    # Top(0) <-> Bottom(5)
    # Front(2) <-> Back(4)
    # Left(1) rotates 180
    # Right(3) rotates 180
    
    # 0 <-> 5
    cube[0], cube[5] = cube[5][::-1], cube[0][::-1] # Wait, if you pitch 180, Top becomes Bottom, but is it upside down?
    # Let's do it by doing X rotation twice.
    # X rotation (pitch forward 90):
    # Top -> Front -> Bottom -> Back -> Top.
    pass

def apply_move(c, m):
    if m == 'U': moves.turn_U(c)
    elif m == "U'": moves.turn_U_prime(c)
    elif m == 'D': moves.turn_D(c)
    elif m == "D'": moves.turn_D_prime(c)
    elif m == 'F': moves.turn_F(c)
    elif m == "F'": moves.turn_F_prime(c)
    elif m == 'B': moves.turn_B(c)
    elif m == "B'": moves.turn_B_prime(c)
    elif m == 'L': moves.turn_L(c)
    elif m == "L'": moves.turn_L_prime(c)
    elif m == 'R': moves.turn_R(c)
    elif m == "R'": moves.turn_R_prime(c)

# Let's just do Z2 rotation! Z2 (roll 180) is much easier!
# Front(2) stays Front, but rotated 180.
# Back(4) stays Back, rotated 180.
# Top(0) <-> Bottom(5).
# Left(1) <-> Right(3).

# Actually, the EASIEST way to do this is to NOT map the algorithms, but just write the solver using the CORRECT standard sequences for the D layer.
