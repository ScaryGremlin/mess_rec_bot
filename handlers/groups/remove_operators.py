import re

from aiogram import types

from data import config
from loader import database
from loader import dispatcher

pattern_user_name = re.compile(r'@[a-zA-Z][a-zA-Z0-9\_]{4,}')
