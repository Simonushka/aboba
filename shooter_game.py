#Создай собственный Шутер!

from pygame import *
from random import randint
import time as timer

lost_ememies = 0
win_enemies = 0 
bullet_draw = 0
sprites_list = []
HP = 100
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 75))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.collideRect =  rect.Rect((335, 400), (40, 55))
        self.collideRect.midbottom = self.rect.midbottom
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        maslina = Bullet("bullet.png", 300, 300, 15)
        bullets.add(maslina)
        sound1.play
            
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (65, 45))
        self.rect.x = randint(20, 630)
    def update(self):
        self.rect.y += self.speed      
        if self.rect.y > 500:
            self.rect.y = -40
            self.rect.x = randint(0, 750)
            global lost_ememies  
            lost_ememies += 1 
        window.blit(self.image,(self.rect.x, self.rect.y))
        

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (20, 30))
        self.rect.y = player.rect.y
        self.rect.x = player.rect.x+5
    def update(self):
        window.blit(self.image,(self.rect.x+17, self.rect.y))
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.kill()

run = True 

R = 500
W = 700

window = display.set_mode((W, R))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
font.init()

font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
sound1 = mixer.Sound('fire.ogg')

clock = time.Clock()

FPS = 60

clock.tick(FPS)

display.update()

player = Player('rocket.png' ,335 , 400, 8)

zloy_4el_1 = Enemy("ufo.png", 0, -40, randint(0, 3))
zloy_4el_2 = Enemy("ufo.png", 0, -40, randint(0, 3))
zloy_4el_3 = Enemy("ufo.png", 0, -40, randint(0, 3))
zloy_4el_4 = Enemy("ufo.png", 0, -40, randint(0, 3))
zloy_4el_5 = Enemy("ufo.png", 0, -40, randint(0, 3))

monsters = sprite.Group()

monsters.add(zloy_4el_1)
monsters.add(zloy_4el_2)
monsters.add(zloy_4el_3)
monsters.add(zloy_4el_4)
monsters.add(zloy_4el_5)

bullets = sprite.Group()
maslina = Bullet("bullet.png", 300, 300, 8)


finish = True
time_2 = 0
while run:
    window.blit(background, (0,0))    
    keys = key.get_pressed()
    for e in event.get(): 
        if e.type == QUIT: 
            run = False
    if finish:
        window.blit(background, (0,0))   
        text_win = font1.render("Побеждено амёб: " + str(win_enemies), 1, (255, 255,255))
        window.blit(text_win, (10,10))
        text_lose = font1.render("Не побеждено амёб: " + str(lost_ememies), 1, (255, 255,255))
        window.blit(text_lose, (10, 41))
        text_hp = font1.render('HP' + str(HP), 1, (248, 255,1))
        window.blit(text_hp, (20, 470))
        player.reset()
        player.update()

        sprites_list = sprite.groupcollide(monsters, bullets, False, True)

        if keys[K_SPACE]:
            time_1 = timer.time()
            if time_1-time_2 >= 0.4:
                player.fire()
                time_2 = timer.time()
        if sprites_list:
            for i in sprites_list:
                i.rect.y = -40 
                i.rect.x = randint(0, 700)
                win_enemies += 1
                HP = HP + 10
        bullets.update() 
        monsters.update()  
        for e in event.get(): 
            if e.type == QUIT: 
                run = False
        if win_enemies >= 30:
            text_win1 = font1.render(('WIN'), 1, (255, 255,255))
            window.blit(text_win1, (350,250))
            finish = False
            if lost_ememies >= 30:
                run = False
        if lost_ememies >= 20:
            text_lose1 = font1.render(('LOSE'), 1, (255, 255,255))
            window.blit(text_lose1, (350,250))
            finish = False
            if lost_ememies >= 30:
                run = False
        hits = sprite.spritecollide(player, monsters, False)
        for i in hits:
            HP = HP - 1
        if HP <= 50:
            text_danger = font1.render(('The rocket is in danger'), 1, (254, 0, 0))
            window.blit(text_danger, (380,470))
        if HP <= 0:
            text_lose1 = font1.render(('LOSE'), 1, (255, 255,255))
            window.blit(text_lose1, (350,250))
            finish = False
        display.update()
        clock.tick(FPS)