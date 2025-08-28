from .sing_command import register_sing_command
from .help_command import register_help_command
from .hello_command import register_hello_command
from .calc_command import register_calc_command
from .weather_command import register_weather_command
from .joke_command import register_joke_command
from .avatar_command import register_avatar_command
from .bilibili_command import register_bilibili_command
from .music_command import register_music_command
from .ai_command import register_ai_command
from .utils import is_allowed_group
from .face_command import register_face_command
from .meinvpic_command import register_meinvpic_command
from .random_avatar_command import register_random_avatar_command
from .heisi_command import register_heisi_command
from .baisi_command import register_baisi_command
from .sixty_command import register_sixty_command

def register_commands():
    register_sing_command()
    register_help_command()
    register_hello_command()
    register_calc_command()
    register_weather_command()
    register_joke_command()
    register_avatar_command()
    register_bilibili_command()
    register_music_command()
    register_ai_command()
    register_face_command()
    register_meinvpic_command()
    register_random_avatar_command()
    register_heisi_command()
    register_baisi_command()
    register_sixty_command()