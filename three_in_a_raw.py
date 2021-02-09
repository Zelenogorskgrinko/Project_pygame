import pygame
import random
import os


# сновной игровой процесс
class Three:
    def __init__(self):
        self.n = 8
        self.otstup = 25
        self.cell_size = 50
        self.border = 2
        self.diamonds = []
        self.temp1, self.temp2 = None, None
        self.flag = False
        self.plus1, self.plus2, self.plus3, self.plus4 = 0, 0, 0, 0
        self.check = []
        self.drop = 0
        self.count = 0
        # рандомное заполнение поля
        for i in range(self.n):
            self.diamonds.append([])
            for j in range(self.n):
                choice = random.choice([1, 2, 3, 4, 5, 6])
                while (j > 1 and choice == self.diamonds[i][j - 1] and choice == self.diamonds[i][j - 2]) or \
                        (i > 1 and choice == self.diamonds[i - 1][j] and choice == self.diamonds[i - 2][j]):
                    choice = random.choice([1, 2, 3, 4, 5, 6])
                self.diamonds[i].append(choice)

    # отрисовка кадра
    def render(self, canvas):
        # работа со сдвигами спрайтов
        flag = False
        for i in range(self.n):
            if self.diamonds[i][0] is None and self.drop % self.cell_size == 0:
                self.diamonds[i][0] = random.choice([1, 2, 3, 4, 5, 6])
                while self.diamonds[i][0] == self.diamonds[i][1] == self.diamonds[i][2]:
                    self.diamonds[i][0] = random.choice([1, 2, 3, 4, 5, 6])
            if None in self.diamonds[i]:
                flag = True
                if self.drop % self.cell_size == self.cell_size - 2:
                    for j in range(self.n - 1, 0, -1):
                        if self.diamonds[i][j] is None and self.diamonds[i][j - 1] is not None:
                            self.diamonds[i][j], self.diamonds[i][j - 1] = self.diamonds[i][j - 1], self.diamonds[i][j]
        self.drop = self.drop + 2 if flag else 0
        # отрисовка поля(клеточек и спрайтов)
        screen.fill("black")
        all_sprites = pygame.sprite.Group()
        for i in range(self.n - 1, -1, -1):
            for j in range(self.n - 1, -1, -1):
                # отрисовка клеточек
                pygame.draw.rect(canvas, "white",
                                 (i * self.cell_size + self.otstup + self.border,
                                  j * self.cell_size + self.otstup + self.border,
                                  self.cell_size - self.border, self.cell_size - self.border))
                if j < 7 and self.diamonds[i][j] is not None and self.diamonds[i][j + 1] is None:
                    drop = self.drop % self.cell_size
                else:
                    drop = 0
                plus1, plus2, plus3, plus4 = self.replace(i, j)
                if self.diamonds[i][j] is not None:
                    if None in self.diamonds[i][j:]:
                        drop = self.drop % self.cell_size
                    # добавление спрайтов
                    diamond_image = pygame.image.load(os.path.join('data', str(self.diamonds[i][j]) + ".png"))
                    diamond = pygame.sprite.Sprite(all_sprites)
                    diamond.image = diamond_image
                    diamond.rect = diamond.image.get_rect()
                    diamond.rect.x = i * self.cell_size + self.otstup + self.border + plus1 + plus3
                    diamond.rect.y = j * self.cell_size + self.otstup + self.border + plus2 + plus4 + drop
        all_sprites.draw(canvas)
        # проверка на наличие новых рядов и их удаление
        if self.drop == 0 and len(self.check) == 0:
            self.checking()
            self.delete()
        # добавление счётчика очков
        font = pygame.font.Font(None, 100)
        text = font.render("Счёт: " + str(self.count), True, (255, 255, 255))
        screen.blit(text, (450 - text.get_width(), 550 - text.get_height()))

    # проверка области клика
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        i = (x - self.otstup) // self.cell_size
        j = (y - self.otstup) // self.cell_size
        if 0 <= i <= self.n - 1 and 0 <= j <= self.n - 1:
            self.swapping(i, j)
            return True
        else:
            return False

    # помена двух алмазов местами
    def swapping(self, x, y):
        if not self.temp1:
            self.temp1 = (x, y)
        elif not self.temp2:
            self.temp2 = (x, y)
            self.diamonds[self.temp1[0]][self.temp1[1]], self.diamonds[self.temp2[0]][self.temp2[1]] = \
                self.diamonds[self.temp2[0]][self.temp2[1]], self.diamonds[self.temp1[0]][self.temp1[1]]
            self.checking()
            self.diamonds[self.temp1[0]][self.temp1[1]], self.diamonds[self.temp2[0]][self.temp2[1]] = \
                self.diamonds[self.temp2[0]][self.temp2[1]], self.diamonds[self.temp1[0]][self.temp1[1]]
            if abs(self.temp1[0] - self.temp2[0]) + abs(self.temp1[1] - self.temp2[1]) > 1 or len(self.check) == 0:
                self.temp1 = None
                self.temp2 = None

    # работа с перемещениями спрайтов
    def replace(self, i, j):
        plus1 = 0
        plus2 = 0
        plus3 = 0
        plus4 = 0
        if self.temp1 and self.temp2:
            if abs(self.plus1) + abs(self.plus2) + abs(self.plus3) + abs(self.plus4) == 100:
                self.diamonds[self.temp1[0]][self.temp1[1]], self.diamonds[self.temp2[0]][self.temp2[1]] = \
                    self.diamonds[self.temp2[0]][self.temp2[1]], self.diamonds[self.temp1[0]][self.temp1[1]]
                self.temp1 = None
                self.temp2 = None
                self.checking()
                self.delete()
                self.flag = False
                self.plus1 = 0
                self.plus2 = 0
                self.plus3 = 0
                self.plus4 = 0
            elif i == self.temp1[0] and j == self.temp1[1]:
                if self.temp2[0] > i:
                    self.plus1 += 2
                if self.temp2[0] < i:
                    self.plus1 -= 2
                if self.temp2[1] > j:
                    self.plus2 += 2
                if self.temp2[1] < j:
                    self.plus2 -= 2
                plus1 = self.plus1
                plus2 = self.plus2
            elif i == self.temp2[0] and j == self.temp2[1]:
                if self.temp1[0] > i:
                    self.plus3 += 2
                if self.temp1[0] < i:
                    self.plus3 -= 2
                if self.temp1[1] > j:
                    self.plus4 += 2
                if self.temp1[1] < j:
                    self.plus4 -= 2
                plus3 = self.plus3
                plus4 = self.plus4
        return plus1, plus2, plus3, plus4

    # проверка на наличие ряда их трёх или более шаров на поле
    def checking(self):
        ls = []
        for i in range(self.n):
            ls1 = []
            ls2 = []
            for j in range(self.n):
                if len(ls1) == 0 or (self.diamonds[ls1[-1][0]][ls1[-1][1]] == self.diamonds[i][j] and
                                     self.diamonds[i][j] is not None):
                    ls1.append([i, j])
                else:
                    if len(ls1) >= 3:
                        ls.append(ls1)
                    ls1 = [[i, j]]
                if len(ls2) == 0 or (self.diamonds[ls2[-1][0]][ls2[-1][1]] == self.diamonds[j][i] and
                                     self.diamonds[j][i] is not None):
                    ls2.append([j, i])
                else:
                    if len(ls2) >= 3:
                        ls.append(ls2)
                    ls2 = [[j, i]]
            if len(ls1) >= 3:
                ls.append(ls1)
            if len(ls2) >= 3:
                ls.append(ls2)
        self.check = ls
        return len(ls)

    # удаление собранных рядов
    def delete(self):
        for i in range(len(self.check)):
            self.count += 1
            for j in self.check[i]:
                self.diamonds[j[0]][j[1]] = None
        self.check = []

    # возвращает счёт
    def score(self):
        return self.count


