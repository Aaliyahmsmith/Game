# finalProject.py 
#
# Made By: Aaliyah and Mamadou
# Date: 11/12/21
#
# This is a game in which the person playing will have to run left to right
# trying to avoid the bombs being thrown from the plane above while simultaneously
# trying to collect the coins that will randomly be appearing on the ground.
# The goal is to collect as many coins as you can to gain as much points as you can
# before you are hit with a bomb and lose the game.

 

import pygame
from random import randint

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("siren.wav")


 

# Constants:
WIDTH  = 900
HEIGHT = 600
CENTER = (WIDTH//2, HEIGHT//2)


INIT_TICK  = 5
# Some basic color names
BLACK     = (0,0,0)
RED       = (255,0,0)
GREEN     = (0,255,0)
BLUE      = (0,0,255)
YELLOW    = (255,255,0)
MAGENTA   = (255,0,255)
CYAN      = (0,255,255)
WHITE     = (255,255,255)
 

TITLE_BG  = MAGENTA
REPLAY_BG = (0,0,127)
GAME_BG   = WHITE
END_BG    = CYAN
WIN_CLR      = (110, 255, 100)
LOSE_CLR     = (128, 0, 0)
END_CLR      = (0, 255, 255)
WIN_LBL_CLR  = (128, 0, 0)
LOSE_LBL_CLR = (110, 255, 100)

PLAYER_DX = 15
BOMB_DY = 20
NUM_BOMBS =10
 

# Background fill colors for the various screens
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Aaliyah and Mamadou")
background = pygame.Surface(screen.get_size())
yay = pygame.mixer.Sound("yay.wav")
boo = pygame.mixer.Sound("boo.wav")
bombsound = pygame.mixer.Sound("bomb.wav")
island = pygame.mixer.Sound("island.wav")
coinsound = pygame.mixer.Sound("coinsound.wav")

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)    # Initialize the sprite.
        self.image = pygame.image.load("plane.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1, 1)) )
        self.image = pygame.transform.scale(self.image, (120,120))
        self.rect = self.image.get_rect()
        self.rect.centery = 50
        self.dx = randint(6,10)  # Either positive or negative

       

    #  self.update() - Move the car left or right across the screen, with wrap.
    def update(self):


        self.rect.centerx += self.dx        # Move the car horizontally.


        # If the car moves off-screen, wrap it to come back in from the other side
        if self.rect.right < 0:
            self.rect.left = screen.get_width()
        elif self.rect.left > screen.get_width():
            self.rect.right = 0

    def get_pos(self):
        return self.rect.center

 
 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("playertwo.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1, 1)) )
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.center = (750, 560)

        

 

    def moveleft(self):
        if (self.rect.left > 0):
            self.rect.centerx -= PLAYER_DX

    def moveright(self):
        if (self.rect.right < screen.get_width()):
            self.rect.centerx += PLAYER_DX

    def get_pos(self):
        return self.rect.center

            



class Bomb(pygame.sprite.Sprite):

 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1, 1)) )
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.dy = 0
        self.shooting = False


    def fire(self, plane_pos):
        if not self.shooting:
            self.rect.center = plane_pos
            self.dy = BOMB_DY
            self.shooting = True

    
    def update(self):
        if self.shooting:                                   
            self.rect.centery += self.dy

    def reset(self):
        self.rect.center = (-100, -100)    
        self.dy = 0
        self.shooting = False


        
