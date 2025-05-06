import sys

import pygame
import random
from PIL import Image

pygame.mixer.init()#ses dosyaları icin
background_sound = pygame.mixer.Sound('backgroundsound.mp3')
match_sound = pygame.mixer.Sound('dogru sesi efekti.mp3')
dismatch_sound = pygame.mixer.Sound('yanlis sesi efekti.mp3')

clock=pygame.time.Clock()


pygame.init()#pygamei kullanabilmek için tanımladık pygamei
pastel_turuncu = (238,118,33)
orange = (210 ,105 ,30)
baby_blue = (58,95,205)
fire_brick = (178,34,34)
dark_gray = (79, 79, 79)
width = 600
height = 600
white = (255, 255, 255)
black= (48, 214, 200)
dark = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)
gray = (128, 128, 120)
green = (0, 255, 0)
green2 = (34,126,63)
fps = 60
rows = 6
cols = 8
correct = [[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]] #rows*cols yani 6x8lik bir kutucuk oluşturduk
spaces = []
used = []
game_over = False
new_board = True
timer = pygame.time.Clock()
screen = pygame.display.set_mode([width, height]) # oyun ekranının boyutunu ayarlıyoruz
pygame.display.set_caption("Matching Game") # oyun açıldığında sekmedeki yazıyı düzenliyoruz
title_font = pygame.font.Font('freesansbold.ttf', 56)
medium_font = pygame.font.Font('freesansbold.ttf', 35)#------------------------> oyundaki kullandığımız text türleri ve boyutları
small_font = pygame.font.Font('freesansbold.ttf', 20)
running = True # programın çalışmasının durumunu belirtir
board_list = [] #kutucukların listesi
options_list = []
first_guess = False
second_guess = False
first_guess_num = 0
second_guess_num = 0
score = 0
best_score = 0
matches = 0
user1_score = 0 #multiplayerda 1. kullanıcının başlangıç skoru
user2_score = 0 #multiplayerda 2. kullanıcının başlangıç skoru
is_two_player_mode = False # çoklu oyun modunu kontrol eder
is_sound_on = True  # oyunun sesini kontrol ediyor


