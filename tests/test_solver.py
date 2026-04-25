# Stress test the solver with various scrambles
import moves, solver, random

def cube_to_tuple(cube):
    return tuple(tuple(f) for f in cube)

def is_solved(cube):
    return all(len(set(face)) == 1 for face in cube)

def test_solve(scramble_moves, label=""):
    cube = moves.init_cube()
    for m in scramble_moves:
        solver.apply_moves_str(cube, m)
    
    c = solver.copy_cube(cube)
    solution = solver.solve_cube_logic(c)
    
    # Apply the solution to the scrambled cube and see if it actually fixes it
    cube2 = moves.init_cube()
    for m in scramble_moves:
        solver.apply_moves_str(cube2, m)
    solver.apply_moves_str(cube2, solution)
    
    solved = is_solved(cube2)
    move_count = len(solution.split()) if solution.strip() else 0
    tag = "PASS" if solved else "FAIL"
    print(f"{tag}: {label} ({move_count} moves)")
    if not solved:
        for i, face in enumerate(cube2):
            if len(set(face)) > 1:
                print(f"  Face {i}: {face}")
    return solved

print("=" * 60)
print("SOLVER VERIFICATION")
print("=" * 60)

# Test 1: Already solved
test_solve([], "Already solved")

# Test 2: Single move scrambles
for m in ["R", "U", "F", "L", "D", "B", "R'", "U'", "F'", "L'", "D'", "B'"]:
    test_solve([m], f"Scramble: {m}")

# Test 3: Two-move scrambles
test_solve(["R", "U"], "Scramble: R U")
test_solve(["F", "R"], "Scramble: F R")
test_solve(["U", "R", "U'", "R'"], "Scramble: sexy move")

# Test 4: Heavy duty random scrambles
random.seed(42)
pass_count = 0
total = 10
for i in range(total):
    all_moves = ["R","R'","L","L'","U","U'","D","D'","F","F'","B","B'"]
    scramble = [random.choice(all_moves) for _ in range(random.randint(3, 15))]
    if test_solve(scramble, f"Random #{i+1}: {' '.join(scramble)}"):
        pass_count += 1

print(f"\nRandom: {pass_count}/{total} passed")
