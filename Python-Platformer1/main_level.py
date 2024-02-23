import pygame
from os.path import isfile, join
from os import listdir


pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)

    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


class Book(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, lessons):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))  # Placeholder image

        self.image_zoomed_out = pygame.image.load(join("assets", "Book", "book.png"))
        self.image_zoomed_out = pygame.transform.scale(
            self.image_zoomed_out, (width, height)
        )
        self.image_zoomed_in = pygame.image.load(
            join("assets", "Book", "book_open.png")
        )
        self.image_zoomed_in = pygame.transform.scale(
            self.image_zoomed_in, (width * 20, height * 20)
        )
        self.rect = self.image_zoomed_out.get_rect(topleft=(x, y))
        self.progress = 0  # Progress of the book
        self.is_zoomed = False  # Flag to indicate whether the book is zoomed in
        self.lessons = lessons
        self.selected_lesson = 1  # Current selected lesson
        self.rendered_text = None  # Rendered text of the current lesson

    def render_text(self):
        lesson_index = self.selected_lesson - 1  # Lesson numbering starts from 1
        if 0 <= lesson_index < len(self.lessons):
            lesson_text = self.lessons[lesson_index]
            font = pygame.font.Font(
                None, 24
            )  # You can adjust the font and size as needed
            lines = lesson_text.split("\n")
            rendered_lines = []
            for line in lines:
                rendered_lines.append(
                    font.render(line, True, (0, 0, 0))
                )  # Rendering the text with black color
            self.rendered_text = rendered_lines

    def draw(self, window, player):
        font = pygame.font.Font(None, 24)
        if self.is_zoomed:
            window.blit(
                self.image_zoomed_in,
                (10, 10),
            )
            # Draw zoom out button
            zoom_out_button = pygame.Rect(450, 650, 100, 50)
            pygame.draw.rect(
                window, (255, 0, 0), zoom_out_button
            )  # Red color for zoom out button
            zoom_out_text = font.render("Zoom Out", True, (0, 0, 0))
            window.blit(zoom_out_text, (zoom_out_button.x + 10, zoom_out_button.y + 15))
            try:
                # Draw the text on the book when zoomed in
                text_x = 50  # Fixed X-coordinate for the text
                text_y = 100  # Fixed Y-coordinate for the text

                for i, line in enumerate(self.rendered_text):
                    window.blit(line, (text_x, text_y + i * 25))

                # Draw navigation buttons
                prev_button = pygame.Rect(
                    50, HEIGHT - 100, 100, 50
                )  # Fixed position for the previous button
                next_button = pygame.Rect(
                    WIDTH - 150, HEIGHT - 100, 100, 50
                )  # Fixed position for the next button
                pygame.draw.rect(
                    window, (0, 255, 0), prev_button
                )  # Green color for previous button
                pygame.draw.rect(
                    window, (0, 0, 255), next_button
                )  # Blue color for next button

                prev_text = font.render("Prev", True, (0, 0, 0))
                next_text = font.render("Next", True, (0, 0, 0))
                window.blit(prev_text, (prev_button.x + 20, prev_button.y + 15))
                window.blit(next_text, (next_button.x + 20, next_button.y + 15))

            except Exception as e:
                print(f"Error: {e}")

        else:
            window.blit(self.image_zoomed_out, (self.x, self.y))

    def zoom_in(self):
        self.is_zoomed = True
        self.render_text()  # Render text when zoomed in

    def zoom_out(self):
        self.is_zoomed = False

    def handle_click(self, pos):
        if self.is_zoomed:
            # Define button positions relative to the book when zoomed in
            book_x, book_y = 10, 10
            prev_button = pygame.Rect(50, HEIGHT - 100, 100, 50)
            next_button = pygame.Rect(WIDTH - 150, HEIGHT - 100, 100, 50)
            zoom_out_button = pygame.Rect(450, 650, 100, 50)

            # Check if the click is inside any of the buttons
            if prev_button.collidepoint(pos):
                self.prev_lesson()
            elif next_button.collidepoint(pos):
                self.next_lesson()
            elif zoom_out_button.collidepoint(pos):
                self.zoom_out()

    def prev_lesson(self):
        self.selected_lesson -= 1
        if self.selected_lesson < 1:
            self.selected_lesson = len(self.lessons)
        self.render_text()  # Render text of the new lesson

    def next_lesson(self):
        self.selected_lesson += 1
        if self.selected_lesson > len(self.lessons):
            self.selected_lesson = 1
        self.render_text()  # Render text of the new lesson


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class SpikeHead(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike_head")
        self.spike_head = load_sprite_sheets("Traps", "Spike Head", width, height)
        self.image = self.spike_head["Idle"][
            0
        ]  # Adjust the sprite sheet name and default animation
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "idle"  # Adjust the default animation name

    def loop(self):
        sprites = self.spike_head[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        if obj and obj.name == "spike_head":
            objects.remove(obj)  # Remove spike head object

            level_transition()


def create_platform(start_x, height, block_width, num_blocks):
    platform = [
        Block(start_x + i * block_width, height, block_width) for i in range(num_blocks)
    ]
    return platform


def level_transition():
    import addition

    addition.main()


def main(window, lessons):
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96
    platform1 = create_platform(200, HEIGHT - block_size - 200, block_size, 5)
    platform2 = create_platform(800, HEIGHT - block_size - 350, block_size, 5)
    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    spike_head = SpikeHead(600, HEIGHT - block_size - 90, 50, 50)
    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size)
        for i in range(-WIDTH // block_size, (WIDTH * 3) // block_size)
    ]
    book = Book(WIDTH - 32, block_size, 32, 32, lessons)  # Create a book object

    objects = [
        *floor,
        Block(0, HEIGHT - block_size * 2, block_size),
        Block(block_size * 3, HEIGHT - block_size * 4, block_size),
        fire,
        *platform1,
        *platform2,
        spike_head,
        book,
    ]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    book.handle_click(
                        mouse_pos
                    )  # Handle mouse click for the book object

                    # Check if the mouse click is on the book object
                    if (
                        968 <= mouse_pos[0] <= 968 + book.width
                        and 96 <= mouse_pos[1] <= 96 + book.height
                    ):
                        if book.is_zoomed:
                            book.zoom_out()
                        else:
                            book.zoom_in()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)

        draw(window, background, bg_image, player, objects, offset_x)

        if (
            (player.rect.right - offset_x >= WIDTH - scroll_area_width)
            and player.x_vel > 0
        ) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window, [])
