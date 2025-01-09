# Chrome Dinosaur Game using Pygame
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = SCREEN_HEIGHT - 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
FPS = 60
GRAVITY = 0.6
JUMP_STRENGTH = -12

# Load assets
FONT = pygame.font.SysFont('Arial', 30)

# Dinosaur class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.jumping = False

    def update(self):
        self.gravity()
        self.rect.y += self.velocity_y
        if self.rect.y >= GROUND_HEIGHT - self.rect.height:
            self.rect.y = GROUND_HEIGHT - self.rect.height
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True

    def gravity(self):
        self.velocity_y += GRAVITY

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 10
        if self.rect.x < -self.rect.width:
            self.kill()

# Game class
class ChromeDinoGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chrome Dinosaur Game')
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.dino = Dinosaur()
        self.all_sprites.add(self.dino)
        self.spawn_timer = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

    def run(self):
        self.show_start_screen()
        while self.running:
            self.clock.tick(FPS)
            self.events()
            if not self.game_over:
                self.update()
                self.draw()
            else:
                self.show_game_over_screen()

    def update(self):
        self.all_sprites.update()
        self.spawn_obstacles()
        self.check_collisions()
        self.score += 1

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.display_score()
        self.display_lives()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.dino.jump()
                if event.key == pygame.K_RETURN and self.game_over:
                    self.reset_game()

    def spawn_obstacles(self):
        self.spawn_timer += 1
        if self.spawn_timer > 90:
            obstacle = Obstacle()
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)
            self.spawn_timer = 0

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.dino, self.obstacles, False):
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            for obstacle in self.obstacles:
                obstacle.kill()

    def display_score(self):
        score_text = FONT.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def display_lives(self):
        lives_text = FONT.render(f'Lives: {self.lives}', True, BLACK)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        for obstacle in self.obstacles:
            obstacle.kill()

    def show_start_screen(self):
        self.screen.fill(WHITE)
        title_text = FONT.render('Chrome Dinosaur Game', True, BLACK)
        start_text = FONT.render('Press ENTER to Start', True, BLACK)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

    def show_game_over_screen(self):
        self.screen.fill(WHITE)
        game_over_text = FONT.render('Game Over', True, BLACK)
        restart_text = FONT.render('Press ENTER to Restart', True, BLACK)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()

# Main loop
if __name__ == '__main__':
    game = ChromeDinoGame()
    game.run()

pygame.quit()
