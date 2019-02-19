# READ ME:
# Input file: create a possible state by swapping pieces (even swaps) and eliminate pieces by writing 0
# Start by checking what the input cube state looks like using inpstate()
# Use listates([draw]) to output all the possible cube states (listates(1) to output images)

########################################################################################################################

# Show the input state
def inpstate():
    with open('inpcube.txt','r') as f:
        for i in range(19):
            commstr = f.readline()  # Ignore comment in text file
        cubestate = [[int(x) for x in line.split()] for line in f]  # Read cube state from input file
    print(cubestate)
    drawcube(cubestate, 0)

########################################################################################################################

# TO DO: Input checks; along with: is the cube state possible for trivial inputs?
#        Consider known permutations but unknown orientations and vice versa. 

# List all possible states from input
def listates(draw):  # draw = 1 means draw all output cube states
    
    # INPUT
    
    with open('inpcube.txt','r') as f:
        for i in range(19):
            commstr = f.readline()  # Ignore comment in text file
        cubestate = [[int(x) for x in line.split()] for line in f]  # Read cube state from input file

    # SET-UP

    outno = 0  # To label, and to count the number of, output cube states
    
    # Arrange into seperate corner and edge arrays
    # Corner Arrays
    cperm = cubestate[0][0:8]
    corient = cubestate[1][0:8]
    # Edge Arrays
    eperm = cubestate[0][8:20]
    eorient = cubestate[1][8:20]
        
    # Check the number of gray "open" corners/edges and act accordingly:
    open_corners = cperm.count(0)  # Find the number of open corners
    open_edges = eperm.count(0)  # Find the number of open edges

    # Find index position of zeros in cperm and eperm
    cindex, eindex = find_zero_index_arrays(open_corners, open_edges, cperm, eperm)

    # PERMUTATIONS
            
    # Find the current number of swaps from given (non-open) pieces; and deal with lost pieces while at it
    swaps = 0
    swaps, lostc = find_current_corner_swaps(swaps, cperm, open_corners)
    swaps, loste = find_current_edge_swaps(swaps, eperm, open_edges)

    # Sort through all possible cases systematically and draw into output file
    ce_perms = even_swaps(lostc, loste, swaps)  # Returns list of [corner perms, edge perms] arrays

    # ORIENTATIONS

    # Find current orientation number; simply sum the orientation numbers for corners and edges
    current_corient = sum(corient)
    current_eorient = sum(eorient)

    # Find and store all possible orientations for open pieces
    list_orients_c = find_possible_corner_orientations(open_corners, current_corient, corient, cindex)
    list_orients_e = find_possible_edge_orientations(open_edges, current_eorient, eorient, eindex)
            
    # Form full orientation arrays
    list_orients = []
    for cor in list_orients_c:
        for eor in list_orients_e:
            totor = cor + eor  # totor = total orientations
            list_orients.append(totor[:])  # List of orientations for corners and edges

    # OUTPUT

    # Combine permutations and orientations, to form cubestates to then draw to file (also list cubestates in single text file)
    # Have lists of: which pieces are lost, the number of open pieces, where the open pieces are, possible perms and possible orients
    with open("outstates.txt", "w") as f:
        list_perms = cubestate[0][:]  # To form final corner and edge perms
        for i in range(len(ce_perms)):
            lc_perm = ce_perms[i][0]  # Lost corner perms
            le_perm = ce_perms[i][1]  # Lost edge perms
                    
            # First form permutation row; use zero_index arrays and combine the current cube state with ce_perms
            # Corners
            j = 0
            for zind in cindex:  # zind = zero index
                list_perms[zind] = lc_perm[j]
                j += 1
            # Edges
            j = 0
            for zind in eindex:  # +8 since referring to cubestate
                list_perms[zind + 8] = le_perm[j]
                j += 1

            # For each permutation found above, loop through the orientations and form cube states to draw
            for ceo in list_orients:  # ceo = corner edge orient
                outno += 1
                if draw == 1:  # then draw cube state
                    outcube = [list_perms[:], ceo[:]]
                    drawcube(outcube, outno)
                # Also, output cubestate in form given in input
                print("Cube State", outno, file=f)
                print(list_perms, file=f)
                print(ceo, end="\n\n", file=f)
    
    print("Number of output cube states =", outno)

########################################################################################################################

