from pygame import *
from random import randint

init()

win_width = 700
win_height = 500

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

lost = 0
score = 0

run = True

finish = False
f = font.Font(None, 36)

FPS = 60

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = transform.scale(image.load(img_back), (win_width, win_height))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, img, x, y, w, h, speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed

        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        bul = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bul)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.speed = randint(1, 3)
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    x = randint(80, win_width - 80)
    speed = randint(1, 3)
    monster = Enemy(img_enemy, x, -40, 80, 50, speed)
    monsters.add(monster)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background, (0, 0))

        text_score = f.render(f"Рахунок: {score}", True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_score = f.render(f"Пропущено: {lost}", True, (255, 255, 255))
        window.blit(text_score, (10, 50))

        ship.update()
        ship.reset()

        monsters.update()
        bullets.update()

        bullets.draw(window)
        monsters.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(80, win_width - 80)
            speed = randint(1, 3)
            monster = Enemy(img_enemy, x, -40, 80, 50, speed)
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 10:
            finish = True
            lose = f.render("YOU LOSE!! HAHA", True, (200, 50, 50))
            window.blit(lose, (200, 200))

        if score >= 30:
            finish = True
            lose = f.render("YOU WIN!!", True, (200, 255, 200))
            window.blit(lose, (200, 200))
        


        display.update()
    clock.tick(FPS)
