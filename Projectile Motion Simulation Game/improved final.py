import pygame
import math
import sys
import random
import copy
from pygame.locals import *
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((1200, 800))

# Load and set the background image for the menu
mytheme = pygame_menu.themes.THEME_DARK.copy()
myimage = pygame_menu.baseimage.BaseImage(image_path="images/background.jpg", drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
mytheme.background_color = myimage

# Screen settings
X_view, Y_view = 1200, 800
Screen_View = pygame.display.set_mode((X_view, Y_view), 0, 32)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREEN = (1, 50, 32)
GREY = (211, 211, 211)
RED = (255, 0, 0)
FPS = 30

# Initialize global variables
global AI_win_count
AI_win_count = 0
global AI_difficulty
AI_difficulty = 100
global test_mode
test_mode = False

# Load images
TARGET = pygame.image.load("images/soilder.png")
TARGET = pygame.transform.scale(TARGET, (20, 40))
BALL = pygame.image.load("images/missle.png")
BALL = pygame.transform.scale(BALL, (40, 15))

# Font settings
Font = pygame.font.Font(None, 64)
questionfont = pygame.font.Font(None, 20)
fpsClock = pygame.time.Clock()

# Main screen dimensions
X_view, Y_view = 900, 600
Screen_View = pygame.display.set_mode((X_view, Y_view), 0, 32)
main_background = pygame.image.load("images/main_back.jpg")
main_background = pygame.transform.scale(main_background, (900, 375))
pygame.display.set_caption("Projectile Motion Simulation")

global win_loss_screen
win_loss_screen = False
global level
level = 0

class Button:
    def __init__(self, label, pos_x, pos_y, width, height, surface):
        self.label = label
        self.font = pygame.font.Font(None, 32)
        self.text_color = (255, 255, 255)
        self.pos_x = pos_x
        self.width = width
        self.height = height
        self.pos_y = pos_y
        self.background_color = (10, 200, 52)
        self.surface = surface

    def display(self):
        button = pygame.draw.rect(self.surface, self.background_color, (self.pos_x, self.pos_y, self.width, self.height))
        self._make_label()

    def _make_label(self):
        label_x = self.pos_x + 10
        label_y = self.pos_y + (self.height // 4)
        button_text = self.font.render(self.label, 1, self.text_color)
        self.surface.blit(button_text, (label_x, label_y))

    def click_seen(self, position):
        if (position[0] in range(self.pos_x, self.pos_x + self.width + 1)) and (position[1] in range(self.pos_y, self.pos_y + self.height + 1)):
            return True
        return False

class CheckBox:
    def __init__(self, pos_x, pos_y, size, surface, label, word_distance):
        self.font = pygame.font.Font(None, 25)
        self.white = (255, 255, 255)
        self.text_color = self.white
        self.word_distance = word_distance
        self.surface = surface
        self.green = (0, 255, 0)
        self.clicked = False
        self.start_x = pos_x
        self.start_y = pos_y
        self.size = size
        self.thickness = 8
        self.label = label

    def draw(self):
        top_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y), (self.start_x + self.size + 2, self.start_y), 1)
        bottom_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y + self.size + 2), (self.start_x + self.size + 2, self.start_y + self.size + 2), 1)
        right_line = pygame.draw.line(self.surface, self.white, (self.start_x + self.size + 2, self.start_y), (self.start_x + self.size + 2, self.start_y + self.size + 2), 1)
        left_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y), (self.start_x - 2, self.start_y + self.size + 2), 1)

        self._add_label()
        if self.clicked:
            self._add_tick()

    def click_seen(self, position):
        if (position[0] in range(self.start_x, self.start_x + self.size + 1)) and (position[1] in range(self.start_y, self.start_y + self.size + 1)):
            self.clicked = not self.clicked

    def _tick_coordinates(self):
        x1 = self.start_x
        y1 = self.start_y + (self.size // 2)
        x2 = self.start_x + (self.size // 2)
        y2 = self.start_y + self.size
        x3 = self.start_x + self.size
        y3 = self.start_y
        return x1, y1, x2, y2, x3, y3

    def _add_tick(self):
        x1, y1, x2, y2, x3, y3 = self._tick_coordinates()
        pygame.draw.line(self.surface, self.green, (x1, y1), (x2, y2), self.thickness)
        pygame.draw.line(self.surface, self.green, (x2, y2), (x3, y3), self.thickness)

    def _add_label(self):
        label_x = self.start_x - self.word_distance
        label_y = self.start_y + 8
        text = self.font.render(self.label, 1, self.text_color)
        self.surface.blit(text, (label_x, label_y))

class InputBox:
    def __init__(self, pos_x, pos_y, label, word_distance, max_length, range_tuple):
        self.start_x = pos_x
        self.max_length = max_length
        self.range = range_tuple
        self.start_y = pos_y
        self.variable = ""
        self.height = 30
        self.width = 200
        self.word_distance = word_distance
        self.clicked = False
        self.label = label
        self.surface = Screen_View
        self.font = pygame.font.Font(None, 25)
        self.white = (255, 255, 255)
        self.text_color = self.white

    def draw(self):
        top_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y), (self.start_x + self.width + 2, self.start_y), 1)
        bottom_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y + self.height + 2), (self.start_x + self.width + 2, self.start_y + self.height + 2), 1)
        right_line = pygame.draw.line(self.surface, self.white, (self.start_x + self.width + 2, self.start_y), (self.start_x + self.width + 2, self.start_y + self.height + 2), 1)
        left_line = pygame.draw.line(self.surface, self.white, (self.start_x - 2, self.start_y), (self.start_x - 2, self.start_y + self.height + 2), 1)
        self._add_label()
        self._display_variable()

    def _add_label(self):
        label_x = self.start_x - self.word_distance - 5
        label_y = self.start_y + 3
        text = self.font.render(self.label, 1, self.text_color)
        self.surface.blit(text, (label_x, label_y))

    def _display_variable(self):
        x_start = self.start_x + 5
        y_start = self.start_y + 3
        text = self.font.render(self.variable, 1, self.text_color)
        self.surface.blit(text, (x_start, y_start))

    def click_seen(self, position):
        if (position[0] in range(self.start_x, self.start_x + self.width + 1)) and (position[1] in range(self.start_y, self.start_y + self.height + 1)):
            self.clicked = True
        else:
            self.clicked = False

    def add_character(self, input_key):
        if input_key == K_BACKSPACE:
            self.variable = self.variable[:-1]
        elif len(self.variable) < self.max_length:
            if input_key == K_PERIOD and '.' not in self.variable:
                self.variable += '.'
            elif K_0 <= input_key <= K_9:
                char = chr(input_key)
                if self._num_in_range(char):
                    self.variable += char

    def _num_in_range(self, num):
        try:
            new_value = float(self.variable + num)
            return self.range[0] <= new_value <= self.range[1]
        except ValueError:
            return False

