# Building own Beat Maker
from ast import Delete
from json import load
from lib2to3.pgen2.token import GREATEREQUAL
from tkinter import EventType, Widget
from turtle import color, width
import typing
import pygame
from pygame import mixer

pygame.init()

# SETTING UP THE SCREEN
WIDHT = 1400
HEIGHT = 800

# Defining colors upfront
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (170, 170, 170)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDHT, HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font("freesansbold.ttf", 32)
medium_font = pygame.font.Font("freesansbold.ttf", 24)

#variables
index = 100
fps = 60
timer = pygame.time.Clock()
beats_count = 8
instruments_count= 6
boxes = []
clicked = [[-1 for _ in range(beats_count)] for _ in range(instruments_count)]
active_list = [1 for _ in range(instruments_count)]
bpm = 240 
playing = True
active_lenght = 0
active_beat = 0
beat_changed = True 
save_menu = False 
load_menu = False 
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    if line != '':
        saved_beats.append(line)
beat_name = ''
typing = False

# load in sounds 
hi_hat = mixer.Sound('sounds\hi_hat.wav')
bassdrum = mixer.Sound('sounds\\bassdrum.wav')
clap = mixer.Sound('sounds\clap.wav')
crash = mixer.Sound('sounds\crash.wav')
floortom = mixer.Sound('sounds\\floortom.wav')
snare = mixer.Sound('sounds\snare.wav')
pygame.mixer.set_num_channels(instruments_count * 3)

