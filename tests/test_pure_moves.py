# Basic move tests - no solver imports, just checking if rotations are right
import moves

def t(cube):
    return tuple(tuple(f) for f in cube)

print("=== MOVE x4 = IDENTITY ===")
for fn, name in [
    (moves.turn_R, "R"), (moves.turn_R_prime, "R'"),
    (moves.turn_L, "L"), (moves.turn_L_prime, "L'"),
    (moves.turn_U, "U"), (moves.turn_U_prime, "U'"),
    (moves.turn_D, "D"), (moves.turn_D_prime, "D'"),
    (moves.turn_F, "F"), (moves.turn_F_prime, "F'"),
    (moves.turn_B, "B"), (moves.turn_B_prime, "B'"),
]:
    c = moves.init_cube(); o = t(c)
    for _ in range(4): fn(c)
    print(f"{'PASS' if t(c)==o else 'FAIL'}: {name} x4")

print("\n=== MOVE + INVERSE = IDENTITY ===")
for fn, inv, name in [
    (moves.turn_R, moves.turn_R_prime, "R"),
    (moves.turn_L, moves.turn_L_prime, "L"),
    (moves.turn_U, moves.turn_U_prime, "U"),
    (moves.turn_D, moves.turn_D_prime, "D"),
    (moves.turn_F, moves.turn_F_prime, "F"),
    (moves.turn_B, moves.turn_B_prime, "B"),
]:
    c = moves.init_cube(); o = t(c)
    fn(c); inv(c)
    print(f"{'PASS' if t(c)==o else 'FAIL'}: {name}+{name}'")

print("\n=== SEXY MOVE (R U R' U')x6 ===")
c = moves.init_cube(); o = t(c)
for _ in range(6):
    moves.turn_R(c); moves.turn_U(c); moves.turn_R_prime(c); moves.turn_U_prime(c)
print(f"{'PASS' if t(c)==o else 'FAIL'}: (R U R' U')x6")

print("\n=== EDGE STICKER CHECK (solved cube) ===")
c = moves.init_cube()
fc = ['W','O','G','R','B','Y']
edges = [
    ((0,7),(2,1)), ((0,3),(1,1)), ((0,1),(4,1)), ((0,5),(3,1)),
    ((2,3),(1,5)), ((1,3),(4,5)), ((4,3),(3,5)), ((3,3),(2,5)),
    ((2,7),(5,1)), ((1,7),(5,3)), ((4,7),(5,7)), ((3,7),(5,5))
]
for (f1,i1),(f2,i2) in edges:
    ok = c[f1][i1]==fc[f1] and c[f2][i2]==fc[f2]
    if not ok:
        print(f"FAIL: Edge ({f1},{i1})-({f2},{i2}): got ({c[f1][i1]},{c[f2][i2]}) want ({fc[f1]},{fc[f2]})")
    else:
        print(f"PASS: Edge ({f1},{i1})-({f2},{i2})")

print("\n=== CORNER STICKER CHECK (solved cube) ===")
corners = [
    ((2,0),(1,2),(0,6)), ((1,0),(4,2),(0,0)),
    ((4,0),(3,2),(0,2)), ((3,0),(2,2),(0,8)),
    ((2,6),(1,8),(5,0)), ((1,6),(4,8),(5,6)),
    ((4,6),(3,8),(5,8)), ((3,6),(2,8),(5,2))
]
for tri in corners:
    cols = [c[f][i] for f,i in tri]
    ok = all(c[f][i]==fc[f] for f,i in tri) and len(set(cols))==3
    if not ok:
        print(f"FAIL: Corner {tri}: colors={cols}")
    else:
        print(f"PASS: Corner {tri}")

# Check the solver's internals without actually running it
print(f"solver.solve_cube exists: {hasattr(solver, 'solve_cube')}")
print(f"solver.solve_cube_logic exists: {hasattr(solver, 'solve_cube_logic')}")

# Check what solve_cube_logic calls
src = inspect.getsource(solver.solve_cube_logic)
print(f"solve_cube_logic calls solve_white_cross: {'solve_white_cross' in src}")
print(f"solve_cube_logic calls solve_white_corners: {'solve_white_corners' in src}")
print(f"solve_cube_logic calls solve_second_layer: {'solve_second_layer' in src}")
print(f"solve_cube_logic calls solve_yellow_cross: {'solve_yellow_cross' in src}")
print(f"solve_cube_logic calls solve_yellow_edges: {'solve_yellow_edges' in src}")
print(f"solve_cube_logic calls solve_yellow_corners: {'solve_yellow_corners' in src}")

# Check if solve_second_layer uses copy
src2 = inspect.getsource(solver.solve_second_layer)
print(f"solve_second_layer uses copy_cube: {'copy_cube' in src2}")
print(f"solve_second_layer mutates input directly: {'apply_sequence_to_temp(cube' in src2 or 'apply_virtual_move(cube' in src2}")

# Check solve_yellow_cross
src3 = inspect.getsource(solver.solve_yellow_cross)
print(f"solve_yellow_cross uses copy_cube: {'copy_cube' in src3}")

# Check solve_yellow_edges
src4 = inspect.getsource(solver.solve_yellow_edges)
print(f"solve_yellow_edges uses copy_cube: {'copy_cube' in src4}")

# Check solve_yellow_corners
src5 = inspect.getsource(solver.solve_yellow_corners)
print(f"solve_yellow_corners uses copy_cube: {'copy_cube' in src5}")

print("\nDONE")
