from api.raw import (
    get_player,
    get_player_scores,
    get_song_list,
    get_song,
    get_alias_list,
    get_icon_list,
    get_icon,
    get_plate_list,
    get_plate,
    get_frame_list,
    get_frame,
    get_collection_genre_list,
    get_collection_genre,
)
from dotenv import get_key

# 请确保 .env 文件中包含正确的个人 API 密钥
player_token = get_key(".env", "LUOXUE_API_KEY")


# ===== 个人 API 测试 =====
def test_get_player():
    result = get_player(player_token)
    print("Player:", result)
    assert result is not None


def test_get_player_scores():
    result = get_player_scores(player_token)
    print(f"Scores Length: {len(result)}, Score[0]: {result[0] if result else 'N/A'}")
    assert result is not None


# ===== 公共 API 测试 =====
def test_get_song_list():
    result = get_song_list()
    print("Song List [songs length]:", len(result["songs"]))
    print("Sample Song:", result["songs"][0])
    print("Song List [genres length]:", len(result["genres"]))
    print("Sample Genre:", result["genres"][0])
    print("Song List [versions length]:", len(result["versions"]))
    print("Sample Version:", result["versions"][0])
    assert "songs" in result and len(result["songs"]) > 0


def test_get_song():
    # 以曲目 ID 8 为例
    result = get_song(8)
    print("Song:", result)
    assert result is not None


def test_get_alias_list():
    result = get_alias_list()
    print(f"Alias Count: {len(result)}")
    assert isinstance(result, list)


def test_get_icon_list():
    result = get_icon_list()
    print(f"Icon Count: {len(result)}")
    assert isinstance(result, list)


def test_get_icon():
    # 以头像 ID 200201 为例（根据实际数据调整）
    result = get_icon(200201)
    print("Icon:", result)
    assert result is not None


def test_get_plate_list():
    result = get_plate_list()
    print(f"Plate Count: {len(result)}")
    assert isinstance(result, list)


def test_get_plate():
    # 以姓名框 ID 200201 为例（根据实际数据调整）
    result = get_plate(200201)
    print("Plate:", result)
    assert result is not None


def test_get_frame_list():
    result = get_frame_list()
    print(f"Frame Count: {len(result)}")
    assert isinstance(result, list)


def test_get_frame():
    # 以背景 ID 300101 为例（根据实际数据调整）
    result = get_frame(300101)
    print("Frame:", result)
    assert result is not None


def test_get_collection_genre_list():
    result = get_collection_genre_list()
    print(f"Collection Genre Count: {len(result)}")
    assert isinstance(result, list)


def test_get_collection_genre():
    # 以收藏品分类 ID 105599 为例（根据实际数据调整）
    result = get_collection_genre(1)
    print("Collection Genre:", result)
    assert result is not None
