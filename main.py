# imports
import math
import random
import time
import pygame


pygame.init()

# constants
WIDTH = 800
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #initialize pygame window

pygame.display.set_caption("Target Showdown")

TARGETINCREMENT = 400
TARGETEVENT = pygame.USEREVENT

TARGETPADDING = 30

BACKGROUNDCOLOUR = (10, 70, 105) #rgb format (red, green, blue) (0,25,40)

LIVES = 3
TOP_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("helvetica", 24)

class Target:
    MAXSIZE = 30
    GROWTHRATE = 0.15
    COLOUR = "white"
    SECOND = "red"

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTHRATE >= self.MAXSIZE:
            self.grow = False
        if self.grow:
            self.size+= self.GROWTHRATE
        else:
            self.size -= self.GROWTHRATE

    def draw(self,win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND, (self.x, self.y), self.size * 0.4)


    def collide(self,x,y):
        dis = math.sqrt((x-self.x)**2 + (y-self.y) **2)
        return dis <= self.size



def draw(win, targets):
    win.fill(BACKGROUNDCOLOUR) #could also so standard colours

    for target in targets:
        target.draw(win) #pass window




def format_time(secs):
    milli = math.floor(int(secs*1000%1000)/100)
    seconds = int(round(secs%60,1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_HEIGHT)) #0,0 is top left coordinate. rest are dimentions of rectangle
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES-misses}", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (450,5))
    win.blit(lives_label, (650,5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BACKGROUNDCOLOUR)

    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2


def main():
    
    run = True
    targets = []
    clock = pygame.time.Clock()

    targetpressed = 0
    clicks = 0
    misses = 0
    start = time.time()

    pygame.time.set_timer(TARGETEVENT, TARGETINCREMENT) #set targetevent every targetincremement milliseconds

    
    while run:
        clock.tick(60) #regular fram rate, or else the target would appear and go away quickly
        click = False
        mouse_pos = pygame.mouse.get_pos() #stores tuple
        elapsed = time.time() -  start


        for event in pygame.event.get():
            if event.type == pygame.QUIT: #when close the window
                run = False
                break
            if event.type == TARGETEVENT:
                x = random.randint(TARGETPADDING, WIDTH-TARGETPADDING) #make sure it doesnt go out of measurement
                y = random.randint(TARGETPADDING + TOP_HEIGHT, HEIGHT - TARGETPADDING)
                target = Target(x,y) #initializing an instance of the target class
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target) #remove target when it has shurnken to size 0 
                misses += 1 #if didnt click

            if click and target.collide(*mouse_pos): #breaks tuple into x and y. same as mouse[0], mouse[1]
                targets.remove(target) 
                targetpressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed, targetpressed, clicks)
        
        draw(WIN, targets)
        draw_top(WIN, elapsed, targetpressed, misses)
        pygame.display.update()



    pygame.quit()

if __name__ == "__main__":
    main()
