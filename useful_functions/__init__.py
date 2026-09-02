from .algorithms import *
from .calcurations import *
from .standard import *
from .utilities import *


# ACCESSIBLES = list(sorted([k for k in list(locals().keys()) if k[0]!='_']))
ACCESSIBLES: list[str] = list(sorted(algorithms.__all__ + calcurations.__all__ + standard.__all__ + utilities.__all__))
"""このモジュールで使えるアクセッサ一覧です。

Example:
>>> for acc in anyfunction.ACCESSIBLES:
>>>     print("\\n\\n\\n")
>>>     print(acc)
>>>     eval(f"print(af.{acc}.__doc__)")
"""