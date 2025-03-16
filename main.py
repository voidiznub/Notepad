import pygame
import random
import math
import os
import sys
import time

pygame.init()
pygame.font.init()
clock = pygame.time.Clock() #set up a tick system

##SETTINGS

screen_width, screen_length = 400, 300
screen = pygame.display.set_mode((screen_width, screen_length))

pygame.display.set_caption("NotePad")

textbox = pygame.Rect(125, 25, 250, 250)
button_image = pygame.image.load("newpage.png")  # Load the button image
button_rect = button_image.get_rect(topleft=(370, 270))  # Define the button's position and size
#tbox = pygame.image.load("textbox.png")
#bottomhbox = pygame.image.load("bottomhbox.png")
#righthbox = pygame.image.load("righthbox.png")
notepad = pygame.image.load("NotePad.png")
sidebar = pygame.image.load("sidebar.png")
page1_img = pygame.image.load("Page1.png")
page2_img = pygame.image.load("Page2.png")
page3_img = pygame.image.load("Page3.png")
selectedpage1_img = pygame.image.load("SelectedPage1.png")
selectedpage2_img = pygame.image.load("SelectedPage2.png")
selectedpage3_img = pygame.image.load("SelectedPage3.png")
page1 = page1_img
page2 = page2_img
page3 = page3_img
selectedpage1 = True
selectedpage2 = False
selectedpage3 = False

x1 = 1
x2 = 1
x3 = 1
x = 1
newx = 0
collisiondetect = False
notepadcollision = False

user_text = [""]
text = ""
cursor = "|"
cursor_pos = 0
cursor_blink = 0
cursor_blink_speed = 500
cursor_blink_timer = 0
cursor_blink_on = True  # True = on, False = off

longest_line = 0
longest_line_index = 0
current_line = 0
current_line_index = 0

cursor_line = 0
cursor_char = 0

