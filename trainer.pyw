import dearpygui.dearpygui as dpg
import twophase.solver as sv
import random as r

corners = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]]
edges = [[8,0],[9,0],[10,0],[11,0],[12,0],[13,0],[14,0],[15,0],[16,0],[17,0],[18,0],[19,0]]
requested_twists = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
requested_parity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
corners_only = False

cornerToFacelet = [ [0,27,47],[2,45,20],[8,18,38],[6,36,29],[9,35,42],[11,44,24],[17,26,51],[15,53,33] ]
edgeToFacelet  = [ [1,46],[5,19],[7,37],[3,28],[10,43],[14,25],[16,52],[12,34],[41,21],[39,32],[48,23],[50,30] ]

cornerColour = [ [0,3,5],[0,5,2],[0,2,4],[0,4,3],[1,3,4],[1,4,2],[1,2,5],[1,5,3] ]
edgeColour  = [ [0,5],[0,2],[0,4],[0,3],[1,4],[1,2],[1,5],[1,3],[4,2],[4,3],[5,2],[5,3] ]

outputList = [0,0,0,0,0,0,0,0,0,
              1,1,1,1,1,1,1,1,1,
              2,2,2,2,2,2,2,2,2,
              3,3,3,3,3,3,3,3,3,
              4,4,4,4,4,4,4,4,4,
              5,5,5,5,5,5,5,5,5,]

modifiedList = [0,0,0,0,0,0,0,0,0,
                0,0,0,0,4,0,0,0,0,
                0,0,0,0,2,0,0,0,0,
                0,0,0,0,1,0,0,0,0,
                0,0,0,0,3,0,0,0,0,
                0,0,0,0,5,0,0,0,0,]

def randomize(tp, pp):
    r.seed()
    if (requested_twists[8][0] == 0):
        for i in range(0,20):
            et1 = r.randint(0,11)
            et2 = r.randint(0,11)
            eo = r.randint(0,1)
            while et1 == et2:
                et2 = r.randint(0,11)

            temp = edges[et1][0]
            edges[et1][0] = edges[et2][0]
            edges[et2][0] = temp
            if eo == 1:
                edges[et1][1] = (edges[et1][1] + 1) % 2
                edges[et2][1] = (edges[et2][1] + 1) % 2

    cycledCorners = []
    for i in range(0,8):
        if i != tp and i != pp and i != 2:
            cycledCorners.append(corners[i])

    for i in range(0,3):
        p1 = r.randint(0,4)
        p2 = r.randint(0,4)
        while p1 == p2:
            p2 = r.randint(0,4)
        temp = cycledCorners[p1]
        cycledCorners[p1] = cycledCorners[p2]
        cycledCorners[p2] = temp

    for i in range(0,2):
        o1 = r.randint(0,2)
        o2 = r.randint(0,2)
        threeCycle(cycledCorners[i*2][0], o1, cycledCorners[i*2+1][0], o2)

def convertToCubestring():
    for i in range(0,8):
        c = corners[i][0]
        o = corners[i][1]
        for k in range(0,3):
            outputList[cornerToFacelet[i][(k + o) % 3]] = cornerColour[c][k]

    for i in range(0,12):
        e = edges[i][0]
        o = edges[i][1]
        for k in range(0,2):
            outputList[edgeToFacelet[i][(k + o) % 2]] = edgeColour[e-8][k]

def threeCycle(ap, ao, bp, bo):
    corners[2][1] = (corners[2][1] + ao) % 3
    corners[ap][1] = (corners[ap][1] + (3-(ao-bo))) % 3
    corners[bp][1] = (corners[bp][1] + (3-bo)) % 3

    temp_p = corners[2]

    corners[2] = corners[bp]
    corners[bp] = corners[ap]
    corners[ap] = temp_p

def convertOutputList():
    for i in range(0,54):
        match outputList[i]:
            case 0:
                modifiedList[i] = 0
            case 1:
                modifiedList[i] = 3
            case 2:
                modifiedList[i] = 1
            case 3:
                modifiedList[i] = 4
            case 4:
                modifiedList[i] = 2
            case 5:
                modifiedList[i] = 5

    for k in range(0,9):
        outputList[k] = modifiedList[k]
        outputList[9 * 1 + k] = modifiedList[9 * 2 + k]
        outputList[9 * 2 + k] = modifiedList[9 * 4 + k]
        outputList[9 * 3 + k] = modifiedList[9 * 1 + k]
        outputList[9 * 4 + k] = modifiedList[9 * 3 + k]
        outputList[9 * 5 + k] = modifiedList[9 * 5 + k]

    for j in range (0,54):
        match outputList[j]:
            case 0:
                outputList[j] = 'U'
            case 1:
                outputList[j] = 'R'
            case 2:
                outputList[j] = 'F'
            case 3:
                outputList[j] = 'D'
            case 4:
                outputList[j] = 'L'
            case 5:
                outputList[j] = 'B'    

