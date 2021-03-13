import sys, os, string
import pygame
pygame.init()

def write(text, color, size, antialias=True, font_name='arial'):
    font = pygame.font.SysFont(font_name, size)
    return font.render(text, antialias, color)

grille = {'A':('A', 'H', 'O', 'V'),
        'B':('B', 'I', 'P', 'W'),
        'C':('C', 'J', 'Q', 'X'),
        'D':('D', 'K', 'R', 'Y'),
        'E':('E', 'L', 'S', 'Z'),
        'F':('F', 'M', 'T'),
        'G':('G', 'N', 'U')}


def musicalisation(string):
    notes = []
    for n in str.upper(string):
        for k in grille:
            if n in grille[k]:
                notes.append(k)
    notes = ''.join(notes)
    return notes

def draw_portee(surface, color=pygame.color.Color('Black'), width=5):
    surface_rect = surface.get_rect()
    pos_portee = []
    for p in range(1, 6):
        start_pos = pygame.math.Vector2(surface_rect.left, surface_rect.h//6 * p)
        end_pos = pygame.math.Vector2(surface_rect.right, surface_rect.h//6 * p)
        pygame.draw.line(surface, color, start_pos, end_pos, width)
        pos_portee.append([start_pos, end_pos])

    return pos_portee

def draw_notes(surface, notes, word, color=pygame.color.Color('Black'), width=5):
    surface_rect = surface.get_rect()
    pos_notes_y =    {'A':surface_rect.h//6 * 3.5,
                    'B':surface_rect.h//6 * 3,
                    'C':surface_rect.h//6 * 2.5,
                    'D':surface_rect.h//6 * 2,
                    'E':surface_rect.h//6 * 1.5,
                    'F':surface_rect.h//6 * 4.5,
                    'G':surface_rect.h//6 * 4}
    index_x = 0
    for n in notes:
        pos_notes_x = (index_x+1) * surface_rect.w//(len(notes)+1)
        pygame.draw.circle(surface, color, (pos_notes_x, pos_notes_y[n]), surface_rect.h//6*0.5)
        note_name_surface = write(word[index_x]+'('+n+')', pygame.color.Color('Blue'), 25)
        surface.blit(note_name_surface, (pos_notes_x-(note_name_surface.get_width()//2), pos_notes_y[n]+surface_rect.h//6*0.5))
        index_x +=1

with open("texte.txt", 'r') as txt:
    word = []
    for line in txt:
        if line != "---\n":
            word.append(line)
        else:
            break
    word = ''.join(word)
    spChar = string.whitespace + string.punctuation
    for sp in spChar:
        word = word.replace(sp, '')
    print(word)
    
notes = ''.join(musicalisation(word))

with open("texte.txt", 'a') as text:
        text.write('\n' + word + " --> " + notes + '\n')


### affichage

screen = pygame.display.set_mode([1200, 200])
screen.fill(pygame.color.Color('White'))
screen_rect = screen.get_rect()
pygame.display.set_caption(word + " --> " + notes)
pygame.draw.rect(screen, pygame.color.Color('Grey'), screen_rect, 20)



while True:

    pos_portee = draw_portee(screen)
    pos_note = draw_notes(screen, notes, word)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("**EXIT**")
            pygame.quit()
            sys.exit()

    pygame.display.flip()
