from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox # our classes


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0: return 1
	return sum(lst) / len(lst)

def set_delta(time_0: float, time_1: float, deltas: list[float], target_fps: float, frame: int) -> tuple[float, float, float, int]:
	time_1 = time.perf_counter()
	last_loop_time = time_1 - time_0
	last_fps = 1 / last_loop_time
	last_delta = target_fps / last_fps
	if (frame > 20): deltas.append(last_delta)
	frame += 1
	time_0 = time.perf_counter()
	return calc_average(deltas), time_0, time_1, frame


def createWindow() -> pygame.Surface:
	pygame.init()
	# win = pygame.display.set_mode((600, 600), FULLSCREEN)
	win = pygame.display.set_mode((800, 800))
	x, y = win.get_size()
	size = (x, y * .8) # WHAT DOES THIS DO???
	pygame.display.set_caption("TempName: v-0.01")
	return win


def handle_events() -> None:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

def handle_keys(keys_down: list[bool], hb1: Hitbox) -> None:
	if keys_down[K_w]:
		hb1.get_pt().set_y(hb1.get_pt().get_y() - 4)
	elif keys_down[K_s]:
		hb1.get_pt().set_y(hb1.get_pt().get_y() + 4)
	elif keys_down[K_a]:
		hb1.get_pt().set_x(hb1.get_pt().get_x() - 4)
	elif keys_down[K_d]:
		hb1.get_pt().set_x(hb1.get_pt().get_x() + 4)

def draw_game(win: pygame.Surface, hb1: Hitbox, hb2: Hitbox) -> None:
	win.fill("#000000")

	color = "#0000ff"
	if hb1.checkCollide(hb2):
		color = "#ff0000"

	hb1.draw(win)
	hb2.draw(win, color)

	pygame.display.flip()


def main():

	target_fps = 60
	deltas = []
	delta = 1.0 # relative to target_fps
	frame = 0

	screen = "game"

	clock = pygame.time.Clock()
	time_0 = time.perf_counter()
	time_1 = time.perf_counter()

	game_status = True

	win = createWindow()

	hb1 = Hitbox(Vector(100, 100), 100, 100)
	hb2 = Hitbox(Vector(400, 400), 100, 100)

	while game_status:
		handle_events()
		handle_keys(pygame.key.get_pressed(), delta, hb1)

		if screen == "game": draw_game(win, hb1, hb2)

		clock.tick_busy_loop(target_fps)
		delta, time_0, time_1, frame = set_delta(time_0, time_1, deltas, target_fps, frame)
		print(delta)

		
main()
