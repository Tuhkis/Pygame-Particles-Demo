import pygame, math, random, json
pygame.init()
pygame.font.init()

# Basic setup
pygame.display.set_caption('PARTICLES DEMO')
win = pygame.display.set_mode((1920 // 1.5, 1080 // 1.5))
clock = pygame.time.Clock()

# Camera
cam = [0, 0]

# A text drawing method
def write(text, x, y, size=32):
	font = pygame.font.SysFont('freesanbold.ttf', size)
	text1 = font.render(str(text), True, (255, 255, 255))
	win.blit(text1, (x, y))

class Particles_emitter:
	# "fire" particles are set as default
	def __init__(self, path="data/particles/fire.json"):
		# Emitter position
		self.pos = [0, 0]
		self.particles = []

		# Goes through the particle JSON file and parses it into data
		ijson = open(path)
		data = ijson.read()
		ijson.close()
		data = json.loads(data)

		self.colour = (data['colour'][0], data['colour'][1], data['colour'][2])
		self.initial_velocity = data['initial_velocity']
		self.velocity_randomness = data['velocity_randomness']
		self.radius = data['radius']
		self.gravity = data['gravity']
		self.shrink = data['shrink']
		self.lifetime = data['lifetime']
		self.tone_variance = data['tone_variance']
	def spawn_particle(self):
		# Does magic to spawn a new particle
		# 0 = x, 1 = y, 2 = radius, 3 = acc, 4 = colour, 5 = age
		darkness = max(random.randrange(self.tone_variance, 11), 1) / 10
		vel = self.initial_velocity.copy()
		vel[0] *= random.randrange(self.velocity_randomness[0][0], self.velocity_randomness[0][1])
		vel[1] *= random.randrange(self.velocity_randomness[1][0], self.velocity_randomness[1][1])
		self.particles.append([self.pos[0], self.pos[1], random.randrange(self.radius, int(self.radius * 1.5)), vel, (self.colour[0] * darkness, self.colour[1] * darkness, self.colour[2] * darkness), 0])
	def draw(self):
		# Draws every particle
		for p in self.particles:
			pygame.draw.circle(win, p[4], (p[0] - cam[0], p[1] - cam[1]), p[2])
	def update(self, delta):
		# Goes through the particles and does magic
		for p in self.particles:
			p[0] += p[3][0] * delta
			p[1] += p[3][1] * delta
			p[3][1] += self.gravity[1] * delta
			p[3][0] += self.gravity[0] * delta
			p[2] -= (self.shrink + random.randrange(0, 35) / 10) * delta
			p[5] += 1 * delta

			if p[5] >= self.lifetime + random.randrange(0, 35) / 10:
				self.particles.remove(p)

def start():
	run = True
	wave = 0

	# Create emitters
	emitters = [Particles_emitter()]

	while run:
		# Basic stuff
		delta = clock.tick(60) / 1000
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				run = False

		# Handles input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_d]:
			cam[0] += 300 * delta
		if keys[pygame.K_a]:
			cam[0] -= 300 * delta
		if keys[pygame.K_w]:
			cam[1] -= 300 * delta
		if keys[pygame.K_s]:
			cam[1] += 300 * delta
		if keys[pygame.K_ESCAPE]:
			run = False

		# Moves the emitter
		emitters[0].pos[1] = math.sin(wave * 5) * 256 + win.get_height() / 2
		emitters[0].pos[0] = math.cos(wave * 3) * 256 + win.get_width() / 2
		win.fill((25, 25, 25))

		# Goes through the emitters spawns a particle, draws and updates
		for p in emitters:
			p.spawn_particle()
			
			p.draw()
			p.update(delta)
		# Adds to "wave" variable
		wave += 1 * delta

		write('FPS: ' + str(int(clock.get_fps())), 10, 10)
		write('USE WASD TO MOVE CAMERA', 10, 10 + 32)
		pygame.display.update()

start()
pygame.quit()