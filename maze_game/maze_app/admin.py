from django.contrib import admin
from .models import GameSession


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "level",
        "game_mode",
        "is_active",
        "current_leader",
        "winner",
        "progress_percent",
        "player_one_score",
        "player_two_score",
        "ai_score",
        "player_one_door_failures",
        "player_two_door_failures",
        "ai_failures",
        "started_at",
        "finished_at",
    )

    list_filter = (
        "is_active",
        "game_mode",
        "winner",
        "level",
        "created_at_date",
    )

    search_fields = (
        "user__username",
        "player_one_name",
        "player_two_name",
    )

    readonly_fields = (
        "started_at",
        "last_update",
        "created_at_date",
    )

    fieldsets = (
        ("Owner & Basic Info", {
            "fields": ("user", "level", "game_mode", "game_mode_detail")
        }),
        ("Players", {
            "fields": ("player_one_name", "player_two_name")
        }),
        ("Status & Timing", {
            "fields": (
                "is_active",
                "started_at",
                "finished_at",
                "last_update",
                "total_time_seconds",
                "progress_percent",
                "current_room",
                "current_door",
                "current_leader",
            )
        }),
        ("Scores & Stats", {
            "fields": (
                "player_one_score",
                "player_two_score",
                "ai_score",
                "player_one_door_failures",
                "player_two_door_failures",
                "ai_failures",
                "correct_answers",
                "incorrect_answers",
                "puzzles_solved",
                "deaths",
                "winner",
            )
        }),
        ("Extra Info", {
            "fields": ("notes", "events_log", "created_at_date")
        }),
    )
