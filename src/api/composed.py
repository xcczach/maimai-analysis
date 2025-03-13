from .raw import get_song
from ..algorithm import (
    get_achievement_loss_from_song,
    extract_notes,
    get_total_achievement_loss_from_song,
)
from ..util import LevelIndex
from typing import Literal


def get_song_notes(
    song_id: int,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    song_type: Literal["standard", "dx"] = None,
    version: int = 24000,
) -> int:
    """
    获取曲目指定难度的总物量

    暂不支持utage
    """
    song = get_song(song_id, version)
    return extract_notes(song, difficulty, song_type)


def get_song_achievement_loss(
    song_id: int,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    note_type: Literal["tap", "hold", "slide", "break"],
    accuracy: Literal["critical_perfect", "perfect", "great", "good", "miss"],
    song_type: Literal["standard", "dx"] = None,
    version: int = 24000,
) -> tuple[int] | tuple[int, int] | tuple[int, int, int]:
    """
    获取曲目指定难度指定Note指定准度达成率损失

    暂不支持utage
    """
    song = get_song(song_id, version)
    return get_achievement_loss_from_song(
        song, difficulty, note_type, accuracy, song_type
    )


def get_song_total_achievement_loss(
    song_id: int,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    loss_dict: dict[str, dict[str, int]],
    song_type: Literal["standard", "dx"] = None,
    version: int = 24000,
) -> tuple[int] | tuple[int, int] | tuple[int, int, int]:
    """
    获取曲目指定难度指定Note指定准度总达成率损失

    暂不支持utage
    """
    song = get_song(song_id, version)
    return get_total_achievement_loss_from_song(song, difficulty, loss_dict, song_type)
