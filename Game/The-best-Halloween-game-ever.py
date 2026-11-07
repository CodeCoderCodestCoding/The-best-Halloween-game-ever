#Modules required
from PIL import Image
from pathlib import Path
import sys
import json
import os
import random
import pygame

#Initialisation
pygame.init()
pygame.font.init()
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Assets"
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
dt = 0
pygame.mixer.set_num_channels(32)

#Settings
SETTINGS_FILE = "settings.json"
default_settings = {
    "Checked tickboxes": [],
    "Epilepsy safety": False,
    "FPS": 60
}
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                return {**default_settings, **json.load(file)}
        except (json.JSONDecodeError, OSError):
            pass
    return default_settings.copy()
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

#Loading fonts and text objects
menu_font = pygame.font.SysFont("Retro Pixel", 60)
small_menu_font = pygame.font.SysFont("Retro Pixel", 40)
instruction_font = pygame.font.SysFont("Retro Pixel", 30)
dialogue_font = pygame.font.SysFont("Retro Pixel", 25)
complete_font = pygame.font.SysFont("Retro Pixel", 50)
tome_font = pygame.font.SysFont("Retro Pixel", 30)

pause_menu_title = menu_font.render("The best Halloween game ever", False, (255, 255, 255))
pause_menu_title_rect = pause_menu_title.get_rect(topleft = (100, 125))
settings_menu_title = menu_font.render("Settings", False, (255, 255, 255))
settings_menu_title_rect = settings_menu_title.get_rect(topleft = (325, 100))

settings_text = [
    small_menu_font.render("Epilepsy Safety:", False, (255, 255, 255)),
    small_menu_font.render("FPS:", False, (255, 255, 255))
]

instruction_jump = instruction_font.render("W to jump", False, (255, 255, 255))
instruction_jump_rect = instruction_jump.get_rect(topleft = (200, 300))
instruction_move = instruction_font.render("A/D to move left/right", False, (255, 255, 255))
instruction_move_rect = instruction_move.get_rect(topleft = (200, 330))
instruction_crouch = instruction_font.render("S to crouch", False, (255, 255, 255))
instruction_crouch_rect = instruction_crouch.get_rect(topleft = (200, 360))
instruction_interact = instruction_font.render("F to interact with things", False, (255, 255, 255))
instruction_interact_rect = instruction_interact.get_rect(topleft = (200, 390))

blargh_dialogue = dialogue_font.render("Want to get out of here?", False, (255, 255, 255))
yes_dialogue = dialogue_font.render("Yeah! (1)", False, (255, 255, 255))
no_dialogue = dialogue_font.render("No (2)", False, (255, 255, 255))
blargh_dialogue_rect = pygame.Rect(150, 350, 500, 150)

level_complete = complete_font.render("LEVEL COMPLETE", False, (255, 255, 255))
level_complete_rect = level_complete.get_rect(topleft = (50, 375))

tome_content = [
    tome_font.render("The breaker box is in the basement...someone turned it off..", False, (255, 255, 255)),
    tome_font.render("The kitchen floor is weird...", False, (255, 255, 255)),
    tome_font.render("What's in that cabinet?", False, (255, 255, 255)),
    tome_font.render("Last I checked, the fireplace was empty...could do with some heat...", False, (255, 255, 255)),
    tome_font.render("There has to be a fire alarm here somewhere, right?", False, (255, 255, 255)),
    tome_font.render("BLARGH WAS HERE...he didn't get out", False, (255, 255, 255)),
    tome_font.render("blargh never really liked noise...", False, (255, 255, 255))
]
tome_content_rect = pygame.Rect(25, 25, 750, 550)

#Loading background function
def load_background(image_path, screen_size):
    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(screen_size, Image.LANCZOS)
        img_bytes = img.tobytes()
        surface = pygame.image.frombuffer(img_bytes, img.size, "RGBA").copy()
        return surface
    except Exception as e:
        print(f"Error loading background: {e}")
        sys.exit(1)

#Loading backgrounds
outside = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Outside.png", screen_size)
stormy_outside = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Stormy.png", screen_size)
lightning1 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning1.png", screen_size)
lightning2 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning2.png", screen_size)
lightning3 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning3.png", screen_size)
lightning4 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning4.png", screen_size)
lightning5 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning5.png", screen_size)
lightning6 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning6.png", screen_size)
creepy_house = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Creepy House.png", screen_size)
basement_bg = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Basement background.png", screen_size)

#Art
def load_art(art):
    try:
        return pygame.image.load(art)
    except Exception as e:
        print(f"Error: Could not load '{art}'. {e}")
        pygame.quit()
        sys.exit()