#nadavator
# devka = mixer.Sound('sounds\\nadavator\devka.mp3')
# kunda = mixer.Sound('sounds\\nadavator\kunda.mp3')
# kurva = mixer.Sound('sounds\\nadavator\kurva.mp3')
# posral = mixer.Sound('sounds\\nadavator\posral.mp3')
# prdel = mixer.Sound('sounds\\nadavator\prdel.mp3')
# syfl = mixer.Sound('sounds\\nadavator\syfl.mp3')

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                bassdrum.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                floortom.play()

    # for i in range(len(clicked)):
    #     if clicked[i][active_beat] == 1:
    #         if i == 0:
    #             devka.play()
    #         if i == 1:
    #             kunda.play()
    #         if i == 2:
    #             kurva.play()
    #         if i == 3:
    #             posral.play()
    #         if i == 4:
    #             prdel.play()
    #         if i == 5:
    #             syfl.play()


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT- 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDHT, 200], 5)
    boxes = []
    colors = [gray, white, gray]

    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    base_drum_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(base_drum_text, (20, 230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_tom_text, (30, 530))


    #nadavator
    # hi_hat_text = label_font.render('Devka', True, white)
    # screen.blit(hi_hat_text, (30, 30))
    # snare_text = label_font.render('Kunda', True, white)
    # screen.blit(snare_text, (30, 130))
    # base_drum_text = label_font.render('Kurva', True, white)
    # screen.blit(base_drum_text, (20, 230))
    # crash_text = label_font.render('Posral', True, white)
    # screen.blit(crash_text, (30, 330))
    # clap_text = label_font.render('Prdel', True, white)
    # screen.blit(clap_text, (30, 430))
    # floor_tom_text = label_font.render('Syfl', True, white)
    # screen.blit(floor_tom_text, (30, 530))

    for i in range(instruments_count):
        pygame.draw.line(screen,gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats_count):
        for j in range(instruments_count):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen,color,
                                    [i * ((WIDHT - 200) // beats_count) + 205, (j * 100) + 5, ((WIDHT - 200) // beats_count) - 10,
                                    ((HEIGHT - 200) // instruments_count) - 10], 0, 3)

            pygame.draw.rect(screen,black,
                        [i * ((WIDHT - 200) // beats_count) + 200, (j * 100), ((WIDHT - 200) // beats_count),
                        ((HEIGHT - 200) // instruments_count)], 5, 5)

            pygame.draw.rect(screen,gold,
                        [i * ((WIDHT - 200) // beats_count) + 200, (j * 100), ((WIDHT - 200) // beats_count),
                        ((HEIGHT - 200) // instruments_count)], 2, 5)

            boxes.append((rect, (i, j)))
        
        active = pygame.draw.rect(screen, blue, [beat * ((WIDHT - 200)//beats_count) + 200, 0, ((WIDHT - 200)//beats_count), instruments_count * 100], 5, 3)
    
    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0,0, WIDHT, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a Name for Current Beat', True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDHT // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    screen.blit(saving_txt, (WIDHT // 2 - 70, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDHT-200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDHT- 160, HEIGHT-70))
    if typing:
        entry_rect = pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0,0, WIDHT, HEIGHT])
    menu_text = label_font.render('LOAD MENU: Select a Beat to Load', True, white)
    loading_btn = pygame.draw.rect(screen, gray, [WIDHT // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render('Load Beat', True, white)
    screen.blit(loading_txt, (WIDHT // 2 - 70, HEIGHT * 0.87 + 30))
    screen.blit(menu_text, (400, 40))
    delete_btn = pygame.draw.rect(screen, gray, [WIDHT // 2 - 500, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_txt = label_font.render('Delete Beat', True, white)
    screen.blit(delete_txt, (WIDHT // 2 - 490, HEIGHT * 0.87 + 30))
    exit_btn = pygame.draw.rect(screen, gray, [WIDHT-200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDHT- 160, HEIGHT-70))

    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, gray, [190, 95 + index*50, 1000, 50])

    for beat in range(len(saved_beats)):
        if beat < 10: 
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index <len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8 : beat_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6 : bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split('], ['))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(loaded_beats):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


run = True
while run:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_list)
    #lower menu buttons 
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (65, HEIGHT - 125))

    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (65, HEIGHT - 85))

    #BPM stuff 

    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT-150, 220, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (310, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (380, HEIGHT - 100))

    bpm_add_rect = pygame.draw.rect(screen, gray, [525, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [525, HEIGHT - 98, 48, 48], 0, 5)

    bpm_add_text = medium_font.render('+5', True, white)
    screen.blit(bpm_add_text, (535, HEIGHT - 135))
    bpm_sub_text = medium_font.render('-5', True, white)
    screen.blit(bpm_sub_text, (535, HEIGHT - 85))

    #BEATS STUFF 
    beats_rect = pygame.draw.rect(screen, gray, [623, HEIGHT - 150, 220, 100],5,5)
    beats_text = medium_font.render('Beats Count', True, white)
    beats_text2 = medium_font.render(f'{beats_count}', True, white)
    screen.blit(beats_text, (660, HEIGHT - 135)) 
    screen.blit(beats_text2,(720, HEIGHT - 100))  
    
    beats_add_rect = pygame.draw.rect(screen, gray, [848, HEIGHT - 150, 48, 48], 0, 5)     
    beats_sub_rect = pygame.draw.rect(screen, gray, [848, HEIGHT - 98, 48, 48], 0, 5)
    beats_add_text = medium_font.render('+1', True, white)
    beats_sub_text = medium_font.render('-1', True, white)
    screen.blit(beats_add_text, (858, HEIGHT - 135))
    screen.blit(beats_sub_text, (862, HEIGHT - 85))

    #Reset 
    reset_rect = pygame.draw.rect(screen, gray, [WIDHT - 190, HEIGHT - 60 , 180, 50], 0, 5)
    reset_text = label_font.render('Reset', True, white)
    screen.blit(reset_text, (WIDHT - 140, HEIGHT - 50))

    #Save and Load 
    load_rect = pygame.draw.rect(screen, gray, [WIDHT - 190, HEIGHT - 120 , 180, 50], 0, 5)
    load_text = label_font.render('Load', True, white)
    screen.blit(load_text, (WIDHT - 140, HEIGHT - 110))

    save_rect = pygame.draw.rect(screen, gray, [WIDHT - 190, HEIGHT - 180 , 180, 50], 0, 5)
    save_text = label_font.render('Save', True, white)
    screen.blit(save_text, (WIDHT - 140, HEIGHT - 170))
    
    #INSTRUMENTS RECTS 
    instrument_rects = []
    for i in range(instruments_count):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)

    if beat_changed:
        play_notes()
        beat_changed = False
    
    #DRAW menus
    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button, loading_button, entry_rectangle, delete_button, loaded_information = draw_load_menu(index)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN  and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos): 
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1 
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing: 
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5 
            elif beats_add_rect.collidepoint(event.pos):
                beats_count += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats_count -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif reset_rect.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats_count)] for _ in range(instruments_count)]
            elif save_rect.collidepoint(event.pos):
                save_menu = True
            elif load_rect.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False 
            if entry_rectangle.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False 
                    elif not typing:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50 

            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w', encoding='utf-8')
                    saved_beats.append(f'name: {beat_name}, beats: {beats_count}, bpm: {bpm}, selected: {clicked}\n')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index <len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats_count = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True 
                        typing = False

        if event.type == pygame.TEXTINPUT and typing: 
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]


            
    beat_lenght = 3600 // bpm

    pygame.display.flip()

    if playing: 
        if active_lenght < beat_lenght:
            active_lenght += 1
        else: 
            active_lenght = 0 
            if active_beat < beats_count - 1: 
                active_beat += 1 
                beat_changed = True
            else: 
                active_beat = 0
                beat_changed = True 

pygame.quit()