def create_widgets():
    displacement_box = InputBox(400, 190, "Displacement (s)(m):", 180, 6, (0.1, 1000))
    velocity_box = InputBox(400, 250, "Initial Velocity (u)(m/s):", 200, 6, (1, 100))
    angle_box = InputBox(400, 310, "Angle (θ)(degrees):", 165, 4, (1, 90))
    mass_box = InputBox(400, 370, "Mass (kg):", 90, 4, (0.1, 10))
    hide_check = CheckBox(480, 440, 30, Screen_View, "Hide Variables:", 140)
    ai_check = CheckBox(480, 480, 30, Screen_View, "AI (ON/OFF):", 120)
    submit_button = Button("Submit", 400, 540, 100, 40, Screen_View)
    return displacement_box, velocity_box, angle_box, mass_box, ai_check, hide_check, submit_button

def input_screen():
    title = Font.render("Answer/variable Input Screen", 1, WHITE)
    warning = questionfont.render("To input, select the box and type (max 2 digits), enter the given variables", 1, RED)
    displacement_box, velocity_box, angle_box, mass_box, ai_check, hide_check, submit_button = create_widgets()

    running = True
    px = random.randint(10, 100)
    py = random.randint(10, 100)
    ptheta = random.randint(10, 85)
    x_var = questionfont.render(f"x = {px}", 1, MAGENTA)
    theta_var = questionfont.render(f"θ = {ptheta}", 1, MAGENTA)
    y_var = questionfont.render(f"y = {py}", 1, MAGENTA)
    rad_ptheta = math.radians(ptheta)

    global a_ans, b_ans
    a_ans = (math.sin(rad_ptheta) * px * 2) / 9.81
    b_ans = math.cos(rad_ptheta) * px * a_ans

    while running:
        Screen_View.fill(BLACK)
        Screen_View.blit(title, (120, 5))
        Screen_View.blit(warning, (230, 55))

        if level == 5:
            question = questionfont.render("If a missile is launched from ground level with an initial velocity of x at an angle of θ degrees", 1, CYAN)
            question_a = questionfont.render("a) Calculate the time taken until it detonates the target", 1, CYAN)
            question_b = questionfont.render("b) How far was the target from the launch site", 1, CYAN)
            Screen_View.blit(question, (160, 80))
            Screen_View.blit(question_a, (280, 110))
            Screen_View.blit(question_b, (280, 140))
            Screen_View.blit(x_var, (430, 170))
            Screen_View.blit(theta_var, (420, 200))
        elif level == 6:
            question = questionfont.render("Given the initial velocity and angle, calculate the horizontal distance the projectile will cover.", 1, CYAN)
            Screen_View.blit(question, (160, 80))
        elif level == 7:
            question = questionfont.render("If the target is y kilometers away, what angle would you need to fire at, assuming velocity is unchanged?", 1, CYAN)
            Screen_View.blit(question, (80, 80))
            Screen_View.blit(y_var, (350, 130))
        elif level == 8:
            question = questionfont.render("Given a new target distance and new initial velocity, find the required angle for the projectile.", 1, CYAN)
            Screen_View.blit(question, (165, 80))

        displacement_box.draw()
        velocity_box.draw()
        angle_box.draw()
        mass_box.draw()
        ai_check.draw()
        hide_check.draw()
        submit_button.display()

        if test_mode:
            display_test_mode_values()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                displacement_box.click_seen(pos)
                velocity_box.click_seen(pos)
                angle_box.click_seen(pos)
                mass_box.click_seen(pos)
                hide_check.click_seen(pos)
                ai_check.click_seen(pos)
                if submit_button.click_seen(pos):
                    running = False
            elif event.type == KEYDOWN:
                if displacement_box.clicked:
                    displacement_box.add_character(event.key)
                elif velocity_box.clicked:
                    velocity_box.add_character(event.key)
                elif angle_box.clicked:
                    angle_box.add_character(event.key)
                elif mass_box.clicked:
                    mass_box.add_character(event.key)

        pygame.display.update()
        fpsClock.tick(FPS)

    h, u, angle = convert(displacement_box.variable, velocity_box.variable, angle_box.variable)
    if u and (angle or h):
        global b_input
        b_input = h
        h, u, v, t, angle, mode = calculate_ans(h, u, angle)
        run_simulation(h, u, v, t, angle, ai_check.clicked, hide_check.clicked, mode)
        show_error_message()

