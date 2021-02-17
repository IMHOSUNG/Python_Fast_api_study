# 환경 별 변수를 넣는 공간
# 서버에는 운영서버(실제 서비스 하는 서버)
# 개발 서버
# QA를 진행하는 스테이징 서버
# 내 컴퓨터에만 돌려보는 로컬 환경
# 그 때 마다 다른 환경에 대한 설정 파일을 넣는 것은 Config.py에서 진행

from dataclasses import dataclass, asdict
from os import path, environ

# 상위 디렉토리를 보여주는 곳
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    # 기본 Configuration
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    # 환경 불러오기 : return
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))


print(asdict(LocalConfig()))