def draw_start_screen():

    global is_two_player_mode
    global is_sound_on
    global is_two_player_mode
    img = Image.open('1player-image.png')
    img2 = Image.open('2players.png')
    logo = Image.open('matching_game.png')
    voiceonimg = Image.open('voiceon.png')
    voiceoffimg = Image.open('voiceoff.png')
    new_width = 100
    new_height = 100
    logo_height=200
    logo_width=200
    voice_width = 50
    voice_height = 50
    resized_logo = logo.resize((logo_height,logo_width))
    resized_img = img.resize((new_width, new_height))
    resized_img2 = img2.resize((new_width, new_height))
    resized_voiceonimg = voiceonimg.resize((voice_width,voice_height))
    resized_voiceoffimg = voiceoffimg.resize((voice_width,voice_height))
    resized_logo.save('logo.png')
    resized_img.save('play_image_resized.png')
    resized_img2.save('play_image_resized2.png')
    resized_voiceonimg.save('von.png')
    resized_voiceoffimg.save('voff.png')
    background_image = pygame.image.load('background2.jpg')  # Resmin dosya yolunu belirtin
    screen.blit(background_image, (0, 0))  # Resmi ekrana çizmek için screen.blit() kullanılır




    matching_logo_image = pygame.image.load('logo.png')
    screen.blit(matching_logo_image, (width // 2 - 100, height // 2 - 270))

    # play_button = pygame.draw.rect(screen, green2, [width // 2 - 225, height // 2 - 200, 450, 100], 0, 5)
    #play_text = title_font.render('Matching Game', True, white)
    #screen.blit(play_text, (width // 2 - 220, height // 2 - 175))

    play_button = pygame.draw.rect(screen,pastel_turuncu , [width // 2 - 80, height // 2 - 55, 250, 100], 0, 5)
    play_text = medium_font.render('Single Play', True, white)
    screen.blit(play_text, (width // 2 - 55, height // 2 - 23))

    # Play button'ın yanına kare resmi ekle
    play_image = pygame.image.load('play_image_resized.png')
    screen.blit(play_image, (width // 2 - 180, height // 2 - 55))

    two_players_button = pygame.draw.rect(screen, baby_blue, [width // 2 - 80, height // 2 + 70, 250, 100], 0, 5)
    two_players_text = medium_font.render('Multi Play', True, white)
    screen.blit(two_players_text, (width // 2 - 40, height // 2 + 100))

    # Two players button'ın yanına kare resmi ekle
    two_players_image = pygame.image.load('play_image_resized2.png')
    screen.blit(two_players_image, (width // 2 - 180, height // 2 + 70))

    exit_button = pygame.draw.rect(screen,fire_brick , [width // 2 - 50, height // 2 + 190, 120, 80], 0, 0)
    exit_text = medium_font.render('Exit', True, white)
    screen.blit(exit_text, (width // 2 - 25, height // 2 + 210))

    voiceon_button = pygame.image.load('von.png')
    music_button = voiceon_button.get_rect()
    music_button.topleft = (25, 25)
    screen.blit(voiceon_button, music_button)

    voiceoff_button = pygame.image.load('voff.png')
    music2_button = voiceoff_button.get_rect()
    music2_button.topleft = (100, 25)
    screen.blit(voiceoff_button, music2_button)

    pygame.display.flip()# bu yaptığımız eklemeleri ekrana güncellemeyi sağlıyor

    waiting_for_play = True #ana ekranı kapatmaya yarayan döngünün boolean durumunu düzenliyor
    while waiting_for_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # yukarıdaki çarpı butonuna basınca oyundan çıkmaya yarıyor
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # click olayları meydana gelince gerçekleşecek olaylar
                if exit_button.collidepoint(event.pos): # exit butonuna basma durumunda gerçekleşecek durum (oyundan çıkma)
                    pygame.quit()
                    exit()
                if play_button.collidepoint(event.pos): # single play butonuna basınca gerçekleşecek durum (waiting_for_play değerini false yapıp while döngüsünü kapatır)
                    waiting_for_play = False
                elif two_players_button.collidepoint(event.pos):# multi play butonuna basınca gerçekleşecek durum (waiting_for_play değerini false yapıp while döngüsünü kapatır)
                    waiting_for_play = False
                    is_two_player_mode = True
                elif music_button.collidepoint(event.pos): # muzik açma butonu
                    background_sound.play() # dosyaya yüklediğimiz müzik açma butonu

                elif music2_button.collidepoint(event.pos): # muzik kapama durumu
                    background_sound.stop()  # dosaya yüklediğimiz müzik kapama butonu

draw_start_screen()

def draw_board():
    global rows
    global cols
    global correct
    start_time = pygame.time.get_ticks()
    board_list = []
    for i in range(cols):
        for j in range(rows):
            piece = pygame.draw.rect(screen, black, [i * 75 + 12, j * 65 + 112, 50, 50], 0, 4)
            board_list.append(piece)

            if show_time:
                piece_text = small_font.render(f'{spaces[i * rows + j]}', True, dark_gray)
                screen.blit(piece_text, (i * 75 + 18, j * 65 + 120))

    for r in range(rows):
        for c in range(cols):
            if correct[r][c] == 1:
                pygame.draw.rect(screen, green, [c * 75 + 10, r * 65 + 110, 54, 54], 3, 4)
                piece_text = small_font.render(f'{spaces[c * rows + r]}', True, dark)
                screen.blit(piece_text, (c * 75 + 18, r * 65 + 120))

    return board_list


def check_guesses(first, second):
    global user1_score
    global user2_score
    global spaces
    global correct
    global score
    global matches
    if spaces[first] == spaces[second]:
        col1 = first // rows
        col2 = second // rows
        row1 = first - (first // rows * rows)
        row2 = second - (second // rows * rows)
        if correct[row1][col1] == 0 and correct[row2][col2] == 0:
            correct[row1][col1] = 1
            correct[row2][col2] = 1
            score += 1
            if score%2 == 1:
                user1_score += 1
                matches += 1
            elif score%2 == 0:
                user2_score += 1
                matches += 1

            match_sound.play()

    else:
        score += 1
        dismatch_sound.play()

def menu_button_calling(): #menu butonu oluşturuyoruz
    menu_button = pygame.draw.rect(screen, gray, [250, height - 90, 80, 80], 0, 5)
    menu_text = small_font.render('MENU', True, white)
    screen.blit(menu_text, (260, 540))
    return menu_button

def draw_backgrounds():
    top_menu = pygame.draw.rect(screen, black, [0, 0, width, 100], 2, 20)
    title_text = title_font.render('The Matching Game!', True, black)
    screen.blit(title_text, (10, 20))
    board_space = pygame.draw.rect(screen, gray, [0, 100, width, height - 200], 0)
    # sondaki ikinci parametre border kalinlıgı ,sonuncu border radius oranı
    bottom_menu = pygame.draw.rect(screen, black, [0, height - 100, width, 100], 0)
    restart_button = pygame.draw.rect(screen, gray, [10, height - 90, 200, 80], 0, 5)
    restart_text = medium_font.render('RESTART', True, white)
    screen.blit(restart_text, (30, 530))
    menu_button_calling()

    if is_two_player_mode:
        if score%2 == 0:
            turn_text_user1 = small_font.render("User1's Turn", True, orange)
            screen.blit(turn_text_user1, (250, 80))
        elif score%2 == 1:
            turn_text_user2 = small_font.render("User2's Turn", True, baby_blue)
            screen.blit(turn_text_user2, (250, 80))


        score_text_user1 = small_font.render(f"User1's Score: {user1_score}", True, orange)
        score_text_user2 = small_font.render(f"User2's Score: {user2_score}", True, baby_blue)
        screen.blit(score_text_user1, (350, 520))
        screen.blit(score_text_user2, (350, 560))
    else:
        score_text = small_font.render(f'Current turns: {score}', True, white)
        best_text = small_font.render(f'Previous best: {best_score}', True, white)
        screen.blit(score_text, (350, 520))
        screen.blit(best_text, (350, 560))

    return restart_button



def generate_board():
    global options_list
    global spaces
    global used
    for item in range(rows * cols // 2):
        options_list.append(item)
    for item in range(rows * cols):
        piece = options_list[random.randint(0, len(options_list) - 1)]
        spaces.append(piece)
        if piece in used:
            used.remove(piece)
            options_list.remove(piece)
        else:
            used.append(piece)

show_time = True  # Gösterim durumu
start_time = pygame.time.get_ticks()

def reset_show_timer():
    global show_time, start_time
    show_time = True
    start_time = pygame.time.get_ticks()

while running:

    timer.tick(fps)
    screen.fill(white)

    if new_board:
        generate_board()
        new_board = False
        reset_show_timer()

    restart = draw_backgrounds()
    menu = menu_button_calling()
    board = draw_board()
    current_time = pygame.time.get_ticks()


    if show_time and current_time - start_time > 5000:  # 5000 milisaniye = 5 saniye
        show_time = False  # Gösterim süresi bittiğinde değişkeni False yap
    if first_guess and second_guess:
        check_guesses(first_guess_num, second_guess_num)
        pygame.time.delay(1000)
        first_guess = False
        second_guess = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)):
                button = board[i]
                if not game_over:
                    if button.collidepoint(event.pos) and not first_guess:
                        first_guess = True
                        first_guess_num = i

                    if button.collidepoint(event.pos) and not second_guess and first_guess and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i

            if restart.collidepoint(event.pos):
                options_list = []
                used = []
                spaces = []
                new_board = True
                score = 0
                matches = 0
                first_guess = False
                second_guess = False
                user1_score = 0
                user2_score = 0
                correct = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                game_over = 0
            if menu.collidepoint(event.pos):
                is_two_player_mode = False
                options_list = []
                used = []
                spaces = []
                new_board = True
                score = 0
                matches = 0
                first_guess = False
                second_guess = False
                user1_score = 0
                user2_score = 0
                correct = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                game_over = 0
                draw_start_screen()


    if matches == rows * cols // 2:
        game_over = True
        winner = pygame.draw.rect(screen, gray, [10, height - 300, width - 20, 80], 0, 5)
        if is_two_player_mode:
            if(user1_score>user2_score):
                winner_text = title_font.render(f'user1 won in {user1_score} moves!', True, white)
                screen.blit(winner_text, (10, height - 290))

            elif (user1_score < user2_score):
                winner_text = title_font.render(f'user2 won in {user2_score} moves!', True, white)
                screen.blit(winner_text, (10, height - 290))

            elif (user1_score == user2_score):
                winner_text = title_font.render('            DRAW!', True, white)
                screen.blit(winner_text, (10, height - 290))
        else:
            winner_text = title_font.render(f'You won in {score} moves!', True, white)
            screen.blit(winner_text, (10, height - 290))

        if (best_score > score or best_score == 0):
            best_score = score

    if first_guess:
        piece_text = small_font.render(f'{spaces[first_guess_num]}', True, blue)
        location = (first_guess_num // rows * 75 + 18, (first_guess_num - (first_guess_num // rows * rows)) * 65 + 120)
        screen.blit(piece_text, (location))

    if second_guess:
        piece_text = small_font.render(f'{spaces[second_guess_num]}', True, blue)
        location = (
            second_guess_num // rows * 75 + 18, (second_guess_num - (second_guess_num // rows * rows)) * 65 + 120)
        screen.blit(piece_text, (location))

    pygame.display.flip()

pygame.quit()
