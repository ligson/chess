# coding=utf-8
import pygame
from pygame.locals import *
from sys import exit
import math

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# 棋盘开始位置
startPosX = 50
startPosY = 50
startPos = (startPosX, startPosY)

# 棋格宽
uWidth = 32
# 棋盘列数
uSize = 19
# 棋盘线宽
lineSize = 3
# 旗子半径
cR = 10

# 输赢状态
win = False
winResult = []
winMsg = ""

# 所有交叉点
points = []
for i in xrange(0, 19):
    linePoints = []
    py = startPosY + i * uWidth
    for j in xrange(0, 19):
        px = startPosX + j * uWidth
        linePoints.append([px, py])
    points.append(linePoints)

screen = pygame.display.set_mode((800, 666), 0, 32)
pygame.display.set_caption("经典五子棋")
bg = pygame.image.load("assets/b2.jpg").convert()
mouse_cursor = pygame.image.load("assets/mouse.png").convert_alpha()
 #隐藏鼠标
pygame.mouse.set_visible(False)


class ChessManSet:
    manSet = []

    def add(self, chessMan):
        exist = False
        for cm in self.manSet:
            if cm.row == chessMan.row and cm.col == chessMan.col:
                exist = True
                break
        if not exist:
            self.manSet.append(chessMan)


# 所有的旗子集合
chessManSet = ChessManSet()


class Chessman:
    point = []
    color = ()
    idx = 0
    role = 1
    row = 0
    col = 0

    def render(self):
        pygame.draw.circle(screen, self.color, self.point, cR, 0)

    def __repr__(self):
        return "(row:" + str(self.row) + ";col:" + str(self.col) + ";role:" + str(self.role) + ")"


# 棋盘上所有棋子个数
chessCount = 0


# 返回同行之前所有棋子
def checkRowBefore(points, chessMan):
    if chessMan.col > 1:
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col - 1
        chessMan2.row = chessMan.row
        cm = existPoint(chessMan2)
        if cm is not None:
            checkRowBefore(points, cm)
            points.append(cm)


# 返回同行之后所有棋子
def checkRowAfter(points, chessMan):
    if chessMan.col < uSize:
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col + 1
        chessMan2.row = chessMan.row
        cm = existPoint(chessMan2)
        if cm is not None:
            checkRowAfter(points, cm)
            points.append(cm)


# 返回同行所有棋子
def checkRow(chessMan):
    points = []
    checkRowBefore(points, chessMan)
    points.append(chessMan)
    checkRowAfter(points, chessMan)
    return points


# 返回同列之上所有棋子
def checkColUp(points, chessMan):
    if chessMan.row > 1:
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col
        chessMan2.row = chessMan.row - 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkColUp(points, cm)
            points.append(cm)


# 返回同列之下所有棋子
def checkColDown(points, chessMan):
    if chessMan.row < uSize:
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col
        chessMan2.row = chessMan.row + 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkColDown(points, cm)
            points.append(cm)


# 返回同列所有棋子
def checkCol(chessMan):
    points = []
    checkColUp(points, chessMan)
    points.append(chessMan)
    checkColDown(points, chessMan)
    return points


# 所判断的棋子是否存在
def existPoint(chessMan):
    for point in chessManSet.manSet:
        if (chessMan.role == point.role) and (chessMan.col == point.col) and (chessMan.row == point.row):
            return point
    return None


# 返回左上所有棋子
def checkLeftUp(points, chessMan):
    if (chessMan.col > 1) and (chessMan.row > 1):
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col - 1
        chessMan2.row = chessMan.row - 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkLeftUp(points, cm)
            points.append(cm)


# 返回右下所有棋子
def checkRightDown(points, chessMan):
    if (chessMan.col < uSize) and (chessMan.row < uSize):
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col + 1
        chessMan2.row = chessMan.row + 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkRightDown(points, cm)
            points.append(cm)


# 斜着从左上到右下
def checkLeftRight(chessMan):
    points = []
    checkLeftUp(points, chessMan)
    points.append(chessMan)
    checkRightDown(points, chessMan)
    print points
    return points


# 返回右上所有棋子
def checkRightUp(points, chessMan):
    if (chessMan.col < uSize) and (chessMan.row > 1):
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col + 1
        chessMan2.row = chessMan.row - 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkRightUp(points, cm)
            points.append(cm)


