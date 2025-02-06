from urllib.parse import urljoin
import requests
from enum import Enum
from typing import TypeVar, Type, List, Union
from dataclasses import dataclass, field, fields

ROOT_URL = "https://maimai.lxns.net/api/v0/"

def get_player_info(token: str, info_type_url: str) -> dict | List[dict]:
    target_url = urljoin(urljoin(ROOT_URL, "user/maimai/"), info_type_url)
    header = {"X-User-Token": token}
    response = requests.get(target_url, headers=header)
    return response.json()["data"]

def get_public_info(info_type_url: str) -> dict:
    target_url = urljoin(urljoin(ROOT_URL, "maimai/"), info_type_url)
    response = requests.get(target_url)
    return response.json()

T = TypeVar("T", bound="ResponseStruct")

@dataclass
class ResponseStruct:
    """
    基础结构，支持递归解析子类、列表，并自动转换枚举类型。
    通过 dataclass 自动生成 __init__、__repr__ 等方法，
    并在 from_dict 中利用 dataclass 的 fields 来解析 JSON 数据。
    """
    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        init_kwargs = {}
        for f in fields(cls):
            # 如果字段 metadata 指定了 json_key，则使用它；否则使用字段名
            json_key = f.metadata.get("json_key", f.name)
            if json_key in data:
                value = data[json_key]
                # 如果值为 None，则直接赋值 None，不进行后续转换
                if value is None:
                    init_kwargs[f.name] = None
                    continue

                field_type = f.type
                # 如果字段类型是 ResponseStruct 子类，则递归解析
                if isinstance(value, dict) and isinstance(field_type, type) and issubclass(field_type, ResponseStruct):
                    init_kwargs[f.name] = field_type.from_dict(value)
                # 处理列表类型
                elif hasattr(field_type, '__origin__') and field_type.__origin__ is list:
                    subtype = field_type.__args__[0]
                    if isinstance(subtype, type) and issubclass(subtype, ResponseStruct):
                        init_kwargs[f.name] = [subtype.from_dict(item) for item in value]
                    elif isinstance(subtype, type) and issubclass(subtype, Enum):
                        init_kwargs[f.name] = [subtype(item) for item in value]
                    else:
                        init_kwargs[f.name] = value
                # 处理枚举类型
                elif isinstance(field_type, type) and issubclass(field_type, Enum):
                    init_kwargs[f.name] = field_type(value)
                else:
                    init_kwargs[f.name] = value
        return cls(**init_kwargs)

    @classmethod
    def from_list(cls: Type[T], data: List[dict]) -> List[T]:
        return [cls.from_dict(item) for item in data]

# 枚举类型定义
class LevelIndex(Enum):
    BASIC = 0
    ADVANCED = 1
    EXPERT = 2
    MASTER = 3
    RE_MASTER = 4

class FCType(Enum):
    AP_PLUS = "app"
    AP = "ap"
    FC_PLUS = "fcp"
    FC = "fc"

class FSType(Enum):
    FDX_PLUS = "fsdp"
    FDX = "fsd"
    FS_PLUS = "fsp"
    FS = "fs"
    SYNC_PLAY = "sync"

class RateType(Enum):
    SSS_PLUS = "sssp"
    SSS = "sss"
    SS_PLUS = "ssp"
    SS = "ss"
    S_PLUS = "sp"
    S = "s"
    AAA = "aaa"
    AA = "aa"
    A = "a"
    BBB = "bbb"
    BB = "bb"
    B = "b"
    C = "c"
    D = "d"

class SongType(Enum):
    STANDARD = "standard"
    DX = "dx"
    UTAGE = "utage"

# 数据结构定义，均使用 dataclass 自动生成方法

@dataclass
class CollectionGenre(ResponseStruct):
    id: int
    title: str
    genre: str

@dataclass
class CollectionRequiredSong(ResponseStruct):
    id: int
    title: str
    type: SongType
    completed: bool = None
    completed_difficulties: List[LevelIndex] = None

@dataclass
class CollectionRequired(ResponseStruct):
    difficulties: List[LevelIndex] = None
    rate: RateType = None
    fc: FCType = None
    fs: FSType = None
    songs: List[CollectionRequiredSong] = None
    completed: bool = None

@dataclass
class Collection(ResponseStruct):
    id: int
    name: str
    color: str = None
    description: str = None
    genre: str = None
    required: List[CollectionRequired] = None

@dataclass
class Version(ResponseStruct):
    id: int
    title: str
    version: int

@dataclass
class Alias(ResponseStruct):
    song_id: int
    aliases: List[str]

@dataclass
class Notes(ResponseStruct):
    total: int
    tap: int
    hold: int
    slide: int
    touch: int
    break_: int = field(metadata={"json_key": "break"})

@dataclass
class BuddyNotes(ResponseStruct):
    left: Notes
    right: Notes

@dataclass
class Genre(ResponseStruct):
    id: int
    title: str
    genre: str

# 使用 kw_only=True 让所有参数仅限关键字传入，从而避免父类默认字段带来的顺序问题
@dataclass(kw_only=True)
class SongDifficulty(ResponseStruct):
    type: SongType
    difficulty: LevelIndex
    level: str
    level_value: float
    note_designer: str
    version: int
    notes: Notes = None

@dataclass(kw_only=True)
class SongDifficultyUtage(SongDifficulty):
    kanji: str
    description: str
    is_buddy: bool
    notes: Union[Notes, BuddyNotes] = None

@dataclass
class SongDifficulties(ResponseStruct):
    standard: List[SongDifficulty]
    dx: List[SongDifficulty]
    utage: List[SongDifficultyUtage] = None

@dataclass
class Song(ResponseStruct):
    id: int
    title: str
    artist: str
    genre: str
    bpm: int
    map: str = None
    version: int = None
    rights: str = None
    disabled: bool = False
    difficulties: SongDifficulties = None

@dataclass
class RatingTrend(ResponseStruct):
    total: int
    standard: int
    dx: int
    date: str

@dataclass
class SimpleScore(ResponseStruct):
    id: int
    song_name: str
    level: str
    level_index: LevelIndex
    fc: FCType = None
    fs: FSType = None
    rate: RateType = None
    type: SongType = None

@dataclass
class Score(ResponseStruct):
    id: int
    song_name: str
    level: str
    level_index: LevelIndex
    achievements: float
    fc: FCType = None
    fs: FSType = None
    dx_score: int = None
    dx_rating: float = None
    rate: RateType = None
    type: SongType = None
    play_time: str = None
    upload_time: str = None
    last_played_time: str = None

@dataclass
class Player(ResponseStruct):
    name: str
    rating: int
    friend_code: int
    trophy: Collection = None
    trophy_name: str = None
    course_rank: int = None
    class_rank: int = None
    star: int = None
    icon: Collection = None
    name_plate: Collection = None
    frame: Collection = None
    upload_time: str = None