def change_ai_difficulty():
    global AI_difficulty, AI_win_count
    if AI_win_count < 0:
        AI_difficulty += 50
    elif AI_win_count > 0:
        AI_difficulty -= 50

def run_simulation(h, u, v, t, angle, ai_enabled, hide, mode):
    if u < 15 or angle < 15:
        input_screen()

    global AI_difficulty, AI_win_count, Screen_View

    # Calculate the initial values
    g = -9.8
    angle_radians = math.radians(angle)
    i = u * math.cos(angle_radians)
    j = u * math.sin(angle_radians)

    pos_x, pos_y = 50, 350  # Initial positions
    coordinates_list, max_x, max_y = get_coordinates(i, j, pos_x, pos_y)

    # Adjust screen dimensions based on max_x and max_y
    new_width = max(900, max_x + 100)  # Add some padding
    new_height = max(600, abs(max_y) + 100)  # Add some padding

    # Update the screen view
    Screen_View = pygame.display.set_mode((new_width, new_height))

    input_button = Button("Inputs", new_width - 300, new_height - 400, 200, 35, Screen_View)
    explain_button = Button("Explain", new_width - 300, new_height - 330, 200, 35, Screen_View)
    menu_button = Button("Return to Main Menu", new_width - 350, new_height - 260, 270, 40, Screen_View)
    hide_checkbox = CheckBox(new_width - 400, new_height - 400, 30, Screen_View, "Hide Parameters:", 160)
    hide_checkbox.clicked = hide

    floor_y_coord = new_height - 250
    pos_x, pos_y = 50, floor_y_coord
    scale_factor = 1.3
    trail_list = copy.deepcopy(coordinates_list)
    trail_list = tweak_trail(trail_list)
    motion = True
    pointer = 0

    Screen_View.fill(WHITE)
    running = True
    pos_x_ai, pos_y_ai = 500, floor_y_coord
    interceptor = pygame.image.load('images/flare.png')
    collision = False
    win = False

    change_ai_difficulty()

    while running:
        Screen_View.fill(BLACK)
        Screen_View.blit(main_background, (0, 0))
        input_button.display()
        explain_button.display()
        menu_button.display()
        hide_checkbox.draw()

        if not hide_checkbox.clicked:
            display_values(h, u, v, t, angle)

        if motion:
            pos_x, pos_y = coordinates_list[pointer]
            Screen_View.blit(BALL, (pos_x, pos_y))

            if level in (5, 6, 7, 8):
                Screen_View.blit(TARGET, (coordinates_list[-1][0], floor_y_coord - 20))

            if ai_enabled:
                diff_x, diff_y = pos_x_ai - pos_x, pos_y_ai - pos_y
                move_x, move_y = diff_x / AI_difficulty, diff_y / AI_difficulty
                x, y = random.randint(-2, 2), random.randint(-2, 2)
                pos_x_ai -= move_x + x
                pos_y_ai -= move_y + y
                Screen_View.blit(interceptor, (pos_x_ai, pos_y_ai))

                if (pos_x - 20 < pos_x_ai < pos_x + 20) and (pos_y - 20 < pos_y_ai < pos_y + 20):
                    collision = True

                if collision:
                    collision_img = pygame.image.load('images/collide.png')
                    collision_img = pygame.transform.scale(collision_img, (50, 50))
                    motion = False

            if pointer == len(coordinates_list) - 1:
                motion = False
            else:
                pointer += 1

        if not motion:
            if collision:
                Screen_View.blit(collision_img, (pos_x, pos_y))
                win = False
                AI_win_count += 1
                AI_difficulty *= 2
                show_loss_screen(win, h, u, v, t, angle, ai_enabled, hide_checkbox, mode)
            else:
                win = True
                AI_win_count -= 1
                AI_difficulty /= 2
                show_win_screen(win, h, u, v, t, angle, ai_enabled, hide_checkbox, mode)

        if pointer > 1:
            pygame.draw.aalines(Screen_View, MAGENTA, False, trail_list[:pointer + 1000], 5)
            pygame.draw.aalines(Screen_View, CYAN, False, trail_list[:pointer], 5)

        pygame.draw.line(Screen_View, BLACK, (0, floor_y_coord + 25), (new_width, floor_y_coord + 25), 1)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                hide_checkbox.click_seen(pos)
                if input_button.click_seen(pos):
                    input_screen()
                elif explain_button.click_seen(pos):
                    if mode == 1:
                        show_explanations_1(h, u, v, t, angle, ai_enabled, hide_checkbox.clicked, mode)
                    elif mode == 2:
                        show_explanations_2(h, u, v, t, angle, ai_enabled, hide_checkbox.clicked, mode)
                elif menu_button.click_seen(pos):
                    menu.mainloop(surface)

        pygame.display.update()
        fpsClock.tick(FPS)

