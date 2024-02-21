import pygame


pygame.init()
import lessons

# Game window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drag And Drop")

# Define a font
font = pygame.font.Font(None, 36)

active_box = None
dragging = False
boxes = []
initial_positions = []  # Store initial positions of boxes
for i in range(10):
    x = 10 + 60 * i
    y = 20

    box = pygame.Rect(x, y, 50, 50)
    boxes.append(box)
    initial_positions.append((x, y))

# Define the position and size of the green square
green_square_position = (400, 225)
green_square_size = (60, 60)

# Define text to be displayed next to the green button
text = "1 + 2 ="

# Define the position and size of the submit button
submit_button_position = (200, 350)
submit_button_size = (100, 50)

# Define text for the submit button
submit_text = "Submit"
submit_text_surface = font.render(submit_text, True, pygame.Color("black"))


def check_buttons_on_green(numbers_on_green):
    for num, box in enumerate(boxes):
        if box.colliderect(
            pygame.Rect(green_square_position, green_square_size)
        ) and not (num in numbers_on_green):
            numbers_on_green.append(num)

        elif len(numbers_on_green) > 1:
            try:
                numbers_on_green.pop(num)
            except:
                pass
    print("Numbers on green:", [num for num in numbers_on_green])
    return numbers_on_green


def submit_answers(number, answer):
    if number == answer:
        import main_level_copy

        main_level_copy.main(screen, [lessons.ADDITION])


def reset_box_positions(numbers_on_green):
    for i in numbers_on_green[:-1]:
        x, y = initial_positions[i]
        boxes[i].x = x
        boxes[i].y = y


run = True
numbers_on_green = []
while run:

    screen.fill("turquoise1")

    # Draw green square
    pygame.draw.rect(
        screen, pygame.Color("green"), (*green_square_position, *green_square_size)
    )

    # Draw text next to the green square
    text_surface = font.render(text, True, pygame.Color("black"))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (150, green_square_position[1] + green_square_size[0] // 2)
    screen.blit(text_surface, text_rect)  # Update the blit position
    # Draw submit button
    submit_button_rect = pygame.Rect(submit_button_position, submit_button_size)

    pygame.draw.rect(
        screen, pygame.Color("blue"), (*submit_button_position, *submit_button_size)
    )
    submit_text_rect = submit_text_surface.get_rect()
    submit_text_rect.center = submit_button_rect.center

    screen.blit(submit_text_surface, submit_text_rect)

    # Update and draw items
    for num, box in enumerate(boxes):
        pygame.draw.rect(screen, "purple", box)

        # Render the index number on each box
        text_surface = font.render(str(num), True, pygame.Color("white"))
        text_rect = text_surface.get_rect(center=box.center)
        screen.blit(text_surface, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = num
                        dragging = True  # Start dragging when a box is clicked

                if submit_button_rect.collidepoint(event.pos):
                    numbers_on_green = check_buttons_on_green(numbers_on_green)
                    submit_answers(numbers_on_green[0], 3)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_box = None
                dragging = False
            numbers_on_green = check_buttons_on_green(numbers_on_green)
            if len(numbers_on_green) > 1:
                reset_box_positions(numbers_on_green)

        if event.type == pygame.MOUSEMOTION:
            if active_box is not None and dragging:
                boxes[active_box].move_ip(event.rel)
            elif active_box is not None and not dragging:
                # Only update box position when not dragging
                boxes[active_box].move_ip(event.rel)

        if event.type == pygame.QUIT:
            run = False

    # Check collision between purple boxes and green box
    if not dragging:
        for i, box in enumerate(boxes):
            if box.colliderect(pygame.Rect(green_square_position, green_square_size)):
                # Move the purple box to the center of the green box
                box.center = pygame.Rect(
                    green_square_position, green_square_size
                ).center
            elif not dragging:  # Only reset when not dragging
                # Reset the purple box to its initial position
                x, y = initial_positions[i]
                box.x = x
                box.y = y

    pygame.display.flip()

pygame.quit()
