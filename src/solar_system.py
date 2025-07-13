"""Main simulation class for the Solar System."""
from typing import List

import pygame

from src.celestial_body import CelestialBody
from src.constants import CELESTIAL_BODIES, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, TIME_STEP, DISTANCE_SCALE, \
    ORBIT_COLOR


class SolarSystem:
    """Main class for the Solar System simulation.
    
    This class manages the celestial bodies and the simulation loop.
    """
    
    def __init__(self):
        """Initialize the solar system with celestial bodies."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solar System Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.speed_factor = 1.0
        self.font = pygame.font.SysFont('Arial', 16)
        
        # Create celestial bodies
        self.bodies = self._create_celestial_bodies()
    
    def _create_celestial_bodies(self) -> List[CelestialBody]:
        """Create and return a list of celestial bodies.
        
        Returns:
            List[CelestialBody]: List of celestial body objects
        """
        bodies = []
        for name, data in CELESTIAL_BODIES.items():
            body = CelestialBody(
                name=name,
                radius=data['radius'],
                color=data['color'],
                mass=data['mass'],
                semi_major_axis=data.get('semi_major_axis', 0),
                orbital_period=data.get('orbital_period', 0)
            )
            # Position the Sun at the center
            if name == 'Sun':
                body.x = SCREEN_WIDTH // 2
                body.y = SCREEN_HEIGHT // 2
            bodies.append(body)
        return bodies
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.speed_factor *= 2
                elif event.key == pygame.K_DOWN:
                    self.speed_factor = max(0.1, self.speed_factor / 2)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update the simulation state."""
        if not self.paused:
            dt = TIME_STEP * self.speed_factor
            for body in self.bodies:
                if body.name != 'Sun':  # Sun doesn't move in this simulation
                    body.update_position(dt)
    
    def draw(self):
        """Draw the simulation."""
        self.screen.fill(BLACK)
        
        # Draw orbits
        for body in self.bodies[1:]:  # Skip the Sun
            pygame.draw.circle(
                self.screen,
                ORBIT_COLOR,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                int(body.semi_major_axis * DISTANCE_SCALE),
                1  # Line width
            )
        
        # Draw celestial bodies
        for body in self.bodies:
            body.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw the user interface."""
        # Draw help text
        help_text = [
            "SPACE: Pause/Resume",
            "UP/DOWN: Increase/Decrease speed",
            "ESC: Quit"
        ]
        
        for i, text in enumerate(help_text):
            text_surface = self.font.render(text, True, WHITE)
            self.screen.blit(text_surface, (10, 10 + i * 20))
        
        # Draw speed factor
        speed_text = f"Speed: {self.speed_factor:.1f}x"
        speed_surface = self.font.render(speed_text, True, WHITE)
        self.screen.blit(speed_surface, (10, SCREEN_HEIGHT - 30))
    
    def run(self):
        """Run the simulation main loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Cap at 60 FPS
        
        pygame.quit()


def main():
    """Main function to run the simulation."""
    simulation = SolarSystem()
    simulation.run()


if __name__ == "__main__":
    main()
