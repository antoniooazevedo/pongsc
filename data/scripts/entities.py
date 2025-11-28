import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.size = size
        self.type = e_type

        self.pos = pygame.math.Vector2(*pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0.99
        self.restitution = 0.99
        self.hitbox = pygame.FRect(*self.pos, self.size, self.size)

        self.forces = []

    def force(self, vel, angle, persist):
        self.forces.append((pygame.math.Vector2(*vel),
                            angle,
                            persist))
        
    def collision(self, pos, bodies):
        self.hitbox = pygame.FRect(*pos, self.size, self.size)

        rects = [body.hitbox for body in bodies]

        return self.hitbox.collidelist(rects)

    def update(self, bodies):
        # split into x and y components to facilitate collision detection
        remaining_forces = []

        for (vel, angle, persist) in self.forces:
            if persist:
                remaining_forces.append((vel, angle, persist))

            # add change velocity based on forces
            rotated_vel = vel.rotate(angle)
            self.velocity += rotated_vel
            
        self.forces = remaining_forces  

        # apply constant default forces, like friction
        self.velocity *= self.friction      

        # after all forces applied, calculate new position and detect collision for each axis seperately
        #   start with x
        self.pos.x += self.velocity.x

        if (len(bodies) > 0):
            index = self.collision(self.pos, bodies)

            if index != -1:
                body = bodies[index]

                # check which side we collided with using velocity
                if self.velocity.x > 0 : # moving right, collided with left
                    self.hitbox.right = body.hitbox.left
                    self.pos.x = self.hitbox.x
                    self.velocity.x *= -1 * self.restitution * body.restitution # bounce with a little lost velocity
                elif self.velocity.x < 0: # moving left, collided with right
                    self.hitbox.left = body.hitbox.right
                    self.pos.x = self.hitbox.x
                    self.velocity.x *= -1 * self.restitution * body.restitution # bounce with a little lost velocity

        #   then do y
        self.pos.y += self.velocity.y

        if (len(bodies) > 0):
            index = self.collision(self.pos, bodies)

            if index != -1:
                body = bodies[index]

                # check which side we collided with using velocity
                if self.velocity.y > 0 : # moving down, collided with top 
                    self.hitbox.bottom = body.hitbox.top
                    self.pos.y = self.hitbox.y
                    self.velocity.y *= -1 * self.restitution * body.restitution # bounce with a little lost velocity
                elif self.velocity.y < 0: # moving up, collided with bottom 
                    self.hitbox.top = body.hitbox.bottom
                    self.pos.y = self.hitbox.y
                    self.velocity.y *= -1 * self.restitution * body.restitution # bounce with a little lost velocity

class TileEntity(PhysicsEntity):
    def __init__(self, game, pos, size, rect):
        super().__init__(game, 'tile', pos, size)
        self.hitbox = rect

    def update(self):
        self.velocity = pygame.math.Vector2(0,0)
        super().update([])

                
class BallEntity(PhysicsEntity):
    def __init__(self, game, pos, size, img):
        super().__init__(game, 'ball', pos, size)
        self.img = img

    def render(self):
        self.game.display.blit(self.img, self.hitbox)

    def update_and_render(self, bodies):
        self.update(bodies)
        self.render()

class PaddleEntity(PhysicsEntity):
    def __init__(self, game, pos, size, img, player=1):
        super().__init__(game, 'paddle', pos, size)
        self.img = img
        self.player = player
        self.restitution = 1.1
        self.speed = 3
        self.friction = 1

    def render(self):
        self.game.display.blit(self.img, self.render_pos)

    def move(self, movement):
        self.velocity.x = (movement[1] - movement[0]) * self.speed

    def update(self):
        super().update([])
        self.hitbox = pygame.FRect(self.pos.x, self.pos.y + 3, 32 + (16 * self.size) , 10)
        self.render_pos = pygame.FRect(*self.pos, 32 + (16 * self.size), 10) 

    def update_and_render(self):
        self.update()
        self.render()
