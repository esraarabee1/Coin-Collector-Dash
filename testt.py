import tkinter as tk
import pygame
import os


pygame.mixer.init()


jump_sound = pygame.mixer.Sound("jump.mp3")
coin_sound = pygame.mixer.Sound("coinrecieved.mp3")
game_over_sound = pygame.mixer.Sound("gamefail.mp3")


root = tk.Tk()
root.title("Game")
root.geometry("800x600")


canvas = tk.Canvas(root, width=800, height=600, bg="deepskyblue")
canvas.pack()


player = None
player_dx = 0  
player_dy = 0  
gravity = 1.5  
jump_strength = -20  
on_ground = False  
level = 1
score = 0


platforms = []
coins = []


def create_player():
    global player
    player = canvas.create_rectangle(50, 550, 80, 580, fill="orange")


def create_platforms():
    global platforms
    platforms = [
        canvas.create_rectangle(0, 580, 800, 600, fill="green"),  
        canvas.create_rectangle(100, 450, 300, 470, fill="#8B4513"),  
        canvas.create_rectangle(400, 350, 600, 370, fill="#D2691E"),  
        canvas.create_rectangle(200, 200, 400, 220, fill="#A52A2A"),
    ]


def create_coins():
    global coins
    coins = [
        canvas.create_oval(120, 420, 140, 440, fill="gold"),  
        canvas.create_oval(420, 320, 440, 340, fill="gold"),  
        canvas.create_oval(250, 170, 270, 190, fill="gold"),
    ]


def move_player(event):
    global player_dx
    if event.keysym == "Left":
        player_dx = -5  
    elif event.keysym == "Right":
        player_dx = 5  
    elif event.keysym == "space" and on_ground:  
        jump()


def stop_player(event):
    global player_dx
    if event.keysym in ["Left", "Right"]:
        player_dx = 0


def jump():
    global player_dy, on_ground
    player_dy = jump_strength  
    on_ground = False  
    jump_sound.play()  


def check_collision():
    global player_dy, on_ground
    player_pos = canvas.coords(player)  
    on_ground = False
    for platform in platforms:
        platform_pos = canvas.coords(platform)
        if (
            player_pos[2] > platform_pos[0]  
            and player_pos[0] < platform_pos[2]
            and player_pos[3] >= platform_pos[1]
            and player_pos[3] <= platform_pos[1] + 10
            and player_dy >= 0
        ):
            player_dy = 0  
            on_ground = True
            canvas.move(player, 0, platform_pos[1] - player_pos[3])  
            break


def check_coin_collection():
    global score, coins
    player_pos = canvas.coords(player)  
    for coin in coins[:]:
        coin_pos = canvas.coords(coin)
        if (
            player_pos[2] > coin_pos[0]  
            and player_pos[0] < coin_pos[2]
            and player_pos[3] > coin_pos[1]
            and player_pos[1] < coin_pos[3]
        ):
            canvas.delete(coin)  
            coins.remove(coin)  
            score += 10  
            coin_sound.play()  
            canvas.itemconfig(score_text, text=f"Score: {score}")  

def update_player():
    global player_dy
    canvas.move(player, player_dx, player_dy)  
    player_dy += gravity  
    check_collision()  
    check_coin_collection()  
    if canvas.coords(player)[3] > 600:  
        game_over()
    else:
        root.after(20, update_player)   

def game_over():
    canvas.create_text(
        400, 300, text="Game Over!", fill="red", font=("Arial", 40)
    )
    game_over_sound.play() 
    canvas.unbind_all("<Key>")  
    canvas.unbind_all("<KeyRelease>")


def start_game():
    create_player()
    create_platforms()
    create_coins()
    update_player()


score_text = canvas.create_text(700, 50, text="Score: 0", fill="black", font=("Arial", 18))


canvas.bind_all("<KeyPress>", move_player)
canvas.bind_all("<KeyRelease>", stop_player)


start_game()
root.mainloop()
