# Импортируем модули
import pygame as pg
import json
import random

# Инициализация pg
pg.init()

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80

DOG_HEIGHT = 500
DOG_WIDTH = 310

BUTTON_HEIGHT = 60
BUTTON_WIDTH = 200

FOOD_SIZE = 200
TOY_SIZE = 100

GRID = 10

fps = 60

font = pg.font.Font(None, 40)
font_mini = pg.font.Font(None, 25)
font_maxi = pg.font.Font(None, 200)

# Начало игры
new_game = {
    "happiness": 20,
    "satiety": 30,
    "health": 20,
    "money": 20,
    "max_score": 0,
    "clothes": [
        {
            "name": "Синяя футболка",
            "price": 15,
            "image": "images/items/blue t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Ботинки",
            "price": 50,
            "image": "images/items/boots.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Шляпа",
            "price": 50,
            "image": "images/items/hat.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Бант",
            "price": 70,
            "image": "images/items/bow.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Кепка",
            "price": 75,
            "image": "images/items/cap.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Златая цепь с дуба",
            "price": 100,
            "image": "images/items/gold chain.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Красная футболка",
            "price": 10,
            "image": "images/items/red t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Очки",
            "price": 80,
            "image": "images/items/sunglasses.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Желтая футболка",
            "price": 20,
            "image": "images/items/yellow t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Серебрянная цепь",
            "price": 85,
            "image": "images/items/silver chain.png",
            "is_using": False,
            "is_bought": False
        }
    ],
    "food": [
        {
            "name": "Яблоко",
            "price": 15,
            "image": "images/food/apple.png",
            "efficiency": 10,
            "is_bought": False,
            "medicine": 1
        },
        {
            "name": "Кость",
            "price": 30,
            "image": "images/food/bone.png",
            "efficiency": 20,
            "is_bought": False,
            "medicine": 1
        },
        {
            "name": "Первоклассный корм",
            "price": 70,
            "image": "images/food/dog food elite.png",
            "efficiency": 30,
            "is_bought": False,
            "medicine": 7
        },
        {
            "name": "Корм",
            "price": 50,
            "image": "images/food/dog food.png",
            "efficiency": 15,
            "is_bought": False,
            "medicine": 1
        },
        {
            "name": "Мясо https://clck.ru/3J55Ej",
            "price": 40,
            "image": "images/food/meat.png",
            "efficiency": 25,
            "is_bought": False,
            "medicine": 5
        },
        {
            "name": "Лекарство",
            "price": 30,
            "image": "images/food/medicine.png",
            "efficiency": 1,
            "is_bought": False,
            "medicine": 15
        }
    ]
}
# Создаем функции
def load_image(file:str, size:tuple):
    """
    Функция для обработки картинок.
    """
    image = pg.image.load(file)
    image = pg.transform.scale(image, size)
    return image
def text_render(text:str|int|float, arg_font=font, color="black"):
    """
    Функция для преобразования текста в "картинку".
    """
    return arg_font.render(str(text), True, color)