current_page = 1
storage_files = {
    1: "/Users/ryan/Documents/Scrapyard/Storage.txt",
    2: "/Users/ryan/Documents/Scrapyard/Storage2.txt",
    3: "/Users/ryan/Documents/Scrapyard/Storage3.txt"
}
font_size1 = (screen_width // 2) // x1
font_size2 = (screen_width // 2) // x2
font_size3 = (screen_width // 2) // x3

##_______________________________________________________________________________________
##FUNCTIONS

def draw_text(text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)
    
def clear_text(current_page):
    global user_text, x1, x2, x3, cursor_line, cursor_char
    user_text = [""]
    if current_page == 1:
        x1 = 1
        x2 = x2
        x3 = x3
    if current_page == 2:
        x2 = 1
        x1 = x1
        x3 = x3
    if current_page == 3:
        x3 = 1
        x1 = x1
        x2 = x2
    cursor_line = 0
    cursor_char = 0
    return user_text, x1, x2, x3

def update_longest_line():
    global longest_line, longest_line_index
    longest_line = 0
    for i, line in enumerate(user_text):
        if len(line) > longest_line:
            longest_line = len(line)
            longest_line_index = i

def save_user_text():
    global font_size1, font_size2, font_size3
    if current_page == 1:
        newx = font_size1
    elif current_page == 2:
        newx = font_size2
    elif current_page == 3:
        newx = font_size3

    with open(storage_files[current_page], 'w') as f:
        f.write(f"{newx}\n")
        for line in user_text:
            f.write(line + '\n')

def load_user_text(page):
    global user_text, font_size1, font_size2, font_size3, current_page, cursor_line, cursor_char
    current_page = page
    if os.path.exists(storage_files[page]):
        with open(storage_files[page], 'r') as f:
            lines = f.readlines()
            if lines:
                try:
                    if page == 1:
                        font_size1 = int(lines[0].strip())
                    elif page == 2:
                        font_size2 = int(lines[0].strip())
                    elif page == 3:
                        font_size3 = int(lines[0].strip())
                except ValueError:
                    if page == 1:
                        font_size1 = (screen_width // 2) // x1
                    elif page == 2:
                        font_size2 = (screen_width // 2) // x2
                    elif page == 3:
                        font_size3 = (screen_width // 2) // x3
                user_text = [line.rstrip('\n') for line in lines[1:]]
    else:
        user_text = [""]
    if not user_text:
        user_text = [""]
    cursor_line = 0
    cursor_char = 0

def get_cursor_position_from_mouse(x, y):
    global cursor_line, cursor_char
    if current_page == 1:
        line_height = font_size1
    elif current_page == 2:
        line_height = font_size2
    elif current_page == 3:
        line_height = font_size3

    cursor_line = (y - textbox.y - 20) // line_height
    cursor_line = max(0, min(cursor_line, len(user_text) - 1))
    line_text = user_text[cursor_line]
    cursor_char = 0
    for i in range(len(line_text) + 1):
        if basefont.size(line_text[:i])[0] + textbox.x + 20 > x:
            break
        cursor_char = i

# Load user_text and font size from storage when the program starts
load_user_text(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_user_text()
            pygame.quit()
            sys.exit()
        if event.type == pygame.TEXTINPUT:
            user_text[cursor_line] = user_text[cursor_line][:cursor_char] + event.text + user_text[cursor_line][cursor_char:]
            cursor_char += len(event.text)
            update_longest_line()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_char > 0:
                    user_text[cursor_line] = user_text[cursor_line][:cursor_char-1] + user_text[cursor_line][cursor_char:]
                    cursor_char -= 1
                elif cursor_line > 0:
                    cursor_char = len(user_text[cursor_line-1])
                    user_text[cursor_line-1] += user_text[cursor_line]
                    user_text.pop(cursor_line)
                    cursor_line -= 1
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))
                update_longest_line()
                if current_line_index == longest_line_index:
                    if current_page == 1:
                        if x1 > 1:
                            larger_font = pygame.font.Font(None, basefont.get_height() + (screen_width//2)//(x1-1))
                            larger_text_width = larger_font.size(user_text[-1])[0]
                            if textbox.x + 20 + larger_text_width < 350:
                                longest_line = len(user_text[-1])
                                x1 -= 1    
                    if current_page == 2:
                        if x2 > 1:
                            larger_font = pygame.font.Font(None, basefont.get_height() + (screen_width//2)//(x2-1))
                            larger_text_width = larger_font.size(user_text[-1])[0]
                            if textbox.x + 20 + larger_text_width < 350:
                                longest_line = len(user_text[-1])
                                x2 -= 1 
                    if current_page == 3:
                        if x3 > 1:
                            larger_font = pygame.font.Font(None, basefont.get_height() + (screen_width//2)//(x3-1))
                            larger_text_width = larger_font.size(user_text[-1])[0]
                            if textbox.x + 20 + larger_text_width < 350:
                                longest_line = len(user_text[-1])
                                x3 -= 1       
            elif event.key == pygame.K_RETURN:
                user_text.insert(cursor_line + 1, user_text[cursor_line][cursor_char:])
                user_text[cursor_line] = user_text[cursor_line][:cursor_char]
                cursor_line += 1
                cursor_char = 0
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))
                update_longest_line()
                
            elif event.key == pygame.K_TAB:
                user_text[cursor_line] = user_text[cursor_line][:cursor_char] + "    " + user_text[cursor_line][cursor_char:]
                cursor_char += 4
                update_longest_line()

            elif event.key == pygame.K_ESCAPE:
                user_text, x1, x2, x3 = clear_text(current_page)
                update_longest_line()

            elif event.key == pygame.K_LEFT:
                if cursor_char > 0:
                    cursor_char -= 1
                elif cursor_line > 0:
                    cursor_line -= 1
                    cursor_char = len(user_text[cursor_line])
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))

            elif event.key == pygame.K_RIGHT:
                if cursor_char < len(user_text[cursor_line]):
                    cursor_char += 1
                elif cursor_line < len(user_text) - 1:
                    cursor_line += 1
                    cursor_char = 0
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))

            elif event.key == pygame.K_UP:
                if cursor_line > 0:
                    cursor_line -= 1
                    cursor_char = min(cursor_char, len(user_text[cursor_line]))
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))

            elif event.key == pygame.K_DOWN:
                if cursor_line < len(user_text) - 1:
                    cursor_line += 1
                    cursor_char = min(cursor_char, len(user_text[cursor_line]))
                cursor_line = max(0, min(cursor_line, len(user_text) - 1))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if textbox.collidepoint(mouse_x, mouse_y):
                get_cursor_position_from_mouse(mouse_x, mouse_y)
            elif button_rect.collidepoint(mouse_x, mouse_y):
                clear_text(current_page)  # Clear the text and create a new page
            elif page1.get_rect(topleft=(5, 40)).collidepoint(mouse_x, mouse_y):
                selectedpage3 = False
                selectedpage1 = True 
                selectedpage2 = False
                save_user_text()
                load_user_text(1)
            elif page2.get_rect(topleft=(5, 95)).collidepoint(mouse_x, mouse_y):
                selectedpage3 = False
                selectedpage1 = False
                selectedpage2 = True
                save_user_text()
                load_user_text(2)
            elif page3.get_rect(topleft=(5, 150)).collidepoint(mouse_x, mouse_y):
                selectedpage3 = True
                selectedpage1 = False
                selectedpage2 = False
                save_user_text()
                load_user_text(3)
      
    if user_text:
        current_line = user_text[-1]
        current_line_index = len(user_text) - 1
    
        if len(current_line) > longest_line:
            longest_line = len(current_line)
            longest_line_index = len(user_text) - 1
            
    notepadcollision = textbox.collidepoint(pygame.mouse.get_pos())
    if notepadcollision:
        cursor2 = pygame.cursors.compile(pygame.cursors.textmarker_strings)
        pygame.mouse.set_cursor((8, 16), (0, 0), *cursor2)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
    page1collision = page1.get_rect(topleft=(5, 40)).collidepoint(pygame.mouse.get_pos())
    page2collision = page2.get_rect(topleft=(5, 95)).collidepoint(pygame.mouse.get_pos())
    page3collision = page3.get_rect(topleft=(5, 150)).collidepoint(pygame.mouse.get_pos())
    
    if selectedpage1:
        page1 = selectedpage1_img
    else:
        page1 = page1_img
    if selectedpage2:
        page2 = selectedpage2_img
    else:
        page2 = page2_img
        
    if selectedpage3:
        page3 = selectedpage3_img
    else:
        page3 = page3_img
    
    if current_page == 1:
        font_size1 = (screen_width//2) // x1
        font_size = font_size1
    elif current_page == 2:
        font_size2 = (screen_width//2) // x2
        font_size = font_size2
    elif current_page == 3:
        font_size3 = (screen_width//2) // x3
        font_size = font_size3
        
    if x1 == 0:
        x1 = 1 
    if x2 == 0:
        x2 = 1 
    if x3 == 0:
        x3 = 1 
    # Fill the screen with a color (black in this case)
    pygame.draw.rect(screen, (255, 254, 211), textbox, 5)
    basefont = pygame.font.Font(None, font_size)
    screen.fill((255, 255, 255))
    screen.blit(notepad, (100, 0))
    
    for row, line in enumerate(user_text):
        draw_text(line, basefont, (0, 0, 0), textbox.x + 20, textbox.y + 20 + row * font_size)

    cursor_x = textbox.x + 15 + basefont.size(user_text[cursor_line][:cursor_char])[0]
    cursor_y = textbox.y + 20 + cursor_line * font_size
    text_surface = basefont.render(cursor, True, (255, 250, 100))
    screen.blit(text_surface, (cursor_x, cursor_y))
    
    cursor_rect = pygame.Rect(cursor_x, cursor_y, text_surface.get_width(), text_surface.get_height())
    
    if current_page == 1:
        if textbox.x + 20 + basefont.size(user_text[cursor_line])[0] > 350:
            x1 += 1
        if cursor_y > 250:
            x1 += 1
    if current_page == 2:
        if textbox.x + 20 + basefont.size(user_text[cursor_line])[0] > 350:
            x2 += 1
        if cursor_y > 250:
            x2 += 1
    if current_page == 3:
        if textbox.x + 20 + basefont.size(user_text[cursor_line])[0] > 350:
            x3 += 1
        if cursor_y > 250:
            x3 += 1
        
    cursor_blink_timer += clock.get_time()
    if cursor_blink_timer >= cursor_blink_speed:
        cursor_blink_timer = 0
        cursor_blink_on = not cursor_blink_on
    if cursor_blink_on:
        cursor = "|"
    else:
        cursor = ""
    
    screen.blit(sidebar, (0, 0))
    screen.blit(button_image, button_rect.topleft)  # Draw the button image
    
    screen.blit(page1, (5, 40))
    screen.blit(page2, (5, 95))
    screen.blit(page3, (5, 150))
    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)
