#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

window = display.set_mode((700, 500))#создай окно игры
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

win_width =700
win_height = 500

game = True
finish = False

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

kick = mixer.Sound('fire.ogg')
score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


player = Player('rocket.png', 320, 400, 5, 70, 90)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 5), 80,50)
    monsters.add(monster)

bullets = sprite.Group()


font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 96)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                kick.play()
                player.fire()
    if finish != True:
        window.blit(background, (0,0))
        text_lose = font1.render('Пропушено: ' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Уничтожено: ' + str(score),1, (255, 255, 255))
        
#        if lost >= 3:
#            lose = font2.render('Ты проиграл', True, (255, 0, 0))
#            window.blit(lose, (140,200))
#            finish = True
#        if lost < 3:
        player.update()
        monsters.update()
        bullets.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        sprite_list = sprite.groupcollide(bullets, monsters, True, True)
        for s in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 5), 80,50)
            monsters.add(monster)
   
        text_lose = font1.render('Пропушено: ' + str(lost), 0, (255, 255, 255))
        text_win = font1.render('Уничтожено: ' + str(score),0, (255, 255, 255))
        window.blit(text_lose, (10,50))
        window.blit(text_win, (10,20))


        if score >= 10:
            win = font2.render('Ты выиграл', True, (255, 255, 0))
            text_lose = font1.render('Пропушено: ' + str(lost), 0, (255, 255, 255))
            text_win = font1.render('Уничтожено: ' + str(score),0, (255, 255, 255))
            window.blit(text_lose, (10,50))
            window.blit(text_win, (10,20))
            window.blit(win, (140,200))
            finish = True

        if lost >= 5 or sprite.spritecollide(player, monsters, False, False):
            lose = font2.render('Ты проиграл', True, (255, 0, 0))
            text_lose = font1.render('Пропушено: ' + str(lost), 0, (255, 255, 255))
            text_win = font1.render('Уничтожено: ' + str(score),0, (255, 255, 255))
            window.blit(text_lose, (10,50))
            window.blit(text_win, (10,20))
            window.blit(lose, (140,200))
            finish = True
        
    else:
        time.delay(3000)
        finish = False
        player.kill()
        score = 0
        lost = 0
        player = Player('rocket.png', 320, 400, 5, 70, 90) 
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()

        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 5), 80,50)
            monsters.add(monster)
        

    
        
    display.update()
    clock.tick(FPS)
