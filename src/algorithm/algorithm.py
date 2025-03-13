from ..util import (
    Song,
    SongType,
    LevelIndex,
    Notes,
    SongDifficulty,
)
from typing import Literal


def str_to_difficulty(difficulty: str) -> LevelIndex:
    """
    将字符串难度转换为 LevelIndex 枚举
    """
    if difficulty == "basic":
        return LevelIndex.BASIC
    elif difficulty == "advanced":
        return LevelIndex.ADVANCED
    elif difficulty == "expert":
        return LevelIndex.EXPERT
    elif difficulty == "master":
        return LevelIndex.MASTER
    elif difficulty == "re_master":
        return LevelIndex.RE_MASTER


def extract_notes(
    song: Song,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    type: SongType | Literal["dx", "standard"] = None,
) -> Notes:
    """
    获取指定曲目的Notes
    暂不支持utage
    """
    if isinstance(difficulty, str):
        difficulty = str_to_difficulty(difficulty)
    difficulties = song.difficulties

    def get_notes(difficulty_list: list[SongDifficulty]) -> Notes:
        for diff in difficulty_list:
            if diff.difficulty == difficulty:
                return diff.notes
        return None

    if not difficulties.standard and not difficulties.utage:
        return get_notes(difficulties.dx)
    if not difficulties.dx and not difficulties.utage:
        return get_notes(difficulties.standard)
    if type is not None:
        type = SongType(type)
        if type == SongType.UTAGE:
            return get_notes(difficulties.utage)
        elif type == SongType.DX:
            return get_notes(difficulties.dx)
        elif type == SongType.STANDARD:
            return get_notes(difficulties.standard)
    return None


def get_equi_taps_from_notes(notes: Notes) -> int:
    """
    从 Notes 中获取总物量
    """
    return notes.tap + notes.hold * 2 + notes.slide * 3 + notes.touch + notes.break_ * 5


def get_achievement_loss_from_notes(
    notes: Notes,
    note_type: Literal["tap", "hold", "slide", "break"],
    accuracy: Literal["critical_perfect", "perfect", "great", "good", "miss"],
) -> tuple[float] | tuple[float, float] | tuple[float, float, float]:
    """
    获取一组Notes中指定Note类型在不同判定的达成率损失
    """
    x = 1 / get_equi_taps_from_notes(notes)
    if note_type == "tap":
        if accuracy == "critical_perfect" or accuracy == "perfect":
            return (0,)
        elif accuracy == "great":
            return (0.2 * x,)
        elif accuracy == "good":
            return (0.5 * x,)
        elif accuracy == "miss":
            return (x,)
    elif note_type == "hold":
        if accuracy == "critical_perfect" or accuracy == "perfect":
            return (0,)
        elif accuracy == "great":
            return (0.4 * x,)
        elif accuracy == "good":
            return (x,)
        elif accuracy == "miss":
            return (2 * x,)
    elif note_type == "slide":
        if accuracy == "critical_perfect" or accuracy == "perfect":
            return (0,)
        elif accuracy == "great":
            return (0.6 * x,)
        elif accuracy == "good":
            return (1.5 * x,)
        elif accuracy == "miss":
            return (3 * x,)
    elif note_type == "break":
        y_scaled = 1 / notes.break_ * 0.01
        if accuracy == "critical_perfect":
            return (0,)
        elif accuracy == "perfect":
            return (0.25 * y_scaled, 0.5 * y_scaled)
        elif accuracy == "great":
            return (
                x + 0.6 * y_scaled,
                2 * x + 0.6 * y_scaled,
                2.5 * x + 0.6 * y_scaled,
            )
        elif accuracy == "good":
            return (3 * x + 0.7 * y_scaled,)
        elif accuracy == "miss":
            return (5 * x + y_scaled,)


def get_achievement_loss_from_song(
    song: Song,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    note_type: Literal["tap", "hold", "slide", "break"],
    accuracy: Literal["critical_perfect", "perfect", "great", "good", "miss"],
    song_type: SongType | Literal["dx", "standard"] = None,
) -> tuple[float] | tuple[float, float] | tuple[float, float, float]:
    """
    获取指定曲目指定Note类型在不同判定的达成率损失
    暂不支持utage
    """
    notes = extract_notes(song, difficulty, song_type)
    return get_achievement_loss_from_notes(notes, note_type, accuracy)


def get_total_achievement_loss_from_notes(
    notes: Notes, loss_dict: dict[str, dict[str, int]]
) -> tuple[float, float]:
    """
    获取一组Notes中在loss_dict情况下的达成率损失

    - loss_dict: 未达到满达成率的物量配置 e.g. {"tap":{"miss":1},"break":{"perfect":1}}
    返回值: (达成率损失下限,达成率损失上限)
    """
    lower = 0
    upper = 0
    for note_type, accuracy_dict in loss_dict.items():
        for accuracy, loss in accuracy_dict.items():
            lower += (
                get_achievement_loss_from_notes(notes, note_type, accuracy)[0] * loss
            )
            upper += (
                get_achievement_loss_from_notes(notes, note_type, accuracy)[-1] * loss
            )
    return (lower, upper)


def get_total_achievement_loss_from_song(
    song: Song,
    difficulty: (
        LevelIndex | Literal["basic", "advanced", "expert", "master", "re_master"]
    ),
    loss_dict: dict[str, dict[str, int]],
    song_type: SongType | Literal["dx", "standard"] = None,
) -> tuple[float, float]:
    """
    获取指定曲目在loss_dict情况下的达成率损失

    - loss_dict: 未达到满达成率的物量配置 e.g. {"tap":{"miss":1},"break":{"perfect":1}}
    返回值: (达成率损失下限,达成率损失上限)

    暂不支持utage
    """
    notes = extract_notes(song, difficulty, song_type)
    return get_total_achievement_loss_from_notes(notes, loss_dict)
