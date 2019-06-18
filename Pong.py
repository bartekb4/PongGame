import pygame
import sys
import random
import math
import Configure as c

FRAME_DELAY = 5                             #kolorki i inne stałę
ROUND_WIN_DELAY = 500
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (129, 203, 248)
BROWN = (222, 184, 135)
PLAYER_MOVEMENT_UNITS = 5

COMP=c.comp
RACKET_WIDTH = c.rWidth
RACKET_HEIGHT = c.rHeight
SCREEN_W = c.scWidth
SCREEN_H = c.scHeight                   #przekazanie konfiguracji z modułu configure
comp_MOVEMENT_UNITS = c.diff
BALL_DEFAULT_SPEED = c.ballspeed
BALL_RADIUS=c.ballsize
class Ball:
    def __init__(self):
        self.x=0
        self.y=0
        self.radius=BALL_RADIUS
        self.color=GREEN
        self.speed=BALL_DEFAULT_SPEED                       #tworzy się obiekt ball
        self.dir_x=1
        self.dir_y=1

    def change_dir_x(self):
        self.dir_x*=-1

    def change_dir_y(self):
        self.dir_y *=-1

    def throw(self):
        self.x=SCREEN_W//2                                          #metoda to wprowadzania piłki
        self.y=SCREEN_H//2
        self.dir_x=1 if random.randint(0,1) % 2 else -1
        self.speed=BALL_DEFAULT_SPEED

    def move(self):                                                    #ruchy piłki
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def keep_screen(self):
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_H:    #pilka nie wypada z ekranu góra
            self.dir_y *= -1

    def leave_screen(self):
        return self.x + self.radius < 0 or self.x - self.radius > SCREEN_W      #piłka wypada z boku

class Racket:
    def __init__(self, x, color=GREEN):
        self.x=x
        self.y=SCREEN_H//2                                              #tworzy się obiekt racket
        self.width=RACKET_WIDTH
        self.height=RACKET_HEIGHT
        self.g_line_x=x+RACKET_WIDTH if x <SCREEN_W//2 else x
        self.color=color
        self.score=0
        self.pred_y=None

    def collides_with_ball(self, ball):
        left_side_hit, left_side_overlap = self.__collides_with_ball(ball, self.x)                  #jej zderzenie z piłką
        if left_side_hit:
            return left_side_hit, left_side_overlap

        right_side_hit, right_side_overlap = self.__collides_with_ball(ball, self.x + self.width)
        return right_side_hit, right_side_overlap




    def __collides_with_ball(self, ball, x):
        a = 1
        b = -2 * ball.y
        c = ball.y ** 2 + x ** 2 - 2 * x * ball.x + ball.x ** 2 - ball.radius ** 2     #tu rozwiązania równań ruchu piłku
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            #brak rozwiązan, piłka nie dociera do 'bramki'
            return (False, False)
        elif discriminant == 1:
            # jedno rozwiazanie, pilka zderza sie z rakietka
            y = (-b + (math.sqrt(discriminant))) / (2 * a)
            return (True, self.y < y < self.y + self.height)
        else:
            #dwa rozwiazania, rakieka i pilka zderzaja sie w dwoch miejscach
            # points, this is due to the increments of the ball movement
            sqrt_discriminant = math.sqrt(discriminant)
            y0 = (-b + (sqrt_discriminant)) / (2 * a)
            y1 = (-b - (sqrt_discriminant)) / (2 * a)
            return (True, self.y < y0 < self.y + self.height or self.y < y1 < self.y + self.height)


def comp_pred (ball,comp):
    pred_dir=ball.dir_y
    y=ball.y
    for x in range(ball.x+ball.radius, comp.x, ball.speed):    #komputer przewiduje ruchy piłki
        if y-ball.radius<0 or y+ball.radius>SCREEN_H:
            pred_dir*=-1
        y+=ball.speed*pred_dir
    return y

