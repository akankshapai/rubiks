import solver
import moves
import test_solver

c = moves.init_cube()
solver.apply_moves_str(c, "F")

# print original state just in case
print("Scramble F applied.")

sol_str = solver.solve_cube_logic(c)
print("Solution length:", len(sol_str.split()))
print("Solution:", sol_str)

c = moves.init_cube()
solver.apply_moves_str(c, "F")
solver.apply_moves_str(c, sol_str)

solved = moves.init_cube()
if c == solved:
    print("SUCCESS!")
else:
    print("FAILED!")
    for i in range(6):
        if c[i] != solved[i]:
            print(f"Face {i}:", c[i])
