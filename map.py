from utils import randbool, randcell, randcell2

# Исправляем символы для отображения
CELL_TYPES = "🟩🌲🌊🏥🏪🔥"  # Правильные индексы: 0-пусто, 1-дерево, 2-река, 3-госпиталь, 4-магазин, 5-огонь

TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 1000

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(5, 10)
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        return 0 <= x < self.h and 0 <= y < self.w

    def print_map(self, helico, clouds):
        print("⬛" * (self.w + 2))
        for ri in range(self.h):
            print("⬛", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if clouds.cells[ri][ci] == 1:
                    print("⛅", end="")
                elif clouds.cells[ri][ci] == 2:
                    print("⚡", end="")
                elif helico.x == ri and helico.y == ci:
                    print("🚁", end="")
                elif 0 <= cell < len(CELL_TYPES):
                    print(CELL_TYPES[cell], end="")
                else:
                    print("?", end="")  # На случай ошибки
            print("⬛")
        print("⬛" * (self.w + 2))

    def generate_river(self, length):
        rx, ry = randcell(self.w, self.h)
        self.cells[rx][ry] = 2
        
        while length > 0:
            rx2, ry2 = randcell2(rx, ry)
            if self.check_bounds(rx2, ry2):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                length -= 1

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_tree(self):
        cx, cy = randcell(self.w, self.h)
        if self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1
            return True
        return False

    def generate_upgrade_shop(self):
        cx, cy = randcell(self.w, self.h)
        self.cells[cx][cy] = 4

    def generate_hospital(self):
        cx, cy = randcell(self.w, self.h)
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        cx, cy = randcell(self.w, self.h)
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5
            return True
        return False

    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                if self.cells[ri][ci] == 5:
                    self.cells[ri][ci] = 0  
        for i in range(5):  
            self.add_fire()

    def process_helicopter(self, helico, clouds):
        if not self.check_bounds(helico.x, helico.y):
            return 
        c = self.cells[helico.x][helico.y]
        
        cloud_type = 0
        if 0 <= helico.x < clouds.h and 0 <= helico.y < clouds.w:
            cloud_type = clouds.cells[helico.x][helico.y]
        
        if c == 2:  
            helico.tank = helico.mxtank
            
        elif c == 5 and helico.tank > 0:
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
            
        elif c == 4 and helico.score >= UPGRADE_COST:
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
            
        elif c == 3 and helico.score >= LIFE_COST:
            helico.lives += 10
            helico.score -= LIFE_COST
            
        if cloud_type == 2:
            helico.lives -= 1
            
        if helico.lives <= 0:
            helico.game_over()