def find_current_corner_swaps(swaps, cperm, open_corners):  # Corners
    
    lostc = []
    if open_corners > 1:  # Need to deal with swaps and lost pieces
        for i in range(1,9):
            # Check if number exists; if does then find its index; else find index of first zero above finished numbers
            num_exists = cperm.count(i)
            if num_exists == 1:
                swapno = cperm.index(i)
            else:  # Found missing number; deal with next zero
                lostc.append(i)
                swapno = cperm.index(0)
            swaps = swaps + swapno
            # Update swap_arr; remove i or 0 to focus on rest of array
            cperm.pop(swapno)
    elif open_corners == 1:  # Only need to deal with a single lost piece
        for i in range(1,9):
            cubie_set = cperm.count(i)
            if cubie_set == 0:
                lostc.append(i)
                break  # Found only lost corner so can break for loop
        
    return swaps, lostc

########################################################################################################################

def find_current_edge_swaps(swaps, eperm, open_edges):
    
    loste = []
    if open_edges > 1:  # Need to deal with swaps and lost pieces
        for i in range(9,21):
            # Check if number exists; if does then find its index; else find index of first zero above finished numbers
            num_exists = eperm.count(i)
            if num_exists == 1:
                swapno = eperm.index(i)
            else:  # Found missing number; deal with next zero
                loste.append(i)
                swapno = eperm.index(0)
            swaps = swaps + swapno
            # Update swap_arr; remove i or 0 to focus on rest of array
            eperm.pop(swapno)
    elif open_edges == 1:  # Only need to deal with a single lost piece
        for i in range(9,21):
            cubie_set = eperm.count(i)
            if cubie_set == 0:
                loste.append(i)
                break  # Found only lost corner so can break for loop
        
    return swaps, loste

########################################################################################################################

def find_zero_index_arrays(open_corners, open_edges, cperm, eperm):
    
    # Corners
    cindex = []
    start = 0
    for i in range(open_corners):
        zero_index = cperm.index(0, start)
        cindex.append(zero_index)
        start = zero_index + 1
    # Edges
    eindex = []
    start = 0
    for i in range(open_edges):
        zero_index = eperm.index(0, start)
        eindex.append(zero_index)
        start = zero_index + 1

    return cindex, eindex

########################################################################################################################

def find_possible_corner_orientations(open_corners, current_corient, corient, cindex):
    
    list_orients_c = []
    imax = 3**open_corners  # Max i is such that all possibilities are gone through
    for i in range(imax):
        trial = []  # Trial array for orientation
        for j in range(open_corners):
            orient = (int(i/(3**j)))%3
            trial.append(orient)
        orient_poss = (current_corient + sum(trial))%3  # Orientation is possible if the sum of all orientations is 0 (modulo 3)
        if orient_poss == 0:  # Possible
            j = 0
            for zind in cindex:  # zind = zero index
                corient[zind] = trial[j]
                j += 1
            list_orients_c.append(corient[:])  # Add orientation array to list

    return list_orients_c

########################################################################################################################

def find_possible_edge_orientations(open_edges, current_eorient, eorient, eindex):
    
    list_orients_e = []
    imax = 2**open_edges
    for i in range(imax):
        trial = []
        for j in range(open_edges):
            orient = (int(i/(2**j)))%2
            trial.append(orient)
        orient_poss = (current_eorient + sum(trial))%2
        if orient_poss == 0:
            j = 0
            for zind in eindex:  # zind = zero index
                eorient[zind] = trial[j]
                j += 1
            list_orients_e.append(eorient[:])

    return list_orients_e

########################################################################################################################

# Function to systematically sort through possible permutations (defined by an even number of swaps only), with the list ouput
def even_swaps(perm_arr, carry_arr, swaps):  # Array to permute, array to carry through, the number of swaps applied to perm_arr
    tot_arrs = []  # Total arrays
    length = len(perm_arr)
    
    if length > 2:
        for i in range(length):
            index = length - i - 1  # Index at which to insert before
            next_arr = perm_arr[0:length-1]  # The next array to process is the current array minus the entry (always at the end) just permuted
            last_ent = perm_arr[length-1]  # The last entry, which is permuted here
            new_swaps = swaps + i  # i = no. of swaps just done
            
            out_arrs = even_swaps(next_arr, carry_arr, new_swaps)  # Output list of permutations; using a function within itself allows arbitrary for loops
            for j in range(len(out_arrs)):
                out_arrs[j][0].insert(index, last_ent)  # Insert last entry at index of each altered "next_arr"
                tot_arrs.append(out_arrs[j][:])  # Add the two arrays (modified perm_arr and carry_arr) to the final array to be output
    elif length == 2:
        if len(carry_arr) > 2:
            # Apply the function, swapping the current roles of perm_arr and carry_arr
            tot_arrs = even_swaps(carry_arr, perm_arr, swaps)
            for j in range(len(tot_arrs)):
                tot_arrs[j].reverse()
        elif len(carry_arr) == 2:
            # Two pairs of both corners and edges
            if swaps%2 == 0:  # If swaps is even, do nothing or swap both
                tot_arrs.append([perm_arr[:], carry_arr[:]])
                perm_arr.reverse()
                carry_arr.reverse()
                tot_arrs.append([perm_arr[:], carry_arr[:]])
            else:  # If swaps is odd, swap one and not the other (both ways)
                perm_arr.reverse()
                tot_arrs.append([perm_arr[:], carry_arr[:]])
                perm_arr.reverse()
                carry_arr.reverse()
                tot_arrs.append([perm_arr[:], carry_arr[:]])
        else:  # length of carry_arr < 2
            # Just do one pair of corners/edges
            if swaps%2 == 0:  # If swaps is even, do not swap
                tot_arrs = [[perm_arr, carry_arr]]
            else:  # If swaps is odd, swap
                perm_arr.reverse()
                tot_arrs = [[perm_arr, carry_arr]]
            
    else:  # If length of perm array < 2
        if len(carry_arr) > 2:
            # Apply the function, swapping the current roles of perm_arr and carry_arr
            tot_arrs = even_swaps(carry_arr, perm_arr, swaps)
            for j in range(len(tot_arrs)):
                tot_arrs[j].reverse()
        elif len(carry_arr) == 2:
            # Just do one pair of corners/edges
            if swaps%2 == 0:  # If swaps is even, do not swap
                tot_arrs = [[perm_arr, carry_arr]]
            else:  # If swaps is odd, swap
                carry_arr.reverse()
                tot_arrs = [[perm_arr, carry_arr]]
        else:
            tot_arrs = [[perm_arr, carry_arr]]
            
    return tot_arrs
            