class Coins(pygame.sprite.Sprite):
    
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)    # Initialize the sprite.
        self.image = pygame.image.load("coin.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1, 1)) )
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.center = position

    def reposition(self, coinGroup):
        self.rect.centerx = randint(2, (screen.get_width()))
        self.rect.centery = randint(545,550)
       
        #while( pygame.sprite.spritecollide(self, coinGroup, False) ) :
           # self.rect.centerx = randint(3, (screen.get_width()))
           # self.rect.centery = randint(545,550)

class Label(pygame.sprite.Sprite):

 
    def __init__(self, textStr, center, fontType, fontSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontType, fontSize)
        self.text = textStr
        self.center = center
        self.textColor = textColor
 


    def update(self):
        self.image = self.font.render(self.text, 1, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.center = self.center
 

def titleScreen():
    background = pygame.image.load("war.png")
    background = background.convert()
    screen.blit(background,(0,0))
    island.play()
    #pygame.mixer.music.play(-1)
    #background = pygame.Surface(screen.get_size()) # Construct a background
    #background = background.convert()
    #background.fill(TITLE_BG)   # Clear the background
    #screen.blit(background, (0,0))
 
    titleMsg = Label("Surviver!", (screen.get_width()//2, 100), None, 90, BLACK)
    playMsg = Label("Aim of the game: Collect coins while simultaneously avoiding the bombs", (screen.get_width()//2, 190), None, 30, BLACK)
    directMsg = Label("Use the left and right arrow keys to move", (screen.get_width()//2, 230), None, 30, BLACK)

   
    labelGroup = pygame.sprite.Group(titleMsg, playMsg, directMsg)
    clock = pygame.time.Clock()
    keepGoing = True


    while keepGoing: 
        clock.tick(20)
 

        for event in pygame.event.get():      # Handle any events
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # Title screen ends
                keepGoing = False
            elif event.type == pygame.KEYDOWN:         # or any key pressed
                keepGoing = False

                                                      
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)
        pygame.display.flip()

 

def game():

    background = pygame.image.load("war.png")
    background = background.convert()
    screen.blit(background,(0,0))
    island.stop()
    pygame.mixer.music.play(-1)
    count = 0
    timer = 20
    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill( GAME_BG )
    #screen.blit(background, (0,0))
    pygame.mixer.music.play(-1)
    coinGroup = pygame.sprite.Group()
    player = Player()
    bomb = Bomb()
    plane = Plane()
    coins = Coins((randint(0,screen.get_width()),randint(540,550 )))
    #coins = Coins()
    coins.reposition(coinGroup)

    allsprites = pygame.sprite.Group(plane, coins, bomb, player)
    
    timerMsg = Label("Timer: {timer}", (120,40), None, 30,(0,0,0))
    counterMsg = Label("Coins Collected: 0", (780,40), None, 30,(0,0,0))
    labelGroup = pygame.sprite.Group(timerMsg,counterMsg)
    
    clock = pygame.time.Clock()    
    keepGoing = True               
    win = False                    
    shooting = False
    count = 0
    timer = 20
    frames = 0
    
    while keepGoing:
        clock.tick(30)
        shooting = True
        bomb.fire(plane.get_pos())
        
        
        for event in pygame.event.get():      # Handle any events
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False
                #elif event.key == pygame.K_SPACE:

                    #if shooting == False:
                       # bomb.fire(plane.get_pos())
                       # shooting = True

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                player.moveleft()
        elif keys[pygame.K_RIGHT]:
                player.moveright()

        if pygame.sprite.collide_rect(bomb, player) :
            win = False
            keepGoing = False
            bomb.reset()

        
        
        if pygame.sprite.collide_rect(coins, player) :      
            coins.reposition(coinGroup) 
            count = count + 1
            print(count)
            coinsound.play()
            

        # Check if the bomb missed the target (i.e. if it went off the right 
        #             side of the screen.  If it missed, update the count of 
        #             remaining bombs and move the bomb sprite offstage by
        #             calling its reset() method.                    
        if bomb.rect.top >= screen.get_height() :
            shooting = False  # Update the scoreboard
            bomb.reset()
            bombsound.play()
        # Check if all bombs are used up. If so, the player has not won the game.
        frames = frames + 1
        if frames == 30:
            frames = 0
            timer = timer - 1

        if timer == 0:
            keepGoing = False
            win = False

        if count == 5:
            keepGoing = False
            win = True
            
        timerMsg.text=(f"Time Remaining: {timer}")
        counterMsg.text=(f"Coins Collected: {count}")

        allsprites.clear(screen, background)
        labelGroup.clear(screen, background)
        
        allsprites.update()
        labelGroup.update()
        
        allsprites.draw(screen)
        labelGroup.draw(screen)
        
        pygame.display.flip()
        
    return win, count,timer


def playAgain(winLose,count,timer):
    background = pygame.image.load("war.png")
    background = background.convert()
    
    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill( REPLAY_BG )    # Fill the background
    # Blit background to screen
    if winLose:
        fillColor = WIN_CLR
        labelText = "You Win!!"
        labelmessage = (f"You collected {count} coins with {timer} seconds remaining!")
        labelColor = BLACK
        pygame.mixer.music.stop() 
        yay.play()
        
        
    else:
        fillColor = LOSE_CLR
        labelText = "You Lose..."
        labelmessage = (f"You collected {count} coins with {timer} seconds remaining!")
        labelColor = BLACK
        pygame.mixer.music.stop() 
        boo.play()
        
    #### Add code here to construct Label sprites that:
    ####    Display a message about whether the player won or lost
    ####    Ask the player if they want to play again
    #### Then add your Label sprites to labelGroup
    screen.blit(background,(0,0))
    label0 = Label(labelText, (450,100), None, 60, labelColor)
    #label2 = Label("You Win!", (450,120), None, 60, (0,0,0))
    #label2 = Label("You Lose!", (450,120), None, 60, (0,0,0))
    label5 = Label("Try Again? Y/N",(450,170), None, 50, (0,0,0)) 
    msgCount = Label(labelmessage, (450,230), None, 35, labelColor)
    
    labelGroup = pygame.sprite.Group(label5,label0, msgCount) 
     
    clock = pygame.time.Clock()
    keepGoing = True
    replay = False

    while keepGoing:
    
        clock.tick(30)  

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:         # or any key pressed
                keepGoing = False
                if event.key == pygame.K_y:
                    replay = True
                
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        pygame.display.flip()
        
    return replay
 

def endScreen():
    background = pygame.image.load("gameova.png")
    background = background.convert()
    screen.blit(background,(0,0))
   # background = pygame.Surface(screen.get_size()) # Construct a background
    #background = background.convert()
    #background.fill(END_CLR)
    #screen.blit(background, (0,0))   # Blit background to screen only once.
 

    # Construct a Label object to display the message and add it to a group.
    #label1 = Label("Thanks for Playing!", (450,80), None, 60, (WHITE))
    #labelGroup = pygame.sprite.Group( label11, label2, label3 )
    label2 = Label("Aaliyah and Mamadou", (450,50), None, 40, (WHITE))
    label3 = Label("11/18/2021", (450,550), None, 40, (WHITE))
    labelGroup = pygame.sprite.Group( label2, label3 )
 

    clock = pygame.time.Clock()
    keepGoing = True
    frames = 0                  # 5 seconds will be 150 frames
 
    while keepGoing:
   
        clock.tick(30)          # Frame rate 30 frames per second.
        frames = frames + 1     # Count the number of frames displayed
        if frames == 150:        # After 5 seconds end the message display
            keepGoing = False
 
        for event in pygame.event.get():    # Impatient people can quit earlier
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN or
                event.type == pygame.MOUSEBUTTONDOWN) :
                keepGoing = False
 
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)
       
        pygame.display.flip()
 


def main():
 
    titleScreen()
 
    replay = True
 
    while replay == True:
        win, count,timer = game()
        replay = playAgain(win,count,timer)   
        
    endScreen()
 
 
main()
pygame.quit()