# Класс кнопка
class Button:
    """
    Класс "Кнопка"
    """
    def __init__(self, text, x, y, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, text_font=font, func=None):
        self.func = func

        self.image = load_image("images/button.png", (width, height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, "black")

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        """
        Функция для отрисовки кнопки.
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def is_clicked(self, event):
        """
        Функция для осуществления функции кнопки.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.func()

# Класс "Меню одежды"
class ClothesMenu():
    def __init__(self, game, data={}):
        # Меню
        self.game = game
        self.data = data
        self.menu_page = load_image("images/menu/menu_page.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.menu_rect = self.menu_page.get_rect()
        self.items = []
        # Одежда
        for item in data:
            clothes_item = Item(*item.values())
            self.items.append(clothes_item)
        self.current_item = 0
        self.render_item()
        # Индикаторы
        self.indicator_dict = {
            True: "on",
            False: "off"
        }
        # Куплено
        self.indicator_bought = load_image(f"images/menu/top_label_{self.indicator_dict[self.data[self.current_item]["is_bought"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bought_dict = {
            True: "Куплено",
            False: "Не куплено"
        }
        self.is_bought_text = text_render(self.bought_dict[self.data[self.current_item]["is_bought"]], arg_font=font_mini)
        self.bought_text_rect = self.is_bought_text.get_rect()
        self.bought_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*13)
        self.bought_rect = self.indicator_bought.get_rect()
        self.bought_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        # Надето
        self.using_dict = {
            True: "Надето",
            False: "Не надето"
        }
        self.indicator_using = load_image(f"images/menu/bottom_label_{self.indicator_dict[self.data[self.current_item]["is_using"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.is_using_text = text_render(self.using_dict[self.data[self.current_item]["is_using"]], arg_font=font_mini)
        self.using_text_rect = self.is_using_text.get_rect()
        self.using_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*20)
        self.using_rect = self.indicator_using.get_rect()
        self.using_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        # Кнопки перемещения одежды
        self.next_button = Button("Вперед", SCREEN_WIDTH-BUTTON_WIDTH-GRID*10, SCREEN_HEIGHT-GRID*14, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.next_item)
        self.previous_button = Button("Назад", GRID*14, SCREEN_HEIGHT-14*GRID, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.previous_item)
        # Кнопки "одеть" и "купить"
        self.buy_button = Button("Купить", SCREEN_WIDTH//2 - int(BUTTON_WIDTH//1.3)//2, SCREEN_HEIGHT-GRID*18, width=int(BUTTON_WIDTH//1.3), height=int(BUTTON_HEIGHT//1.3), func=self.buy)
        self.use_button = Button("Надеть", GRID*14, SCREEN_HEIGHT-15*GRID-BUTTON_HEIGHT, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.use)
        self.take_of_button = Button("Снять", SCREEN_WIDTH-BUTTON_WIDTH-GRID*10, SCREEN_HEIGHT-15*GRID-BUTTON_HEIGHT, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.take_of)

    def draw(self, screen, game):
        screen.blit(self.menu_page, self.menu_rect)
        screen.blit(self.items[self.current_item].image, self.item_rect)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.indicator_bought, self.bought_rect)
        screen.blit(self.indicator_using, self.using_rect)
        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.buy_button.draw(screen)
        self.use_button.draw(screen)
        self.take_of_button.draw(screen)
        screen.blit(self.is_bought_text, self.bought_text_rect)
        screen.blit(self.is_using_text, self.using_text_rect)

        # Индикаторы        
        game.money_surface = text_render(game.money)
        screen.blit(game.money_surface, (20*GRID, 11*GRID)) 
          
        screen.blit(game.money_image, (10*GRID, 7*GRID))
        
    def render_item(self):
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH//2, GRID*18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH//2, GRID*12)

        self.bought_dict = {
            True: "Куплено",
            False: "Не куплено"
        }
        self.using_dict = {
            True: "Надето",
            False: "Не надето"
        }
        self.indicator_dict = {
            True: "on",
            False: "off"
        }

        self.indicator_bought = load_image(f"images/menu/top_label_{self.indicator_dict[self.data[self.current_item]["is_bought"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.is_bought_text = text_render(self.bought_dict[self.data[self.current_item]["is_bought"]], arg_font=font_mini)
        self.bought_text_rect = self.is_bought_text.get_rect()
        self.bought_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*13)

        self.is_using_text = text_render(self.using_dict[self.data[self.current_item]["is_using"]], arg_font=font_mini)
        self.using_text_rect = self.is_using_text.get_rect()
        self.using_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*20)

        self.indicator_using = load_image(f"images/menu/bottom_label_{self.indicator_dict[self.data[self.current_item]["is_using"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

    def next_item(self):
        if self.current_item+1 < len(self.data):
            self.current_item += 1
        else:
            self.current_item = 0
        self.render_item()

    def previous_item(self):
        if self.current_item-1 >= 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.data)-1
        self.render_item()

    def buy(self):
        if self.data[self.current_item]["price"] < self.game.money and self.data[self.current_item]["is_bought"] == False:
            self.game.money -= self.data[self.current_item]["price"]
            self.data[self.current_item]["is_bought"] = True
            self.items[self.current_item].is_bought = True
        self.render_item()

    def use(self):
        if self.data[self.current_item]["is_using"] == False and self.data[self.current_item]["is_bought"] == True:
            self.data[self.current_item]["is_using"] = True
            self.items[self.current_item].is_using = True
        self.render_item()

    def take_of(self):
        if self.data[self.current_item]["is_using"] == True and self.data[self.current_item]["is_bought"] == True:
            self.data[self.current_item]["is_using"] = False
            self.items[self.current_item].is_using = False
        self.render_item()
