from logger import log_state, log_event
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (drawable, updatable)
    Asteroid.containers = (drawable, updatable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (drawable, updatable, shots)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    asteroidfield = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        for object in drawable:
            object.draw(screen)

        asteroids_collision_check(asteroids, shots, player)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

def asteroids_collision_check(asteroids, shots, player) -> None:
    def player_hit():
        log_event("player_hit")
        print("Game Over!")
        sys.exit()

    def destroy_asteroid_and_shot(asteroid, shot):
        log_event("asteroid_shot")
        asteroid.kill()
        shot.kill()

    for asteroid in asteroids:
        if asteroid.collides_with(player):
            player_hit()
        for shot in shots:
            if asteroid.collides_with(shot):
                destroy_asteroid_and_shot(asteroid, shot)

if __name__ == "__main__":
    main()
