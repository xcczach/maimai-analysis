from .util import (
    get_player_info,
    get_public_info,
    Player,
    Score,
    Song,
    Genre,
    Version,
    Alias,
    Collection,
    CollectionGenre,
    SimpleScore,
    RatingTrend,
)

# ===== 个人 API =====
def get_player(token: str) -> Player:
    """
    获取玩家信息
    """
    return Player.from_dict(get_player_info(token, "player"))

def get_player_scores(token: str) -> list[Score]:
    """
    获取玩家所有成绩
    """
    return Score.from_list(get_player_info(token, "player/scores"))

# ===== 公共 API =====
def get_song_list(version: int = 24000, notes: bool = False) -> dict:
    """
    获取曲目列表
    返回字典包含：
      - songs: List[Song]
      - genres: List[Genre]
      - versions: List[Version]
    """
    result = get_public_info(f"song/list?version={version}&notes={str(notes).lower()}")
    data = result.get("data", result)
    songs = Song.from_list(data.get("songs", []))
    genres = Genre.from_list(data.get("genres", []))
    versions = Version.from_list(data.get("versions", []))
    return {"songs": songs, "genres": genres, "versions": versions}

def get_song(song_id: int, version: int = 24000) -> Song:
    """
    获取指定曲目信息
    """
    result = get_public_info(f"song/{song_id}?version={version}")
    data = result.get("data", result)
    return Song.from_dict(data)

def get_alias_list() -> list[Alias]:
    """
    获取曲目别名列表
    """
    result = get_public_info("alias/list")
    data = result.get("data", result)
    return Alias.from_list(data.get("aliases", []))

# 以下接口中 Icon、Plate、Frame 均为 Collection 类型
def get_icon_list(version: int = 24000, required: bool = False) -> list[Collection]:
    """
    获取头像列表
    """
    result = get_public_info(f"icon/list?version={version}&required={str(required).lower()}")
    data = result.get("data", result)
    return Collection.from_list(data.get("icons", []))

def get_icon(icon_id: int, version: int = 24000) -> Collection:
    """
    获取指定头像信息
    """
    result = get_public_info(f"icon/{icon_id}?version={version}")
    data = result.get("data", result)
    return Collection.from_dict(data)

def get_plate_list(version: int = 24000, required: bool = False) -> list[Collection]:
    """
    获取姓名框列表
    """
    result = get_public_info(f"plate/list?version={version}&required={str(required).lower()}")
    data = result.get("data", result)
    return Collection.from_list(data.get("plates", []))

def get_plate(plate_id: int, version: int = 24000) -> Collection:
    """
    获取指定姓名框信息
    """
    result = get_public_info(f"plate/{plate_id}?version={version}")
    data = result.get("data", result)
    return Collection.from_dict(data)

def get_frame_list(version: int = 24000, required: bool = False) -> list[Collection]:
    """
    获取背景列表
    """
    result = get_public_info(f"frame/list?version={version}&required={str(required).lower()}")
    data = result.get("data", result)
    return Collection.from_list(data.get("frames", []))

def get_frame(frame_id: int, version: int = 24000) -> Collection:
    """
    获取指定背景信息
    """
    result = get_public_info(f"frame/{frame_id}?version={version}")
    data = result.get("data", result)
    return Collection.from_dict(data)

def get_collection_genre_list(version: int = 24000) -> list[CollectionGenre]:
    """
    获取收藏品分类列表
    """
    result = get_public_info(f"collection-genre/list?version={version}")
    data = result.get("data", result)
    return CollectionGenre.from_list(data.get("collectionGenres", []))

def get_collection_genre(collection_genre_id: int, version: int = 24000) -> CollectionGenre:
    """
    获取指定收藏品分类信息
    """
    result = get_public_info(f"collection-genre/{collection_genre_id}?version={version}")
    data = result.get("data", result)
    return CollectionGenre.from_dict(data)
