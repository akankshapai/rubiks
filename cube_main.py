import moves
import solver


def print_cube(cube):
    
    for i in [0, 3, 6]:
        print("      ", cube[0][i], cube[0][i+1], cube[0][i+2])

    print()

    for i in [0, 3, 6]:
        print(
            cube[1][i], cube[1][i+1], cube[1][i+2], " ",
            cube[2][i], cube[2][i+1], cube[2][i+2], " ",
            cube[3][i], cube[3][i+1], cube[3][i+2], " ",
            cube[4][i], cube[4][i+1], cube[4][i+2]
        )

    print()

    for i in [0, 3, 6]:
        print("      ", cube[5][i], cube[5][i+1], cube[5][i+2])

def apply_move(cube, move):
    if move == 'R':
        moves.turn_R(cube)
    elif move == "R'":
        moves.turn_R_prime(cube)

    elif move == 'U':
        moves.turn_U(cube)
    elif move == "U'":
        moves.turn_U_prime(cube)

    elif move == 'L':
        moves.turn_L(cube)
    elif move == "L'":
        moves.turn_L_prime(cube)

    elif move == 'D':
        moves.turn_D(cube)
    elif move == "D'":
        moves.turn_D_prime(cube)

    elif move == 'F':
        moves.turn_F(cube)
    elif move == "F'":
        moves.turn_F_prime(cube)

    elif move == 'B':
        moves.turn_B(cube)
    elif move == "B'":
        moves.turn_B_prime(cube)

    else:
        print("Invalid move:", move)
def apply_sequence(cube, sequence):
    for move in sequence.split():
        apply_move(cube, move)

def main():
    cube = moves.init_cube()

    while True:
        print_cube(cube)
        cmd = input("Enter moves (R U R' or Q or S): ").strip()

        if cmd.upper() == 'Q':
            break

        elif cmd.upper() == 'S':
            solution = solver.solve_cube_logic(cube)
            print("Solver:", solution)
            apply_sequence(cube, solution)

        else:
            apply_sequence(cube, cmd)

if __name__ == "__main__":
    main()