def show_win_screen(win, s, u, v, t, angle, ai, hide, mode):
    message = Font.render("You are correct!!", 1, WHITE)
    while win:
        win_loss_screen = True
        Screen_View.fill(BLACK)
        Screen_View.blit(message, (260, 250))
        menu_button = Button("Return to Main Menu", 300, 530, 270, 40, Screen_View)
        explain_button = Button("Explain", 340, 450, 200, 35, Screen_View)
        menu_button.display()
        explain_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                hide.click_seen(pos)
                if menu_button.click_seen(pos):
                    win = False
                    menu.mainloop(surface)
                elif explain_button.click_seen(pos):
                    if mode == 1:
                        show_explanations_1(s, u, v, t, angle, ai, hide.clicked, mode)
                    elif mode == 2:
                        show_explanations_2(s, u, v, t, angle, ai, hide.clicked, mode)

        pygame.display.update()
        fpsClock.tick(FPS)

def show_loss_screen(win, s, u, v, t, angle, ai, hide, mode):
    message = Font.render("Sadly, you are incorrect, try again", 1, WHITE)
    while not win:
        win_loss_screen = True
        Screen_View.fill(BLACK)
        Screen_View.blit(message, (120, 250))
        menu_button = Button("Return to Main Menu", 300, 530, 270, 40, Screen_View)
        explain_button = Button("Explain", 340, 450, 200, 35, Screen_View)
        menu_button.display()
        explain_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.click_seen(pos):
                    menu.mainloop(surface)
                elif explain_button.click_seen(pos):
                    if mode == 1:
                        show_explanations_1(s, u, v, t, angle, ai, hide.clicked, mode)
                    elif mode == 2:
                        show_explanations_2(s, u, v, t, angle, ai, hide.clicked, mode)

        pygame.display.update()
        fpsClock.tick(FPS)