#Loading art
crate = load_art(ASSETS_DIR / "Art" / "Objects" / "Crate.png")
small_crate = load_art(ASSETS_DIR / "Art" / "Objects" / "Small crate.png")
not_pressed_button_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Button (not pressed).png")
not_pressed_button_art = pygame.transform.rotate(not_pressed_button_art, 90)
pressed_button_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Button (pressed).png")
pressed_button_art = pygame.transform.rotate(pressed_button_art, 90)
passable_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Passable crate.png")
balcony_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Balcony.png")
door_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Door.png")
fireplace_closed_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace closed.png")
fireplace_open_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace open.png")
fireplace_with_coal_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace with coal.png")
fireplace_lit_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace lit.png")
fireplace_chimney_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace chimney.png")
chair_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Chair.png")
other_chair_art = pygame.transform.flip(chair_art, True, False)
floorboard_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Floorboard.png")
dining_table_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Dining table.png")
stove_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Stove.png")
cupboard_closed_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Cupboard closed.png")
cupboard_open_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Cupboard open.png")
elevator_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Elevator.png")
breaker_box_off = load_art(ASSETS_DIR / "Art" / "Objects" / "Breaker box off.png")
breaker_box_on = load_art(ASSETS_DIR / "Art" / "Objects" / "Breaker box on.png")
cobblestone_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Cobblestone.png")
light_bulb_off = load_art(ASSETS_DIR / "Art" / "Objects" / "Light bulb off.png")
light_bulb_on = load_art(ASSETS_DIR / "Art" / "Objects" / "Light bulb on.png")
coal_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Lump of coal.png")
lighter_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Lighter.png")
bed_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Bed.png")
blarghs_bed = load_art(ASSETS_DIR / "Art" / "Objects" / "Blargh bed.png")
blargh_art = load_art(ASSETS_DIR / "Art" / "Objects" / "BLARGH.png")
blargh_art = pygame.transform.flip(blargh_art, True, False)
tome_art = load_art(ASSETS_DIR / "Art" / "Objects" / "The tome.png")
ghost_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Ghost.png")
other_ghost_art = pygame.transform.flip(ghost_art, True, False)
play_button_art = load_art(ASSETS_DIR / "Art" / "Menu stuff" / "Play button.png")
exit_button_art = load_art(ASSETS_DIR / "Art" / "Menu stuff" / "Exit button.png")
settings_button_art = load_art(ASSETS_DIR / "Art" / "Menu stuff" / "Settings button.png")
exit_settings_button_art = load_art(ASSETS_DIR / "Art" / "Menu stuff" / "Exit settings button.png")

#Loading player models
bob_art = load_art(ASSETS_DIR / "Art" / "BOB" / "BOB.png")
crouching_art = load_art(ASSETS_DIR / "Art" / "BOB" / "BOB_crouch.png")

#SFX
jump_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Jump.mp3")
landing_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Landing.mp3")
raining_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Raining.mp3")
raining_channel = pygame.mixer.Channel(2)
click_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Button clicked.mp3")
thunder_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Thunder.mp3")
balcony_creaking_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Balcony creaking.mp3")
creaking_channel = pygame.mixer.Channel(1)
walking_grass_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Walking on grass.mp3")
landing_grass_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Landing on grass.mp3")
walking_wood_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Walking on wood.mp3")
walking_stone_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Walking on stone.mp3")
walking_channel = pygame.mixer.Channel(4)
fire_alarm_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Fire alarm.mp3")
electricity_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Static.mp3")
electricity_channel = pygame.mixer.Channel(3)