def printOutputList(list):
    for i in range(0,6):
        for k in range(0,9):
            print(list[9 * i + k], end='')
        print()

fake_scram = "F R2 U2 B' R U2 B R F' L U2 F2 R2 F2 R2 B2 D' F2 R2 D"
solution = ""
parity = [0,0]
twist = [0,0]
testbool = False
queued_twists = []

def parity_callback(sender, app_data, user_data):
    if (app_data == True):
        requested_parity[user_data[0]][user_data[1]] = 1
    else:
        requested_parity[user_data[0]][user_data[1]] = 0

def twist_callback(sender, app_data, user_data):
    if (app_data == True):
        requested_twists[user_data[0]][user_data[1] - 1] = 1
    else:
        requested_twists[user_data[0]][user_data[1] - 1] = 0
    queued_twists.clear()

def co_callback(sender, app_data, user_data):
    if (app_data == True):
        requested_twists[8][0] = 1
    else:
        requested_twists[8][0] = 0

def determine_parity():
    reduced = []
    count = -1
    for i in range(0,8):
        for j in range(0,3):
            if (requested_parity[i][j] == 1):
                reduced.append([i,j])
                count += 1
            
    rand = r.randint(0,count)
    return reduced[rand]

def determine_twist(queue):
    if len(queue) == 0:
        count = -1
        for i in range(0,8):
            for j in range(0,2):
                if (requested_twists[i][j] == 1):
                    queued_twists.append([i,j + 1])
                    count += 1
        for k in range(0,10):
            a = r.randint(0,count)
            b = r.randint(0,count)

            temp = queued_twists[a]
            queued_twists[a] = queued_twists[b]
            queued_twists[b] = temp

    t = queued_twists.pop()
    return t

