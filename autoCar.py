import sys, pygame
import os
import time
import math

# Fuzzy

def Fuzzy(front, left, right):
    """
    Functional fuzzy
    :param front: 汽車前方的距離
    :param left: 汽車左方的距離
    :param right: 汽車右方的距離
    :return: 去模糊化後要轉的角度
    """
    output = [55, -55, -40, 40, 60]
    input = [
        mf_Right(left, 'large'), # every each is compete to a rule
        mf_Left(right, 'large'),
        mf_Right(right, 'middle'),
        mf_Left(left, 'middle'),
        mf_Front(front, 'small')
    ]
    return max(min(40, weightAvg(input, output)),-40)

def FuzzyMean(front, left, right):
    """
    Mean Mx fuzzy
    :param front: 汽車前方的距離
    :param left: 汽車左方的距離
    :param right: 汽車右方的距離
    :return: 去模糊化後要轉的角度
    """
    output = [
        [[0,0], [50,1], [60,1]], # left large
        [[-60, 1], [-50, 1], [0, 0]], # right large
        [[-45, 1], [-40, 0], [0, 0]], # right middle
        [[0, 0], [40, 0], [45, 1]], # left middle
        [[0, 1], [20, 1], [40, 1]], # front large, right small
        [[-40, 0], [-20, 1], [0, 1]], # front large, left small
        [[0, 0], [40, 0], [60, 1]] # front small
    ]
    input = [
        mf_Right(left, 'large'), # every each is compete to a rule
        mf_Left(right, 'large'),
        mf_Right(right, 'middle'),
        mf_Left(left, 'middle'),
        mf_Front(front, 'large') * mf_Left(right, 'small'),
        mf_Front(front, 'large') * mf_Left(left, 'small'),
        mf_Front(front, 'small')
    ]
    return max(min(40, meanMax(input, output)), -40)

def FuzzyGravity(front, left, right):
    """
    Center Gravity fuzzy
    :param front: 汽車前方的距離
    :param left: 汽車左方的距離
    :param right: 汽車右方的距離
    :return: 去模糊化後要轉的角度
    """
    output = [
        [[0,0], [50,1], [60,1]], # left large
        [[-60, 1], [-50, 1], [0, 0]], # right large
        [[-45, 1], [-40, 0], [0, 0]], # right middle
        [[0, 0], [40, 0], [45, 1]], # left middle
        [[0, 1], [20, 1], [40, 1]], # front large, right small
        [[-40, 0], [-20, 1], [0, 1]], # front large, left small
        [[0, 0], [40, 0], [60, 1]] # front small
    ]
    input = [
        mf_Right(left, 'large'), # every each is compete to a rule
        mf_Left(right, 'large'),
        mf_Right(right, 'middle'),
        mf_Left(left, 'middle'),
        mf_Front(front, 'large') * mf_Left(right, 'small'),
        mf_Front(front, 'large') * mf_Left(left, 'small'),
        mf_Front(front, 'small')
    ]
    return max(min(40, center(input, output)),-40)

def frange(start, stop, step):
    i = start
    while i < stop:
        yield round(i, 1)
        i += step

def mf_Front(distance, cat):
    if cat == 'small':
        if distance < 3: return 1
        if distance < 10: return -distance/7 + 10/7
    elif cat == 'middle' or cat == 'large':
        if distance < 30: return 0
        else: return 1
    return 0

def mf_Left(distance, cat):
    if cat == 'small':
        if distance < 4: return 1
        if distance < 5: return distance + 5
    elif cat == 'middle':
        if distance < 4: return 0
        if distance < 10: return distance/6-4/6
        if distance < 16: return distance/6+16/6
    elif cat == 'large':
        if distance < 8: return 0
        if distance < 16: return distance/8-1
        return 1
    return 0

def mf_Right(distance, cat):
    if cat == 'small':
        if distance < 4: return 1
        if distance < 5: return -distance + 5
    elif cat == 'middle':
        if distance < 4: return 0
        if distance < 10: return distance/6-4/6
        if distance < 16: return -distance/6+16/6
    elif cat == 'large':
        if distance < 10: return 0
        if distance < 16: return distance/6-10/6
        return 1
    return 0

def weightAvg(input, output):
    A = B = 0
    for i in range(len(input)):
        A += input[i] * output[i]
        B += input[i]
    if abs(B) < 1e-6: return 0
    return A/B