# начало и конец игры, превью
class Preview:
    def __init__(self):
        self.font = pygame.font.Font(None, 80)
        self.text = self.font.render("НОВАЯ ИГРА", True, (0, 0, 0))
        self.text_x = 450 // 2 - self.text.get_width() // 2
        self.text_y = 550 // 2 - self.text.get_height() // 2
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()

    # проверка области клика при старте
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        if self.text_x - 10 <= x <= self.text_x + self.text_w + 10 and \
                self.text_y - 10 <= y <= self.text_y + self.text_h + 10:
            return True
        else:
            return False

    # межигровая заставка
    def win(self, canva, score):
        pygame.draw.rect(canva, "white", (self.text_x - 10, self.text_y - 10, self.text_w + 20, self.text_h + 20))
        pygame.draw.rect(canva, "black", (self.text_x - 10, self.text_y - 10, self.text_w + 20, self.text_h + 20), 5)
        canva.blit(self.text, (self.text_x, self.text_y))
        pygame.draw.rect(canva, "black", (0, 450, 450, 100))
        text = self.font.render("МОЛОДЕЦ!!!", True, (255, 255, 255))
        text_x = 450 // 2 - text.get_width() // 2
        canva.blit(text, (text_x, 440))
        font = pygame.font.Font(None, 50)
        text = font.render("ТЫ НАБРАЛ " + str(score) + " ОЧКОВ", True, (255, 255, 255))
        text_x = 450 // 2 - text.get_width() // 2
        canva.blit(text, (text_x, 500))


# запуск программы
if __name__ == '__main__':
    pygame.init()

    # задание размера и имени окна
    screen = pygame.display.set_mode((450, 550))
    pygame.display.set_caption('Три в ряд')

    # инициализация двух классов
    three = Three()
    preview = Preview()

    # отрисовка и показ стартового кадра
    screen.blit(pygame.image.load(os.path.join('data', "cover.png")), (0, 0))
    pygame.display.flip()

    # инициализация прочих переменных
    clock = pygame.time.Clock()
    running = True
    flipping = False
    gaming = False
    score = None
    MYEVENTTYPE = pygame.USEREVENT + 1

    # основной цикл программы
    while running:
        # обработка событий
        for event in pygame.event.get():

            # обработка выхода из игры
            if event.type == pygame.QUIT:
                running = False

            # обработка клика в окне
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (not gaming) and preview.get_click(event.pos):
                    gaming = True
                    flipping = True
                elif gaming:
                    flipping = three.get_click(event.pos)

            # перезапуск игрового процесса
            if event.type == MYEVENTTYPE:
                preview.win(screen, score)
                pygame.display.flip()
                gaming = False
                flipping = False
                three = Three()
                pygame.time.set_timer(MYEVENTTYPE, 0)

        # отрисовка и переворачивание кадров по таймеру
        if flipping:
            three.render(screen)
            clock.tick(40)
            pygame.display.flip()

            # проверка на конец игры
            if three.score() >= 10:
                score = three.score()
                pygame.time.set_timer(MYEVENTTYPE, 10)
# разработала ученица 2-го курса проекта Яндекс.Лицей Гринько Анастасия
