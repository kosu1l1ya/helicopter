from utils import randcell
import os

class Helicopter:
    def __init__(self, w, h):
        self.x, self.y = randcell(w, h)
        self.w = w
        self.h = h
        self.tank = 0
        self.mxtank = 3
        self.score = 0
        self.lives = 20

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.h and 0 <= ny < self.w:
            self.x, self.y = nx, ny

    def print_stats(self):
        print(f"🛢️  {self.tank} / {self.mxtank} | 🏆  {self.score} | 💗  {self.lives}")

    def game_over(self):
        os.system("cls" if os.name == 'nt' else "clear")
        print("╔═════════════════════════════╗")
        print("║          GAME OVER          ║")
        print("╠═════════════════════════════╣")
        print(f"║     Ваш счет: {self.score:10}    ║")
        print("╚═════════════════════════════╝")
        input("Нажмите Enter для выхода...")
        exit(0)

    def export_data(self):
        return {
            "score": self.score,
            "lives": self.lives,
            "x": self.x,
            "y": self.y,
            "tank": self.tank,
            "mxtank": self.mxtank
        }