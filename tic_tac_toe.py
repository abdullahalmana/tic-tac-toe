import os
import sys
import time
import pygame as pg

# ---------------------------------------------------------
# Helper function: Ensure X and O images exist automatically
# ---------------------------------------------------------
def create_default_images():
    if not os.path.exists("x.png") or not os.path.exists("o.png"):
        try:
            from PIL import Image, ImageDraw
            if not os.path.exists("x.png"):
                img_x = Image.new("RGBA", (100, 100), (255, 255, 255, 0))
                draw_x = ImageDraw.Draw(img_x)
                draw_x.line([(15, 15), (85, 85)], fill=(0, 0, 0, 255), width=8)
                draw_x.line([(85, 15), (15, 85)], fill=(0, 0, 0, 255), width=8)
                img_x.save("x.png")

            if not os.path.exists("o.png"):
                img_o = Image.new("RGBA", (100, 100), (255, 255, 255, 0))
                draw_o = ImageDraw.Draw(img_o)
                draw_o.ellipse([(15, 15), (85, 85)], outline=(0, 0, 0, 255), width=8)
                img_o.save("o.png")
        except Exception as e:
            print(f"Note: Could not auto-generate images with PIL: {e}")

# Ensure image files exist before Pygame attempts to load them
create_default_images()

# ---------------------------------------------------------
# Global Parameters & Setup
# ---------------------------------------------------------
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)
winning_line_color = (250, 0, 0)
board = [[None]*3, [None]*3, [None]*3]

# Initializing Pygame environment
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# Loading image assets
x_img = pg.image.load("x.png")
o_img = pg.image.load("o.png")

# Scaling images to fit grid cells nicely
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))


def game_initiating_window():
    """Initializes the game window, setting up white background and grid lines."""
    screen.fill(white)
    
    # Drawing vertical grid lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    
    # Drawing horizontal grid lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    
    draw_status()


def draw_status():
    """Displays current turn, win, or draw status at the bottom of the window."""
    global draw, winner
    
    if winner:
        message = winner.upper() + " Won!"
    elif draw:
        message = "Game Draw!"
    else:
        message = XO.upper() + "'s Turn"

    font = pg.font.Font(None, 30)
    text = font.render(message, True, (255, 255, 255))
    
    # Fill status bar background at the bottom
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    """Evaluates row-wise, column-wise, and diagonal win/draw conditions."""
    global board, winner, draw
    
    # Checking for winning rows
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, winning_line_color, 
                         (0, (row + 1)*height/3 - height/6), 
                         (width, (row + 1)*height/3 - height/6), 6)
            break

    # Checking for winning columns
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pg.draw.line(screen, winning_line_color, 
                         ((col + 1)*width/3 - width/6, 0), 
                         ((col + 1)*width/3 - width/6, height), 6)
            break

    # Checking for diagonal win (top-left to bottom-right)
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        pg.draw.line(screen, winning_line_color, (50, 50), (350, 350), 6)

    # Checking for diagonal win (top-right to bottom-left)
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        pg.draw.line(screen, winning_line_color, (350, 50), (50, 350), 6)

    # Checking for draw condition
    if all(all(row) for row in board) and winner is None:
        draw = True

    draw_status()


def drawXO(row, col):
    """Draws X or O image at specified board coordinates and toggles turn."""
    global board, XO
    
    # Determine Y position
    if row == 1:
        posy = 30
    elif row == 2:
        posy = height / 3 + 30
    elif row == 3:
        posy = height / 3 * 2 + 30

    # Determine X position
    if col == 1:
        posx = 30
    elif col == 2:
        posx = width / 3 + 30
    elif col == 3:
        posx = width / 3 * 2 + 30

    board[row - 1][col - 1] = XO
    
    if XO == 'x':
        screen.blit(x_img, (posx, posy))
        XO = 'o'
    else:
        screen.blit(o_img, (posx, posy))
        XO = 'x'
        
    pg.display.update()
    check_win()


def user_click():
    """Captures mouse position on click and determines row and column."""
    x, y = pg.mouse.get_pos()

    # Get column from mouse x coordinate
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # Get row from mouse y coordinate
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and board[row - 1][col - 1] is None:
        drawXO(row, col)


def reset_game():
    """Resets global parameters and game board to initial state."""
    global board, winner, XO, draw
    time.sleep(1)
    XO = 'x'
    draw = False
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
    game_initiating_window()


# ---------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------
def main():
    game_initiating_window()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                user_click()
                if winner or draw:
                    reset_game()
                    
        pg.display.update()
        CLOCK.tick(fps)


if __name__ == "__main__":
    main()