def show_explanations_1(h, u, v, t, angle, ai, hide, mode):
    explanation_font = pygame.font.Font(None, 32)
    explaining = True

    v_explain2_str = f"v = -{u}"
    time_explain3_str = f"t = {u}sin({angle})/4.9"
    angle_explain3_str = f"θ = sin^-1(√(2*g*{h}))/u"

    v_explain1 = explanation_font.render("v = -u", 1, WHITE)
    v_explain2 = explanation_font.render(v_explain2_str, 1, WHITE)
    angle_explain1 = explanation_font.render("Rearrange v^2 =u^2 + 2as where v = 0", 1, WHITE)
    angle_explain2 = explanation_font.render("usinθ = √(2gs) => θ = sin^-1((√2gs))/u", 1, WHITE)
    angle_explain3 = explanation_font.render(angle_explain3_str, 1, WHITE)
    time_explain1 = explanation_font.render("Rearrange s = ut + 0.5at^2 where s = 0", 1, WHITE)
    time_explain2 = explanation_font.render("t = usinθ/4.9", 1, WHITE)
    time_explain3 = explanation_font.render(time_explain3_str, 1, WHITE)
    ok_button = Button("OK", 400, 500, 100, 35, Screen_View)

    while explaining:
        display_explanations(v_explain1, v_explain2, angle_explain1, angle_explain2, angle_explain3, time_explain1, time_explain2, time_explain3, ok_button)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    explaining = False
                    if win_loss_screen:
                        menu.mainloop(surface)

        pygame.display.update()
        fpsClock.tick(FPS)

def show_explanations_2(h, u, v, t, angle, ai, hide, mode):
    explanation_font = pygame.font.Font(None, 32)
    explaining = True

    v_explain2_str = f"v = -{u}"
    time_explain3_str = f"t = {u}sin({angle})/4.9"
    displacement_explain3_str = f"s = {u}sin({angle})({round(t, 2)}/2) - 4.9({round(t, 2)}/2)^2"

    v_explain1 = explanation_font.render("v = -u", 1, WHITE)
    v_explain2 = explanation_font.render(v_explain2_str, 1, WHITE)
    time_explain1 = explanation_font.render("Rearrange s = ut + 0.5at^2 where s = 0", 1, WHITE)
    time_explain2 = explanation_font.render("t = usinθ/4.9", 1, WHITE)
    time_explain3 = explanation_font.render(time_explain3_str, 1, WHITE)
    displacement_explain1 = explanation_font.render("At time, t/2, height is at a max => using s = ut + 0.5at^2", 1, WHITE)
    displacement_explain2 = explanation_font.render("s = usinθ(t/2) - 4.9(t/2)^2", 1, WHITE)
    displacement_explain3 = explanation_font.render(displacement_explain3_str, 1, WHITE)
    ok_button = Button("OK", 400, 500, 100, 35, Screen_View)

    while explaining:
        display_explanations(v_explain1, v_explain2, time_explain1, time_explain2, time_explain3, displacement_explain1, displacement_explain2, displacement_explain3, ok_button)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    explaining = False
                    if win_loss_screen:
                        menu.mainloop(surface)

        pygame.display.update()
        fpsClock.tick(FPS)

