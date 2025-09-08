from pynput import keyboard
from clouds import Clouds
from map import Map
import time
import os
from helicopter import Helicopter as Helico
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
game_paused = False

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}

def save_game():
    global game_paused
    data = {
        "helico": helico.export_data(),
        "field": field.cells,
        "clouds": clouds.export_data(),
        "tick": tick
    }
    with open("savegame.json", "w", encoding='utf-8') as f:
        json.dump(data, f)
    print("Игра сохранена!")
    game_paused = True
    time.sleep(2)

def load_game():
    global helico, field, clouds, tick, game_paused
    try:
        with open("savegame.json", "r", encoding='utf-8') as f:
            data = json.load(f)
        
        helico.score = data["helico"]["score"]
        helico.lives = data["helico"]["lives"]
        helico.x = data["helico"]["x"]
        helico.y = data["helico"]["y"]
        helico.tank = data["helico"]["tank"]
        helico.mxtank = data["helico"]["mxtank"]
        
        field.cells = data["field"]
        clouds.cells = data["clouds"]["cells"]
        tick = data["tick"]
        
        print("Игра загружена!")
        game_paused = True
        time.sleep(2)
    except FileNotFoundError:
        print("Сохранение не найдено!")
        time.sleep(1)
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        time.sleep(1)

def process_key(key):
    global helico, field, clouds, tick
    try:
        c = key.char.lower()
        if c in MOVES.keys():
            dx, dy = MOVES[c][0], MOVES[c][1]
            helico.move(dx, dy)
        elif c == 'z':
            save_game()
        elif c == 'x':
            load_game()
    except AttributeError:
        pass

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

tick = 1

while True:
    if game_paused:
        input("Нажмите Enter чтобы продолжить...")
        game_paused = False
        os.system("cls" if os.name == 'nt' else "clear")
    
    os.system("cls" if os.name == 'nt' else "clear")
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    print("TICK", tick)
    print("Управление: W,A,S,D - движение, Z - сохранить, X - загрузить")
    tick += 1
    time.sleep(TICK_SLEEP)
    
    if helico.lives <= 0:
        break
        
    if tick % TREE_UPDATE == 0:
        field.generate_tree()
    if tick % FIRE_UPDATE == 0:
        field.update_fires()
    if tick % CLOUDS_UPDATE == 0:
        clouds.update()