########################################################################################################################

# Draw the cube state
def drawcube(cubestate, outno):
    # Import Libraries
    from matplotlib import pyplot as plt
    from shapely.geometry.polygon import Polygon
    from descartes import PolygonPatch

    # Set up face arrays
    # centre sticker colours = [W, B, R, G, Y, O]
    mult = [[1,0,0,1], [1,0,0,1], [1,0,0,1], [0.707,0,0.707,1], [1,0.707,0,0.707], [1,0,0,1]]  # mulitpliers for sticker coordinates; [xhm, xvm, yhm, yvm]
    init_coords = [[4,1], [1,4], [4,4], [7,4], [4,7], [9.12,6.12]]  # initial (x,y) coordinates for each face in final drawing

    # Set key array to convert cubie coordinates to sticker coordinates: [face coordinate, sticker coordinate]
    #        U     R     F
    URF = [[4,2],[3,6],[2,8]]
    UFL = [[4,0],[2,6],[1,8]]
    UBR = [[4,8],[5,6],[3,8]]
    ULB = [[4,6],[1,6],[5,8]]
    DFR = [[0,8],[2,2],[3,0]]
    DLF = [[0,6],[1,2],[2,0]]
    DRB = [[0,2],[3,2],[5,0]]
    DBL = [[0,0],[5,2],[1,0]]
    UF = [[4,1],[2,7]]
    UB = [[4,7],[5,7]]
    UR = [[4,5],[3,7]]
    UL = [[4,3],[1,7]]
    FR = [[2,5],[3,3]]
    FL = [[2,3],[1,5]]
    BR = [[5,3],[3,5]]
    BL = [[5,5],[1,3]]
    DF = [[0,7],[2,1]]
    DB = [[0,1],[5,1]]
    DR = [[0,5],[3,1]]
    DL = [[0,3],[1,1]]
    keyarr = [URF, UFL, UBR, ULB, DFR, DLF, DRB, DBL, UF, UB, UR, UL, FR, FL, BR, BL, DF, DB, DR, DL]

    # Initialise cubie colours; read clockwise for corners, and starting with sticker of ref for orientation (orientation like ZZ edges; corners point U,D)
    #         U     R       F
    URF = ["gold", "g", "crimson"]
    UFL = ["gold", "crimson", "b"]
    UBR = ["gold", "orangered", "g"]
    ULB = ["gold", "b", "orangered"]
    DFR = ["w", "crimson", "g"]
    DLF = ["w", "b", "crimson"]
    DRB = ["w", "g", "orangered"]
    DBL = ["w", "orangered", "b"]
    UF = ["gold", "crimson"]
    UB = ["gold", "orangered"]
    UR = ["gold", "g"]
    UL = ["gold", "b"]
    FR = ["crimson", "g"]
    FL = ["crimson", "b"]
    BR = ["orangered", "g"]
    BL = ["orangered", "b"]
    DF = ["w", "crimson"]
    DB = ["w", "orangered"]
    DR = ["w", "g"]
    DL = ["w", "b"]
    solvedcube = [URF, UFL, UBR, ULB, DFR, DLF, DRB, DBL, UF, UB, UR, UL, FR, FL, BR, BL, DF, DB, DR, DL]

    # Set up blank colour array, with centre stickers filled in (black stickers showing means an error)
    totcol = []
    totcol.append(["k", "k", "k", "k", "w", "k", "k", "k", "k"])
    totcol.append(["k", "k", "k", "k", "b", "k", "k", "k", "k"])
    totcol.append(["k", "k", "k", "k", "crimson", "k", "k", "k", "k"])
    totcol.append(["k", "k", "k", "k", "g", "k", "k", "k", "k"])
    totcol.append(["k", "k", "k", "k", "gold", "k", "k", "k", "k"])
    totcol.append(["k", "k", "k", "k", "orangered", "k", "k", "k", "k"])
    
    # Calculate sticker colours
    # Loop through each corner
    for i in range(8):
        # Determine cubie state
        if cubestate[0][i] == 0:  # Gray cubies show cube states to sort through
            cubie = ["darkgray", "darkgray", "darkgray"]
        else:  # Fixed cubies are ignored
            index = cubestate[0][i] - 1  # Permutation
            orient = cubestate[1][i]  # Orientation
            cubie = solvedcube[index]
            if orient == 1:  # if orient == 1 then shift one way (clockwise), if 2 then the other (anti-clockwise), if 0 do nothing
                tmpsticker = cubie.pop()
                cubie.insert(0, tmpsticker)
            elif orient == 2:
                tmpsticker = cubie.pop(0)
                cubie.insert(3, tmpsticker)

        key = keyarr[i]  # Extract key for this particular cubie
        for j in range(3):  # Loop through each sticker on cubie
            fcoord = key[j][0]  # Set face coord
            scoord = key[j][1]  # Set sticker coord
            totcol[fcoord][scoord] = cubie[j]  # Insert correct sticker colour into total colour array

    # Loop through each edge
    for i in range(8, 20):
        if cubestate[0][i] == 0:
            cubie = ["darkgray", "darkgray"]
        else:
            index = cubestate[0][i] - 1  # Permutation
            orient = cubestate[1][i]  # Orientation
            cubie = solvedcube[index]
            if orient == 1:  # if orient == 1 then swap colours, otherwise do nothing
                tmpsticker = cubie.pop()
                cubie.insert(0, tmpsticker)

        key = keyarr[i]
        for j in range(2):
            fcoord = key[j][0]
            scoord = key[j][1]
            totcol[fcoord][scoord] = cubie[j]

    
    # Set Polygons; first initialise figure
    fig = plt.figure(1, figsize=(13,10), dpi=90)
    ax = fig.add_subplot(111)

    # sticker coords to define 4 corners
    h1 = 0.1
    h2 = 0.9
    h3 = 0.9
    h4 = 0.1
    v1 = 0.1
    v2 = 0.1
    v3 = 0.9
    v4 = 0.9
    # Loop through each face
    for i in range(6):
        # multipliers
        xhm = mult[i][0]
        xvm = mult[i][1]
        yhm = mult[i][2]
        yvm = mult[i][3]
        # initial coords
        x0 = init_coords[i][0]
        y0 = init_coords[i][1]

        # Loop through each sticker
        for n in range(9):
            h = n%3  # stciker x coord
            v = n//3  # sticker y coord
            xb = x0 + h*xhm + v*xvm  # base x coord
            yb = y0 + h*yhm + v*yvm  # base y coord
            
            x = [xb + h1*xhm + v1*xvm, xb + h2*xhm + v2*xvm, xb + h3*xhm + v3*xvm, xb + h4*xhm + v4*xvm]  # x coordinates of face stickers
            y = [yb + h1*yhm + v1*yvm, yb + h2*yhm + v2*yvm, yb + h3*yhm + v3*yvm, yb + h4*yhm + v4*yvm]  # y coordinates of face stickers
            # draw filled polygon
            ax.fill(x, y, totcol[i][n])
    
    # Settings:
    ax.set_title('Cube State ' + str(outno))
    xrange = [0,13]
    yrange = [0,10]
    ax.set_xlim(*xrange)
    ax.set_ylim(*yrange)
    ax.set_xticklabels([])  # Turn off axes values
    ax.set_yticklabels([])
    ax.set_aspect(1)
    ax.set_facecolor('lightgray')  # Set background colour
    
    # Show Plot
    if outno != 0:
        # Draw to file; do not show; name cube state after number in outno
        #file_name = ''
        #for i in range(19):
        #    file_name += str(cubestate[0][i]) + '-' + str(cubestate[1][i]) + '__'
        #file_name += str(cubestate[0][19]) + '-' + str(cubestate[1][19]) + '.png'
        file_name = "Cube_State_" + str(outno) + ".png"
        plt.savefig(file_name)
        plt.close(fig)
    else:
        # Show immediately; not saved to file
        plt.show()

