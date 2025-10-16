import pygame
import sys
from world.city import Street, Building

def show_map(city, player_x, player_y, screen):
    """
    Draws a fullscreen map using the existing Pygame window.
    - city: City object
    - player_x, player_y: player coordinates
    - screen: the existing pygame.display surface (from TextGUI)
    """
    clock = pygame.time.Clock()

    # Calculate tile size to fill entire screen
    screen_width, screen_height = screen.get_size()
    tile_width = screen_width // city.width
    tile_height = screen_height // city.height
    tile_size = min(tile_width, tile_height)

    # Font for short labels
    #font_size = max(tile_size // 3, 12)
    font_size = 15
    font = pygame.font.SysFont("monospace", font_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                running = False  # close map on any key

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw the city grid
        for y in range(city.height):
            for x in range(city.width):
                cell = city.get_cell(x, y)
                rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)

                # Color based on content
                if isinstance(cell.content, Street):
                    color = (180, 180, 180)  # grey
                elif isinstance(cell.content, Building):
                    color = (150, 75, 0)     # brown
                else:
                    color = (50, 50, 50)     # dark empty

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # black border

                # Optional short label
                if isinstance(cell.content, Street) or isinstance(cell.content, Building):
                    label = cell.content.name[:11]
                    text_surf = font.render(label, True, (255, 255, 255))
                    screen.blit(text_surf, (rect.x + 2, rect.y + 2))

        # Draw player
        player_rect = pygame.Rect(player_x*tile_size + 5,
                                  player_y*tile_size + 5,
                                  tile_size - 10,
                                  tile_size - 10)
        pygame.draw.rect(screen, (0, 0, 255), player_rect)

        # Update display
        pygame.display.flip()
        clock.tick(30)