def display_explanations(a, b, c, d, e, f, g, h, button):
    Screen_View.fill(BLACK)
    Screen_View.blit(a, (40, 30))
    Screen_View.blit(b, (40, 70))
    Screen_View.blit(c, (40, 120))
    Screen_View.blit(d, (40, 170))
    Screen_View.blit(e, (40, 220))
    Screen_View.blit(f, (40, 270))
    Screen_View.blit(g, (40, 320))
    Screen_View.blit(h, (40, 370))
    button.display()

def convert(displacement, velocity, angle):
    try:
        displacement = float(displacement)
    except ValueError:
        displacement = ""
    try:
        velocity = float(velocity)
    except ValueError:
        velocity = ""
    try:
        angle = float(angle)
        angle = math.radians(angle)
    except ValueError:
        angle = ""
    return displacement, velocity, angle

def get_coordinates(i, j, pos_x, pos_y):
    g = -9.8
    vertical_list = vertical_coordinates(j, g, pos_y, True, False)
    horizontal_list = x_coordinates(i, pos_x, len(vertical_list))
    main_list = merge_lists(horizontal_list, vertical_list)

    # Calculate max_x and max_y
    max_x = max(horizontal_list)
    max_y = min(vertical_list)  # Since vertical_list contains negative values for upward motion

    # Scaling factors based on screen size
    scale_x = X_view / (max_x + 100)
    scale_y = Y_view / (abs(max_y) + 100)

    scaled_main_list = scale_coordinates(main_list, scale_x, scale_y)

    return scaled_main_list, max_x, max_y

def vertical_coordinates(j, g, pos_y, up, down):
    scale_factor = 2
    floor_y_coord = 350
    if up:
        pos_y -= (scale_factor * (j / FPS))
        j += (g / FPS)
        if j <= 0:
            return [pos_y] + vertical_coordinates(j, g, pos_y, False, True)
        return [pos_y] + vertical_coordinates(j, g, pos_y, True, False)
    elif down:
        pos_y -= (scale_factor * (j / FPS))
        j += (g / FPS)
        if pos_y >= floor_y_coord:
            return [pos_y]
        return [pos_y] + vertical_coordinates(j, g, pos_y, False, True)

def x_coordinates(i, pos_x, length_of_vertical_list):
    scale_factor = 2
    coordinates = []
    for _ in range(length_of_vertical_list):
        pos_x += (scale_factor * (i / FPS))
        coordinates.append(pos_x)
    return coordinates

def merge_lists(list_x, list_y):
    merged_list = []
    for i in range(len(list_x)):
        merged_list.append([list_x[i], list_y[i]])
    return round_coordinates(merged_list)

def round_coordinates(coordinates):
    for coord in coordinates:
        coord[0] = round(coord[0], 1)
        coord[1] = round(coord[1], 1)
    return coordinates

def scale_coordinates(coordinates, scale_x, scale_y):
    for coord in coordinates:
        coord[0] *= scale_x
        coord[1] *= scale_y
    return coordinates

def tweak_trail(trail):
    for coord in trail:
        coord[0] += 2
        coord[1] += 13
    return trail

def display_values(h, u, v, t, angle):
    parameter_font = pygame.font.Font(None, 30)
    displacement = parameter_font.render(f"S  = {b_ans:.1f} m", 1, WHITE)
    initial_velocity = parameter_font.render(f"U = {u:.1f} m/s", 1, WHITE)
    final_velocity = parameter_font.render(f"V = {v:.1f} m/s", 1, WHITE)
    acceleration = parameter_font.render("A = -g = -9.8 m/s^2", 1, WHITE)
    time = parameter_font.render(f"T = {t:.1f} s", 1, WHITE)
    angle = parameter_font.render(f"θ = {angle:.1f}°", 1, WHITE)

    Screen_View.blit(displacement, (40, 400))
    Screen_View.blit(initial_velocity, (40, 430))
    Screen_View.blit(final_velocity, (40, 460))
    Screen_View.blit(acceleration, (40, 490))
    Screen_View.blit(time, (40, 520))
    Screen_View.blit(angle, (40, 550))

