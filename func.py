from variable import Variable
import random
import copy


class Func(Variable):
    # 七種一巡の法則になるようにネクストミノをランダムにリストに格納
    def nextMino(variable):
        if len(variable.nextList) == 0:
            variable.l = [0, 1, 2, 3, 4, 5, 6]
            for i in range(7):
                mino = random.choice(variable.l)
                variable.l.remove(mino)
                variable.nextList.append(mino)
        elif len(variable.l) == 0:
            variable.l = [0, 1, 2, 3, 4, 5, 6]
            next1 = variable.nextList[0]
            variable.nextList.remove(next1)
            mino = random.choice(variable.l)
            variable.l.remove(mino)
            variable.nextList.append(mino)
        else:
            next1 = variable.nextList[0]
            variable.nextList.remove(next1)
            mino = random.choice(variable.l)
            variable.l.remove(mino)
            variable.nextList.append(mino)
        return variable.nextList

    # SRS回転
    def srs(variable, rotate):
        for i in range(5):
            srsOffset_X = variable.SRSoffset[variable.minoType][variable.rotate][i][0] - \
                variable.SRSoffset[variable.minoType][rotate][i][0]
            srsOffset_Y = variable.SRSoffset[variable.minoType][variable.rotate][i][1] - \
                variable.SRSoffset[variable.minoType][rotate][i][1]
            ishit = Func.isHit(variable.minoX+srsOffset_X, variable.minoY -
                               srsOffset_Y, variable.minoType, rotate, variable)
            if not ishit:
                variable.minoX += srsOffset_X
                variable.minoY -= srsOffset_Y
                variable.rotate = rotate
                variable.lastcommand = True
                variable.offsetnum = i
                return

    def isSpin(variable):
        if(variable.minoType == 5 and variable.lastcommand):
            fill_corner_count = 0
            fill_pink_corner_count = 0
            for i in range(4):
                current_counter = fill_corner_count
                mino_X = variable.spinT[variable.rotate][i][0]
                mino_Y = variable.spinT[variable.rotate][i][1]
                if(variable.minoX+mino_X) < 0:
                    fill_corner_count += 1
                elif(variable.minoX+mino_X) >= variable.FIELD_WIDTH:
                    fill_corner_count += 1
                elif(variable.minoY+mino_Y) >= variable.FIELD_HEIGHT:
                    fill_corner_count += 1
                elif variable.field[variable.minoY+mino_Y][variable.minoX+mino_X]:
                    fill_corner_count += 1
                if (i == 0 or i == 1) and (fill_corner_count > current_counter):
                    fill_pink_corner_count += 1
            if fill_corner_count >= 3:
                if(fill_pink_corner_count == 2 or variable.offsetnum == 4):
                    return 1  # T-spin である
                else:
                    return 2  # T-spin mini である
            else:
                return 0  # T-spinではない
        return 0  # T-spinではない

    # ゲーム画面をリセット
    def regamefield(variable):
        variable.setreset()
        variable.nextList = []
        variable.minoX = 3
        variable.minoY = 0
        variable.rotate = 0
        variable.minoType = Func.nextMino(variable)[0]
        variable.holdMino = 100
        variable.changeCount = 0
        text = ""
        for i in range(variable.FIELD_HEIGHT):
            for j in range(variable.FIELD_WIDTH):
                variable.field[i][j] = 0
        variable.newField = copy.deepcopy(variable.field)
        for i in range(4):
            variable.newField[variable.minoY+variable.minoShapes[variable.minoType][variable.rotate][i][1]
                              ][variable.minoX+variable.minoShapes[variable.minoType][variable.rotate][i][0]] = 1
        for i in range(variable.FIELD_HEIGHT):
            for j in range(variable.FIELD_WIDTH):
                if variable.newField[i][j] == 0:
                    prints = "・"
                else:
                    prints = "■"
                text += prints
            if(i == 0):
                if(variable.holdMino == 100):
                    text += "hold:None\n"
                else:
                    text += f"hold:{variable.minoName[variable.holdMino]}\n"
            elif(i == 1):
                text += f"next1:{variable.minoName[variable.nextList[1]]}\n"
            elif(i == 2):
                text += f"next2:{variable.minoName[variable.nextList[2]]}\n"
            elif(i == 3):
                text += f"next3:{variable.minoName[variable.nextList[3]]}\n"
            else:
                text += "\n"
        text += f"Score:0"
        return text

    # 現在のゲーム画面
    def gamefield(variable):
        text = ""
        variable.newField = copy.deepcopy(variable.field)
        for i in range(4):
            variable.newField[variable.minoY+variable.minoShapes[variable.minoType][variable.rotate][i][1]
                              ][variable.minoX+variable.minoShapes[variable.minoType][variable.rotate][i][0]] = 1
        for i in range(variable.FIELD_HEIGHT):
            for j in range(variable.FIELD_WIDTH):
                if variable.newField[i][j] == 0:
                    prints = "・"
                else:
                    prints = "■"
                text += prints
            if(i == 0):
                if(variable.holdMino == 100):
                    text += "hold:None\n"
                else:
                    text += f"hold:{variable.minoName[variable.holdMino]}\n"
            elif(i == 1):
                text += f"next1:{variable.minoName[variable.nextList[1]]}\n"
            elif(i == 2):
                text += f"next2:{variable.minoName[variable.nextList[2]]}\n"
            elif(i == 3):
                text += f"next3:{variable.minoName[variable.nextList[3]]}\n"
            else:
                text += "\n"
        text += f"Score:{variable.score}"
        return text

    # Score管理
    def scorePlus(linecount, setflag):
        if(setflag):
            if(linecount == 0):
                score = 0
            elif(linecount == 1):
                score = 100
            elif(linecount == 2):
                score = 300
            elif(linecount == 3):
                score = 500
            elif(linecount == 4):
                score = 1200
        else:
            score = 1
        return score

    # ミノが壁や他のミノにぶつかるか判断する
    def isHit(X, Y, _minoType, _minoAngle, variable):
        for i in range(4):
            mino_X = variable.minoShapes[_minoType][_minoAngle][i][0]
            mino_Y = variable.minoShapes[_minoType][_minoAngle][i][1]
            if(X+mino_X) < 0:
                return True
            if(X+mino_X) >= variable.FIELD_WIDTH:
                return True
            if(Y+mino_Y) >= variable.FIELD_HEIGHT:
                return True
            if variable.field[Y+mino_Y][X+mino_X]:
                return True
        return False

    # そろってるLINEがあれば消す
    def checkField(variable):
        linecount = 0
        for i in range(variable.FIELD_HEIGHT):
            lineFill = True
            for j in range(variable.FIELD_WIDTH):
                if not variable.field[i][j]:
                    lineFill = False
            if lineFill:
                linecount += 1
                line = i
                for j in range(variable.FIELD_WIDTH):
                    variable.field[i][j] = 0
                for j in range(i+1):
                    if (line-1)>=0:
                        variable.field[line] = copy.deepcopy(variable.field[line-1])
                        line -= 1
                    else:
                        for z in range(variable.FIELD_WIDTH):
                            variable.field[line][z]=0
        variable.score += Func.scorePlus(linecount, True)

    # ミノを設置する
    def setMino(variable):
        spin = Func.isSpin(variable)
        # if spin == 1:
        #     print("T-spin")
        # elif spin == 2:
        #     print("T-spin mini")
        for i in range(4):
            mino_X = variable.minoShapes[variable.minoType][variable.rotate][i][0]
            mino_Y = variable.minoShapes[variable.minoType][variable.rotate][i][1]
            variable.field[variable.minoY+mino_Y][variable.minoX+mino_X] = 1
        Func.checkField(variable)
        variable.minoX = 3
        variable.minoY = 0
        variable.rotate = 0
        variable.changeCount = 0
        variable.minoType = Func.nextMino(variable)[0]
