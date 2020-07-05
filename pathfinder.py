import math
import pygame
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

screen = pygame.display.set_mode((600, 600))


class Point:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def add_neighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row-1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])


# Colors
red = (255, 0, 0)
green = (49, 203, 27)
blue = (0, 0, 255)
grey = (220, 220, 220)

cols = 50
grid = [0 for i in range(cols)]
row = 50
openSet = []
closedSet = []
w = 600 / cols
h = 600 / row
cameFrom = []


for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Create a Point with x and y for each 'cell' in the grid
for i in range(cols):
    for j in range(row):
        grid[i][j] = Point(i, j)


# Default start and end point if none are selected
start = grid[7][12]
end = grid[38][41]

# Show the points on the screen
for i in range(cols):
    for j in range(row):
        grid[i][j].show((255, 255, 255), 1)

# Draw border and disable those points
for i in range(0, row):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].show(grey, 0)
    grid[i][row-1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True

# Set custom start and finish
def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
openSet.append(start)


def mouse_press(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // cols)
    g2 = w // (600 // row)
    access = grid[g1][g2]
    if access != start and access != end:
        if not access.obs:
            access.obs = True
            access.show((255, 255, 255), 0)


end.show((255, 213, 0), 0)
start.show((255, 213, 0), 0)


loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mouse_press(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

# Set left, right, bottom and top neighbor for each point
for i in range(cols):
    for j in range(row):
        grid[i][j].add_neighbors(grid)


def heuristic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    return d


def main():
    end.show((255, 213, 0), 0)
    start.show((255, 213, 0), 0)
    if len(openSet) > 0:
        lowest_index = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest_index].f:
                lowest_index = i

        current = openSet[lowest_index]
        if current == end:
            start.show((255, 213, 0),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 213, 0), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The shortest distance \n to the path is ' + str(temp) + ' blocks away.'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                again = True
                while again:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            again = False
                            break
            pygame.quit()

        openSet.pop(lowest_index)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                temp_g = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > temp_g:
                        neighbor.g = temp_g
                else:
                    neighbor.g = temp_g
                    openSet.append(neighbor)

            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous is None:
                neighbor.previous = current
    if var.get():
        for i in range(len(openSet)):
            openSet[i].show(green, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].show(red, 0)
    current.closed = True


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