def next_scramble():
    for i in range(0,8):
        corners[i][0] = i
        corners[i][1] = 0
    for i in range(0,12):
        edges[i][0] = i + 8
        edges[i][1] = 0
    edges[1][0] = 10
    edges[2][0] = 9
    
    parity = determine_parity()
    temp = corners[2][0]
    corners[2][0] = corners[parity[0]][0]
    corners[parity[0]][0] = temp

    corners[2][1] = (3 - parity[1]) % 3
    corners[parity[0]][1] = parity[1]

    twist = determine_twist(queued_twists)
    print(queued_twists)
    corners[twist[0]][1] = twist[1]
    corners[parity[0]][1] = (corners[parity[0]][1] - twist[1]) % 3

    randomize(twist[0], parity[0])

    convertToCubestring()
    convertOutputList()

    cubestring = ''.join(outputList)
    solution = sv.solve(cubestring)
    print(solution)

    actualLength = int((len(solution) - 5) / 3);
    convertedSol = []
    scramble = []

    realSol = ""
    realScram = ""

    for i in range(0,actualLength):
        base = stringToMoveBase(solution[i*3])
        base += int(solution[i*3 + 1]) - 1
        convertedSol.append(moveToString(base))
        realSol = ' '.join(convertedSol)

    for i in range(0,actualLength):
        base = (stringToMoveBase(convertedSol[actualLength-i-1]) // 3) * 3
        dir = 2 - (stringToMoveBase(convertedSol[actualLength-i-1]) % 3)
        scramble.append(moveToString(base + dir))
        realScram = ' '.join(scramble)

    dpg.set_value("scram", realScram)

def stringToMoveBase(s):
    match s:
        case 'U':
            return 0
        case 'U2':
            return 1
        case "U'":
            return 2
        case 'D':
            return 3
        case 'D2':
            return 4
        case "D'":
            return 5
        case 'R':
            return 6
        case 'R2':
            return 7
        case "R'":
            return 8
        case 'L':
            return 9
        case 'L2':
            return 10
        case "L'":
            return 11
        case 'F':
            return 12
        case 'F2':
            return 13
        case "F'":
            return 14
        case 'B':
            return 15
        case 'B2':
            return 16
        case "B'":
            return 17

def moveToString(m):
    match(m):
        case 0:
            return "U"
        case 1:
            return "U2"
        case 2:
            return "U'"
        case 3:
            return "D"
        case 4:
            return "D2"
        case 5:
            return "D'"
        case 6:
            return "R"
        case 7:
            return "R2"
        case 8:
            return "R'"
        case 9:
            return "L"
        case 10:
            return "L2"
        case 11:
            return "L'"
        case 12:
            return "F"
        case 13:
            return "F2"
        case 14:
            return "F'"
        case 15:
            return "B"
        case 16:
            return "B2"
        case 17:
            return "B'"

dpg.create_context()
dpg.create_viewport(title="LTCT Trainer", width=800, height=400, small_icon="resources/smoothswaggin.ico", large_icon="resources/smoothswaggin.ico", resizable=False)
dpg.setup_dearpygui()
title_offset = "                                                    "

with dpg.font_registry():
    default_f = dpg.add_font("resources/Roboto-Regular.ttf", 15)
    scramble_f = dpg.add_font("resources/Roboto-Regular.ttf", 25)
    title_f = dpg.add_font("resources/Roboto-Regular.ttf", 30)

with dpg.window(label="Testing", tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Edit Solutions")
    title_t = dpg.add_text(f"{title_offset}LTCT Trainer", label="title-text")
    scramble_t = dpg.add_text(solution, label="scramble-text", tag="scram")

    dpg.add_button(label="Next Scramble", callback=next_scramble)

    dpg.add_text("Parity Targets:")
    with dpg.group(label="Parity Targets O", horizontal=True):
        dpg.add_checkbox(label="UBL", callback=parity_callback, user_data=[0,0])
        dpg.add_checkbox(label="UBR", callback=parity_callback, user_data=[1,0])
        dpg.add_checkbox(label="UFL", callback=parity_callback, user_data=[3,0])
        dpg.add_checkbox(label="DFL", callback=parity_callback, user_data=[4,0])
        dpg.add_checkbox(label="DFR", callback=parity_callback, user_data=[5,0])
        dpg.add_checkbox(label="DBR", callback=parity_callback, user_data=[6,0])
        dpg.add_checkbox(label="DBL", callback=parity_callback, user_data=[7,0])

    with dpg.group(label="Parity Targets C", horizontal=True):
        dpg.add_checkbox(label="LUB", callback=parity_callback, user_data=[0,1])
        dpg.add_checkbox(label="BUR", callback=parity_callback, user_data=[1,1])
        dpg.add_checkbox(label="FUL", callback=parity_callback, user_data=[3,1])
        dpg.add_checkbox(label="LDF", callback=parity_callback, user_data=[4,1])
        dpg.add_checkbox(label="FDR", callback=parity_callback, user_data=[5,1])
        dpg.add_checkbox(label="RDB", callback=parity_callback, user_data=[6,1])
        dpg.add_checkbox(label="BDL", callback=parity_callback, user_data=[7,1])

    with dpg.group(label="Parity Targets CC", horizontal=True):
        dpg.add_checkbox(label="BUL", callback=parity_callback, user_data=[0,2])
        dpg.add_checkbox(label="RUB", callback=parity_callback, user_data=[1,2])
        dpg.add_checkbox(label="LUF", callback=parity_callback, user_data=[3,2])
        dpg.add_checkbox(label="FDL", callback=parity_callback, user_data=[4,2])
        dpg.add_checkbox(label="RDF", callback=parity_callback, user_data=[5,2])
        dpg.add_checkbox(label="BDR", callback=parity_callback, user_data=[6,2])
        dpg.add_checkbox(label="LDB", callback=parity_callback, user_data=[7,2])

    dpg.add_text("Corner Twists:")
    with dpg.group(label="Parity Targets C", horizontal=True):
        dpg.add_checkbox(label="[LUB]", callback=twist_callback, user_data=[0,1])
        dpg.add_checkbox(label="[BUR]", callback=twist_callback, user_data=[1,1])
        dpg.add_checkbox(label="[FUL]", callback=twist_callback, user_data=[3,1])
        dpg.add_checkbox(label="[LDF]", callback=twist_callback, user_data=[4,1])
        dpg.add_checkbox(label="[FDR]", callback=twist_callback, user_data=[5,1])
        dpg.add_checkbox(label="[RDB]", callback=twist_callback, user_data=[6,1])
        dpg.add_checkbox(label="[BDL]", callback=twist_callback, user_data=[7,1])

    with dpg.group(label="Parity Targets CC", horizontal=True):
        dpg.add_checkbox(label="[BUL]", callback=twist_callback, user_data=[0,2])
        dpg.add_checkbox(label="[RUB]", callback=twist_callback, user_data=[1,2])
        dpg.add_checkbox(label="[LUF]", callback=twist_callback, user_data=[3,2])
        dpg.add_checkbox(label="[FDL]", callback=twist_callback, user_data=[4,2])
        dpg.add_checkbox(label="[RDF]", callback=twist_callback, user_data=[5,2])
        dpg.add_checkbox(label="[BDR]", callback=twist_callback, user_data=[6,2])
        dpg.add_checkbox(label="[LDB]", callback=twist_callback, user_data=[7,2])
        
    dpg.add_checkbox(label="Corners Only", callback=co_callback)

    dpg.bind_font(default_f)
    dpg.bind_item_font(title_t, title_f)
    dpg.bind_item_font(scramble_t, scramble_f)

dpg.set_primary_window("Primary Window", True)
dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()