import json
import os

LEADERBOARD_FILE = "leaderboard.json"
MAX_ENTRIES = 10


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
    return []


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)


def update_leaderboard(player_name, highscore):
    leaderboard = load_leaderboard()
    highscore = round(highscore)

    leaderboard = [
        entry for entry in leaderboard if entry["name"] != player_name
    ]

    leaderboard.append({"name": player_name, "score": highscore})

    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[
        :MAX_ENTRIES
    ]

    save_leaderboard(leaderboard)


def display_leaderboard(screen, font):
    leaderboard = load_leaderboard()
    y = 50
    screen.fill((0, 0, 0))

    for entry in leaderboard:
        text = f"{entry['name']}: {entry['score']}"
        rendered_text = font.render(text, True, (255, 255, 255))
        screen.blit(rendered_text, (50, y))
        y += 30
