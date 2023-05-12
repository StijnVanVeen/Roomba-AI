import sys
import pygame as pg
from .settings import *
from .ui import *
from .graph import Graph


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode(SIZE, 0, 32)
        self.clock = pg.time.Clock()

        # UI
        self.start_ai_button = Button("Start AI", (100, 30), (10, 10))
        self.start_ai_button.on_click(self.start_ai)
        self.home = Button("Go Home", (100, 30), (10, 50))
        self.home.on_click(self.go_home)
        # self.pause = Button("Pause", (100, 30), (790, 10), bg_color=pg.Color('yellow'), anchor='topright')
        # self.pause.on_click(self.do_pause)

        self.sett, self.inst = False, False
        self.stai = False
        self.paused = False
        self.score = 0.0

        # Navigation Graph
        self.graph = Graph((600, 500), (50, 150))
        self.init()

    def show_instructions(self):
        self.inst = not self.inst

    def go_home(self):
        print('Going home...')

        # Amount of visited nodes
        visited = []
        for node in self.graph.nodes:
            if node.visited:
                visited.append(node)

        # Call navigate() visited[n] times
        for i in range(len(visited)):
            self.graph.navigate()

    def start_ai(self):
        self.stai = True
        print('Starting AI...')

    # def do_pause(self):
    #     self.pause.set_text("Pause" if self.paused else "Resume")
    #     self.paused = not self.paused

    def calculate_score(self):
        visited = []
        total = []
        for node in self.graph.nodes:
            if node.walkable:
                total.append(node)
        for node in self.graph.nodes:
            if node.visited:
                visited.append(node)
        self.score = round((len(visited) / len(total)) * 100, 2)

    def init(self):
        self.graph.add_agent((75, 175))
        self.graph.set_agent_target((75, 175))

    def run(self):

        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.home.event(ev)
                self.start_ai_button.event(ev)
                # self.pause.event(ev)
                self.graph.event(ev, dt)

            # Draw
            self.screen.fill(BACKGROUND)

            draw_header(self.screen, self.score)
            self.graph.draw(self.screen)

            self.start_ai_button.draw(self.screen)
            self.home.draw(self.screen)
            # self.pause.draw(self.screen)
            self.calculate_score()

            if self.sett:
                draw_settings(self.screen)
            if self.stai:
                self.graph.something()

            pg.display.flip()

            # Update

            if not self.paused:
                self.graph.update(dt)