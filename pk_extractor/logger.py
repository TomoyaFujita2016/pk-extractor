import os
from logging import DEBUG, Formatter, StreamHandler, getLogger

"""ロギング関係
"""

log = getLogger(__name__)
formatter = Formatter(
    "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
)

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(DEBUG)
log.propagate = False