def meanMax(input, output):
    g = []
    for i in range(7):
        g.append(getIntersection(input[i], output[i]))
    A = B = mxVal = 0
    for i in frange(-60,60,0.1):
        mx = 0
        for j in g: mx = max(mx, getVal(j, i))
        mxVal = max(mxVal, mx)
    for i in frange(-60,60,0.1):
        mx = 0
        for j in g: mx = max(mx, getVal(j, i))
        if abs(mxVal - mx) < 1e-5:
            A += i
            B += 1
    return A / B

def center(input, output):
    g = []
    for i in range(7):
        g.append(getIntersection(input[i], output[i]))
    A = B = mxVal = 0
    for i in frange(-60,60,0.1):
        mx = 0
        for j in g: mx = max(mx, getVal(j, i))
        mxVal = max(mxVal, mx)
        A += mx*i
        B += mx
    if abs(B) < 1e-6: return 0
    return A/B

def getIntersection(input, output):
    px = 100
    py = -100
    arr = []
    for i in range(len(output)-1):
        vx = output[i+1][0] - output[i][0]
        vy = output[i+1][1] - output[i][1]
        if abs(px-output[i][0]) > 1e-6 or abs(py - output[i][1]) > 1e-6:
            arr.append([output[i][0], min(output[i][1], input)])
            px = output[i][0]
            py = min(output[i][1], input)
        if abs(vy) >= 1e-6:
            x = output[i][0] + (input - output[i][1])/vy*vx
            if output[i][0] <= x and x <= output[i+1][0]:
                if abs(px-x) > 1e-6 or abs(py-input) > 1e-6:
                    arr.append([x, input])
                    px = x
                    py = input
        if abs(px-output[i+1][0]) > 1e-6 or abs(py - output[i+1][1]) > 1e-6:
            px = output[i + 1][0]
            py = min(output[i + 1][1], input)
            arr.append([px, py])
    r = []
    for i in range(len(arr)):
        r.append(arr[i])
    return r

def getVal(g, angle, alpha = 1):
    for i in range(len(g)-1):
        if g[i][0] <= angle and angle <= g[i+1][0]:
            vx = g[i+1][0] - g[i][0]
            vy = g[i+1][1] - g[i+1][1]
            if abs(vx) < 1e-6: return  min(g[i+1][1], alpha)
            y = g[i][1]+(angle-g[i][0])/vx*vy
            return min(y, 1)
    return 0

# 車子的運行與感測

ZERO = 1e-9
class Point(object):
    x = y =0
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
class Vector(object):
    def __init__(self, start_point, end_point):
        self.start, self.end = start_point, end_point
        self.x = end_point.x - start_point.x
        self.y = end_point.y - start_point.y
def negative(vector):
    return Vector(vector.end, vector.start)

def vector_product(vectorA, vectorB):
    return vectorA.x * vectorB.y - vectorB.x * vectorA.y
def is_intersected(A, B, C, D):
    """
    尋找汽車是否與邊界有交集
    :param A: 線A的X
    :param B: 線A的Y
    :param C: 線B的X
    :param D: 線B的Y
    :return: True, False
    """
    AC = Vector(A, C)
    AD = Vector(A, D)
    BC = Vector(B, C)
    BD = Vector(B, D)
    CA = negative(AC)
    CB = negative(BC)
    DA = negative(AD)
    DB = negative(BD)
    return (vector_product(AC, AD) * vector_product(BC, BD) <= ZERO) \
        and (vector_product(CA, CB) * vector_product(DA, DB) <= ZERO)

def GetLinePara(line):
    line.a =line.p1.y - line.p2.y
    line.b = line.p2.x - line.p1.x
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y

def GetCrossPoint(l1,l2):
    """
    找到兩線的焦點
    :param l1: 線A的X, Y
    :param l2: 線B的X, Y
    :return: 兩線的交點的座標點
    """
    GetLinePara(l1)
    GetLinePara(l2)
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p

def getDistanceFront(car, car2, point1, point2):
    """
    輸出汽車到邊界的距離
    :param car: 汽車射出距離線A點的X, Y
    :param car2: 汽車射出距離線B點的X, Y
    :param point1: 牆壁點A的X, Y
    :param point2: 牆壁點B的X, Y
    :return: 距離
    """
    p1 = Point(car[0], car[1])
    p2 = Point(car2[0], car2[1])
    p3 = Point(point1[0], point1[1])
    p4 = Point(point2[0], point2[1])
    crossPoint = GetCrossPoint(Line(p1, p2), Line(p3, p4))
    return ((car[0]-crossPoint.x)**2 + (car[1]-crossPoint.y)**2)**0.5, crossPoint

def car(pos, degree, fixX): # 畫出汽車
    pygame.draw.circle(gameDisplay, Red, [int(pos[0]), int(pos[1])], 6)

