import sys
import pygame as pg
from .settings import *
from .ui import *
from .graph import Graph
from .timer import Timer


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
        self.pause = Button("Pause", (100, 30), (790, 10), bg_color=pg.Color('red'), anchor='topright')
        self.pause.on_click(self.do_pause)
        self.reset = Button("Reset", (100, 30), (790, 50), bg_color=pg.Color('red'), anchor='topright')
        self.reset.on_click(self.do_reset)

        self.sett, self.inst = False, False
        self.stai = False
        self.going_home = False
        self.stopped = False
        self.paused = False
        self.score = 0.0
        self.timer_on = False
        self.timer = Timer()
        self.time_elapsed = 0.0

        # Navigation Graph
        self.graph = Graph((600, 500), (50, 150))
        self.init()

    def show_instructions(self):
        self.inst = not self.inst

    def go_home(self):
        print('Going home...')
        self.stopped = False
        self.stai = False
        self.going_home = True

    def start_ai(self):
        self.stopped = False
        self.stai = True
        self.going_home = False
        print('Starting AI...')

    def do_pause(self):
        if not self.paused:
            print('pausing...')
            self.pause.set_text("Resume")
            self.timer.pause()
        else:
            print('resuming...')
            self.pause.set_text("Pause")
            self.timer.unpause()
        self.paused = not self.paused

    def do_reset(self):
        print('resetting...')
        self.graph.reset()
        self.stai = False
        self.going_home = False
        self.stopped = False
        self.time_elapsed = 0.0
        self.timer_on = False
        self.init()

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
        if self.score == 100.0:
            self.going_home = True

    def check_if_home(self):
        for ag in self.graph.agents:

            dx = self.graph.target[0] - ag.true_pos[0]
            dy = self.graph.target[1] - ag.true_pos[1]
            distance = pg.math.Vector2(dx, dy).length()

            if distance < 5:
                print('stopping...')
                self.stopped = True
                self.timer_on = False
                self.time_elapsed = round(self.timer.stop(), 2)

    def init(self):
        self.graph.add_agent((75, 175))
        self.graph.set_agent_target((75, 175))

    def event(self, ev):
        if ev.type == pg.KEYDOWN:
            if not self.timer_on:
                self.timer_on = True
                self.timer.start()
        if self.stai:
            if not self.timer_on:
                self.timer_on = True
                self.timer.start()

    def run(self):

        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.home.event(ev)
                self.start_ai_button.event(ev)
                self.pause.event(ev)
                self.graph.event(ev)
                self.reset.event(ev)
                self.event(ev)

            # Draw
            self.screen.fill(BACKGROUND)

            draw_header(self.screen, self.score, self.time_elapsed)
            self.graph.draw(self.screen)

            self.start_ai_button.draw(self.screen)
            self.home.draw(self.screen)
            self.pause.draw(self.screen)
            self.reset.draw(self.screen)
            self.calculate_score()

            if self.sett:
                draw_settings(self.screen)
            if self.stai and not self.stopped:
                self.graph.something()

            if self.going_home and not self.stopped:
                self.graph.navigate()
                self.check_if_home()

            pg.display.flip()

            # Update
            if not self.paused:
                self.graph.update(dt)