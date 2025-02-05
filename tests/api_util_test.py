from src.api.util import get_player_info, get_public_info
from dotenv import get_key

player_token = get_key(".env","LUOXUE_API_KEY")

def test_get_player_info():
    result = get_player_info(player_token, "player")
    print(result)
    assert result is not None

def test_get_public_info():
    result = get_public_info("song/8")
    print(result)
    assert result is not None