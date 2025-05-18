import pygame
import sys
import random
from pygame.math import Vector2
import json
import os

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)
        
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Modal:
    def __init__(self, width, height, title, content):
        self.width = width
        self.height = height
        self.title = title
        self.content = content
        self.visible = False
        self.rect = pygame.Rect(
            (screen.get_width() - width) // 2,
            (screen.get_height() - height) // 2,
            width,
            height
        )
        self.close_button = Button(
            self.rect.right - 40, self.rect.top + 10, 
            35, 35, "X", (200, 50, 50), (250, 70, 70))
        
    def draw(self, surface):
        if not self.visible:
            return
            
       
        s = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        surface.blit(s, (0, 0))
        
        
        pygame.draw.rect(surface, (240, 240, 240), self.rect, border_radius=15)
        pygame.draw.rect(surface, (50, 50, 50), self.rect, 3, border_radius=15)
        
       
        title_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
        title_surface = title_font.render(self.title, True, (50, 50, 150))
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        
       
        pygame.draw.rect(surface, (200, 200, 255), 
                            (title_rect.left - 20, title_rect.top - 10, 
                             title_rect.width + 40, title_rect.height + 10), 
                            border_radius=10)
        pygame.draw.rect(surface, (50, 50, 150), 
                            (title_rect.left - 20, title_rect.top - 10, 
                             title_rect.width + 40, title_rect.height + 10), 
                            2, border_radius=10)
        
        surface.blit(title_surface, title_rect)
        
       
        content_font = pygame.font.Font(None, 24)
        y_offset = title_rect.bottom + 20
        
        for line in self.content.split('\n'):
            if "════" in line:  
                line_surface = content_font.render(line, True, (100, 100, 100))
            else:
                line_surface = content_font.render(line, True, (0, 0, 0))
                
            line_rect = line_surface.get_rect(center=(self.rect.centerx, y_offset))
            surface.blit(line_surface, line_rect)
            y_offset += 30
        
      
        self.close_button.draw(surface)
        
    def handle_event(self, event):
        if not self.visible:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        self.close_button.check_hover(mouse_pos)
        
        if self.close_button.is_clicked(mouse_pos, event):
            self.visible = False
            return True
            
        return False