def carMove(x, y, angleNow, Role): # 傳入目前汽車的X, Y，輸出下一部汽車的位子與轉向角度
    """
    :param x: 目前汽車的 x
    :param y: 目前汽車的 y
    :param angleNow: 目前汽車的轉角
    :param Role: 要汽車轉幾度
    :return: 輸出汽車新位置的x, y, 和角度
    """
    xNext = x + math.cos(angleNow+Role) + math.sin(angleNow) * math.sin(Role)
    yNext = y + math.sin(Role + angleNow) - math.sin(Role) * math.cos(angleNow)
    angleNext = angleNow - math.asin((2*math.sin(Role))/6)
    return xNext, yNext, angleNext

def getLength(car, p1, p2): # 若目前汽車角度為垂直，輸出垂汽車對地圖邊界的長度
    a = ((car[0]-p1[0])**2+ (car[1]-p1[1])**2)**0.5
    b = ((car[0]-p2[0])**2+ (car[1]-p2[1])**2)**0.5
    c = ((p2[0]-p1[0])**2+ (p2[1]-p1[1])**2)**0.5
    s = (a + b + c) / 2
    area =  (s*(s-a)*(s-b)*(s-c)) ** 0.5 # getLength([5,8], [12,4], [3,2]) Ans: 25
    return (area*2)/c

def carSensor(car, degree, mapWall):
    """
    :param car: 汽車目前的[x, y]
    :param degree: 汽車目前的角度
    :param mapWall: 地圖的邊界 格式為: [[x1,y1], [x2,y2]....]
    :return: 汽車對 前、左、右 三個方向的到邊界的距離
    """
    temTop = disRight = disLeft = 99999
    if (degree/(math.pi/180))%90 == 0: # 若目前汽車的角度為垂直或垂橫，做下列動作
        rightPoint2 = math.tan(math.radians(45) + degree)*400
        leftPoint2 = math.tan(degree - math.radians(45))*400
        if (degree / (math.pi / 180))+9 < -180 :
            countRight = -400
            countLeft = 400
            rightPoint2 = -rightPoint2
        else:
            countLeft = -400
            countRight = 400
            leftPoint2 = -leftPoint2
        crossPointRight = crossPointLeft = crossPointFront = 0
        for n, i in enumerate(mapWall[:-1]):
            j = mapWall[n+1]
            a = ((car[0] - i[0]) ** 2 + (car[1] - i[1]) ** 2) ** 0.5
            b = ((car[0] - j[0]) ** 2 + (car[1] - j[1]) ** 2) ** 0.5
            if (((i[0]<=car[0] and j[0]>=car[0]) or (i[0]>=car[0] and j[0]<=car[0])) and (i[1]<=car[1] and j[1]<=car[1])) and a+b<temTop:
                temTop = a+b
                front = [i, j]
            if is_intersected(Point(i[0], i[1]), Point(j[0], j[1]), Point(car[0], car[1]),Point(car[0] + countLeft, leftPoint2 + car[1])):
                temLeft, temCrossPointLeft = getDistanceFront(car, [car[0] + countLeft, leftPoint2 + car[1]], i, j)
                if temLeft < disLeft:
                    disLeft = temLeft
                    crossPointLeft = temCrossPointLeft
            if is_intersected(Point(i[0], i[1]), Point(j[0], j[1]), Point(car[0], car[1]),Point(car[0] + countRight, rightPoint2 + car[1])):
                temRight, temCrossPointRight = getDistanceFront(car, [car[0] + countRight, rightPoint2 + car[1]], i, j)
                if temRight < disRight:
                    disRight = temRight
                    crossPointRight = temCrossPointRight
        if (degree/(math.pi/180)) == -90 or (degree/(math.pi/180)) == -180: pygame.draw.line(gameDisplay, Red, car, [car[0], -j[1]])
        else: pygame.draw.line(gameDisplay, Red, car, [i[0], car[1]])
        pygame.draw.line(gameDisplay, Green, car, [crossPointLeft.x, crossPointLeft.y])
        pygame.draw.line(gameDisplay, Blue, car, [crossPointRight.x, crossPointRight.y])
        return disLeft, disRight, getLength(car, front[0], front[1])
    else: # 若汽車角度不為垂直，也就是角度 % 90 != 0，做下面動作
        frontPoint2 = math.tan(degree)*400
        rightPoint2 = math.tan(math.radians(45) + degree)*400
        leftPoint2 = math.tan(degree - math.radians(45))*400
        crossPointRight = crossPointLeft = crossPointFront = 0
        # Front Fix
        if (degree/(math.pi/180)) > -90 or (degree/(math.pi/180)) < -270: countFront = 400
        else:
            countFront = -400
            frontPoint2 = -frontPoint2
        # Left Fix
        if (degree / (math.pi / 180)) >= -135 or (degree / (math.pi / 180)) <= -315:
            countRight = 400
        else: # (degree / (math.pi / 180)) < -135 :
            countRight = -400
            rightPoint2 = -rightPoint2
        # Right Fix
        if (degree / (math.pi / 180)) > -45 or (degree / (math.pi / 180)) < -225:
            countLeft = 400
        else:
            leftPoint2 = -leftPoint2
            countLeft = -400

        disLeft = disRight = disFront = 99999
        for n, i in enumerate(mapWall[:-1]):
            j = mapWall[n + 1]
            if is_intersected(Point(i[0], i[1]), Point(j[0], j[1]), Point(car[0], car[1]),Point(car[0]+countFront, car[1]+frontPoint2)):
                temFront, temcrossPointFront = getDistanceFront(car, [car[0] + countFront, frontPoint2+car[1]], i, j)
                if temFront<disFront:
                    disFront = temFront
                    crossPointFront = temcrossPointFront
            if is_intersected(Point(i[0], i[1]), Point(j[0], j[1]), Point(car[0], car[1]),Point(car[0] + countLeft, leftPoint2 + car[1])):
                temLeft, temCrossPointLeft = getDistanceFront(car, [car[0] + countLeft, leftPoint2 + car[1]], i, j)
                if temLeft < disLeft:
                    disLeft = temLeft
                    crossPointLeft = temCrossPointLeft
            if is_intersected(Point(i[0], i[1]), Point(j[0], j[1]), Point(car[0], car[1]),Point(car[0] + countRight, rightPoint2 + car[1])):
                temRight, temCrossPointRight = getDistanceFront(car, [car[0] + countRight, rightPoint2 + car[1]], i, j)
                if temRight < disRight:
                    disRight = temRight
                    crossPointRight = temCrossPointRight
        pygame.draw.line(gameDisplay, Red, car, [crossPointFront.x, crossPointFront.y])
        pygame.draw.line(gameDisplay, Green, car, [crossPointLeft.x, crossPointLeft.y])
        pygame.draw.line(gameDisplay, Blue, car, [crossPointRight.x, crossPointRight.y])
        return disLeft, disRight, disFront

