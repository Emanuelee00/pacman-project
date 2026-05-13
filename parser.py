import json
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path


class LevelConfig(BaseModel):
    """Configuration for a single game level."""

    id: int = Field(ge=1)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    pacgum_count: int = Field(ge=0)
    super_pacgum_count: int = Field(ge=0)


class GameConfig(BaseModel):
    """Global game configuration, loaded from config.json."""

    highscore_filename: str
    lives: int = Field(default=3, ge=0)
    points_per_pacgum: int = Field(default=10, gt=0)
    points_per_super_pacgum: int = Field(default=50, gt=0)
    points_per_ghost: int = Field(default=200, gt=0)
    seed: int = 42
    level_max_time: int = Field(default=90, gt=0)
    levels: List[LevelConfig]


class HighscoreEntry(BaseModel):
    """A single entry in the leaderboard: player name and score."""

    name: str = Field(min_length=1, max_length=20)
    score: int = Field(ge=0)


class Highscores(BaseModel):
    """Full leaderboard loaded from highscores.json."""

    scores: List[HighscoreEntry] = []


def load_config(path: str = "config.json") -> GameConfig:
    """Load and validate the game configuration from a JSON file.

    Args:
        path: Path to the JSON config file.

    Returns:
        A validated GameConfig instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValidationError: If the JSON data fails validation.
    """
    if not path.endswith(".json"):
        raise ValueError("File must in json format")
    if Path(path).is_dir():
         raise ValueError("You can't insert a directory")
    with open(path) as f:
        data = json.load(f)
    return GameConfig.model_validate(data)


def load_highscores(path: str = "highscores.json") -> Highscores:
    """Load and validate the leaderboard from a JSON file.

    Args:
        path: Path to the JSON highscores file.

    Returns:
        A validated Highscores instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValidationError: If the JSON data fails validation.
    """
    with open(path) as f:
        data = json.load(f)
    return Highscores.model_validate(data)


def save_highscores(highscores: Highscores, path: str = "highscores.json") -> None:
    """Save the leaderboard to a JSON file.

    Args:
        highscores: The Highscores object to save.
        path: Path to the destination JSON file.
    """
    with open(path, "w") as f:
        json.dump(highscores.model_dump(), f, indent=2)
