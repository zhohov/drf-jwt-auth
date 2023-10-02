from dotenv import load_dotenv, find_dotenv

from .common import *
from .database import *
from .spectacular import *
from .drf import *

load_dotenv(find_dotenv())
