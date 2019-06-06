import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 800)
# 帧率常量
FRAME_PER_SC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=5):

        # 父类不是object时，应该先用super()调用初始化方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        super().__init__("./images/background.jpg")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):

        super().__init__("./images/enemy.png")

        # 指定敌机的随机速度
        self.speed = random.randint(5, 10)

        # 指定敌机的随机初始位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):

        super().update()
        # 敌机飞出屏幕从精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            # 可以将精灵从所有精灵组中移出
            self.kill()


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        super().__init__("./images/hero_plane.png", 0)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):

        self.rect.x += self.speed

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width

    def fire(self):

        for i in range(3):

            bullet = Bullet()

            # 设置子弹位置
            bullet.rect.bottom = self.rect.y - i * 10
            bullet.rect.centerx = self.rect.centerx

            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):

        super().__init__("./images/bullet.png", -2)

    def update(self):

        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            # 可以将精灵从所有精灵组中移出
            self.kill()