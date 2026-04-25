# Verify that cube moves actually work.
# Checks identity, inverses, and a few famous algorithms.

import copy
import moves

def cube_to_tuple(cube):
    return tuple(tuple(f) for f in cube)

def test_move_identity(move_fn, name, n=4):
    # A move done 4 times (or N times) should bring the cube back to original state
    cube = moves.init_cube()
    original = cube_to_tuple(cube)
    for _ in range(n):
        move_fn(cube)
    result = cube_to_tuple(cube)
    if result != original:
        print(f"FAIL: {name} x{n} != identity")
        for i in range(6):
            if original[i] != result[i]:
                print(f"  Face {i}: expected {list(original[i])}, got {list(result[i])}")
        return False
    else:
        print(f"PASS: {name} x{n} = identity")
        return True

def test_inverse_pair(move_fn, inv_fn, name):
    # A move and its inverse should result in no change
    cube = moves.init_cube()
    original = cube_to_tuple(cube)
    move_fn(cube)
    inv_fn(cube)
    result = cube_to_tuple(cube)
    if result != original:
        print(f"FAIL: {name} + {name}' != identity")
        for i in range(6):
            if original[i] != result[i]:
                print(f"  Face {i}: expected {list(original[i])}, got {list(result[i])}")
        return False
    else:
        print(f"PASS: {name} + {name}' = identity")
        return True

    # Checking (R U R' U') x 6 = solved cube
    # Sexy move: (R U R' U') x 6 = identity
    cube = moves.init_cube()
    original = cube_to_tuple(cube)
    for _ in range(6):
        moves.turn_R(cube)
        moves.turn_U(cube)
        moves.turn_R_prime(cube)
        moves.turn_U_prime(cube)
    result = cube_to_tuple(cube)
    if result != original:
        print("FAIL: (R U R' U') x 6 != identity")
        for i in range(6):
            if original[i] != result[i]:
                print(f"  Face {i}: expected {list(original[i])}, got {list(result[i])}")
        return False
    else:
        print("PASS: (R U R' U') x 6 = identity")
        return True

def test_T_perm():
    # T-perm is its own inverse: doing it twice should do nothing
    # T-perm: R U R' U' R' F R2 U' R' U' R U R' F'
    cube = moves.init_cube()
    original = cube_to_tuple(cube)
    
    def do_t_perm(c):
        moves.turn_R(c)
        moves.turn_U(c)
        moves.turn_R_prime(c)
        moves.turn_U_prime(c)
        moves.turn_R_prime(c)
        moves.turn_F(c)
        moves.turn_R(c)
        moves.turn_R(c)
        moves.turn_U_prime(c)
        moves.turn_R_prime(c)
        moves.turn_U_prime(c)
        moves.turn_R(c)
        moves.turn_U(c)
        moves.turn_R_prime(c)
        moves.turn_F_prime(c)
    
    do_t_perm(cube)
    do_t_perm(cube)
    result = cube_to_tuple(cube)
    if result != original:
        print("FAIL: T-perm x2 != identity")
        for i in range(6):
            if original[i] != result[i]:
                print(f"  Face {i}: expected {list(original[i])}, got {list(result[i])}")
        return False
    else:
        print("PASS: T-perm x2 = identity")
        return True

def test_edge_definitions():
    # Verify edge_pairs in solver.py refer to correct physical edges
    cube = moves.init_cube()
    # On a solved cube, each edge pair should have exactly 2 different colors
    # matching the faces they border.
    edge_pairs = [
        ((0, 7), (2, 1)), ((0, 3), (1, 1)),
        ((0, 1), (4, 1)), ((0, 5), (3, 1)),
        ((2, 3), (1, 5)), ((1, 3), (4, 5)),
        ((4, 3), (3, 5)), ((3, 3), (2, 5)),
        ((2, 7), (5, 1)), ((1, 7), (5, 3)),
        ((4, 7), (5, 7)), ((3, 7), (5, 5))
    ]
    
    face_colors = ['W', 'O', 'G', 'R', 'B', 'Y']
    all_ok = True
    for (f1,i1),(f2,i2) in edge_pairs:
        c1 = cube[f1][i1]
        c2 = cube[f2][i2]
        expected_c1 = face_colors[f1]
        expected_c2 = face_colors[f2]
        if c1 != expected_c1 or c2 != expected_c2:
            print(f"FAIL: Edge ({f1},{i1})-({f2},{i2}): got ({c1},{c2}), expected ({expected_c1},{expected_c2})")
            all_ok = False
    if all_ok:
        print("PASS: All edge pair definitions correct on solved cube")
    return all_ok

def test_corner_definitions():
    # Verify corner_triplets in solver.py refer to correct physical corners
    cube = moves.init_cube()
    corner_triplets = [
        ((2, 0), (1, 2), (0, 6)),
        ((1, 0), (4, 2), (0, 0)),
        ((4, 0), (3, 2), (0, 2)),
        ((3, 0), (2, 2), (0, 8)),
        ((2, 6), (1, 8), (5, 0)),
        ((1, 6), (4, 8), (5, 6)),
        ((4, 6), (3, 8), (5, 8)),
        ((3, 6), (2, 8), (5, 2))
    ]
    
    face_colors = ['W', 'O', 'G', 'R', 'B', 'Y']
    all_ok = True
    for triplet in corner_triplets:
        colors = set()
        for (f, i) in triplet:
            c = cube[f][i]
            expected = face_colors[f]
            if c != expected:
                print(f"FAIL: Corner pos ({f},{i}): got {c}, expected {expected}")
                all_ok = False
            colors.add(c)
        if len(colors) != 3:
            print(f"FAIL: Corner {triplet} has {len(colors)} distinct colors, expected 3")
            all_ok = False
    if all_ok:
        print("PASS: All corner triplet definitions correct on solved cube")
    return all_ok