def ai_move(ball,comp):
    if not round_win and ball.dir_x == 1 and ball.x>SCREEN_W//2:
         pred_y=comp.pred_y or comp_pred(ball,comp)                                             #komputer sie rusza
         if pred_y > 0 and pred_y < SCREEN_H and (pred_y < comp.y or pred_y > comp.y + comp.height):
                comp.y += comp_MOVEMENT_UNITS * (-1 if pred_y < comp.y else 1)

def display_text(text, x, y):
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, WHITE)
    screen.blit(textsurface, (x, y))



pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Pong')
pygame.font.init()                                                      #inicjalizacja obietów w grze z pygame

ball = Ball()
ball.throw()
player = Racket(x = 30, color = LIGHT_BLUE)
comp = Racket(x = SCREEN_W - RACKET_WIDTH-40, color = BROWN)
player2=Racket(x = SCREEN_W - RACKET_WIDTH- 40, color = GREEN)
round_win = None
tick = 0
last_key = 1

while True:
    pygame.time.delay(FRAME_DELAY)
    screen.fill(BLACK)

    ball.move()
    ball.keep_screen()

    if round_win and ball.leave_screen():                       #wynik sie nalicza
        round_win.score += 1
        round_win = None
        ball.throw()
        pygame.time.delay(ROUND_WIN_DELAY)
        continue

    player_goal_reached, player_defended = player.collides_with_ball(ball)
    #pilka przekracza linie bramki The ball crosses the goal line
    if player_goal_reached:
        # player odbija pilke, lecimy dalej
        if not round_win and player_defended:
            ball.change_dir_x()
            if last_key:
                ball.direction_y = last_key
        #player nie odbil komputer zdobywa punkt
        elif not round_win and not player_defended:
            if COMP==1:
                round_win = comp
            elif COMP==0:
                round_win=player2
        #odbilo sie ale krzywo i wypadlo poza bramke
        elif round_win and player_defended:
            ball.change_dir_y()

    if COMP==0: # dla zera sterujemy playerem2
        player2_goal_reached, player2_defended = player2.collides_with_ball(ball)
        # pilka przekracza linie bramki The ball crosses the goal line
        if player2_goal_reached:
            #player odbija pilke, lecimy dalej
            if not round_win and player2_defended:
                ball.change_dir_x()
                if last_key:
                    ball.direction_y = last_key
            # komputer zdobywa punkt
            elif not round_win and not player2_defended:
                round_win = player
            # odbilo sie ale krzywo i wypadlo poza bramke
            elif round_win and player2_defended:
                ball.change_dir_y()
    elif COMP==1: #dla 1 komputer przejmuje sterowanie
        comp_goal_reached, comp_defended = comp.collides_with_ball(ball)
        if comp_goal_reached:
            if not round_win and comp_defended:
                ball.change_dir_x()
            elif not round_win and not comp_defended:
                round_win = player
            elif round_win and comp_defended:
                ball.change_dir_y()

    tick += 1
    if tick % 1000 == 0:
        ball.speed += 1


    # ruchy komputera
    if COMP==1:
        ai_move(ball, comp)


    if COMP==1:
        display_text('Computer', SCREEN_W/2+SCREEN_W/6, 0)
        display_text(str(comp.score), SCREEN_W/2+SCREEN_W/4, 45)
        pygame.draw.rect(screen, comp.color, (comp.x, comp.y, comp.width, comp.height), 0)
    elif COMP==0:
        display_text('Player2', SCREEN_W/2+SCREEN_W/4, 0)
        display_text(str(player2.score), SCREEN_W/2+SCREEN_W/4, 45)
        pygame.draw.rect(screen, player2.color, (player2.x, player2.y, player2.width, player2.height), 0)
    display_text('Player', SCREEN_W/2-SCREEN_W/6, 0)
    display_text(str(player.score), SCREEN_W/2-SCREEN_W/4, 45)
    pygame.draw.rect(screen, player.color, (player.x, player.y, player.width, player.height), 0)
    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)
    for i in range(1, SCREEN_H // 10):
        if i % 2 == 0:
            pygame.draw.rect(screen, WHITE, (SCREEN_W // 2, i * 10, 10, 10), 0)
    pygame.display.update()




    #klawisze i inne ruchy
    #player1
    last_key = None
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        player.score=0
        player2.score=0
        comp.score=0

#pause and unpause
    if keys[pygame.K_p]:

        not ball.move()
        BALL_DEFAULT_SPEED=0
        PLAYER_MOVEMENT_UNITS=0

    if keys[pygame.K_u]:
        BALL_DEFAULT_SPEED=c.ballspeed
        PLAYER_MOVEMENT_UNITS=c.diff


#changing ball speed
    if keys[pygame.K_1]:
        BALL_DEFAULT_SPEED=1
    if keys[pygame.K_2]:
        BALL_DEFAULT_SPEED = 2
    if keys[pygame.K_3]:
        BALL_DEFAULT_SPEED = 3
    if keys[pygame.K_4]:
        BALL_DEFAULT_SPEED = 4
    if keys[pygame.K_5]:
        BALL_DEFAULT_SPEED = 5
    if keys[pygame.K_6]:
        BALL_DEFAULT_SPEED = 6
    if keys[pygame.K_7]:
        BALL_DEFAULT_SPEED = 7
    if keys[pygame.K_8]:
        BALL_DEFAULT_SPEED = 8
    if keys[pygame.K_9]:
        BALL_DEFAULT_SPEED = 9

    if keys[pygame.K_w]:
        goal_reached, overlap = player.collides_with_ball(ball)
        if goal_reached and player.y - PLAYER_MOVEMENT_UNITS < ball.y + ball.radius:
            continue
        player.y = 0 if player.y - PLAYER_MOVEMENT_UNITS < 0 else player.y - PLAYER_MOVEMENT_UNITS
        last_key = -1

    if keys[pygame.K_s]:
        goal_reached, overlap = player.collides_with_ball(ball)
        if goal_reached and player.y + player.height + PLAYER_MOVEMENT_UNITS > ball.y - ball.radius:
            continue
        player.y = SCREEN_H - player.height if player.y + player.height + PLAYER_MOVEMENT_UNITS > SCREEN_H else player.y + PLAYER_MOVEMENT_UNITS
        last_key = 1
    #player2
    if COMP==0:
        #{
        keys = pygame.key.get_pressed()
     #   if keys[pygame.K_UP]:
      #      goal_reached, overlap = player2.collides_with_ball(ball)
      #      if goal_reached and player2.y - PLAYER_MOVEMENT_UNITS < ball.y + ball.radius:
      #          continue
      #      player2.y = 0 if player2.y - PLAYER_MOVEMENT_UNITS < 0 else player2.y - PLAYER_MOVEMENT_UNITS
    #      last_key = -1
#
 #       if keys[pygame.K_DOWN]:
  #          goal_reached, overlap = player2.collides_with_ball(ball)
   #         if goal_reached and player2.y + player2.height + PLAYER_MOVEMENT_UNITS > ball.y - ball.radius:
    #            continue
     #       player2.y = SCREEN_H - player2.height if player2.y + player2.height + PLAYER_MOVEMENT_UNITS > SCREEN_H else player2.y + PLAYER_MOVEMENT_UNITS
      #      last_key = 1
            #}

    #sterowanie myszka
    for event in pygame.event.get():
        (mouseX, mouseY)=pygame.mouse.get_rel()
        if mouseY<=0:
            goal_reached, overlap = player2.collides_with_ball(ball)
            if goal_reached and player2.y - PLAYER_MOVEMENT_UNITS < ball.y + ball.radius:
                continue
            player2.y = 0 if player2.y - PLAYER_MOVEMENT_UNITS < 0 else player2.y - PLAYER_MOVEMENT_UNITS
            last_key = -1

        if mouseY>0:
            goal_reached, overlap = player2.collides_with_ball(ball)
            if goal_reached and player2.y + player2.height + PLAYER_MOVEMENT_UNITS > ball.y - ball.radius:
                continue
            player2.y = SCREEN_H - player2.height if player2.y + player2.height + PLAYER_MOVEMENT_UNITS > SCREEN_H else player2.y + PLAYER_MOVEMENT_UNITS
            last_key = 1

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()  #wyjscie esc









