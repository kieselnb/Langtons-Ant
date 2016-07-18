'''
Created on Oct 22, 2015

@author: nick
'''

import tkinter
import threading

lock = threading.Lock()

def main():
    root = tkinter.Tk()
    root.title("Langton's Ant")
    gridBlocks = []

    blockWidth = 10

    canvasWidth = blockWidth * 190
    canvasHeight = blockWidth * 100

    canvas = tkinter.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES, padx=10, pady=10)

    root.maxsize(canvasWidth + 22, canvasHeight + 22)
    root.minsize(canvasWidth + 22, canvasHeight + 22)

    medianIndex = int(((canvasWidth / blockWidth) * (canvasHeight / blockWidth)) / 2)

    total = 1
    for k in range(int(canvasWidth / blockWidth)):
        gridBlocks.append([])
        for j in range(int(canvasHeight / blockWidth)):
#             if total % 1000 == 0:
#                 color = 'black'
#             else:
#                 color = 'white'
            color = 'white'
            newBlock = canvas.create_rectangle(k * blockWidth, j * blockWidth, (k + 1) * blockWidth, (j + 1) * blockWidth, outline='black', fill=color)
            gridBlocks[k].append(newBlock)
            total += 1
            if total == medianIndex:
                center_x = canvas.coords(newBlock)[0]
                center_y = int(canvas.coords(newBlock)[1] - (int(j / 2) * blockWidth))
                rowIndex = int(j / 2)
                columnIndex = k

    ants = []

    ant1 = Ant(root, canvas, center_x, center_y, blockWidth, gridBlocks)
    ant1.Direction = 'Up'
    ant1.RowIndex = rowIndex
    ant1.ColumnIndex = columnIndex
    ants.append(ant1)

#     ant2 = Ant(root, canvas, center_x, center_y, blockWidth, gridBlocks)
#     ant2.Direction = 'Up'
#     ant2.RowIndex = rowIndex
#     ant2.ColumnIndex = columnIndex
#     ants.append(ant2)
#
#     ant3 = Ant(root, canvas, center_x, center_y, blockWidth, gridBlocks)
#     ant3.Direction = 'Up'
#     ant3.RowIndex = rowIndex
#     ant3.ColumnIndex = columnIndex
#     ants.append(ant3)

    root.bind('<space>', lambda event: MultiThreadUpdate(root, ants))

    root.mainloop()

def start(root, ant):

    count = 0
    while ant.Quit:
        ant.Move()
        count += 1
        root.title("Langton's Ant - Step " + str(count))
        root.update()

def Stop(ants):
    for ant in ants:
        ant.Quit = False

def Exit(root):
    root.destroy()

class Ant():
    def __init__(self, Root, Canvas, x_Pos, Y_Pos, Size, Blocks):
        self.Direction = None
        self.Size = Size
        self.Quit = True
        self.RowIndex = None
        self.ColumnIndex = None
        self.Canvas = Canvas
        self.Root = Root
        self.Blocks = Blocks
        self.MoveCount = 0

        self.Tag = Canvas.create_oval(x_Pos, Y_Pos, x_Pos + self.Size, Y_Pos + self.Size, fill='hot pink')

    def Move(self):
        self.MoveCount += 1
        for k in range(self.ColumnIndex - 1, self.ColumnIndex + 2):
            for j in range(self.RowIndex - 1, self.RowIndex + 2):
                if self.Canvas.coords(self.Blocks[k][j]) == self.Canvas.coords(self.Tag):
                    thisBlock = self.Blocks[k][j]
                    self.RowIndex = j
                    self.ColumnIndex = k
                    break
        with lock:
            if self.Canvas.itemcget(thisBlock, "fill") == 'white':
                color = 'black'
                turn = "RightHand"
            else:
                color = 'white'
                turn = "LeftHand"
            self.Canvas.itemconfigure(thisBlock, fill=color)

        if self.Direction == "Up":
            y_Move = 0
            if turn == 'RightHand':
                self.Direction = "Right"
                x_Move = self.Size
            else:
                self.Direction = 'Left'
                x_Move = -self.Size
        elif self.Direction == 'Right':
            x_Move = 0
            if turn == 'RightHand':
                self.Direction = 'Down'
                y_Move = self.Size
            else:
                self.Direction = 'Up'
                y_Move = -self.Size
        elif self.Direction == 'Down':
            y_Move = 0
            if turn == 'RightHand':
                self.Direction = 'Left'
                x_Move = -self.Size
            else:
                self.Direction = 'Right'
                x_Move = self.Size
        elif self.Direction == 'Left':
            x_Move = 0
            if turn == 'RightHand':
                self.Direction = 'Up'
                y_Move = -self.Size
            else:
                self.Direction = 'Down'
                y_Move = self.Size

        self.Canvas.move(self.Tag, x_Move, y_Move)

def MultiThreadUpdate(root, Ants):
    root.unbind('<space>')
    root.bind('<space>', lambda event: Stop(Ants))
    root.bind('<x>', lambda event: Exit(root))

    for ant in Ants:
        thisThread = threading.Thread(target=start, args=(root, ant,))
        thisThread.start()

if __name__ == "__main__":
    main()