def display_test_mode_values():
    parameter_font = pygame.font.Font(None, 30)
    displacement = parameter_font.render(f"Correct S  = {b_ans:.1f} m", 1, RED)
    time = parameter_font.render(f"Correct T = {a_ans:.1f} s", 1, RED)
    
    Screen_View.blit(displacement, (650, 500))  # Adjusted x-coordinate
    Screen_View.blit(time, (650, 530))  # Adjusted x-coordinate

def show_error_message():
    title1 = Font.render("Please Enter The Initial Velocity &", 1, WHITE)
    title2 = Font.render("EITHER The Angle Of Projection", 1, WHITE)
    title3 = Font.render("OR The Displacement", 1, WHITE)
    ok_button = Button("OK", 380, 450, 100, 40, Screen_View)
    running = True

    while running:
        Screen_View.fill(BLACK)
        Screen_View.blit(title1, (85, 100))
        Screen_View.blit(title2, (100, 200))
        Screen_View.blit(title3, (170, 300))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False

        pygame.display.update()
        fpsClock.tick(FPS)

    input_screen()

def calculate_ans(h, u, angle):
    g = 9.8
    if h and not angle:
        if math.sqrt(2 * g * h) / u > 1:
            show_impossible_situation()
        else:
            mode = 1
            v = -u
            angle = math.asin(math.sqrt(2 * g * h) / u)
            t = (u * math.sin(angle)) / 4.9
            return h, u, v, t, math.degrees(angle), mode
    elif not h and angle:
        mode = 2
        v = -u
        t = (u * math.sin(angle)) / 4.9
        h = (u * math.sin(angle) * (t / 2)) - (4.9 * (t / 2) ** 2)
        return h, u, v, t, math.degrees(angle), mode
    else:
        show_error_message()

def show_impossible_situation():
    title1 = Font.render("The inputs are not valid.", 1, WHITE)
    title2 = Font.render("The value for Displacement is too high", 1, WHITE)
    title3 = Font.render("for the given velocity.", 1, WHITE)
    title4 = Font.render("Such a situation shouldn't occur.", 1, WHITE)
    title5 = Font.render("Please reload the program.", 1, WHITE)
    ok_button = Button("OK", 350, 500, 100, 40, Screen_View)
    running = True

    while running:
        Screen_View.fill(BLACK)
        Screen_View.blit(title1, (150, 50))
        Screen_View.blit(title2, (40, 130))
        Screen_View.blit(title3, (175, 210))
        Screen_View.blit(title4, (70, 290))
        Screen_View.blit(title5, (180, 370))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False
                    input_screen()

        pygame.display.update()
        fpsClock.tick(FPS)

def load_level_1():
    show_units()

def load_level_2():
    show_components()

def load_level_3():
    show_velocity_level()

def load_level_4():
    show_acceleration_level()

def load_level_5():
    global level
    level = 5
    input_screen()

def load_level_6():
    global level
    level = 6
    input_screen()

def load_level_7():
    global level
    level = 7
    input_screen()

def load_level_8():
    global level
    level = 8
    input_screen()

def show_units():
    font = pygame.font.Font(None, 33)
    title1 = font.render("Displacement, letter s, measured in meters, unit symbol m", 1, RED)
    title2 = font.render("Initial velocity, letter u, measured in meters per second, unit symbol m/s", 1, RED)
    title3 = font.render("Final velocity, letter v, measured in meters per second, unit symbol m/s", 1, RED)
    title4 = font.render("Acceleration, letter a, measured in meters per second squared, unit symbol m/s^2", 1, RED)
    title5 = font.render("Time, letter t, measured in seconds, unit symbol s", 1, RED)
    ok_button = Button("OK", 380, 550, 100, 40, Screen_View)
    running = True

    while running:
        Screen_View.fill(WHITE)
        Screen_View.blit(title1, (0, 50))
        Screen_View.blit(title2, (0, 150))
        Screen_View.blit(title3, (0, 250))
        Screen_View.blit(title4, (0, 350))
        Screen_View.blit(title5, (0, 450))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False

        pygame.display.update()
        fpsClock.tick(FPS)

