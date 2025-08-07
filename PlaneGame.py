# :3 a cute Simple Game in less than 500 Lines of Code!
# I am a Newbie
import pygame
import random
import time
def Plane(PosX, PosY, Rad = 10, Col = (200, 200, 230)):
    PlaneCol = Col
    Point1 = (PosX, PosY - Rad)
    Point2 = (PosX, PosY + Rad)
    Point3 = (PosX + Rad + 5, PosY)
    PlanePoint_TriCoordinates = [Point1, Point2, Point3]
    pygame.draw.polygon(screen, PlaneCol, PlanePoint_TriCoordinates)
    return pygame.Rect(PosX - Rad, PosY - Rad, Rad * 2 + 5, Rad * 2) # Return plane's rect for collision

class Clouds:
    def __init__(self, Surface, CloudNo = 5, MinSize = 5, MaxSize = 15, Margin = 10, Speed = 3, Night = False):
        self.CloudCol = (230,230,240) if not Night else (80, 80, 80)
        self.ClNo = CloudNo
        self.Sc = Surface
        self.Swidth = self.Sc.get_width()
        self.Sheight = self.Sc.get_height()
        self.SizeLimit = [MinSize, MaxSize]
        self.Margin = Margin
        self.Speed = Speed
        self.cloud_list = []
        self.initialize_clouds()

    def initialize_clouds(self):
        for _ in range(self.ClNo):
            cloud_size = random.randint(self.SizeLimit[0], self.SizeLimit[1])
            cloud_y = random.randint(self.Margin, self.Sheight - self.Margin)
            cloud_x = self.Swidth + random.randint(self.Margin, self.Swidth // 2)
            self.cloud_list.append({'x': cloud_x, 'y': cloud_y, 'size': cloud_size})

    def Cloud(self, PosX, PosY, Size = 10):
        Col = self.CloudCol
        Sf = self.Sc

        RectWidth = Size * 6
        RectHeight = Size * 2
        RectX = PosX - RectWidth//2
        RectY = PosY - RectHeight
        pygame.draw.rect(Sf, Col, (RectX, RectY, RectWidth, RectHeight))

        Cir1Y = RectY + RectHeight//2
        Cir1X = RectX
        Cir1Rad = RectHeight//2
        Cir1Pos = (Cir1X, Cir1Y)
        pygame.draw.circle(Sf, Col, Cir1Pos, Cir1Rad)

        Cir2X = RectX + RectWidth
        Cir2Y = Cir1Y
        Cir2Rad = Cir1Rad
        Cir2Pos = (Cir2X, Cir2Y)
        pygame.draw.circle(Sf, Col, Cir2Pos, Cir2Rad)

        Cir3X = RectX + RectWidth//7
        Cir3Y = RectY
        Cir3Rad = Size * 2
        Cir3Pos = (Cir3X, Cir3Y)
        pygame.draw.circle(Sf, Col, Cir3Pos, Cir3Rad)

        Cir4X = RectX + RectWidth//2
        Cir4Rad = Size * 2.5
        Cir4Y = RectY - Cir4Rad//1.5
        Cir4Pos = (Cir4X, Cir4Y)
        pygame.draw.circle(Sf, Col, Cir4Pos, Cir4Rad)

        Cir5X = RectX + RectWidth - RectWidth//7
        Cir5Rad = Size * 2
        Cir5Y = RectY
        Cir5Pos = (Cir5X, Cir5Y)
        pygame.draw.circle(Sf, Col, Cir5Pos, Cir5Rad) # Corrected typo

    def CloudAnim(self):
        for cloud in self.cloud_list:
            self.Cloud(cloud['x'], cloud['y'], cloud['size'])
            cloud['x'] -= self.Speed
            if cloud['x'] < -cloud['size'] * 4:
                cloud['size'] = random.randint(self.SizeLimit[0], self.SizeLimit[1])
                cloud['y'] = random.randint(self.Margin, self.Sheight - self.Margin)
                cloud['x'] = self.Swidth + random.randint(self.Margin, self.Swidth // 2)

class Enemy:
    def __init__(self, Surface, Speed = 2):
        self.EnemyCol = (255, 0, 0)
        self.Sc = Surface
        self.Swidth = self.Sc.get_width()
        self.Sheight = self.Sc.get_height()
        self.Rad = 12
        self.PosX = self.Swidth + self.Rad * 2
        self.PosY = random.randint(self.Rad, self.Sheight - self.Rad)
        self.Speed = Speed

    def draw(self):
        Point1 = (self.PosX, self.PosY - self.Rad)
        Point2 = (self.PosX, self.PosY + self.Rad)
        Point3 = (self.PosX - self.Rad - 5, self.PosY)
        EnemyPoint_TriCoordinates = [Point1, Point2, Point3]
        pygame.draw.polygon(self.Sc, self.EnemyCol, EnemyPoint_TriCoordinates)
        return pygame.Rect(self.PosX - self.Rad - 5, self.PosY - self.Rad, self.Rad + 5 + self.Rad, self.Rad * 2)

    def update(self):
        self.PosX -= self.Speed
        if self.PosX < -self.Rad * 2:
            return True # Indicate that the enemy is off-screen
        return False

def draw_sun(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)

def draw_moon(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(surface, NightBG, (center[0] - radius // 3, center[1]), radius)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.color
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            if pygame.mouse.get_pressed()[0] and self.action:
                self.action()
        pygame.draw.rect(surface, current_color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

def interpolate_color(color1, color2, progress):
    r = int(color1[0] + (color2[0] - color1[0]) * progress)
    g = int(color1[1] + (color2[1] - color1[1]) * progress)
    b = int(color1[2] + (color2[2] - color1[2]) * progress)
    return (r, g, b)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    SCwidth = 1200
    SCheight = 800
    screen = pygame.display.set_mode((SCwidth, SCheight))
    pygame.display.set_caption("My Little Plane")
    clock = pygame.time.Clock()
    fps = 60
    BG = (0,0,0)
    NwBG = [150, 200, 255]
    NwBG_tuple = tuple(NwBG)
    NightBG = (30, 30, 80)
    font_small = pygame.font.SysFont("Arial", 20)
    font_large = pygame.font.SysFont("Arial", 48)
    font_game_details = pygame.font.SysFont("Arial", 14)
    font_menu = pygame.font.SysFont("Arial", 36)

    PlaneY = SCheight//2
    PlaneX = SCwidth//7
    PlaneSize = 20
    PlaneCol = (130, 130, 130)
    MoveSpeed = 5
    running = True
    game_state = "START_MENU" # States: START_MENU, PLAYING, GAME_OVER

    cloud_num = random.randint(4, 8)
    cloud_speed = 2
    Cld = Clouds(screen, CloudNo=cloud_num, Speed=cloud_speed)
    Cld_night = Clouds(screen, CloudNo=cloud_num, Speed=cloud_speed, Night=True)

    enemies = []
    enemy_spawn_rate = 120 # Initial spawn rate
    enemy_spawn_counter = 0
    enemy_speed = 2
    enemy_speed_increase_rate = 900 # Increase speed every 15 seconds
    enemy_speed_counter = 0
    last_enemy_spawn_time = time.time() # Track last spawn time

    game_over = False
    score = 0
    start_time = 0
    elapsed_game_time = 0 # Initialize elapsed game time
    transition_duration = 1000
    start_anim_time = pygame.time.get_ticks()
    start_anim = True

    day_night_cycle_time = 30
    day_night_timer = 0
    is_day = True
    last_cycle_change_time = time.time()
    day_night_transition_duration = 2000
    day_night_transition_start_time = 0
    in_day_night_transition = False
    target_bg_color = NwBG_tuple
    current_bg_color = BG

    sun_color = (255, 255, 0)
    sun_radius = 40
    moon_color = (200, 200, 200)
    moon_radius = 30
    cycle_phase = 0

    stars = []
    star_spawned = False

    sun_start_pos = (int(SCwidth * 1.1), int(SCheight * 0.1))
    sun_end_pos = (int(SCwidth * 0.9), int(SCheight * 0.1))
    moon_start_pos = (int(SCwidth * 1.1), int(SCheight * 0.1))
    moon_end_pos = (int(SCwidth * 0.9), int(SCheight * 0.1))
    
    game_name = "My Little Plane"
    game_version = "7.5 Alpha"
    game_author = "Fabian"
    my_instagram = "cyberfab_10"
    cat_face = ":3"
    fabian_relation_status = "Single Forever"
    my_age = 15
    idk_why_i_did_this = True

    # Game Over Buttons
    retry_button = Button("RETRY", SCwidth // 2 - 100, SCheight // 2 + 50, 200, 50, (100, 100, 100), (150, 150, 150))
    main_menu_button = Button("START MENU", SCwidth // 2 - 100, SCheight // 2 + 120, 200, 50, (100, 100, 100), (150, 150, 150))

    # Start Menu Buttons
    start_button = Button("START", SCwidth // 2 - 100, SCheight // 2 + 50, 200, 50, (100, 100, 100), (150, 150, 150))

    def reset_game():
        global game_over, enemies, score, start_time, elapsed_game_time, enemy_spawn_rate, enemy_speed, enemy_speed_counter, is_day, last_cycle_change_time, start_anim, start_anim_time, stars, star_spawned, PlaneY
        game_over = False
        enemies = []
        score = 0
        start_time = time.time()
        elapsed_game_time = 0
        enemy_spawn_rate = 120
        enemy_speed = 2
        enemy_speed_counter = 0
        is_day = True
        last_cycle_change_time = time.time()
        start_anim = True
        start_anim_time = pygame.time.get_ticks()
        stars = []
        star_spawned = False
        PlaneY = SCheight // 2
        global game_state
        game_state = "PLAYING"

    retry_button.action = reset_game
    start_button.action = reset_game
    main_menu_button.action = lambda: setattr(globals()['game_state'], 'value', "START_MENU")

    while running:
        current_frame_time = time.time()

        if game_state == "START_MENU":
            screen.fill(NwBG_tuple if is_day else NightBG)
            if is_day:
                Cld.CloudAnim()
            else:
                if not star_spawned:
                    stars = []
                    for _ in range(200):
                        star_x = random.randint(0, SCwidth)
                        star_y = random.randint(0, SCheight)
                        stars.append((star_x, star_y, random.randint(150, 255), random.randint(150, 255), random.randint(200, 255)))
                    star_spawned = True
                for star in stars:
                    pygame.draw.circle(screen, (star[2], star[3], star[4]), (star[0], star[1]), 2)
                Cld_night.CloudAnim()

            overlay = pygame.Surface((SCwidth, SCheight), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 191))
            screen.blit(overlay, (0, 0))

            title_text = font_menu.render("My Little Plane", True, (255, 255, 255))
            author_text = font_small.render(f"By {game_author}", True, (255, 255, 255))
            detail_text = font_small.render(f"v{game_version}", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(SCwidth // 2, SCheight // 2 - 80))
            detail_rect = detail_text.get_rect(center=(60, SCheight - 30))
            author_rect = author_text.get_rect(center=(SCwidth // 2, SCheight // 2 - 40))
            screen.blit(title_text, title_rect)
            screen.blit(author_text, author_rect)
            screen.blit(detail_text, detail_rect)
            start_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.rect.collidepoint(event.pos):
                        reset_game()

        elif game_state == "PLAYING":
            if not game_over and not start_anim:
                elapsed_game_time = current_frame_time - start_time
                score = int(elapsed_game_time * 10)

            if start_anim:
                elapsed_anim_time = pygame.time.get_ticks() - start_anim_time
                if elapsed_anim_time < transition_duration:
                    progress = elapsed_anim_time / transition_duration
                    current_r = int(BG[0] + (NwBG[0] - BG[0]) * progress)
                    current_g = int(BG[1] + (NwBG[1] - BG[1]) * progress)
                    current_b = int(BG[2] + (NwBG[2] - BG[2]) * progress)
                    current_bg_color = (current_r, current_g, current_b)
                else:
                    current_bg_color = NwBG_tuple
                    BG = current_bg_color
                    start_anim = False
                    start_time = current_frame_time
                screen.fill(current_bg_color)
            elif game_over:
                screen.fill((0, 0, 0))
                game_over_text = font_large.render("Game Over", True, (255, 255, 255))
                score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
                time_survived_text = font_small.render(f"Time Survived: {int(elapsed_game_time)} seconds", True, (255, 255, 255))
                game_over_rect = game_over_text.get_rect(center=(SCwidth // 2, SCheight // 2 - 60))
                score_rect = score_text.get_rect(center=(SCwidth // 2, SCheight // 2))
                time_survived_rect = time_survived_text.get_rect(center=(SCwidth // 2, SCheight // 2 + 30))
                screen.blit(game_over_text, game_over_rect)
                screen.blit(score_text, score_rect)
                screen.blit(time_survived_text, time_survived_rect)
                retry_button.draw(screen)
                main_menu_button.draw(screen)
            else:
                keys = pygame.key.get_pressed()
                screen.fill(NwBG_tuple if is_day else NightBG)

                # Plane Movement
                if keys[pygame.K_w] and keys[pygame.K_s]:
                    PlaneY = PlaneY
                elif keys[pygame.K_w]:
                    PlaneY -= MoveSpeed
                elif keys[pygame.K_s]:
                    PlaneY += MoveSpeed
                if PlaneY > SCheight - PlaneSize:
                    PlaneY = SCheight - PlaneSize
                if PlaneY < PlaneSize:
                    PlaneY = PlaneSize

                if is_day:
                    sun_progress = (pygame.time.get_ticks() - day_night_transition_start_time) / day_night_transition_duration if in_day_night_transition and not is_day else 1.0
                    sun_x = int(sun_start_pos[0] + (sun_end_pos[0] - sun_start_pos[0]) * sun_progress)
                    sun_y = int(sun_start_pos[1] + (sun_end_pos[1] - sun_start_pos[1]) * sun_progress)
                    draw_sun(screen, sun_color, (sun_x, sun_y), sun_radius)
                    Cld.CloudAnim()
                else:
                    for star in stars:
                        pygame.draw.circle(screen, (star[2], star[3], star[4]), (star[0], star[1]), 2)
                    moon_progress = (pygame.time.get_ticks() - day_night_transition_start_time) / day_night_transition_duration if in_day_night_transition and is_day == True else 1.0
                    moon_x = int(moon_start_pos[0] + (moon_end_pos[0] - moon_start_pos[0]) * moon_progress)
                    moon_y = int(moon_start_pos[1] + (moon_end_pos[1] - moon_start_pos[1]) * moon_progress)
                    draw_moon(screen, moon_color, (moon_x, moon_y), moon_radius)
                    Cld_night.CloudAnim()

                plane_rect = Plane(PlaneX, PlaneY, PlaneSize, PlaneCol)

                # Enemy spawning
                current_time = time.time()
                if current_time - last_enemy_spawn_time >= enemy_spawn_rate / fps:
                    enemies.append(Enemy(screen, enemy_speed))
                    last_enemy_spawn_time = current_time
                    if elapsed_game_time > 10 and enemy_spawn_rate > 30:
                        enemy_spawn_rate -= 3
                    elif elapsed_game_time > 30 and enemy_spawn_rate > 15:
                        enemy_spawn_rate -= 2
                    elif elapsed_game_time > 60 and enemy_spawn_rate > 5:
                        enemy_spawn_rate -= 0.5
                for enemy in list(enemies):
                    enemy.draw()
                    if enemy.update():
                        enemies.remove(enemy)
                    elif plane_rect.colliderect(enemy.draw()):
                        game_over = True
                enemy_speed_counter += 1
                if enemy_speed_counter >= enemy_speed_increase_rate:
                    enemy_speed += 0.75
                    enemy_speed_counter = 0
                # Day/Night cycle
                if current_frame_time - last_cycle_change_time >= day_night_cycle_time:
                    is_day = not is_day
                    last_cycle_change_time = current_frame_time
                    day_night_transition_start_time = pygame.time.get_ticks()
                    in_day_night_transition = True
                    target_bg_color = NwBG_tuple if is_day else NightBG
                    BG = current_bg_color
                    if is_day == False:
                        Cld_night = Clouds(screen, CloudNo=cloud_num, Speed=cloud_speed, Night=True)
                    else:
                        Cld = Clouds(screen, CloudNo=cloud_num, Speed=cloud_speed)

                # Display Score
                score_text_surface = font_small.render(f"Score: {score}", True, (0, 0, 0) if is_day else (255, 255, 255))
                screen.blit(score_text_surface, (10, 10))

                # Display Game Details
                fps_text = f"FPS: {int(clock.get_fps())}"
                game_details_text = f"v{game_version} | - {game_author} - | {fps_text}"
                details_surface = font_game_details.render(game_details_text, True, (30, 30, 30) if is_day else (100, 100, 100))
                details_surface.set_alpha(150)
                screen.blit(details_surface, (10, SCheight - 20))

        elif game_state == "GAME_OVER":
            screen.fill((0, 0, 0))
            game_over_text = font_large.render("Game Over", True, (255, 255, 255))
            score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
            time_survived_text = font_small.render(f"Time Survived: {int(elapsed_game_time)} seconds", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(SCwidth // 2, SCheight // 2 - 60))
            score_rect = score_text.get_rect(center=(SCwidth // 2, SCheight // 2))
            time_survived_rect = time_survived_text.get_rect(center=(SCwidth // 2, SCheight // 2 + 30))
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)
            screen.blit(time_survived_text, time_survived_rect)
            retry_button.draw(screen)
            main_menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    reset_game()
                elif game_state == "START_MENU" and event.key == pygame.K_SPACE:
                    reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "GAME_OVER":
                    if retry_button.rect.collidepoint(event.pos):
                        reset_game()
                    if main_menu_button.rect.collidepoint(event.pos):
                        game_state = "START_MENU"
                elif game_state == "PLAYING" and game_over: # Handle clicks on game over buttons
                    if retry_button.rect.collidepoint(event.pos):
                        reset_game()
                    if main_menu_button.rect.collidepoint(event.pos):
                        game_state = "START_MENU"
                elif game_state == "START_MENU":
                    if start_button.rect.collidepoint(event.pos):
                        reset_game()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    pygame.font.quit()
