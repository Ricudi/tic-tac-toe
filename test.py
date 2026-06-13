import pygame

TRANSPARENT = 0, 0, 0, 0

class ImageHandler:
    def __init__(self, dot_size):
        self.blue_dot = self.create_circle('blue', dot_size)
        self.red_dot = self.create_circle('red', dot_size)

    def create_circle(self, color, size):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill(TRANSPARENT)
        rect = surface.get_rect()
        pygame.draw.circle(surface, color, rect.center, size // 2)
        return surface

def main():
    # Basic Pygame Setup
    pygame.display.set_caption("Example")
    surface = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    rect = surface.get_rect()
    running = True
    delta = 0
    fps = 60

    # Variables
    background = 'grey10'
    dot_size = 10
    image = ImageHandler(dot_size)
    dots = []

    # Main Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(dots) > 0:
                        dots = [event.pos, dots[0]]
                    else:
                        dots = [event.pos]
            elif event.type == pygame.QUIT:
                running = False

        surface.fill(background)
        if len(dots) == 2:
            a, b = dots
            rect = pygame.Rect(min(a[0], b[0]),
                               min(a[1], b[1]),
                               abs(b[0] - a[0]),
                               abs(b[1] - a[1]))

            if a != rect.bottomleft and b != rect.bottomleft:
                right_angle = rect.bottomleft
            else:
                right_angle = rect.topleft

            rect = pygame.Rect(0, 0, dot_size, dot_size)
            rect.center = right_angle
            surface.blit(image.red_dot, rect)
            pygame.draw.line(surface, 'red', a, right_angle)
            pygame.draw.line(surface, 'red', b, right_angle)
            pygame.draw.line(surface, 'blue', a, b)

        for dot in dots:
            rect = pygame.Rect(0, 0, dot_size, dot_size)
            rect.center = dot
            surface.blit(image.blue_dot, rect)


        pygame.display.flip()
        delta = clock.tick(fps) * 0.001

pygame.init()
main()
pygame.quit()