def show_components():
    font = pygame.font.Font(None, 33)
    title1 = font.render("Every force is made up of two components, horizontal and vertical, as shown in the diagram", 1, RED)
    title2 = font.render("You can find the horizontal component by doing Fcos(angle)", 1, RED)
    title3 = font.render("You can find the vertical component by doing Fsin(angle)", 1, RED)
    ok_button = Button("OK", 380, 550, 100, 40, Screen_View)
    running = True
    image = pygame.image.load('images/components.png')

    while running:
        Screen_View.fill(WHITE)
        Screen_View.blit(title1, (0, 50))
        Screen_View.blit(title2, (0, 150))
        Screen_View.blit(title3, (0, 250))
        Screen_View.blit(image, (300, 300))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False

        pygame.display.update()
        fpsClock.tick(FPS)

def show_velocity_level():
    font = pygame.font.Font(None, 30)
    large_font = pygame.font.Font(None, 55)
    title1 = Font.render("Velocity is the rate of change of distance", 1, RED)
    title2 = large_font.render("You can find the velocity by doing distance/time", 1, RED)
    title3 = font.render("Remember velocity is a vector, so depending on the direction can be negative or positive", 1, RED)
    ok_button = Button("OK", 380, 550, 100, 40, Screen_View)
    running = True
    image = pygame.image.load('images/velocitydiagram.png')

    while running:
        Screen_View.fill(WHITE)
        Screen_View.blit(title1, (0, 50))
        Screen_View.blit(title2, (10, 150))
        Screen_View.blit(title3, (10, 250))
        Screen_View.blit(image, (70, 300))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False

        pygame.display.update()
        fpsClock.tick(FPS)

def show_acceleration_level():
    font = pygame.font.Font(None, 30)
    large_font = pygame.font.Font(None, 55)
    small_font = pygame.font.Font(None, 25)
    title1 = large_font.render("Acceleration is the rate of change of velocity", 1, RED)
    title2 = large_font.render("You can find the acceleration by doing (v-u)/t", 1, RED)
    title3 = font.render("Remember acceleration is a vector, so depending on the direction can be negative or positive", 1, RED)
    title4 = font.render("Newton's 2nd law: F=ma, you can also use this to find acceleration", 1, RED)
    title5 = small_font.render("In projectile motion, the only acceleration on the object is g, so acceleration always equals to -9.81 m/s^2", 1, RED)
    ok_button = Button("OK", 380, 550, 100, 40, Screen_View)
    running = True

    while running:
        Screen_View.fill(WHITE)
        Screen_View.blit(title1, (40, 50))
        Screen_View.blit(title2, (30, 150))
        Screen_View.blit(title3, (0, 250))
        Screen_View.blit(title4, (100, 350))
        Screen_View.blit(title5, (15, 450))
        ok_button.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ok_button.click_seen(pos):
                    running = False

        pygame.display.update()
        fpsClock.tick(FPS)

# Create the main menu
menu = pygame_menu.Menu("Projectile Motion Simulation", 900, 600, theme=mytheme)
test_mode_checkbox = CheckBox(750, 540, 30, surface, "Test Mode:", 120)

def set_test_mode():
    global test_mode
    test_mode = test_mode_checkbox.clicked

menu.add.button('Level 1: Units and Conversions', load_level_1)
menu.add.button('Level 2: Components', load_level_2)
menu.add.button('Level 3: Velocity', load_level_3)
menu.add.button('Level 4: Acceleration', load_level_4)
menu.add.button('Level 5: Exam Questions 1', load_level_5)
menu.add.button('Level 6: Exam Questions 2', load_level_6)
menu.add.button('Level 7: Exam Questions 3', load_level_7)
menu.add.button('Level 8: Exam Questions 4', load_level_8)
menu.add.button('Quit', pygame_menu.events.EXIT)

def menu_loop():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        menu.update(events)
        menu.draw(surface)
        test_mode_checkbox.draw()
        set_test_mode()

        pygame.display.flip()
        fpsClock.tick(30)

menu_loop()
