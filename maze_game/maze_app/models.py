from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import numpy as np
import cv2
import sys
import random


# 🔹 Full game session log for each playthrough
class GameSession(models.Model):
    class GameMode(models.TextChoices):
        SINGLE = "single", "Single Player"
        MULTI = "multi", "Two Players"
        AI_VS_P1 = "ai_vs_p1", "Player vs AI"

    class WinnerChoices(models.TextChoices):
        PLAYER_ONE = "player_one", "Player One"
        PLAYER_TWO = "player_two", "Player Two"
        AI = "ai", "AI"
        NONE = "none", "No Winner / Incomplete"

    class LeaderChoices(models.TextChoices):
        LEADER_P1 = "player_one", "Player One"
        LEADER_P2 = "player_two", "Player Two"
        LEADER_AI = "ai", "AI"
        TIE = "tie", "Tie / Equal"
        UNKNOWN = "unknown", "Unknown"

    # Which logged-in user this session belongs to
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="game_sessions"
    )

    # Basic session info
    level = models.PositiveIntegerField()
    game_mode = models.CharField(
        max_length=20,
        choices=GameMode.choices,
        default=GameMode.SINGLE
    )

    # Player names as shown in the game (can be same as username, or custom)
    player_one_name = models.CharField(max_length=150)
    player_two_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Leave empty if there is no Player 2"
    )

    # Timing + status
    is_active = models.BooleanField(
        default=True,
        help_text="True if game is still in progress"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    # Optional total duration (you can fill this when you finish the game)
    total_time_seconds = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total time from start to finish, in seconds"
    )

    # Progress info (for unfinished games)
    progress_percent = models.FloatField(
        default=0,
        help_text="Rough percent of maze completed (0–100)."
    )
    current_room = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g., 'Room 3' or coordinates"
    )
    current_door = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Door index the player is currently near"
    )

    # Who is currently winning (for in-progress games)
    current_leader = models.CharField(
        max_length=20,
        choices=LeaderChoices.choices,
        default=LeaderChoices.UNKNOWN
    )

    # Scores & per-player stats
    player_one_score = models.IntegerField(default=0)
    player_two_score = models.IntegerField(default=0)
    ai_score = models.IntegerField(default=0)

    player_one_door_failures = models.PositiveIntegerField(default=0)
    player_two_door_failures = models.PositiveIntegerField(default=0)
    ai_failures = models.PositiveIntegerField(default=0)

    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    puzzles_solved = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(
        default=0,
        help_text="Number of times a player 'died'/failed hard."
    )

    # Final result
    winner = models.CharField(
        max_length=20,
        choices=WinnerChoices.choices,
        default=WinnerChoices.NONE
    )

    # Extra info / debugging / notes
    game_mode_detail = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional: e.g. 'Player1 vs AI (hard)'"
    )
    notes = models.TextField(blank=True, null=True)

    # Full replay / event log (you can store JSON of moves here)
    events_log = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional JSON of moves, doors, etc."
    )

    created_at_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Session #{self.id} - {self.user.username} - Level {self.level}"

    class Meta:
        ordering = ["-started_at"]  # newest first in admin


# 🔹 Your existing maze generation code (unchanged)
class Backtracking:
    def __init__(self, height, width, path, display_maze):
        # makes sure the maze is always odd numbered
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.path = path
        self.display_maze = display_maze

    def create_maze(self):
        maze = np.ones((self.height, self.width), dtype=float)  # Creates a 2D array

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height or j == self.width - 1:
                    maze[i, j] = 0.5  # this determines the visited cells

        sx = random.choice(range(2, self.width - 2, 2))
        sy = random.choice(range(2, self.height - 2, 2))
        self.generator(sx, sy, maze)

        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1

        maze[1, 2] = 1  # top left
        maze[self.height - 2, self.width - 3] = 1  # bottom right

        if self.display_maze:
            # cv2.namedWindow('Math Maze', cv2.WINDOW_NORMAL)
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        maze = maze * 255.0
        cv2.imwrite(self.path, maze)

    def generator(self, cx, cy, grid):
        grid[cy, cx] = 0.5

        if (
            grid[cy - 2, cx] == 0.5
            and grid[cy + 2, cx] == 0.5
            and grid[cy, cx - 2] == 0.5
            and grid[cy, cx + 2] == 0.5
        ):
            pass
        else:
            li = [1, 2, 3, 4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir == Directions.UP.value:
                    nx = cx
                    mx = cx
                    ny = cy - 2
                    my = cy - 1
                elif dir == Directions.DOWN.value:
                    nx = cx
                    mx = cx
                    ny = cy + 2
                    my = cy + 1
                elif dir == Directions.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                    ny = cy
                    my = cy
                elif dir == Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                    ny = cy
                    my = cy
                else:
                    nx = cx
                    mx = cx
                    ny = cy
                    my = cy

                if grid[ny, nx] != 0.5:  # randomly chooses an element and gets directions
                    grid[my, mx] = 0.5
                    self.generator(nx, ny, grid)


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
