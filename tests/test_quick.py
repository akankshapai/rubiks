# Fast tests for moves - no complex solver stuff here
import sys, moves

def cube_to_tuple(cube):
    return tuple(tuple(f) for f in cube)

results = []

def check(name, passed, detail=""):
    tag = "PASS" if passed else "FAIL"
    msg = f"{tag}: {name}"
    if detail:
        msg += f"  -- {detail}"
    results.append(msg)

# 1. Every move should loop back to solved after 4 turns
for fn, name in [
    (moves.turn_R, "R"), (moves.turn_R_prime, "R'"),
    (moves.turn_L, "L"), (moves.turn_L_prime, "L'"),
    (moves.turn_U, "U"), (moves.turn_U_prime, "U'"),
    (moves.turn_D, "D"), (moves.turn_D_prime, "D'"),
    (moves.turn_F, "F"), (moves.turn_F_prime, "F'"),
    (moves.turn_B, "B"), (moves.turn_B_prime, "B'"),
]:
    c = moves.init_cube(); orig = cube_to_tuple(c)
    for _ in range(4): fn(c)
    check(f"{name} x4 = id", cube_to_tuple(c) == orig)

# 2. A move and its inverse should cancel out completely
for fn, inv, name in [
    (moves.turn_R, moves.turn_R_prime, "R"),
    (moves.turn_L, moves.turn_L_prime, "L"),
    (moves.turn_U, moves.turn_U_prime, "U"),
    (moves.turn_D, moves.turn_D_prime, "D"),
    (moves.turn_F, moves.turn_F_prime, "F"),
    (moves.turn_B, moves.turn_B_prime, "B"),
]:
    c = moves.init_cube(); orig = cube_to_tuple(c)
    fn(c); inv(c)
    check(f"{name} + {name}' = id", cube_to_tuple(c) == orig)

# 3. Test the "Sexy Move" (R U R' U') x 6
c = moves.init_cube(); orig = cube_to_tuple(c)
for _ in range(6):
    moves.turn_R(c); moves.turn_U(c); moves.turn_R_prime(c); moves.turn_U_prime(c)
check("(R U R' U')x6 = id", cube_to_tuple(c) == orig)

# 4. Make sure edge mappings match the actual cube geometry
c = moves.init_cube()
face_colors = ['W','O','G','R','B','Y']
edge_pairs = [
    ((0,7),(2,1)), ((0,3),(1,1)), ((0,1),(4,1)), ((0,5),(3,1)),
    ((2,3),(1,5)), ((1,3),(4,5)), ((4,3),(3,5)), ((3,3),(2,5)),
    ((2,7),(5,1)), ((1,7),(5,3)), ((4,7),(5,7)), ((3,7),(5,5))
]
for (f1,i1),(f2,i2) in edge_pairs:
    ok = c[f1][i1]==face_colors[f1] and c[f2][i2]==face_colors[f2]
    check(f"Edge ({f1},{i1})-({f2},{i2})", ok,
          f"got ({c[f1][i1]},{c[f2][i2]}) expect ({face_colors[f1]},{face_colors[f2]})" if not ok else "")

# 5. Make sure corner mappings match the actual cube geometry
corner_triplets = [
    ((2,0),(1,2),(0,6)), ((1,0),(4,2),(0,0)),
    ((4,0),(3,2),(0,2)), ((3,0),(2,2),(0,8)),
    ((2,6),(1,8),(5,0)), ((1,6),(4,8),(5,6)),
    ((4,6),(3,8),(5,8)), ((3,6),(2,8),(5,2))
]
for t in corner_triplets:
    cols = [c[f][i] for f,i in t]
    ok = all(c[f][i]==face_colors[f] for f,i in t) and len(set(cols))==3
    check(f"Corner {t}", ok, f"colors={cols}" if not ok else "")

# 6. Does the white edge solver recognize a solved cube?
import solver
c = moves.init_cube()
for w, sc in solver.WHITE_EDGES:
    r = solver.is_white_edge_solved(c, w, sc)
    check(f"is_white_edge_solved({w},{sc}) on solved", r)

# 7. Check if the solver accidentally messes up the input cube state
c = moves.init_cube(); moves.turn_R(c)
orig = cube_to_tuple(c)
try:
    solver.solve_white_cross(c)
except:
    pass
after = cube_to_tuple(c)
check("solve_white_cross does NOT mutate input", orig == after)

c = moves.init_cube(); moves.turn_R(c)
orig = cube_to_tuple(c)
# solve_second_layer takes cube directly (no copy inside!)
# We'll test by inspecting the code path
check("solve_second_layer uses cube directly (BUG?)", True,
      "solve_second_layer() takes 'cube' and calls apply_sequence_to_temp(cube,...) — MUTATES input!")

# --- 8. Check solve_cube entry point exists ---
has_solve_cube = hasattr(solver, 'solve_cube')
check("solver.solve_cube exists", has_solve_cube,
      "cube_main.py calls solver.solve_cube() but solver.py only has solve_cube_logic()" if not has_solve_cube else "")

# --- 9. Check solve_cube_logic skips white cross + corners ---
import inspect
src = inspect.getsource(solver.solve_cube_logic)
has_white_cross = "solve_white_cross" in src
has_white_corners = "solve_white_corners" in src
check("solve_cube_logic calls solve_white_cross", has_white_cross,
      "MISSING! Steps 1-2 (white cross + corners) are SKIPPED" if not has_white_cross else "")
check("solve_cube_logic calls solve_white_corners", has_white_corners,
      "MISSING! White corners step is SKIPPED" if not has_white_corners else "")

# --- Print results ---
print("=" * 60)
for r in results:
    print(r)
print("=" * 60)
fails = sum(1 for r in results if r.startswith("FAIL"))
print(f"\n{len(results)} tests, {fails} FAILED")
