import pygame as pg
from itertools import permutations as perm

from .agent import Agent
from .astar import a_star_search, reconstruct_path


class Node:
    SIZE = 50
    BORDER = 5

    def __init__(self, pos, walkable, visited):
        self.position = pos
        self.size = self.SIZE
        self.walkable = walkable
        self.visited = visited

        self.rect = pg.Rect(pos[0], pos[1], self.size, self.size)

    def set_size(self, val):
        self.size = val
        px, py = self.position
        self.rect = pg.Rect(px, py, self.size, self.size)

    def draw(self, surface):
        col = pg.Color('white')

        if not self.walkable:
            col = pg.Color('black')
        if self.visited:
            col = pg.Color('green')

        pg.draw.rect(surface, col, self.rect.inflate(-self.BORDER, -self.BORDER))

    def get_neighbours(self):
        refx, refy = self.rect.center
        four_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        neighs = []
        for d in four_dirs:
            dx, dy = d
            px, py = refx + (dx * Node.SIZE), refy + (dy * Node.SIZE)
            neighs.append((px, py))
        return neighs


class Graph:
    def __init__(self, size, pos):
        self.size = size
        self.position = pos
        self.nodes = self.make()

        self.agents = []
        self.target = None
        self.closest_node = None

    def make(self):
        cx, cy = [gs // ns for ns, gs in zip((Node.SIZE, Node.SIZE), self.size)]
        offx, offy = self.position

        res = []
        for x in range(cx + 2):
            for y in range(cy - 2):
                pos = offx + (x * Node.SIZE), offy + (y * Node.SIZE)
                n = Node(pos, True, False)
                res.append(n)
        return res

    def draw(self, surface):
        # Draw nodes
        for node in self.nodes:
            for ag in self.agents:
                dx = node.rect.center[0] - ag.true_pos[0]
                dy = node.rect.center[1] - ag.true_pos[1]

                if pg.math.Vector2(dx, dy).length() < 1 and not node.visited:
                    node.visited = True
            node.draw(surface)

        # Draw agents
        if self.agents:
            for ag in self.agents:
                ag.draw(surface)

        # Draw Target
        if self.target:
            pg.draw.circle(surface, pg.Color('black'), self.target, 20)
            pg.draw.circle(surface, pg.Color('blue'), self.target, 15)

    def event(self, ev):
        if ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.add_agent(ev.pos)
            if ev.button == 2:
                self.set_node_walkable(ev.pos)
            if ev.button == 3:
                self.set_agent_target(ev.pos)

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_w or ev.key == pg.K_UP:
                self.move_up()
            if ev.key == pg.K_s or ev.key == pg.K_DOWN:
                self.move_down()
            if ev.key == pg.K_a or ev.key == pg.K_LEFT:
                self.move_left()
            if ev.key == pg.K_d or ev.key == pg.K_RIGHT:
                self.move_right()

    def full_coverage(self):
        not_visited = []
        for node in self.nodes:
            if not node.visited and node.walkable:
                not_visited.append(node)

        closest_node = None
        closest_node_distance = 2000
        for node in not_visited:
            for ag in self.agents:
                dx = node.position[0] + 25 - ag.true_pos[0]
                dy = node.position[1] + 25 - ag.true_pos[1]
                distance = pg.math.Vector2(dx, dy).length()

                if distance < closest_node_distance:
                    closest_node_distance = distance - 5
                    ag.closest_node = node

        #self.closest_node = closest_node
        if len(not_visited) == 0:
            self.navigate()
        else:
            self.navigate_closest_node()

    def move_down(self):
        positions = self.neighbors(self.position)
        for position in positions:
            if position[1] > (self.position[1] + 25):
                self.position = position
                for ag in self.agents:
                    ag.next = position

    def move_up(self):
        positions = self.neighbors(self.position)
        for position in positions:
            if position[1] < (self.position[1] + 25):
                self.position = position
                for ag in self.agents:
                    ag.next = position

    def move_left(self):
        positions = self.neighbors(self.position)
        for position in positions:
            if position[0] < (self.position[0] + 25):
                self.position = position
                for ag in self.agents:
                    ag.next = position

    def move_right(self):
        positions = self.neighbors(self.position)
        for position in positions:
            if position[0] > (self.position[0] + 25):
                self.position = position
                for ag in self.agents:
                    ag.next = position

    def update(self, dt):
        for ag in self.agents:
            ag.update(dt)

    def set_node_walkable(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                node.walkable = not node.walkable
                if node.visited:
                    node.visited = not node.visited
                    node.walkable = not node.walkable

    def set_node_visited(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                node.visited = True

    def set_agent_target(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                if node.walkable:
                    self.target = node.rect.center

    def add_agent(self, pos):
        walkable = [n.position for n in self.nodes if n.walkable]
        try:
            node = [n for n in self.nodes if n.rect.collidepoint(pos)][-1]
        except IndexError:
            return

        if node.position in walkable:
            self.agents.append(Agent(node.rect.center))

    def navigate(self):
        # return if there is no target
        if not self.target:
            return

        # calculate paths for all agents
        for ag in self.agents:
            start = ag.rect.center
            goal = self.target

            cf, cost = a_star_search(self, start, goal)
            try:
                path = reconstruct_path(cf, start, goal)
            except KeyError:
                return

            if len(path) < 5:
                ag.next = path[len(path) - 1]
            else:
                # Remove start position
                ag.set_path(path[2:])

    def navigate_closest_node(self):
        # calculate paths for all agents
        for ag in self.agents:
            if not ag.closest_node:
                return
            start = ag.rect.center
            goal_pos = ag.closest_node.position

            gx = ag.closest_node.position[0]
            gy = ag.closest_node.position[1]
            goal = (gx + 25, gy + 25)

            cf, cost = a_star_search(self, start, goal)

            try:
                path = reconstruct_path(cf, start, goal)
            except KeyError:
                return

            if len(path) < 5:
                ag.next = path[len(path) - 1]
            else:
                # Remove start position
                ag.set_path(path[2:])

    def reset(self):
        self.agents.clear()
        self.target = None

        for n in self.nodes:
            if not n.walkable:
                n.walkable = True
            if n.visited:
                n.visited = False

    # These two last methods must be implemented for a_star to work
    def neighbors(self, pos):
        # determine the node at pos
        node = [n for n in self.nodes if n.rect.collidepoint(pos)][-1]

        # Get neighbouring nodes
        positions = node.get_neighbours()

        # Filter un-walkable positions
        res = []
        for p in positions:
            for n in self.nodes:
                if n.rect.collidepoint(p):
                    if n.walkable:
                        res.append(p)
        return res

    def cost(self, p1, p2):
        return 10