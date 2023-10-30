import pygame
import sys
from io import StringIO
import keyword

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FONT_SIZE = 36

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Python Code Editor")

# Font and text variables
font = pygame.font.Font(None, FONT_SIZE)
text = ""
code = {0: text}
cursor_index = 0  # Initial cursor position
cursor_ln = 0

# Saving Variables
ctrl_pressed = False

# Running
running = True

# Code execution variables
output_text = ""  # Store the output of the executed code
is_running_code = False

# Capture standard output and error
output_capture = StringIO()
error_capture = StringIO()
sys.stdout = output_capture
sys.stderr = error_capture

# Define keywords for syntax highlighting
keywords = keyword.kwlist
built_in_functions = ["print", "input", "len", "range", "int", "str", "float", "for", "while", "if", "else"]

# Color definitions
keyword_color = (0, 128, 255)  # Blue
function_color = (255, 69, 0)  # Red-Orange
integer_color = (255, 165, 0) # Orange

while running:
    WIDTH, HEIGHT = pygame.display.get_window_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_index > 0:
                    code[cursor_ln] = code[cursor_ln][:cursor_index - 1] + code[cursor_ln][cursor_index:]
                    cursor_index -= 1
            # Enter Key
            elif event.key == pygame.K_RETURN:
                if cursor_ln + 1 not in code:
                    code[cursor_ln + 1] = ""
                if cursor_index == 0:
                    for i in code:
                        if len(code) - 1 > i >= cursor_ln:
                            if code[i + 1] not in code:
                                code[i + 1] = ""
                            code[i+1] = code[i]
                            code[i] = ""
                cursor_ln += 1
                cursor_index = 0

            # Arrow Keys
            elif event.key == pygame.K_LEFT:
                if cursor_index > 0:
                    cursor_index -= 1
            elif event.key == pygame.K_RIGHT:
                if cursor_index < len(code[cursor_ln]):
                    cursor_index += 1
            elif event.key == pygame.K_UP:
                if cursor_ln != 0:
                    if cursor_ln - 1 not in code:
                        code[cursor_ln - 1] = ""
                    cursor_ln -= 1
                    cursor_index = 0
            elif event.key == pygame.K_DOWN:
                if cursor_ln + 1 not in code:
                    code[cursor_ln + 1] = ""
                cursor_ln += 1
                cursor_index = 0

            elif event.key == pygame.K_LSHIFT:
                pass
            elif event.key == pygame.K_LCTRL:
                ctrl_pressed = True
            else:
                code[cursor_ln] = code[cursor_ln][:cursor_index] + event.unicode + code[cursor_ln][cursor_index:]
                cursor_index += 1
            # Saving the code
            if event.key == pygame.K_s:
                if ctrl_pressed:
                    print("saved 2")
                    with open("saved_code.py", "w") as file:
                        file.write(text)
            # Running the code
            elif event.key == pygame.K_F5:
                # Run the code (F5 key)
                output_capture.truncate(0)
                error_capture.truncate(0)
                output_capture.seek(0)
                error_capture.seek(0)
                output_text = ""
                run_text = "; ".join(value for value in code.values() if value.strip())
                try:
                    exec(run_text)
                    output_text = (output_capture.getvalue())[:-1]
                except Exception as e:
                    output_text = str(e)
                    # Capture mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button (1)
                mouse_x, mouse_y = event.pos
                for i in range(len(code)):
                    line_y = 10 + i * FONT_SIZE
                    if line_y <= mouse_y < line_y + FONT_SIZE:
                        cursor_ln = i
                        cursor_index = 0
                        line_text = code[i]

    # Clear the screen
    screen.fill((30, 30, 30))

    # Render and display the line number
    for i in range(len(code)):
        ln_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(ln_text, (10, i * FONT_SIZE + 10))

    # Render and display the text with syntax highlighting
    for i in code:
        lines = code[i].split('\n')
        y = 10 + i * FONT_SIZE
        for line in lines:
            x = 10
            for word in line.split():
                color = (255, 255, 255)  # Default color
                if word in keywords:
                    color = keyword_color
                elif word in built_in_functions:
                    color = function_color
                elif word.isdigit() or word.isidentifier():
                    color = integer_color
                word_surface = font.render(word, True, color)
                screen.blit(word_surface, (x + FONT_SIZE*4*0.235, y))
                x += word_surface.get_width() + font.size(' ')[0]
            y += FONT_SIZE

    # Calculate cursor position based on text width
    cursor_x = 10 + font.size(code[cursor_ln][:cursor_index])[0]
    cursor_y = 10 + cursor_ln*FONT_SIZE

    # Draw the cursor
    pygame.draw.rect(screen, (255, 255, 255), (cursor_x + FONT_SIZE*4*0.235, cursor_y, 2, FONT_SIZE - 10))

    # Render and display the output of the executed code
    output_surface = font.render(output_text, True, (255, 0, 0))
    screen.blit(output_surface, (10, HEIGHT - FONT_SIZE - 10))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