def test_solver_white_cross():
    # Scramble the cube and see if the white cross solver can fix it
    import solver
    cube = moves.init_cube()
    # Apply R U to scramble slightly
    moves.turn_R(cube)
    moves.turn_U(cube)
    
    sol = solver.solve_white_cross(cube)
    print(f"White cross solution for R U scramble: '{sol}'")
    
    # Apply solution to a fresh scrambled cube
    cube2 = moves.init_cube()
    moves.turn_R(cube2)
    moves.turn_U(cube2)
    
    if sol:
        for m in sol.split():
            solver.apply_virtual_move(cube2, m)
    
    # Check: all 4 edges on face 0 should be white
    white_edges_ok = all(cube2[0][i] == 'W' for i in [1, 3, 5, 7])
    if white_edges_ok:
        print("PASS: White cross solver produces white edges on top")
    else:
        print(f"FAIL: White cross solver - top edge colors: {[cube2[0][i] for i in [1,3,5,7]]}")
    return white_edges_ok

def test_solve_cube_logic():
    # Test the full solver pipeline
    import solver
    cube = moves.init_cube()
    # Apply known scramble
    moves.turn_R(cube)
    moves.turn_U(cube)
    
    cube_copy = [face[:] for face in cube]
    sol = solver.solve_cube_logic(cube_copy)
    print(f"Full solve solution for R U: '{sol}'")
    
    # Apply to original scrambled state
    cube2 = moves.init_cube()
    moves.turn_R(cube2)
    moves.turn_U(cube2)
    
    if sol:
        for m in sol.split():
            solver.apply_virtual_move(cube2, m)
    
    solved = moves.init_cube()
    if cube_to_tuple(cube2) == cube_to_tuple(solved):
        print("PASS: Full solver restores cube to solved state")
    else:
        print("FAIL: Full solver does NOT restore cube to solved state")
        for i in range(6):
            if cube2[i] != solved[i]:
                print(f"  Face {i}: {cube2[i]} vs expected {solved[i]}")
    
def test_solver_mutates_original():
    # Check if solver mutates the input cube (it shouldn't if using copy)
    import solver
    cube = moves.init_cube()
    moves.turn_R(cube)
    original = cube_to_tuple(cube)
    
    # solve_white_cross should use temp_cube internally
    sol = solver.solve_white_cross(cube)
    after = cube_to_tuple(cube)
    
    if original == after:
        print("PASS: solve_white_cross does NOT mutate input cube")
    else:
        print("FAIL: solve_white_cross MUTATES input cube!")
        return False
    
    # solve_second_layer mutates?
    cube = moves.init_cube()
    moves.turn_R(cube)
    original = cube_to_tuple(cube)
    sol = solver.solve_second_layer(cube)
    after = cube_to_tuple(cube)
    if original == after:
        print("PASS: solve_second_layer does NOT mutate input cube")
    else:
        print("FAIL: solve_second_layer MUTATES input cube!")
    
    return True

def test_is_white_edge_solved():
    # Test the is_white_edge_solved function on solved cube
    import solver
    cube = moves.init_cube()
    
    all_ok = True
    for white, side_color in solver.WHITE_EDGES:
        result = solver.is_white_edge_solved(cube, white, side_color)
        if not result:
            print(f"FAIL: is_white_edge_solved says ({white},{side_color}) NOT solved on solved cube")
            all_ok = False
    if all_ok:
        print("PASS: All white edges correctly identified as solved on solved cube")
    return all_ok

if __name__ == "__main__":
    print("=" * 60)
    print("MOVE IDENTITY TESTS (move x 4 = identity)")
    print("=" * 60)
    test_move_identity(moves.turn_R, "R")
    test_move_identity(moves.turn_R_prime, "R'")
    test_move_identity(moves.turn_L, "L")
    test_move_identity(moves.turn_L_prime, "L'")
    test_move_identity(moves.turn_U, "U")
    test_move_identity(moves.turn_U_prime, "U'")
    test_move_identity(moves.turn_D, "D")
    test_move_identity(moves.turn_D_prime, "D'")
    test_move_identity(moves.turn_F, "F")
    test_move_identity(moves.turn_F_prime, "F'")
    test_move_identity(moves.turn_B, "B")
    test_move_identity(moves.turn_B_prime, "B'")
    
    print()
    print("=" * 60)
    print("INVERSE PAIR TESTS (M + M' = identity)")
    print("=" * 60)
    test_inverse_pair(moves.turn_R, moves.turn_R_prime, "R")
    test_inverse_pair(moves.turn_L, moves.turn_L_prime, "L")
    test_inverse_pair(moves.turn_U, moves.turn_U_prime, "U")
    test_inverse_pair(moves.turn_D, moves.turn_D_prime, "D")
    test_inverse_pair(moves.turn_F, moves.turn_F_prime, "F")
    test_inverse_pair(moves.turn_B, moves.turn_B_prime, "B")
    
    print()
    print("=" * 60)
    print("COMMUTATOR TESTS")
    print("=" * 60)
    test_commutator_identity()
    test_T_perm()
    
    print()
    print("=" * 60)
    print("EDGE & CORNER DEFINITION TESTS")
    print("=" * 60)
    test_edge_definitions()
    test_corner_definitions()
    
    print()
    print("=" * 60)
    print("SOLVER LOGIC TESTS")
    print("=" * 60)
    test_is_white_edge_solved()
    test_solver_mutates_original()
    test_solver_white_cross()
    test_solve_cube_logic()