def level_one():
    global outside, not_pressed_button_art, breaker_box_off

    #Objects
    darkness = pygame.Surface((800, 600))
    darkness.fill((0, 0, 0))
    darkness.set_alpha(100)


    wall0 = [
        pygame.Rect(2000, 0, 100, 100),
        pygame.Rect(2000, 100, 100, 100),
        pygame.Rect(2000, 200, 100, 100),
        pygame.Rect(2000, 300, 100, 100),
        pygame.Rect(2000, 400, 100, 100)
    ]
    button = pygame.Rect(1300, 413, 40, 74)
    passable_gameplay = [
        pygame.Rect(2200, 400, 100, 20),
        pygame.Rect(2200, 300, 100, 20)
    ]
    gameplay = [
        pygame.Rect(800, 200, 100, 100),
        pygame.Rect(900, 200, 100, 100),
        pygame.Rect(700, 300, 100, 100),
        pygame.Rect(800, 300, 100, 100),
        pygame.Rect(900, 300, 100, 100),
        pygame.Rect(600, 400, 100, 100),
        pygame.Rect(700, 400, 100, 100),
        pygame.Rect(800, 400, 100, 100),
        pygame.Rect(900, 400, 100, 100),

        pygame.Rect(1200, 400, 100, 100),
        pygame.Rect(1200, 300, 100, 100),
        pygame.Rect(1300, 300, 100, 100),
        pygame.Rect(1400, 300, 100, 100),
        pygame.Rect(1500, 300, 100, 100),
        pygame.Rect(1600, 300, 100, 100),
        pygame.Rect(1700, 300, 100, 100), 
        pygame.Rect(1500, 150, 100, 100), 
        pygame.Rect(1600, 150, 100, 100),
        pygame.Rect(1700, 150, 100, 100),
        pygame.Rect(1700, 50, 100, 100),
        pygame.Rect(1700, -50, 100, 100),

        pygame.Rect(2300, 200, 100, 100),
        pygame.Rect(2400, 200, 100, 100),
        pygame.Rect(2500, 200, 100, 100),
        pygame.Rect(2600, 200, 100, 100),
        pygame.Rect(2300, 300, 100, 100),
        pygame.Rect(2400, 300, 100, 100),
        pygame.Rect(2500, 300, 100, 100),
        pygame.Rect(2600, 300, 100, 100),
        pygame.Rect(2300, 400, 100, 100),
        pygame.Rect(2400, 400, 100, 100),
        pygame.Rect(2500, 400, 100, 100),
        pygame.Rect(2600, 400, 100, 100),

    ]
    gameplay.extend(wall0)

    entrance = [
        pygame.Rect(4000, 0, 100, 100),
        pygame.Rect(4000, 100, 100, 100),
        pygame.Rect(4000, 200, 100, 100),
    ]
    door = pygame.Rect(4000, 300, 100, 200)
    balcony = [
        pygame.Rect(3800, 200, 100, 100),
        pygame.Rect(3900, 200, 100, 100)
    ]
    floor = [
        pygame.Rect(0, 500, 100, 100),
        pygame.Rect(100, 500, 100, 100),
        pygame.Rect(200, 500, 100, 100),
        pygame.Rect(300, 500, 100, 100),
        pygame.Rect(400, 500, 100, 100),
        pygame.Rect(500, 500, 100, 100),
        pygame.Rect(600, 500, 100, 100),
        pygame.Rect(700, 500, 100, 100),
        pygame.Rect(800, 500, 100, 100),
        pygame.Rect(900, 500, 100, 100),
        pygame.Rect(1000, 500, 100, 100),
        pygame.Rect(1100, 500, 100, 100),
        pygame.Rect(1200, 500, 100, 100),
        pygame.Rect(1300, 500, 100, 100),
        pygame.Rect(1400, 500, 100, 100),
        pygame.Rect(1500, 500, 100, 100),
        pygame.Rect(1600, 500, 100, 100),
        pygame.Rect(1700, 500, 100, 100),
        pygame.Rect(1800, 500, 100, 100),
        pygame.Rect(1900, 500, 100, 100),
        pygame.Rect(2000, 500, 100, 100),
        pygame.Rect(2100, 500, 100, 100),
        pygame.Rect(2300, 500, 100, 100),
    ]
    ceiling = [
        pygame.Rect(0, 0, 100, 100),
        pygame.Rect(100, 0, 100, 100),
        pygame.Rect(200, 0, 100, 100),
        pygame.Rect(300, 0, 100, 100),
        pygame.Rect(400, 0, 100, 100),
        pygame.Rect(500, 0, 100, 100),
        pygame.Rect(600, 0, 100, 100),
        pygame.Rect(700, 0, 100, 100),
        pygame.Rect(800, 0, 100, 100),
        pygame.Rect(900, 0, 100, 100),
        pygame.Rect(1000, 0, 100, 100),
        pygame.Rect(1100, 0, 100, 100),
        pygame.Rect(1200, 0, 100, 100),
        pygame.Rect(1300, 0, 100, 100),
        pygame.Rect(1400, 0, 100, 100),
        pygame.Rect(1500, 0, 100, 100),
        pygame.Rect(1600, 0, 100, 100),
        pygame.Rect(1700, 0, 100, 100),
        pygame.Rect(1800, 0, 100, 100),
        pygame.Rect(1900, 0, 100, 100),
        pygame.Rect(2000, 0, 100, 100),
        pygame.Rect(2100, 0, 100, 100),
        pygame.Rect(2300, 0, 100, 100),
    ]
    cobblestone_floor = [
        pygame.Rect(100 * k, 500, 100, 100)
        for k in range(24)
    ]
    fireplace = pygame.Rect(3600, 400, 100, 100)
    fireplace_chimney = [
        pygame.Rect(3640, 300, 20, 100),
        pygame.Rect(3640, 200, 20, 100),
        pygame.Rect(3640, 100, 20, 100),
        pygame.Rect(3640, 0, 20, 100)
    ]
    chair = [
        pygame.Rect(3450, 300, 100, 200),
        pygame.Rect(4300, 300, 100, 200)
    ]
    other_chair = [
        pygame.Rect(3750, 300, 100, 200),
        pygame.Rect(4600, 300, 100, 200)
    ]
    tome = pygame.Rect(5700, 400, 100, 100)
    dining_table = pygame.Rect(4375, 400, 150, 100)
    cupboards = [
        pygame.Rect(5100, 300, 100, 200),
        pygame.Rect(5100, 100, 100, 100)
    ]
    ghosts = [
        pygame.Rect(5600, 300, 70, 90),
        pygame.Rect(5700, 300, 70, 90),
        pygame.Rect(900, -200, 70, 90)
    ]
    other_ghosts = [
        pygame.Rect(5800, 300, 70, 90),
        pygame.Rect(5900, 300, 70, 90)
    ]
    light_bulb = pygame.Rect(375, 100, 50, 50)
    stove = pygame.Rect(5000, 400, 100, 100)
    elevator = pygame.Rect(5500, 400, 100, 100)
    elevator_floor = pygame.Rect(5500, 480, 100, 20)
    basement_parkour = [
        pygame.Rect(2000, 1000, 100, 100),
        pygame.Rect(1900, 1000, 100, 100),
        pygame.Rect(1700, 1000, 100, 100),
        pygame.Rect(1700, 900, 100, 100),
        pygame.Rect(1950, 800, 100, 100),
        pygame.Rect(2050, 700, 100, 100),
        pygame.Rect(2000, 550, 100, 100),
        pygame.Rect(1700, 760, 50, 50),
        pygame.Rect(1600, 800, 100, 100),

        pygame.Rect(1500, 800, 100, 100),
        pygame.Rect(1400, 800, 100, 100),
        pygame.Rect(1300, 700, 50, 50),
        pygame.Rect(1350, 700, 50, 50),
        pygame.Rect(1250, 700, 50, 50),
        pygame.Rect(1350, 600, 50, 50),
        pygame.Rect(1200, 800, 50, 50),
        pygame.Rect(1200, 1000, 100, 100),
        pygame.Rect(1250, 950, 50, 50),
        pygame.Rect(1400, 800, 100, 100),
        pygame.Rect(1400, 1000, 100, 100),
        pygame.Rect(1100, 1000, 100, 100),
        pygame.Rect(1000, 900, 100, 100),
        pygame.Rect(900, 800, 100, 100),
        pygame.Rect(800, 700, 100, 100),

        pygame.Rect(700, 700, 100, 100),
        pygame.Rect(650, 800, 50, 50),
        pygame.Rect(600, 900, 100, 100),
        pygame.Rect(600, 1000, 100, 100),
        pygame.Rect(300, 900, 100, 100),
        pygame.Rect(300, 1000, 100, 100),
        pygame.Rect(100, 800, 100, 100),
        pygame.Rect(100, 900, 100, 100),
        pygame.Rect(100, 1000, 100, 100)
    ]
    breaker_box = pygame.Rect(0, 700, 100, 100)
    coal = pygame.Rect(5500, 400, 100, 100)
    lighter = pygame.Rect(5500, 300, 11, 45)
    beds = [
        pygame.Rect(200, -500, 400, 400),
        pygame.Rect(1000, -500, 400, 400),
        pygame.Rect(1800, -500, 400, 400)
    ]
    blargh = pygame.Rect(25, -250, 150, 150)
    house = [fireplace, tome, dining_table, stove, blargh]
    house.extend(fireplace_chimney + chair + other_chair + floor + cupboards + beds + ghosts + other_ghosts)
    basement = [elevator, elevator_floor, breaker_box]
    basement.extend(cobblestone_floor + basement_parkour)

    raining_area = pygame.Rect(3000, 0, 10, 600)
    camera_change = pygame.Rect(3670, 0, 10, 600)
    transition_rect = pygame.Rect(4200, 0, 10, 600)
    house_wall_left = pygame.Rect(4500, -600, 10, 1800)
    house_wall_right = pygame.Rect(5000, -600, 10, 1800)
    move_left_in_house = pygame.Rect(4500, 0, 10, 600)
    move_right_in_house = pygame.Rect(5300, 0, 10, 600)
    basement_switch = pygame.Rect(5200, 600, 100, 10)
    fire_alarm_check = pygame.Rect(5600, 0, 10, 600)

    house.append(house_wall_left)
    house.append(house_wall_right)
    house.append(fire_alarm_check)
    basement.append(basement_switch)

    #BOB
    bob = pygame.Rect(300, 400, 100, 100)
    normal_hitbox_height = 100
    crouch_hitbox_height = 50
    hitbox_width = 75
    bobs_hitbox = pygame.Rect(bob.left, bob.bottom - normal_hitbox_height, hitbox_width, normal_hitbox_height)
    bob_y = float(bobs_hitbox.y)
    isCrouching = False
    on_ground = False
    jump_speed = 900
    gravity = 2880
    velocity_y = 0
    house.append(bob)
    house.append(bobs_hitbox)

    pause_menu = pygame.Surface((750, 550))
    pause_menu.set_alpha(223)
    pause_menu.fill((0, 0, 0))
    pause_menu_outline = pygame.Rect(25, 25, 750, 550)
    play_button = pygame.Rect(350, 250, 100, 100)
    exit_button = pygame.Rect(150, 250, 100, 100)
    settings_button = pygame.Rect(550, 250, 100, 100)
    settings_menu = pygame.Surface((750, 550))
    settings_menu.set_alpha(223)
    settings_menu.fill((0, 0, 0))
    settings_menu_outline = pygame.Rect(25, 25, 750, 550)
    settings_exit_button = pygame.Rect(700, 50, 50, 50)
    settings_checkboxes = [
        pygame.Rect(600, 150, 50, 50)
    ]
    settings_entries = [
        pygame.Rect(550, 210, 100, 50)
    ]
    new_fps = ""

    #Pre-main loop variables
    running = True
    isRaining = False
    rain = []
    for k in range(150):
        x = random.randint(0, screen_size[0])
        y = random.randint(0, 100)
        speed = random.randint(480, 900)
        length = random.randint(8, 18)
        rain.append([x, y, speed, length])
    clicked = False
    remainder_time = pygame.time.get_ticks() + 5000
    lightning_duration = 200
    lightning_active = False
    lightning_end_time = 0
    camera_locked = False
    transitioning = False
    game_paused = False
    settings_open = False
    entry_active = []
    walking_paused = False
    balcony_falling = False
    balcony_fall_distance = 0
    balcony_fell = False
    creaking_played = False
    isStart_of_fadeSet = False
    has_bob_moved_after_transition = False
    inventory = []
    fireplace_state = "Closed"
    current_fireplace_art = fireplace_closed_art
    OUTSIDE = "Outside"
    BASEMENT = "Basement"
    GROUND_FLOOR = "Ground floor"
    FIRST_FLOOR = "First floor"
    current_area = OUTSIDE
    lights_on = False
    elevator_moving = False
    elevator_move_distance = 0
    elevator_speed = 180
    cupboard_open = False
    coal_in_inventory = False
    lighter_in_inventory = False
    fire_alarm_on = False
    tome_opened = False
    dialogue_active = False
    dialogue_stage = 0
    completed = False

    settings = load_settings()

    #Main loop
    while running:
        #Initialisation
        dt_ms = clock.tick(settings["FPS"])
        dt = dt_ms / 1000

        print(
            f"Target: {settings['FPS']} | "
            f"Actual: {1 / dt:.1f} FPS | "
            f"Frame time: {dt_ms} ms | "
            f"Average FPS: {clock.get_fps():.1f}"
        )

        #If game is quit
        for event in pygame.event.get():
            save_settings(settings)
            if event.type == pygame.QUIT:
                running = False


            #Menu buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor_pos = pygame.mouse.get_pos()
                if game_paused == True:
                    if play_button.collidepoint(cursor_pos) == True:
                        game_paused = False
                    elif exit_button.collidepoint(cursor_pos) == True:
                        running = False
                    elif settings_button.collidepoint(cursor_pos) == True:
                        settings_open = True

                if settings_open == True:
                    if settings_exit_button.collidepoint(cursor_pos) == True:
                        settings_open = False
                    for k in range(len(settings_checkboxes)):
                        if settings_checkboxes[k].collidepoint(cursor_pos) == True:
                            if k in settings["Checked tickboxes"]:
                                settings["Checked tickboxes"].remove(k)
                            else:
                                settings["Checked tickboxes"].append(k)
                            if k == 0:
                                settings["Epilepsy safety"] = not settings["Epilepsy safety"]
                            save_settings(settings)
                    for k in range(len(settings_entries)):
                        if settings_entries[k].collidepoint(cursor_pos) == True:
                            if k in entry_active:
                                entry_active.remove(k)
                            else:
                                entry_active.append(k)
            
            #Not WASD key presses
            elif event.type == pygame.KEYDOWN:

                #FPS entry
                if settings_open == True and 0 in entry_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            int(new_fps)
                            if 1 <= int(new_fps) <= 240:
                                settings["FPS"] = int(new_fps)
                            new_fps = ""
                            entry_active.remove(0)
                        except ValueError:
                            new_fps = ""
                    elif event.key == pygame.K_BACKSPACE:
                        new_fps = new_fps[:-1]
                    elif event.unicode.isdigit():
                        if len(new_fps) < 3:
                            new_fps += event.unicode
                    save_settings(settings)

                #Pause the game
                if event.key == pygame.K_ESCAPE:
                    game_paused = True

                #Interactions
                elif event.key == pygame.K_f:

                    #Button interaction
                    if bobs_hitbox.colliderect(button) == True and clicked == False:
                        for rect in wall0:
                            if rect in gameplay:
                                gameplay.remove(rect)
                        wall0.clear()
                        not_pressed_button_art = pressed_button_art
                        click_sfx.play()
                        clicked = True

                    #Fireplace interaction
                    if bobs_hitbox.colliderect(fireplace) == True:
                        if "Lighter" in inventory and fireplace_state == "Contains Coal":
                            current_fireplace_art = fireplace_lit_art
                            fireplace_state = "Lit"
                        elif "Coal" in inventory and fireplace_state == "Open":
                            current_fireplace_art = fireplace_with_coal_art
                            fireplace_state = "Contains Coal"
                        elif fireplace_state != "Closed":
                            current_fireplace_art = fireplace_closed_art
                            fireplace_state = "Closed"
                        elif fireplace_state not in ["Contains Coal", "Lit"]:
                            current_fireplace_art = fireplace_open_art
                            fireplace_state = "Open"

                    #Breaker box interaction
                    if bobs_hitbox.colliderect(breaker_box) == True and lights_on == False:
                        breaker_box_off = breaker_box_on
                        electricity_channel.play(electricity_sfx, -1)
                        lights_on = True

                    #Open cupboard
                    for rect in cupboards:
                        if bobs_hitbox.colliderect(rect) == True:
                            cupboard_open = True
                            for k in range(len(cupboards)):
                                cupboards[k].topleft = (600, 100 + 200*k)
                            coal.topleft = (620, 250)
                            lighter.topleft = (650, 250)

                    #Talk to Blargh
                    if bobs_hitbox.colliderect(blargh):
                        if fire_alarm_on == True:
                            if dialogue_active == False:
                                dialogue_active = True
                                dialogue_stage = 1

                    if bobs_hitbox.colliderect(tome):
                        tome_opened = not tome_opened

                if dialogue_active == True:
                    if dialogue_stage == 1:
                        if event.key == pygame.K_1:
                            dialogue_stage = 2
                            dialogue_active = False
                            completed = True

                        elif event.key == pygame.K_2:
                            dialogue_active = False
                            dialogue_stage = 0

                #Go up in elevator
                elif event.key == pygame.K_UP:
                    if bobs_hitbox.colliderect(elevator):
                        if lights_on == True:
                            if elevator_moving == False:
                                if current_area == BASEMENT:
                                    elevator_move_distance = 0
                                    elevator_speed = 180
                                    elevator_moving = True

                                elif current_area == GROUND_FLOOR:
                                    elevator_move_distance = 0
                                    elevator_speed = 180
                                    elevator_moving = True

                #Go down in elevator
                elif event.key == pygame.K_DOWN:
                    if bobs_hitbox.colliderect(elevator):
                        if lights_on == True:
                            if elevator_moving == False:
                                if current_area == FIRST_FLOOR:
                                    elevator_move_distance = 0
                                    elevator_speed = -180
                                    elevator_moving = True

                                elif current_area == GROUND_FLOOR:
                                    elevator_move_distance = 0
                                    elevator_speed = -180
                                    elevator_moving = True

        def elevator_arrived():
            nonlocal current_area, elevator_moving
            elevator_moving = False
            if elevator_speed > 0:
                if current_area == BASEMENT:
                    current_area = GROUND_FLOOR
                elif current_area == GROUND_FLOOR:
                    current_area = FIRST_FLOOR
            elif elevator_speed < 0:
                if current_area == FIRST_FLOOR:
                    current_area = GROUND_FLOOR
                elif current_area == GROUND_FLOOR:
                    current_area = BASEMENT

        # Moving the elevator
        if elevator_moving:
            move_y = elevator_speed * dt
            if elevator_speed > 0:
                move_y = min(elevator_speed * dt, 600 - elevator_move_distance)
            else:
                move_y = max(elevator_speed * dt, -600 - elevator_move_distance)
            elevator.y -= move_y
            elevator_floor.y -= move_y
            bobs_hitbox.y -= move_y
            bob_y = float(bobs_hitbox.y)
            elevator_move_distance += move_y
            if abs(elevator_move_distance) >= 600:
                elevator_arrived()
                if elevator_speed > 0:
                    for rect in house:
                        rect.move_ip(0, 600)
                        if rect == bob or rect == bobs_hitbox:
                            rect.move_ip(0, -100)
                    elevator.move_ip(0, 600)
                    elevator_floor.move_ip(0, 600)
                    for rect in basement_parkour:
                        rect.move_ip(0, 600)
                    breaker_box.move_ip(0, 600)
                elif elevator_speed < 0:
                    for rect in house:
                        rect.move_ip(0, -600)
                    elevator.move_ip(0, -600)
                    elevator_floor.move_ip(0, -600)
                    for rect in basement_parkour:
                        rect.move_ip(0, -600)
                    breaker_box.move_ip(0, -600)

        #Alpha fade function
        def alpha_fade(surface, current_alpha, target_alpha, fade_speed):
            if current_alpha < target_alpha:
                current_alpha = min(
                    current_alpha + fade_speed * dt,
                    target_alpha
                )
            elif current_alpha > target_alpha:
                current_alpha = max(
                    current_alpha - fade_speed * dt,
                    target_alpha
            )
            surface.set_alpha(int(current_alpha))
            return current_alpha

        #Detects which key was pressed
        key = pygame.key.get_pressed()

        #Draw background(s)
        screen.blit(outside, (0, 0))
        if isRaining == True:
            raining()
        if current_area == GROUND_FLOOR or current_area == FIRST_FLOOR:
            screen.blit(creepy_house, (0,0))
        if current_area == BASEMENT:
            screen.blit(basement_bg, (0,0))

        #Crouch logic
        crouch_request = key[pygame.K_s] and on_ground and velocity_y == 0
        if crouch_request == True:
            isCrouching = True
        else:
            standing_box = bobs_hitbox.copy()
            standing_box.height = normal_hitbox_height
            standing_box.bottom = bobs_hitbox.bottom
            blocked_above = any(
                standing_box.colliderect(rect)
                for rect in gameplay + basement_parkour
            )
            if not blocked_above:
                isCrouching = False
        old_bottom = bobs_hitbox.bottom
        if isCrouching == True:
            bobs_hitbox.height = crouch_hitbox_height
        else:
            bobs_hitbox.height = normal_hitbox_height
        bobs_hitbox.bottom = old_bottom
        bob_y = float(bobs_hitbox.y)

        #Object interactions
        if bobs_hitbox.colliderect(camera_change) == True:
            camera_locked = True
        if bobs_hitbox.colliderect(transition_rect) == True:
            transitioning = True
            walking_channel.stop()
            if creaking_played == False:
                creaking_played = True
                creaking_channel.play(balcony_creaking_sfx)
            if creaking_channel.get_busy() == False:
                balcony_falling = True
            if balcony_fell == True:
                alpha_fade(darkness, darkness.get_alpha(), 255, 240)
                if isStart_of_fadeSet == False:
                    start_of_fade = pygame.time.get_ticks()
                    isStart_of_fadeSet = True
                if pygame.time.get_ticks() - start_of_fade >= 3000:
                    current_area = GROUND_FLOOR
                    fireplace.topleft = (400, 400)
                    tome.topleft = (100, 400)
                    chair[0].topleft = (250, 300)
                    chair[1].topleft = (1050, 300)
                    other_chair[0].topleft = (550, 300)
                    other_chair[1].topleft = (1400, 300)
                    dining_table.topleft = (1175, 400)
                    cupboards[0].topleft = (2300, 300)
                    cupboards[1].topleft = (2300, 100)
                    stove.topleft = (1600, 400)
                    move_left_in_house.topleft = (-100, 0)
                    move_right_in_house.topleft = (890, 0)
                    house_wall_left.topleft = (-10, -600)
                    house_wall_right.topleft = (2410, -600)
                    basement_switch.topleft = (2200, 600)
                    elevator.topleft = (2200, 400)
                    elevator_floor.topleft = (2200, 180)
                    coal.topleft = (2200, 400)
                    lighter.topleft = (2245, 340)
                    fire_alarm_check.topleft = (800, 0)
                    ghosts[0].topleft = (280, 300)
                    ghosts[1].topleft = (1080, 300)
                    other_ghosts[0].topleft = (520, 300)
                    other_ghosts[1].topleft = (1370, 300)
                    for k in range(len(fireplace_chimney)):
                        fireplace_chimney[k].topleft = (440, 312 - 100*k)
                    alpha_fade(darkness, darkness.get_alpha(), 240, 1200)
                    transitioning = False
                    entrance.clear()
                    balcony.clear()
        if bobs_hitbox.colliderect(basement_switch) == True and current_area != BASEMENT:
            for rect in house:
                rect.move_ip(0, -600)
            elevator_floor.move_ip(0, 300)
            for rect in basement_parkour:
                rect.move_ip(0, -600)
            breaker_box.move_ip(0, -600)
            current_area = BASEMENT
        if bobs_hitbox.colliderect(coal) == True and coal_in_inventory == False:
            inventory.append("Coal")
            coal_in_inventory = True
        if bobs_hitbox.colliderect(lighter) == True and lighter_in_inventory == False:
            inventory.append("Lighter")
            lighter_in_inventory = True
        if bobs_hitbox.colliderect(fire_alarm_check) == True and fire_alarm_on == False and fireplace_state == "Lit":
            fire_alarm_sfx.play(-1)
            fire_alarm_on = True

        #Left-Right movement
        scroll_x = 0
        if transitioning == False and game_paused == False:
            if key[pygame.K_a] == True:
                scroll_x = 420 * dt
            elif key[pygame.K_d] == True:
                scroll_x = -420 * dt
            isMoving = (key[pygame.K_a] or key[pygame.K_d]) and not transitioning and not game_paused
            if isMoving == True:
                if current_area == OUTSIDE and bobs_hitbox.bottom >= screen_size[1] - 100:
                    sound_to_play = walking_grass_sfx
                elif current_area == GROUND_FLOOR or bobs_hitbox.bottom < screen_size[1] - 100:
                    sound_to_play = walking_wood_sfx
                else:
                    sound_to_play = walking_stone_sfx
                if walking_channel.get_sound() != sound_to_play:
                    walking_channel.stop()
                    walking_channel.play(sound_to_play, loops=-1)
                    walking_paused = False
                elif walking_paused == True:
                    walking_channel.unpause()
                    walking_paused = False
                elif not walking_channel.get_busy():
                    walking_channel.play(sound_to_play, loops=-1)
            else:
                if walking_paused == False:
                    walking_channel.pause()
                    walking_paused = True
            if scroll_x != 0 or transitioning == True or game_paused == True:
                if camera_locked == True:
                    future_hitbox = bobs_hitbox.move(-scroll_x, 0)
                    if not any(future_hitbox.colliderect(rect) for rect in gameplay + balcony + entrance + floor + basement_parkour + [dining_table] + [house_wall_right] + [house_wall_left] + [elevator_floor]):
                        bobs_hitbox.x -= scroll_x
                        bob_y = float(bobs_hitbox.y)
                    if bobs_hitbox.colliderect(move_left_in_house) == True:
                        for rect in house:
                            rect.move_ip(800, 0)
                        for rect in basement:
                            rect.move_ip(800, 0)
                    elif bobs_hitbox.colliderect(move_right_in_house) == True:
                        for rect in house:
                            rect.move_ip(-800, 0)
                        for rect in basement:
                            rect.move_ip(-800, 0)
                else:
                    can_scroll = True
                    for rect in gameplay:
                        future_rect = rect.move(scroll_x, 0)
                        if bobs_hitbox.colliderect(future_rect) == True:
                            can_scroll = False
                            break
                    if can_scroll == True:

                        for rect in gameplay + [button] + passable_gameplay + entrance + balcony + [raining_area] + [door] + [camera_change] + [transition_rect]:
                            rect.move_ip(scroll_x, 0)
                        instruction_jump_rect.x += scroll_x
                        instruction_move_rect.x += scroll_x
                        instruction_crouch_rect.x += scroll_x
                        instruction_interact_rect.x += scroll_x

        #Jump mechanic
        was_on_ground = on_ground
        if key[pygame.K_w] == True and on_ground == True and isCrouching == False and transitioning == False and game_paused == False:
            velocity_y = -jump_speed
            on_ground = False
            jump_sfx.play()

        #Gravity
        if game_paused == False:
            previous = bobs_hitbox.copy()
            velocity_y += gravity * dt
            bob_y += velocity_y * dt
            bobs_hitbox.y = round(bob_y)
            on_ground = False
            for rect in gameplay + balcony + floor + basement_parkour + [dining_table] + [elevator_floor]:
                if bobs_hitbox.colliderect(rect) == False:
                    continue
                if velocity_y >= 0 and previous.bottom <= rect.top:
                    bobs_hitbox.bottom = rect.top
                    bob_y = float(bobs_hitbox.y)
                    velocity_y = 0
                    on_ground = True
                elif velocity_y < 0 and previous.top >= rect.bottom:
                    bobs_hitbox.top = rect.bottom
                    bob_y = float(bobs_hitbox.y)
                    velocity_y = 0
            for rect in passable_gameplay:
                if (velocity_y >= 0 and previous.bottom <= rect.top and bobs_hitbox.bottom >= rect.top and bobs_hitbox.right > rect.left and bobs_hitbox.left < rect.right):
                    bobs_hitbox.bottom = rect.top
                    bob_y = float(bobs_hitbox.y)
                    velocity_y = 0
                    on_ground = True
            if bobs_hitbox.bottom >= screen_size[1] - 100 and current_area != GROUND_FLOOR:
                bobs_hitbox.bottom = screen_size[1] - 100
                bob_y = float(bobs_hitbox.y)
                velocity_y = 0
                on_ground = True
            if on_ground == True and was_on_ground == False and previous.bottom < bobs_hitbox.bottom:
                landing_sfx.play()
            bob.midbottom = bobs_hitbox.midbottom
            bob_y = float(bobs_hitbox.y)

        #Falling baclony logic
        if balcony_falling == True:
            fall_speed = 180
            move_y = min(fall_speed * dt, 200 - balcony_fall_distance)
            for rect in balcony:
                rect.y += move_y
            balcony_fall_distance += move_y
            if balcony_fall_distance >= 200:
                balcony_falling = False
                balcony_fell = True
                landing_grass_sfx.play()

        #Drawing Outside art on screen
        screen.blit(instruction_jump, instruction_jump_rect)
        screen.blit(instruction_move, instruction_move_rect)
        screen.blit(instruction_crouch, instruction_crouch_rect)
        screen.blit(instruction_interact, instruction_interact_rect)
        screen.blit(not_pressed_button_art, button.topleft)
        for rect in gameplay + entrance:
            screen.blit(crate, rect.topleft)
        for rect in passable_gameplay:
            screen.blit(passable_art, rect.topleft)
        for rect in balcony:
            screen.blit(balcony_art, rect.topleft)
        if current_area == OUTSIDE:
            screen.blit(door_art, door.topleft)

        #Raining function
        def raining():
            global outside
            nonlocal lightning_duration, lightning_active, lightning_end_time, remainder_time
            if transitioning == False and current_area == OUTSIDE:
                darkness.set_alpha(150)
            for drop in rain:
                drop[1] += drop[2] * dt
                drop_rect = pygame.Rect(drop[0] - 3, drop[1], 4, drop[3])
                hit_block = any(
                    drop_rect.colliderect(block)
                    for block in gameplay + passable_gameplay + balcony
                )
                if hit_block or drop[1] > screen_size[1] - 100:
                    drop[0] = random.randint(0, screen_size[0])
                    drop[1] = random.randint(-20, -5)
                pygame.draw.line(
                    screen,
                    (150, 180, 220),
                    (drop[0], drop[1]),
                    (drop[0] - 3, drop[1] + drop[3]),
                    2
                )
            #Lightning logic
            if transitioning == False:
                lightning_timer = pygame.time.get_ticks()
                if lightning_timer - remainder_time >= 10000:
                    lightning_strike = random.randint(0, 5)
                    lightning_backgrounds = [
                        lightning1, lightning2, lightning3,
                        lightning4, lightning5, lightning6
                    ]
                    outside = lightning_backgrounds[lightning_strike]
                    thunder_sfx.play()
                    lightning_active = True
                    if current_area != BASEMENT and settings["Epilepsy safety"] == True:
                        darkness.set_alpha(0)
                    lightning_end_time = lightning_timer + lightning_duration
                    remainder_time = lightning_timer
                if lightning_active and lightning_timer >= lightning_end_time:
                    outside = stormy_outside
                    lightning_active = False
                    if current_area == OUTSIDE:
                        darkness.set_alpha(150)
                    else:
                        darkness.set_alpha(240)

        #Activate raining
        if bob.colliderect(raining_area) == True and isRaining == False:
            raining_channel = raining_sfx.play(-1)
            outside = stormy_outside
            isRaining = True

        #Drawing house art and doing other housey things
        if current_area == GROUND_FLOOR:
            if has_bob_moved_after_transition == False:
                bobs_hitbox.move_ip(-600, 0)
                bob_y = float(bobs_hitbox.y)
                has_bob_moved_after_transition = True
            screen.blit(current_fireplace_art, fireplace.topleft)
            screen.blit(tome_art, tome.topleft)
            screen.blit(dining_table_art, dining_table.topleft)
            screen.blit(stove_art, stove.topleft)
            for rect in chair:
                screen.blit(chair_art, rect.topleft)
            for rect in other_chair:
                screen.blit(other_chair_art, rect.topleft)
            for rect in fireplace_chimney:
                screen.blit(fireplace_chimney_art, rect.topleft)
            for rect in cupboards:
                if cupboard_open == False:
                    screen.blit(cupboard_closed_art, rect.topleft)
                else:
                    screen.blit(cupboard_open_art, rect.topleft)
            if cupboard_open == True:
                if coal_in_inventory == False:
                    screen.blit(coal_art, coal.topleft)
                if lighter_in_inventory == False:
                    screen.blit(lighter_art, lighter.topleft)
            for rect in floor + ceiling:
                screen.blit(floorboard_art, rect.topleft)

        if current_area == FIRST_FLOOR:
            for k in range(len(beds)):
                if k == 0:
                    if fire_alarm_on == False:
                        screen.blit(blarghs_bed, beds[k].topleft)
                    else:
                        screen.blit(bed_art, beds[k].topleft)
                        screen.blit(blargh_art, blargh.topleft)
                else:
                    screen.blit(bed_art, beds[k].topleft)

        #Drawing basement art and doing other basementy things
        if current_area == BASEMENT:
            screen.blit(breaker_box_off, breaker_box.topleft)
            for rect in cobblestone_floor:
                screen.blit(cobblestone_art, rect.topleft)
            for rect in basement_parkour:
                if rect.width == 50:
                    screen.blit(small_crate, rect.topleft)
                else:
                    screen.blit(crate, rect.topleft)

        if current_area != OUTSIDE:
            if current_area == BASEMENT:
                light_bulb.topleft = (375, 0)
            else:
                light_bulb.topleft = (375, 100)
            if lights_on == True:
                screen.blit(light_bulb_on, light_bulb.topleft)
            else:
                screen.blit(light_bulb_off, light_bulb.topleft)

        if ((current_area == GROUND_FLOOR or current_area == FIRST_FLOOR) and lights_on) == True or current_area == BASEMENT:
            screen.blit(elevator_art, elevator.topleft)

        #Dialogue box
        if dialogue_active == True:
            pygame.draw.rect(screen, (20, 20, 20), blargh_dialogue_rect)
            pygame.draw.rect(screen, (255, 255, 255), blargh_dialogue_rect, 3)
            screen.blit(blargh_dialogue, (175, 370))
            screen.blit(yes_dialogue, (200, 430))
            screen.blit(no_dialogue, (450, 430))

        #Drawing BOB
        if isCrouching == True:
            current_art = crouching_art
        else:
            current_art = bob_art
        art_x = bobs_hitbox.centerx - current_art.get_width() // 2
        art_y = bobs_hitbox.bottom - current_art.get_height()
        screen.blit(current_art, (art_x, art_y))

        #Darkness overlay
        if lights_on == False or completed == True:
            screen.blit(darkness, (0,0))

        #Ghosts
        if current_area != BASEMENT:
            if lights_on == False:
                if darkness.get_alpha() != 0:
                    for rect in ghosts:
                        screen.blit(ghost_art, rect.topleft)
                    for rect in other_ghosts:
                        screen.blit(other_ghost_art, rect.topleft)

        #The tome
        if tome_opened == True:
            pygame.draw.rect(screen, (20, 20, 20), tome_content_rect)
            pygame.draw.rect(screen, (255, 255, 255), tome_content_rect, 3)
            for k in range(len(tome_content)):
                screen.blit(tome_content[k], (75, 75 + 50*k))

        if game_paused == True:
            screen.blit(pause_menu, (25, 25))
            pygame.draw.rect(screen, (255, 255, 255), pause_menu_outline, 3)
            screen.blit(pause_menu_title, pause_menu_title_rect)
            screen.blit(play_button_art, play_button.topleft)
            screen.blit(exit_button_art, exit_button.topleft)
            screen.blit(settings_button_art, settings_button.topleft)

        if settings_open == True:
            screen.blit(settings_menu, (25, 25))
            pygame.draw.rect(screen, (255, 255, 255), settings_menu_outline, 3)
            screen.blit(settings_menu_title, settings_menu_title_rect)
            screen.blit(exit_settings_button_art, settings_exit_button)
            for k in range(len(settings_text)):
                screen.blit(settings_text[k], (100, 150 + 60*k))
            for k in range(len(settings_checkboxes)):
                if k in settings["Checked tickboxes"]:
                    pygame.draw.rect(screen, (192, 192, 192), settings_checkboxes[k])
                    pygame.draw.rect(screen, (255, 255, 255), settings_checkboxes[k], 3)
                else:
                    pygame.draw.rect(screen, (64, 64, 64), settings_checkboxes[k])
                    pygame.draw.rect(screen, (255, 255, 255), settings_checkboxes[k], 3)
            for k in range(len(settings_entries)):
                if k in entry_active:
                    pygame.draw.rect(screen, (92, 92, 92), settings_entries[k])
                    pygame.draw.rect(screen, (255, 255, 255), settings_entries[k], 3)
                else:
                    pygame.draw.rect(screen, (64, 64, 64), settings_entries[k])
                    pygame.draw.rect(screen, (255, 255, 255), settings_entries[k], 3)
            new_fps_text = small_menu_font.render(new_fps, False, (255, 255, 255))
            screen.blit(new_fps_text, (settings_entries[0].x + 5, settings_entries[0].y + 5))

        #Escape
        if completed == True:
            alpha_fade(darkness, darkness.get_alpha(), 255, 240)
            screen.blit(level_complete, level_complete_rect)
            pygame.mixer.stop()

        #Refresh rate
        pygame.display.flip()

level_one()

#Once loop is exited
pygame.quit()
sys.exit()