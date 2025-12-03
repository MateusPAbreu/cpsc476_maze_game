from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.utils import timezone

import json
import random
from enum import Enum

import numpy as np
import cv2

from .models import GameSession


def home(request):
    return HttpResponse("Maze!")


def menu(request):
    """
    First screen: login/create user + Start Game button on same page.
    """
    message = None
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            error = "Please enter both a username and a password."
        else:
            existing = User.objects.filter(username=username).first()

            if existing:
                if existing.check_password(password):
                    login(request, existing)
                    message = f"Welcome back, {username}!"
                else:
                    error = "Incorrect password. Please try again."
            else:
                try:
                    user = User.objects.create_user(
                        username=username,
                        password=password
                    )
                    login(request, user)
                    message = f"New user created: {username}"
                except Exception:
                    error = "Could not create account. Try a different username."

    return render(request, "menu.html", {"message": message, "error": error})


def play(request):
    return render(request, "play.html")


def options(request):
    return render(request, "options.html")


def maze(request):
    """
    When the maze page opens, create a GameSession row
    for the current logged-in user.
    """
    try:
        level = int(request.GET.get("level", "1"))
    except ValueError:
        level = 1

    session_obj = None
    if request.user.is_authenticated:
        session_obj = GameSession.objects.create(
            user=request.user,
            level=level,
            # REQUIRED by your model:
            player_one_name=request.user.username,
            # default mode for now; you can change per game mode later
            game_mode=GameSession.GameMode.SINGLE,
        )

    context = {
        "game_session_id": session_obj.id if session_obj else None,
        "level": level,
    }
    return render(request, "maze.html", context)


def ai_view(request):
    return render(request, "ai.html")


def select_level(request):
    return render(request, "select.html")


def tutorial(request):
    return render(request, "tutorial.html")


# =====================  API FOR LIVE GAME LOGGING  ===================== #

@require_POST
def update_game_session(request, session_id):
    """
    JSON API the front-end calls while the game runs.

    It expects JSON with fields like:
      {
        "event": "start" | "door_attempt" | "game_over",
        "player": "player_one" | "player_two" | "ai",
        "correct": true/false,
        "level": 1,
        "game_mode": "single" | "two" | "ai",
        "winner": "player_one" | "player_two" | "ai",
        "progress_percent": 35.0
      }
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "auth required"}, status=403)

    try:
        session = GameSession.objects.get(id=session_id, user=request.user)
    except GameSession.DoesNotExist:
        return JsonResponse({"error": "session not found"}, status=404)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    event = data.get("event")
    changed = False

    # 1) Game start: mark active, set level/mode
    if event == "start":
        level = data.get("level")
        game_mode = data.get("game_mode")  # "single", "two", "ai"

        if level is not None:
            try:
                session.level = int(level)
            except (TypeError, ValueError):
                pass

        # map short codes from JS to model enum values
        if game_mode == "single":
            session.game_mode = GameSession.GameMode.SINGLE
        elif game_mode == "two":
            session.game_mode = GameSession.GameMode.MULTI
        elif game_mode == "ai":
            session.game_mode = GameSession.GameMode.AI_VS_P1

        session.is_active = True
        changed = True

    # 2) Door attempt: update scores/failures, leader, global correct/incorrect
    elif event == "door_attempt":
        player = data.get("player")      # "player_one" | "player_two" | "ai"
        correct = bool(data.get("correct"))

        if player == "player_one":
            if correct:
                session.player_one_score += 1
                session.correct_answers += 1
            else:
                session.player_one_door_failures += 1
                session.incorrect_answers += 1

        elif player == "player_two":
            if correct:
                session.player_two_score += 1
                session.correct_answers += 1
            else:
                session.player_two_door_failures += 1
                session.incorrect_answers += 1

        elif player == "ai":
            if correct:
                session.ai_score += 1
                session.correct_answers += 1
            else:
                session.ai_failures += 1
                session.incorrect_answers += 1

        # you can treat each correct door as a "puzzle solved"
        if correct:
            session.puzzles_solved += 1

        # recompute current leader using enum values
        p1 = session.player_one_score
        p2 = session.player_two_score
        ai_score = session.ai_score

        max_score = max(p1, p2, ai_score)
        leaders = []
        if p1 == max_score and max_score > 0:
            leaders.append("p1")
        if p2 == max_score and max_score > 0:
            leaders.append("p2")
        if ai_score == max_score and max_score > 0:
            leaders.append("ai")

        if len(leaders) == 1:
            if leaders[0] == "p1":
                session.current_leader = GameSession.LeaderChoices.LEADER_P1
            elif leaders[0] == "p2":
                session.current_leader = GameSession.LeaderChoices.LEADER_P2
            else:
                session.current_leader = GameSession.LeaderChoices.LEADER_AI
        elif len(leaders) > 1:
            session.current_leader = GameSession.LeaderChoices.TIE
        else:
            session.current_leader = GameSession.LeaderChoices.UNKNOWN

        changed = True

    # 3) Game over: set winner & mark inactive
    elif event == "game_over":
        winner = data.get("winner")   # "player_one" | "player_two" | "ai"

        if winner == "player_one":
            session.winner = GameSession.WinnerChoices.PLAYER_ONE
        elif winner == "player_two":
            session.winner = GameSession.WinnerChoices.PLAYER_TWO
        elif winner == "ai":
            session.winner = GameSession.WinnerChoices.AI
        else:
            session.winner = GameSession.WinnerChoices.NONE

        session.is_active = False
        session.finished_at = timezone.now()
        changed = True

    # 4) Optional progress update (sent with any event)
    progress = data.get("progress_percent") or data.get("progress")
    if progress is not None:
        try:
            val = float(progress)
            # keep max so progress never goes backwards
            if val > session.progress_percent:
                session.progress_percent = val
                changed = True
        except (TypeError, ValueError):
            pass

    if changed:
        session.save()

    return JsonResponse({"ok": True})


# =====================  OLD BACKTRACKING CODE  ===================== #

class Backtracking:
    def __init__(self, height, width, path, display_maze):

        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.path = path
        self.display_maze = display_maze

    def create_maze(self):
        maze = np.ones((self.height, self.width), dtype=float)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height or j == self.width - 1:
                    maze[i, j] = 0.5

        sx = random.choice(range(2, self.width - 2, 2))
        sy = random.choice(range(2, self.height - 2, 2))
        self.generator(sx, sy, maze)

        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1

        maze[1, 2] = 1
        maze[self.height - 2, self.width - 3] = 1

        if self.display_maze:
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        maze = maze * 255.0
        cv2.imwrite(self.path, maze)

    def generator(self, cx, cy, grid):
        grid[cy, cx] = 0.5

        if (grid[cy - 2, cx] == 0.5 and
            grid[cy + 2, cx] == 0.5 and
            grid[cy, cx - 2] == 0.5 and
            grid[cy, cx + 2] == 0.5):
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

                if grid[ny, nx] != 0.5:
                    grid[my, mx] = 0.5
                    self.generator(nx, ny, grid)


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
