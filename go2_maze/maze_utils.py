"""Random perfect-maze generation, A* planning, and waypoint utilities.

Coordinates:
  maze cells are (row, col), row 0 is the top row.
  world x increases to the right; world y increases upward.
"""
from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
import random
from typing import Dict, Iterable, List, Optional, Set, Tuple

Cell = Tuple[int, int]
DIRECTIONS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


@dataclass
class Maze:
    rows: int
    cols: int
    passages: Dict[Cell, Set[str]]
    start: Cell
    goal: Cell

    def neighbors(self, cell: Cell) -> Iterable[Cell]:
        r, c = cell
        for direction in self.passages[cell]:
            dr, dc = DIRECTIONS[direction]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield (nr, nc)


def generate_maze(rows: int = 7, cols: int = 7, seed: int = 7) -> Maze:
    """Generate a connected 'perfect maze' using randomized depth-first search."""
    if rows < 2 or cols < 2:
        raise ValueError("rows and cols must both be >= 2")
    rng = random.Random(seed)
    passages: Dict[Cell, Set[str]] = {
        (r, c): set() for r in range(rows) for c in range(cols)
    }
    start = (0, 0)
    visited = {start}
    stack = [start]

    while stack:
        r, c = stack[-1]
        choices = []
        for direction, (dr, dc) in DIRECTIONS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                choices.append((direction, (nr, nc)))
        if not choices:
            stack.pop()
            continue
        direction, nxt = rng.choice(choices)
        passages[(r, c)].add(direction)
        passages[nxt].add(OPPOSITE[direction])
        visited.add(nxt)
        stack.append(nxt)

    return Maze(rows, cols, passages, start, (rows - 1, cols - 1))


def astar(maze: Maze, start: Optional[Cell] = None, goal: Optional[Cell] = None) -> List[Cell]:
    """Return a shortest path (including start and goal), or [] if unreachable."""
    start = maze.start if start is None else start
    goal = maze.goal if goal is None else goal

    def h(cell: Cell) -> int:
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    frontier = [(h(start), 0, start)]
    came_from: Dict[Cell, Optional[Cell]] = {start: None}
    g_cost = {start: 0}

    while frontier:
        _, cost, current = heapq.heappop(frontier)
        if current == goal:
            path = []
            node: Optional[Cell] = goal
            while node is not None:
                path.append(node)
                node = came_from[node]
            return list(reversed(path))
        if cost != g_cost[current]:
            continue
        for nxt in maze.neighbors(current):
            new_cost = cost + 1
            if new_cost < g_cost.get(nxt, math.inf):
                g_cost[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(frontier, (new_cost + h(nxt), new_cost, nxt))
    return []


def cell_center(cell: Cell, rows: int, cols: int, cell_size: float) -> Tuple[float, float]:
    """Map (row, col) to world-space cell center (x, y)."""
    r, c = cell
    x = (c - (cols - 1) / 2.0) * cell_size
    y = ((rows - 1) / 2.0 - r) * cell_size
    return x, y


def maze_wall_segments(maze: Maze, cell_size: float = 1.0):
    """Return unique wall segments as ((x1,y1),(x2,y2)); used for XML and plots."""
    rows, cols = maze.rows, maze.cols
    half_w = cols * cell_size / 2.0
    half_h = rows * cell_size / 2.0
    segments = []

    # Outer boundary, split by cell for simple geometry generation.
    for r in range(rows):
        y = half_h - (r + 0.5) * cell_size
        segments.append(((-half_w, y - cell_size/2), (-half_w, y + cell_size/2)))
        segments.append(((half_w, y - cell_size/2), (half_w, y + cell_size/2)))
    for c in range(cols):
        x = -half_w + (c + 0.5) * cell_size
        segments.append(((x - cell_size/2, half_h), (x + cell_size/2, half_h)))
        segments.append(((x - cell_size/2, -half_h), (x + cell_size/2, -half_h)))

    # Internal vertical walls: the right edge of each cell except last column.
    for r in range(rows):
        y = half_h - (r + 0.5) * cell_size
        for c in range(cols - 1):
            if "E" not in maze.passages[(r, c)]:
                x = -half_w + (c + 1) * cell_size
                segments.append(((x, y - cell_size/2), (x, y + cell_size/2)))

    # Internal horizontal walls: the lower edge of each cell except last row.
    for r in range(rows - 1):
        y = half_h - (r + 1) * cell_size
        for c in range(cols):
            if "S" not in maze.passages[(r, c)]:
                x = -half_w + (c + 0.5) * cell_size
                segments.append(((x - cell_size/2, y), (x + cell_size/2, y)))
    return segments


def plot_maze(maze: Maze, path: List[Cell], cell_size: float, output_path: str) -> None:
    """Save a top-down plan image with the A* route overlaid."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    half_w = maze.cols * cell_size / 2
    half_h = maze.rows * cell_size / 2
    ax.add_patch(Rectangle((-half_w, -half_h), 2*half_w, 2*half_h,
                           facecolor="#f8fafc", edgecolor="none"))
    for a, b in maze_wall_segments(maze, cell_size):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#263238", linewidth=3.0,
                solid_capstyle="projecting")
    if path:
        points = [cell_center(cell, maze.rows, maze.cols, cell_size) for cell in path]
        ax.plot([p[0] for p in points], [p[1] for p in points],
                color="#0ea5e9", linewidth=2.5, marker="o", markersize=3)
    sx, sy = cell_center(maze.start, maze.rows, maze.cols, cell_size)
    gx, gy = cell_center(maze.goal, maze.rows, maze.cols, cell_size)
    ax.scatter([sx], [sy], s=100, marker="o", color="#16a34a", label="start", zorder=5)
    ax.scatter([gx], [gy], s=120, marker="*", color="#dc2626", label="goal", zorder=5)
    ax.set_xlim(-half_w - 0.15, half_w + 0.15)
    ax.set_ylim(-half_h - 0.15, half_h + 0.15)
    ax.set_xlabel("world x (m)")
    ax.set_ylabel("world y (m)")
    ax.set_title(f"Random maze + A* route (length={max(0, len(path)-1)} steps)")
    ax.legend(loc="upper right")
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def yaw_from_quat_wxyz(q) -> float:
    w, x, y, z = [float(v) for v in q]
    return math.atan2(2.0 * (w*z + x*y), 1.0 - 2.0 * (y*y + z*z))


def wrap_angle(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def world_velocity_to_body(vx_world: float, vy_world: float, yaw: float):
    """Rotate a planar world-frame velocity into the robot's body frame."""
    c, s = math.cos(yaw), math.sin(yaw)
    return c * vx_world + s * vy_world, -s * vx_world + c * vy_world