# 返回左下所有棋子
def checkLeftDown(points, chessMan):
    if (chessMan.col > 1) and (chessMan.row < uSize):
        chessMan2 = Chessman()
        chessMan2.role = chessMan.role
        chessMan2.col = chessMan.col - 1
        chessMan2.row = chessMan.row + 1
        cm = existPoint(chessMan2)
        if cm is not None:
            checkLeftDown(points, cm)
            points.append(cm)


# 斜着从右上到左下
def checkRightLeft(chessMan):
    points = []
    checkRightUp(points, chessMan)
    points.append(chessMan)
    checkLeftDown(points, chessMan)
    return points


# 判断输赢
def check(chessMan):
    if len(chessManSet.manSet) >= 9:
        # 检查行
        rowPoints = checkRow(chessMan)
        if len(rowPoints) >= 5:
            return rowPoints
        # 检查列
        colPoints = checkCol(chessMan)
        if len(colPoints) >= 5:
            return colPoints
        # 检查从左上到右下
        l_r_points = checkLeftRight(chessMan)
        if len(l_r_points) >= 5:
            return l_r_points
        # 检查从右上到左下
        r_l_points = checkRightLeft(chessMan)
        if len(r_l_points) >= 5:
            return r_l_points
    return None


def drawBlodWin(chessMans):
    for chessMan in chessMans:
        pygame.draw.circle(screen, (255, 0, 0), chessMan.point, cR + 3, 3)


font = pygame.font.Font("assets/simkai.ttf", 40)


def drawString(msg, color, point):
    text_surface = font.render(unicode(msg), True, color)
    screen.blit(text_surface, point)


bgsound = pygame.mixer.Sound("assets/3399.wav")
bgsound.play(-1)
kasound = pygame.mixer.Sound("assets/5390.wav")

while True:
    for event in pygame.event.get():
        # print event.type
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONUP:
            if not win:
                mx, my = pygame.mouse.get_pos()
                print str(mx) + "," + str(my)
                for idx1, pointLine in enumerate(points):
                    for idx2, point in enumerate(pointLine):
                        len2 = math.sqrt((point[0] - mx) * (point[0] - mx) + (point[1] - my) * (point[1] - my))
                        if len2 < cR:
                            chessMan = Chessman()
                            chessMan.point = point
                            chessMan.idx = chessCount
                            if chessCount % 2 == 0:
                                chessMan.color = (0, 0, 0)
                                chessMan.role = 1
                            else:
                                chessMan.color = (255, 255, 255)
                                chessMan.role = 2
                            chessMan.row = idx1 + 1
                            chessMan.col = idx2 + 1
                            print "点击了第" + str(chessMan.row) + "行第" + str(chessMan.col) + "列"
                            chessCount += 1
                            chessManSet.add(chessMan)
                            result = check(chessMan)
                            kasound.play(1)
                            if result is not None:
                                win = True
                                winResult = result
                                winMsg = (u"黑棋赢" if chessMan.role == 1 else u"白棋赢")
                                print winMsg

    screen.blit(bg, (0, 0))
    for i in xrange(0, 19):
        # 横线
        pygame.draw.line(screen, (0, 0, 0), (startPosX, startPosY + i * uWidth),
                         (startPosX + uWidth * (uSize - 1), startPosY + i * uWidth), lineSize)
        # 竖线
        pygame.draw.line(screen, (0, 0, 0), (startPosX + i * uWidth, startPosY),
                         (startPosX + i * uWidth, startPosY + uWidth * (uSize - 1)), lineSize)
    # for pointLine in points:
    #     for point in pointLine:
    #         pygame.draw.circle(screen, (0, 0, 0), point, cR, 0)
    for chessMan in chessManSet.manSet:
        chessMan.render()
    drawBlodWin(winResult)
    if win:
        drawString(winMsg, (255, 0, 0), (250, 0))

    x, y = pygame.mouse.get_pos()
    # 获得鼠标位置
    #x -= mouse_cursor.get_width() / 2
    #y -= mouse_cursor.get_height() / 2
    # 计算光标的左上角位置
    screen.blit(mouse_cursor, (x, y))
    # 把光标画上去

    pygame.display.update()