# Класс "Меню еды"
class FoodMenu():
    def __init__(self, game, data={}):
        # Меню
        self.game = game
        self.data = data
        self.menu_page = load_image("images/menu/menu_page.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.menu_rect = self.menu_page.get_rect()
        self.items = []
        # Еда
        for item in data:
            food_item = Food(*item.values())
            self.items.append(food_item)
        self.current_item = 0
        self.render_item()
        # Индикаторы
        self.indicator_dict = {
            True: "on",
            False: "off"
        }
        # Куплено
        self.indicator_bought = load_image(f"images/menu/top_label_{self.indicator_dict[self.data[self.current_item]["is_bought"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bought_dict = {
            True: "Куплено",
            False: "Не куплено"
        }
        self.is_bought_text = text_render(self.bought_dict[self.data[self.current_item]["is_bought"]], arg_font=font_mini)
        self.bought_text_rect = self.is_bought_text.get_rect()
        self.bought_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*13)
        self.bought_rect = self.indicator_bought.get_rect()
        self.bought_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        # Кнопки перемещения еды
        self.next_button = Button("Вперед", SCREEN_WIDTH-BUTTON_WIDTH-GRID*10, SCREEN_HEIGHT-GRID*14, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.next_item)
        self.previous_button = Button("Назад", GRID*14, SCREEN_HEIGHT-14*GRID, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.previous_item)
        # Кнопки "съесть" и "купить"
        self.buy_button = Button("Купить", SCREEN_WIDTH//2 - int(BUTTON_WIDTH//1.3)//2, SCREEN_HEIGHT-GRID*18, width=int(BUTTON_WIDTH//1.3), height=int(BUTTON_HEIGHT//1.3), func=self.buy)
        self.eat_button = Button("Съесть", GRID*14, SCREEN_HEIGHT-15*GRID-BUTTON_HEIGHT, width=int(BUTTON_WIDTH//1.2), height=int(BUTTON_HEIGHT//1.2), func=self.eat)

    def draw(self, screen, game):
        screen.blit(self.menu_page, self.menu_rect)
        screen.blit(self.items[self.current_item].image, self.item_rect)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.indicator_bought, self.bought_rect)
        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.buy_button.draw(screen)
        self.eat_button.draw(screen)
        screen.blit(self.is_bought_text, self.bought_text_rect)
        # Индикаторы
        game.health_surface = text_render(game.health)
        screen.blit(game.health_surface, (20*GRID, 18*GRID))

        game.satiety_surface = text_render(game.satiety)
        screen.blit(game.satiety_surface, (20*GRID, 11*GRID))
        
        game.money_surface = text_render(game.money)
        screen.blit(game.money_surface, (SCREEN_WIDTH-23*GRID, 19*GRID)) 
          
        screen.blit(game.money_image, (SCREEN_WIDTH-20*GRID, 15*GRID))
        screen.blit(game.satiety_image, ((10*GRID, 7*GRID)))
        screen.blit(game.health_image, (10*GRID, 14*GRID))

        self.add_health = text_render(f"+{self.items[self.current_item].medicine}", color="#5f8f21")
        screen.blit(self.add_health, (25*GRID, 18*GRID))

        self.add_satiety = text_render(f"+{self.items[self.current_item].efficiency[0]}", color="#5f8f21")
        screen.blit(self.add_satiety, (25*GRID, 11*GRID))


    def render_item(self):
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH//2, GRID*18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH//2, GRID*12)

        self.bought_dict = {
            True: "Куплено",
            False: "Не куплено"
        }

        self.indicator_dict = {
            True: "on",
            False: "off"
        }

        self.indicator_bought = load_image(f"images/menu/top_label_{self.indicator_dict[self.data[self.current_item]["is_bought"]]}.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.is_bought_text = text_render(self.bought_dict[self.data[self.current_item]["is_bought"]], arg_font=font_mini)
        self.bought_text_rect = self.is_bought_text.get_rect()
        self.bought_text_rect.center = (SCREEN_WIDTH-20*GRID, GRID*13)

    def next_item(self):
        if self.current_item+1 < len(self.data):
            self.current_item += 1
        else:
            self.current_item = 0
        self.render_item()
    def previous_item(self):
        if self.current_item-1 >= 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.data)-1
        self.render_item()
    def buy(self):
        if self.data[self.current_item]["price"] < self.game.money and self.data[self.current_item]["is_bought"] == False:
            self.game.money -= self.data[self.current_item]["price"]
            self.data[self.current_item]["is_bought"] = True
            self.items[self.current_item].is_bought = True
        self.render_item()

    def eat(self):
        if self.data[self.current_item]["is_bought"] == True:
            self.data[self.current_item]["is_bought"] = False
            self.game.satiety += self.data[self.current_item]["efficiency"]
            self.game.health += self.data[self.current_item]["medicine"]
            self.items[self.current_item].is_bought = False
        self.render_item()

# Класс "Предмет" (одежда)
class Item:
    def __init__(self, name, price, file, is_using, is_bought):
        self.name = name
        self.price = price
        self.image = load_image(file, (DOG_WIDTH//1.7, DOG_HEIGHT//1.7))
        self.is_using = is_using
        self.is_bought = is_bought
        self.full_image = load_image(file, (DOG_WIDTH, DOG_HEIGHT))
# Класс "Еда"
class Food:
    def __init__(self, name, price, file, efficiency, is_bought, medicine):
        self.name = name
        self.price = price
        self.image = load_image(file, (FOOD_SIZE, FOOD_SIZE))
        self.efficiency = efficiency,
        self.is_bought = is_bought,
        self.medicine = medicine
# Класс "Мини-игра"
class MiniGame:
    def __init__(self, game):
        self.bg = load_image("images/game_background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.max_score = game.max_score
        self.new_game()
    def new_game(self):
        self.score = 0
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.start_time = pg.time.get_ticks()

    def update(self, screen, game):
        if random.randint(1, 100) > 93:
            self.toys.add(Toy())
        screen.blit(self.bg, (0, 0))
        self.dog.update(screen)
        screen.blit(text_render(f"Score: {self.score}", font_mini), (13*GRID, 12*GRID))
        screen.blit(text_render(f"Max score: {self.max_score}", font_mini), (13*GRID, 10*GRID))
        self.toys.update()
        self.toys.draw(screen)

        # Столкновение
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_circle_ratio(0.5))
        for hit in hits:
            self.score += hit.score_add
        if pg.time.get_ticks() - self.start_time > 40000:
            game.happiness += round(self.score//10)
            if self.score > self.max_score:
                self.max_score = self.score
            game.mode = "main"
# Спрайт собаки
class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/dog.png", (DOG_WIDTH//2, DOG_HEIGHT//2))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH//2
        self.rect.centery = SCREEN_HEIGHT - GRID*14

    def update(self, screen):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if  self.rect.x >= 9*GRID:
                self.rect.x -= 15
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.rect.x <= SCREEN_WIDTH - self.rect.width - 8*GRID:
                self.rect.x += 15
        screen.blit(self.image, self.rect)

# Класс "Игрушка"
class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        toy_dict = {
            "ball": 5,
            "blue bone": 10,
            "red bone": 15
        }
        self.type = random.choice(list(toy_dict.keys()))
        self.image = load_image(f"images/toys/{self.type}.png", (70, 70))
        self.score_add = toy_dict[self.type]
        self.speed = toy_dict[self.type]*2

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(9*GRID, SCREEN_WIDTH - self.rect.width - 8*GRID)
        self.rect.y = -10
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Игровой цикл
class Game:
    def __init__(self):
        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")
        # Время
        self.clock = pg.time.Clock()
        # Отрисовываем иконки
        self.background = load_image("images/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.character_image = load_image("images/dog.png", (310, 500))
        self.money_image = load_image("images/money.png", (100, 100))
        self.health_image = load_image("images/health.png", (100, 100))
        self.satiety_image = load_image("images/satiety.png", (100, 100))
        self.happiness_image = load_image("images/happiness.png", (100, 100))
        with open("save.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
            self.happiness = self.data["happiness"]
            self.money = self.data["money"]
            self.health = self.data["health"]
            self.satiety = self.data["satiety"]
            self.max_score = self.data["max_score"]
        # Создаем события
        self.INCREASE_COINS = pg.USEREVENT + 1
        self.DECREASE = pg.USEREVENT + 2
        # Создаем кнопки
        self.eat_button = Button("Еда", SCREEN_WIDTH-GRID-BUTTON_WIDTH, 10*GRID, func=self.food_menu_on)
        self.clothes_button = Button("Одежда", SCREEN_WIDTH-GRID-BUTTON_WIDTH, 12*GRID+BUTTON_HEIGHT, func=self.clothes_menu_on)
        self.play_button = Button("Игра", SCREEN_WIDTH-GRID-BUTTON_WIDTH, 14*GRID+2*BUTTON_HEIGHT, func=self.mini_game_on)
        # Каждую секунду увеличиваем кол-во монеток
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        pg.time.set_timer(self.DECREASE, 1000)
        self.mode = "main"
        # Создаем меню
        self.clothes_menu = ClothesMenu(self, data=self.data["clothes"])
        self.food_menu = FoodMenu(self, data=self.data["food"])
        self.mini_game = MiniGame(self)
        # Запускаем игровой цикл
        self.run()


    def clothes_menu_on(self):
        """
        Меню "Одежда".
        """
        self.mode = "clothes"
    
    def food_menu_on(self):
        """
        Меню "Еда".
        """
        self.mode = "food"
    
    def mini_game_on(self):
        self.mode = "mini game"
        self.mini_game.new_game()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                with open("save.json", "w", encoding="utf-8") as file:
                    self.data["clothes"] = self.clothes_menu.data
                    self.data["food"] = self.food_menu.data
                    self.data["happiness"] = self.happiness
                    self.data["satiety"] = self.satiety
                    self.data["health"] = self.health
                    self.data["money"] = self.money
                    self.data["max_score"] = self.mini_game.max_score
                    json.dump(self.data, file, ensure_ascii = False)
                pg.quit()
                exit()
            if event.type == self.INCREASE_COINS:
                self.money += 1
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += 1
            if event.type == self.DECREASE:
                if random.randint(1, 10) >= 7:
                    self.satiety -= 1
                elif random.randint(1, 10) >= 8:
                    self.happiness -= 1
                elif random.randint(1, 10) >= 9:
                    self.health -= 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.mode == "mini game":
                        self.happiness += round(self.mini_game.score//10)
                        if self.mini_game.score > self.mini_game.max_score:
                            self.mini_game.max_score = self.mini_game.score
                    self.mode = "main"
            if self.mode == "main":
                self.eat_button.is_clicked(event)
                self.clothes_button.is_clicked(event)
                self.play_button.is_clicked(event)
            if self.mode == "clothes":
                self.clothes_menu.next_button.is_clicked(event)
                self.clothes_menu.previous_button.is_clicked(event)
                self.clothes_menu.buy_button.is_clicked(event)
                self.clothes_menu.use_button.is_clicked(event)
                self.clothes_menu.take_of_button.is_clicked(event)
            if self.mode == "food":
                self.food_menu.next_button.is_clicked(event)
                self.food_menu.previous_button.is_clicked(event)
                self.food_menu.buy_button.is_clicked(event)
                self.food_menu.eat_button.is_clicked(event)

    def update(self):
        if self.satiety <= 0 or self.happiness <= 0 or self.health <= 0:
            self.mode = "game_over"
            with open("save.json", "w", encoding="utf-8") as file:
                json.dump(new_game, file, ensure_ascii = False)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        self.character_rect = self.character_image.get_rect()
        self.character_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.screen.blit(self.character_image, (self.character_rect.x, 100))
        self.screen.blit(self.money_image, (780, GRID))
        self.screen.blit(self.satiety_image, (20, GRID))
        self.screen.blit(self.health_image, (20, 80))
        self.screen.blit(self.happiness_image, (20, 150))

        if self.happiness <= 10:
            self.sad_face = load_image("images/sad_face.png", (DOG_WIDTH, SCREEN_HEIGHT))
            self.sad_rect = self.sad_face.get_rect()
            self.sad_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 7.4*GRID)
            self.screen.blit(self.sad_face, self.sad_rect)
        if self.happiness >= 70:
            self.happy_face = load_image("images/happy_face.png", (DOG_WIDTH, SCREEN_HEIGHT))
            self.happy_rect = self.happy_face.get_rect()
            self.happy_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 7.4*GRID)
            self.screen.blit(self.happy_face, self.happy_rect)
        if self.health <= 5:
            self.sick_face = load_image("images/sick_face.png", (DOG_WIDTH, SCREEN_HEIGHT))
            self.sick_rect = self.sick_face.get_rect()
            self.sick_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 7.4*GRID)
            self.screen.blit(self.sick_face, self.sick_rect)
        
        self.health_surface = text_render(self.health)
        self.screen.blit(self.health_surface, (115, 120))

        self.satiety_surface = text_render(self.satiety)
        self.screen.blit(self.satiety_surface, (115, 50))

        self.happiness_surface = text_render(self.happiness)
        self.screen.blit(self.happiness_surface, (115, 190))
        
        self.money_surface = text_render(self.money)
        self.screen.blit(self.money_surface, (740, 50))

        self.clothes_button.draw(self.screen)
        self.eat_button.draw(self.screen)
        self.play_button.draw(self.screen)
        if self.mode == "game_over":
            self.screen.blit(self.background, (0, 0))
            self.game_over_text = text_render("Game over!")
            self.game_over_rect = self.game_over_text.get_rect()
            self.game_over_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            self.screen.blit(self.game_over_text, self.game_over_rect)
        if self.mode == "clothes":
            self.clothes_menu.draw(self.screen, self)
        if self.mode == "food":
            self.food_menu.draw(self.screen, self)
        if self.mode == "mini game":
            self.mini_game.update(self.screen, self)
        if self.mode == "main":
            for item in self.clothes_menu.items:
                if item.is_bought and item.is_using:
                    item.rect = item.full_image.get_rect()
                    item.rect.centery = self.character_rect.centery + 7.4*GRID
                    item.rect.centerx = self.character_rect.centerx
                    self.screen.blit(item.full_image, item.rect)

    def run(self):
        while True:
            self.update()
            self.event()
            self.draw()
            # Следующий кадр
            pg.display.flip()
            self.clock.tick(fps)

if __name__ == "__main__":
    Game()