# 畫圖

def readMap(name):
    with open(name, 'r') as f:
        data = f.read()
    return [i.split(',') for i in data.split('\n')]

def drawCarPath(carPath):
    pygame.draw.lines(gameDisplay, LightPink, False, carPath, 2)

def drawMap(mapWall):
    pygame.draw.lines(gameDisplay, Black, False, mapWall, 5)
def text_objects(text, font):
    textSurface = font.render(text, True, Red)
    return textSurface, textSurface.get_rect()

def noMap():
    while True:
        largeText = pygame.font.Font('freesansbold.ttf', 15)
        textSurf, textRect = text_objects('No map.txt or Method.txt found in your working direction', largeText)
        textRect.center = ((width / 2), (higth / 2))
        gameDisplay.fill(White)
        gameDisplay.blit(textSurf, textRect)
        pygame.display.update()
        clock.tick(60)
        time.sleep(5)
        pygame.quit()
        quit()

def success(name = 'screenShot'):
    textSurf, textRect = text_objects('Successsssssssss!', largeText)
    textRect.center = ((width / 2), (higth / 2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    clock.tick(60)
    rect = pygame.Rect(0, 0, higth, width)
    sub = gameDisplay.subsurface(rect)
    pygame.image.save(sub, name+".jpg")
    time.sleep(5)
    pygame.quit()
    quit()

def showCarInfo(left, right, top, degree):
    text = 'Left:'+str(int(left))+' Right:'+str(int(right))+' Top'+str(int(top))+' Degree'+str(round(degree/(math.pi/180), 2))
    textSurf, textRect = text_objects(text, middleText)
    textRect.center = ((width / 2) , 70)
    gameDisplay.blit(textSurf, textRect)

def showGameInfo():
    text = 'Press P to Pause. Auto Screenshot after game finish.'
    textSurf, textRect = text_objects(text, middleText)
    textRect.center = ((width / 2), 40)
    gameDisplay.blit(textSurf, textRect)

width = 600
higth = 600

Black = (0,0,0)
White = (255,255,255)
Red = (255, 0, 0)
Green  = (0, 255, 0)
Blue = (0,0,255)
LightPink = (255,165,232)

pygame.init()
gameDisplay = pygame.display.set_mode((width,higth))
pygame.display.set_caption('Auto Car')
clock = pygame.time.Clock()

largeText = pygame.font.Font('freesansbold.ttf', 30)
middleText = pygame.font.Font('freesansbold.ttf', 14)
windowCenter = ((width / 2) - 30, (higth / 2))
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('Black'))

def gameLoop():
    end = False
    zeroX = width*0.5
    zeroY = higth*0.9
    if not os.path.isfile('map.txt') or not os.path.isfile('Method.txt'):
        noMap()
    if not os.path.isdir('log/'):
        os.mkdir('log/')
    with open('Method.txt', 'r') as f: method = f.read()
    # carImg = pygame.image.load('car.png')
    mapInfo = readMap('map.txt')
    mapWall = []
    for i in mapInfo[3:]:
        mapWall.append([float(i[0]), float(i[1])])
    fixX = (width-max(mapWall[0]) - (0-min(mapWall[0])))//100
    # fixY = (higth-max(mapWall[1]) + (min(mapWall[1])))//100
    # carImg = pygame.transform.scale(carImg, (int(6*fixX), int(6*fixX)))
    car_x = (zeroX + float(mapInfo[0][0])*fixX)
    car_y = (zeroY + float(mapInfo[0][1])*fixX)
    car_degree = math.radians(-float(mapInfo[0][2]))
    print(zeroX-car_x, zeroY-car_y)
    for n, i in enumerate(mapWall):
        mapWall[n] = [zeroX+i[0]*fixX, zeroY-(i[1]*fixX)]
        print(zeroX+i[0]*fixX, zeroY-(i[1]*fixX))
    g1 = [zeroX + float(mapInfo[1][0]) * fixX, zeroY - (float(mapInfo[1][1]) * fixX)]
    g2 = [zeroX+float(mapInfo[2][0])*fixX, zeroY-(float(mapInfo[2][1])*fixX)]
    carLeft, carRight, carFront = carSensor([car_x, car_y], car_degree, mapWall)
    gameState = 1
    carPath = [[car_x, car_y],[car_x, car_y]]
    outputlg4D = []
    outputlg6D = []
    while not end:
        gameDisplay.fill(White)
        for event in pygame.event.get(): # get everything of the game information include mouse position
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: Roal = 15
                elif event.key == pygame.K_RIGHT: Roal = -15
                elif event.key == pygame.K_UP: Roal = 0
                elif event.key == pygame.K_DOWN: Roal = 180
                if event.key == pygame.K_p: gameState *= -1
                if event.key:
                    pass
        if gameState == 1:
            if method == 'FuzzyGravity':Roal = FuzzyGravity(carFront / fixX, carLeft / fixX, carRight / fixX)
            elif method == 'FuzzyMean': Roal = FuzzyMean(carFront / fixX, carLeft / fixX, carRight / fixX)
            elif method == 'Fuzzy': Roal = Fuzzy(carFront / fixX, carLeft / fixX, carRight / fixX)
            car_x, car_y, car_degree = carMove(car_x, car_y, car_degree, math.radians(Roal))
            carPath.append([car_x, car_y])
            if car_degree / (math.pi / 180) > 0: car_degree = math.radians(-360 + car_degree / (math.pi / 180))
            if car_degree / (math.pi / 180) < -360: car_degree = math.radians(car_degree / (math.pi / 180) + 360)
            pygame.draw.rect(gameDisplay, Green, [g1[0], g1[1], g2[0]-g1[0], g1[1]-g2[1]])
            carLeft, carRight, carFront = carSensor([car_x, car_y], car_degree, mapWall)
            drawCarPath(carPath)
            car([car_x, car_y], car_degree, fixX)
            drawMap(mapWall)
            showGameInfo()
            showCarInfo(carLeft, carRight, carFront, car_degree)
            outputlg4D.append(str(carFront/fixX) +' '+ str(carRight/fixX) +' '+ str(carLeft/fixX) +' '+ str(-round(Roal, 2)))
            outputlg6D.append(str((car_x-zeroX)/fixX) +' '+ str(-(car_y-zeroY)/fixX) +' '+ str(carFront/fixX) +' '+ str(carRight/fixX) +' '+ str(carLeft/fixX) +' '+ str(-round(Roal, 2)))
            if car_x > g1[0] and car_y < g2[1]:
                with open('log/log4D_'+method+'.txt', 'w') as f:
                    for i in outputlg4D:
                        f.write(i+'\n')
                with open('log/log6D_' + method+'.txt', 'w') as f:
                    for i in outputlg6D:
                        f.write(i+'\n')
                success(method)
        else:
            gameDisplay.blit(pause_text, windowCenter)
        pygame.display.update()
        clock.tick(15)


gameLoop()
pygame.quit()
quit()