class SNAKE:
    def __init__(self):
        self.reset()
        self.load_graphics()
        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')
        
    def load_graphics(self):
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        if len(self.body) > 1:
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1, 0): self.head = self.head_left
            elif head_relation == Vector2(-1, 0): self.head = self.head_right
            elif head_relation == Vector2(0, 1): self.head = self.head_up
            elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        if len(self.body) > 1:
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1, 0): self.tail = self.tail_left
            elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
            elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
            elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  
        self.new_block = False

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_active = False
        self.game_over = False
        self.score = 0
        self.high_scores = self.load_high_scores()
        self.difficulty = "Medium"  
        
    def update(self):
        if self.game_active and not self.game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        if self.game_active:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
        else:
            self.draw_welcome_screen()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1 
            self.snake.play_crunch_sound()
            print(f"Apple eaten, score: {self.score}")
            
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def check_fail(self):
       
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.end_game()
            
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.end_game()

    def end_game(self):
        self.game_over = True
        self.update_high_scores()
        
    def reset_game(self):
        self.snake.reset()
        self.fruit.randomize()
        self.game_over = False
        self.score = 0
        self.game_active = True
        
        
        pygame.time.set_timer(SCREEN_UPDATE, self.get_speed())

    def get_speed(self):
        if self.difficulty == "Easy":
            return 200  
        elif self.difficulty == "Medium":
            return 150 
        elif self.difficulty == "Hard":
            return 100  
        return 150  

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
        
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_welcome_screen(self):
        print("Drawing welcome screen")
        
        screen.fill((175, 215, 70))
        
      
        title_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
        title_surface = title_font.render("SNAKE GAME", True, (56, 74, 12))
        title_rect = title_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//4))
        screen.blit(title_surface, title_rect)
        
       
        diff_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
        diff_surface = diff_font.render("Select Difficulty:", True, (56, 74, 12))
        diff_rect = diff_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 80))
        screen.blit(diff_surface, diff_rect)
        
   
        easy_button.rect.center = (screen.get_width()//2 - button_width - button_spacing//2, screen.get_height()//2 - 20)
        medium_button.rect.center = (screen.get_width()//2, screen.get_height()//2 - 20)
        hard_button.rect.center = (screen.get_width()//2 + button_width + button_spacing//2, screen.get_height()//2 - 20)
        
        for button in [easy_button, medium_button, hard_button]:
            button.draw(screen)
        
        
        current_diff_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        current_diff_surface = current_diff_font.render(f"Current: {self.difficulty}", True, (56, 74, 12))
        current_diff_rect = current_diff_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 30))
        screen.blit(current_diff_surface, current_diff_rect)
        
        
        start_button.rect.center = (screen.get_width()//2, screen.get_height()//2 + 100)
        highscores_button.rect.center = (screen.get_width()//2, screen.get_height()//2 + 160)
        instructions_button.rect.center = (screen.get_width()//2, screen.get_height()//2 + 220)
        quit_button.rect.center = (screen.get_width()//2, screen.get_height()//2 + 280)
        
        for button in [start_button, highscores_button, instructions_button, quit_button]:
            button.draw(screen)

    def draw_game_over(self):
       
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
        game_over_surface = game_over_font.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//3))
        screen.blit(game_over_surface, game_over_rect)
        
        
        score_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        score_surface = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(score_surface, score_rect)
        
        if self.score > 0 and self.score >= self.get_high_score_for_difficulty():
            high_score_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
            high_score_surface = high_score_font.render("New High Score!", True, (255, 215, 0))
            high_score_rect = high_score_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
            screen.blit(high_score_surface, high_score_rect)
        
       
        restart_button.rect.center = (screen.get_width()//2 - button_width//2 - button_spacing//2, screen.get_height()//2 + 120)
        menu_button.rect.center = (screen.get_width()//2 + button_width//2 + button_spacing//2, screen.get_height()//2 + 120)
        quit_button_game_over.rect.center = (screen.get_width()//2, screen.get_height()//2 + 180)
        
        for button in [restart_button, menu_button, quit_button_game_over]:
            button.draw(screen)

    def load_high_scores(self):
        try:
            if os.path.exists('highscores.json'):
                with open('highscores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"Easy": 0, "Medium": 0, "Hard": 0}

    def save_high_scores(self):
        with open('highscores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def update_high_scores(self):
        current_high = self.get_high_score_for_difficulty()
        if self.score > current_high:
            self.high_scores[self.difficulty] = self.score
            self.save_high_scores()

    def get_high_score_for_difficulty(self):
        return self.high_scores.get(self.difficulty, 0)

    def draw_high_scores_modal(self):
        
        modal_surface = pygame.Surface((600, 500), pygame.SRCALPHA)
        
      
        pygame.draw.rect(modal_surface, (0, 0, 0, 30), (10, 10, 580, 480), border_radius=15)
        pygame.draw.rect(modal_surface, (240, 240, 240), (0, 0, 580, 480), border_radius=15)
        pygame.draw.rect(modal_surface, (50, 50, 50), (0, 0, 580, 480), 3, border_radius=15)
        
        
        title_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        title_surface = title_font.render("HIGH SCORES", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(290, 60))
        
        
        pygame.draw.rect(modal_surface, (200, 200, 255), 
                            (title_rect.left - 20, title_rect.top - 10, 
                             title_rect.width + 40, title_rect.height + 20), 
                            border_radius=10)
        pygame.draw.rect(modal_surface, (50, 50, 150), 
                            (title_rect.left - 20, title_rect.top - 10, 
                             title_rect.width + 40, title_rect.height + 20), 
                            2, border_radius=10)
        
        modal_surface.blit(title_surface, title_rect)
        
       
        
        
        header_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
        y_offset = 120
        for diff in ["Easy", "Medium", "Hard"]:
            
            diff_surface = header_font.render(diff, True, (255, 255, 255))
            diff_rect = diff_surface.get_rect(center=(290, y_offset))
            
           
            if diff == "Easy":
                bg_color = (70, 200, 70)
            elif diff == "Medium":
                bg_color = (70, 70, 200)
            else:
                bg_color = (200, 70, 70)
                
            pygame.draw.rect(modal_surface, bg_color, 
                                (diff_rect.left - 20, diff_rect.top - 10, 
                                 diff_rect.width + 40, diff_rect.height + 20), 
                                border_radius=10)
            pygame.draw.rect(modal_surface, (0, 0, 0), 
                                (diff_rect.left - 20, diff_rect.top - 10, 
                                 diff_rect.width + 40, diff_rect.height + 20), 
                                2, border_radius=10)
            
            modal_surface.blit(diff_surface, diff_rect)
            
            
            score_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 35)
            score_surface = score_font.render(str(self.high_scores.get(diff, 0)), True, (0, 0, 0))
            score_rect = score_surface.get_rect(center=(290, y_offset + 50))
           
            pygame.draw.rect(modal_surface, (255, 255, 255), 
                                (score_rect.left - 20, score_rect.top - 10, 
                                 score_rect.width + 40, score_rect.height + 20), 
                                border_radius=10)
            pygame.draw.rect(modal_surface, (0, 0, 0), 
                                (score_rect.left - 20, score_rect.top - 10, 
                                 score_rect.width + 40, score_rect.height + 20), 
                                2, border_radius=10)
            
            modal_surface.blit(score_surface, score_rect)
            
            y_offset += 120
       
        close_button_rect = pygame.Rect(modal_surface.get_width() - 60, 20, 40, 40)
        
        for i in range(40):
            color_val = 200 - (i * 2)
            pygame.draw.rect(modal_surface, (color_val, 50, 50), 
                                (close_button_rect.x, close_button_rect.y + i, 
                                 close_button_rect.width, 1))
        
        pygame.draw.rect(modal_surface, (0, 0, 0), close_button_rect, 2, border_radius=20)
        
        close_text = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30).render("×", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        modal_surface.blit(close_text, close_text_rect)
        
        
        modal_rect = modal_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(modal_surface, modal_rect)
        
        return close_button_rect.move(modal_rect.topleft)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 35  
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


try:
    apple = pygame.image.load('Graphics/apple.png').convert_alpha()
except FileNotFoundError:
    print("Error: Graphics/apple.png not found!")
    sys.exit()

try:
    game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
except FileNotFoundError:
    print("Error: Font/PoetsenOne-Regular.ttf not found!")
    sys.exit()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  

main_game = MAIN()


button_width = 150
button_height = 50
button_spacing = 20


easy_button = Button(0, 0, button_width, button_height, "Easy", (50, 50, 50), (70, 200, 70))
medium_button = Button(0, 0, button_width, button_height, "Medium", (50, 50, 150), (70, 70, 200))
hard_button = Button(0, 0, button_width, button_height, "Hard", (50, 50, 50), (200, 70, 70))

start_button = Button(0, 0, button_width, button_height, "Start Game", (50, 150, 50), (70, 200, 70))
highscores_button = Button(0, 0, button_width, button_height, "High Scores", (150, 50, 150), (200, 70, 200))
instructions_button = Button(0, 0, button_width, button_height, "How to Play", (50, 150, 150), (70, 200, 200))
quit_button = Button(0, 0, button_width, button_height, "Quit", (150, 50, 50), (200, 70, 70))

restart_button = Button(0, 0, button_width, button_height, "Restart", (50, 150, 50), (70, 200, 70))
menu_button = Button(0, 0, button_width, button_height, "Main Menu", (50, 50, 150), (70, 70, 200))
quit_button_game_over = Button(0, 0, button_width, button_height, "Quit", (150, 50, 50), (200, 70, 70))


instructions_modal = Modal(
    500, 400,  
    "HOW TO PLAY",
    "\n"
    "Use arrow keys to control the snake\n"
    "Eat apples to grow longer\n"
    "Avoid walls and your own tail!\n"
    "Game speeds up as you grow!\n"
    "\n"
    "Select difficulty before starting:\n"
    " Easy: Slow and steady\n"
    " Medium: Balanced challenge\n"
    " Hard: Lightning speed!"
)

high_scores_modal_visible = False
close_high_scores_rect = None


while True:
    mouse_pos = pygame.mouse.get_pos()
    
    
    if not main_game.game_active or main_game.game_over:
        for button in [easy_button, medium_button, hard_button, start_button, 
                        highscores_button, instructions_button, quit_button,
                        restart_button, menu_button, quit_button_game_over]:
            button.check_hover(mouse_pos)
    
 
    if high_scores_modal_visible:
        print("Drawing high scores modal")
        close_high_scores_rect = main_game.draw_high_scores_modal()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == SCREEN_UPDATE and main_game.game_active and not main_game.game_over:
            main_game.update()
            
        if event.type == pygame.KEYDOWN and main_game.game_active and not main_game.game_over:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if not main_game.game_active:
                if easy_button.is_clicked(mouse_pos, event):
                    main_game.difficulty = "Easy"
                elif medium_button.is_clicked(mouse_pos, event):
                    main_game.difficulty = "Medium"
                elif hard_button.is_clicked(mouse_pos, event):
                    main_game.difficulty = "Hard"
                elif start_button.is_clicked(mouse_pos, event):
                    main_game.reset_game()
                elif highscores_button.is_clicked(mouse_pos, event):
                    print("High Scores button clicked")
                    high_scores_modal_visible = True
                elif instructions_button.is_clicked(mouse_pos, event):
                    instructions_modal.visible = True
                elif quit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
                
           
            elif main_game.game_over:
                if restart_button.is_clicked(mouse_pos, event):
                    main_game.reset_game()
                elif menu_button.is_clicked(mouse_pos, event):
                    main_game.game_active = False
                    main_game.game_over = False
                elif quit_button_game_over.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
                
            
            if high_scores_modal_visible and close_high_scores_rect and close_high_scores_rect.collidepoint(mouse_pos):
                high_scores_modal_visible = False
            
            
            if instructions_modal.handle_event(event):
                pass
    
    
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    

    if instructions_modal.visible:
        instructions_modal.draw(screen)

   
    if high_scores_modal_visible:
        print("Drawing high scores modal")
        close_high_scores_rect = main_game.draw_high_scores_modal()
    
    pygame.display.update()
    clock.tick(60)