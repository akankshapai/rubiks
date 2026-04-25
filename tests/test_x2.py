import moves

def cube_to_tuple(cube):
    return tuple(tuple(f) for f in cube)

c = moves.init_cube()
# Make top and middle distinct
for i in range(9):
    c[0][i] = 'W' # Top (Old U)
    c[5][i] = 'Y' # Bottom (Old D)
for f in [1,2,3,4]:
    for i in range(3): c[f][i] = 'T' # Top row
    for i in range(3,6): c[f][i] = 'M' # Middle row
    for i in range(6,9): c[f][i] = 'B' # Bottom row

original = cube_to_tuple(c)

def apply(cube, alg):
    for m in alg.split():
        if m == 'B': moves.turn_B(cube)
        elif m == "B'": moves.turn_B_prime(cube)
        elif m == 'R': moves.turn_R(cube)
        elif m == "R'": moves.turn_R_prime(cube)
        elif m == 'D': moves.turn_D(cube)
        elif m == "D'": moves.turn_D_prime(cube)

alg = "B R' D R D' B'"
apply(c, alg)

result = cube_to_tuple(c)

ok = True
for f in [1,2,3,4]:
    if list(result[f][0:6]) != ['T','T','T','M','M','M']:
        print(f"Face {f} broken: {result[f][0:6]}")
        ok = False
if list(result[0]) != ['W']*9:
    print("Face 0 broken!")
    ok = False

if ok:
    print("Top and Middle layers PRESERVED!")
else:
    print("Top and Middle layers BROKEN!")
