from collections import deque
from collections.abc import Callable
from copy import deepcopy
from itertools import chain
from math import log
from os import listdir, scandir
from os.path import getsize, isdir, isfile, join, split, splitext
from socket import gethostbyname, gethostname
from sys import getsizeof
from typing import Any, Literal
from uuid import getnode

__all__ = [
    'clearconsole', 
    'xorhash', 
    'UTF8num', 
    'numUTF8', 
    'get_bytes', 
    'slit', 
    'macaddress', 
    'ipaddress', 
    'my_function_call_function', 
    'mutablecopy', 
    'get_dir_size', 
    'get_external_size', 
    'get_dir_size_old', 
    'compute_object_size', 
    'unitparser', 
    'BytesToSIUnit', 
    'NoOverride', 
    'leftshift', 
    'Burrows_Wheeler_Algorithm_encode', 
    'Burrows_Wheeler_Algorithm_decode'
    ]

def clearconsole():
    "PRINT 10000 lanes of `\\n`"
    print("\n"*10000, end="")
    return print((0).to_bytes().decode())

"""hexing - Which do you use??
>>> byte = b"\xab\xcd\xef"
>>> byte.hex()
'abcdef'
>>> import binascii
>>> binascii.hexlify(byte)
b'abcdef'
>>> str(binascii.hexlify(byte), 'utf-8')
'abcdef'
>>> str(binascii.b2a_hex(byte), 'utf-8')
'abcdef'

>>> string = "abcdef"
>>> bytes.fromhex(string)
b'\xab\xcd\xef'
>>> import binascii
>>> binascii.unhexlify(string)
b'\xab\xcd\xef'
>>> binascii.a2b_hex(string)
b'\xab\xcd\xef'
>>> binascii.hexlify(binascii.unhexlify(string) *OR* bytes.fromhex(string))
b'abcdef'


READ THE DOC
https://qiita.com/masakielastic/items/21ba9f68ef6c4fd7692d
"""

def xorhash(hash1:str,hash2:str):
    "from 2hashes to xored hash"
    return hex(int(hash1,base=16)^int(hash2,base=16))[2:]

def UTF8num(string:str) -> int:
    "From utf_8 to num of character code"
    return int.from_bytes(string.encode("utf-8"))
def numUTF8(num:int) -> str:
    "From num of character code to utf_8"
    return get_bytes(num).decode("utf-8")
def get_bytes(num:int, byteorder: Literal['little', 'big'] = "big",*, signed: bool = False) -> bytes:
    "from any `int` to `bytes`"
    return num.to_bytes((num.bit_length()+7)//8, byteorder=byteorder, signed=signed)

def slit(string:str,wide:int) -> list[str]:
    "From long `string` to list with `string` divided per `wide`"
    return [string[i:i+wide] for i in range(0,len(string),wide)]

def macaddress():
    "Return this machine's Mac Address"
    return ":".join(slit(hex(getnode())[2:],2))
def ipaddress():
    "Return this machine's IP Address"
    return gethostbyname(gethostname())

def my_function_call_function(input:Any,func:Callable):
    "this function calls `func`function and inputs `input` to it and returns the returned data"
    return func(input)

def mutablecopy(mutable,loop:int):
    """copy table using deepcopy

    Example:
    >>> nonmuted = mutablecopy({"how":0},2)
    >>> muted = [{"how":0}]*2
    >>> nonmuted[1]["how"] = 2
    >>> muted[1]["how"] = 2
    >>> nonmuted
    [{'how': 0}, {'how': 2}]
    >>> muted
    [{'how': 2}, {'how': 2}]
    """
    return [deepcopy(mutable) for _ in range(loop)]

def get_dir_size(path='.',recursion=True,follow_symlinks=True):
    "get directory size"
    total = 0
    with scandir(path=path) as deit: # DirEntry iterator
        for entry in deit:
            if entry.is_file(follow_symlinks=follow_symlinks):
                total += entry.stat().st_size
            elif recursion and entry.is_dir(follow_symlinks=follow_symlinks):
                total += get_dir_size(entry.path)
    return total

def get_external_size(path='.'):
    "get external things size"
    if isfile(path):
        return getsize(path)
    elif isdir(path):
        return get_dir_size(path)

def get_dir_size_old(path='.'):
    "if python version is older than 3.11(?), you can only use this function"
    total = 0
    for p in listdir(path=path):
        full_path = join(path, p)
        if isfile(full_path):
            total += getsize(full_path)
        elif isdir(full_path):
            total += get_dir_size_old(full_path)
    return total

def compute_object_size(o: Any, handlers={}):
    "computes `o`object size"
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

def unitparser(unitstr:str):
    """
    Parses a unit string containing a number with SI prefix and unit.
    
    Args:
        unitstr: A string containing a number, optional SI prefix, and optional unit.
                 Supports spaces, underscores, and commas as separators (removed).
    
    Returns:
        A tuple of (fixedint, fixedfloat, siunitbase, unit) where:
        - fixedint: The integer part of the number as a string
        - fixedfloat: The fractional part of the number as a string
        - siunitbase: The SI unit multiplier value as a string
        - unit: The unit part of the string after the SI prefix
    
    Examples:
        unitparser("1.5km") -> ("1", "5", "1000", "m")
        unitparser("2.4 GHz") -> ("2", "4", "1000000000", "Hz")
    """
    unitstr = unitstr.replace(" ", "")
    unitstr = unitstr.replace("_", "")
    unitstr = unitstr.replace(",", "")

    NUMB = [str(i) for i in range(10)]
    SIUT = ["p", "n", "μ", "u", "m", "c", "d", "da", "h", "k", "K", "M", "G", "T", "P"] # da = deka <- never hits
    rSIU = [1e-12, 1e-9, 1e-6, 1e-6, 1e-3, 1e-2, 1e-1, 1e1, 1e2, 1e3, 1e3, 1e6, 1e9, 1e12, 1e15]

    fixedint = ""
    fixedfloat = ""
    separatorflag = False
    siunitbase = "0"

    for i in range(len(unitstr)):
        if unitstr[i] in NUMB:
            if separatorflag:
                fixedfloat += unitstr[i]
            else:
                fixedint += unitstr[i]
        elif unitstr[i] == ".":
            separatorflag = True
        elif unitstr[i] in SIUT:
            tmp = rSIU[SIUT.index(unitstr[i])]
            if tmp < 1:
                siunitbase = f"{{:.{f"{tmp:g}"[3:]}f}}".format(tmp)
            else:
                siunitbase = str(tmp)
            unitindex = i+1
            break
        else:
            unitindex = i

    unit = unitstr[unitindex:]

    return fixedint, fixedfloat, siunitbase, unit

def BytesToSIUnit(size:int, isdata:bool=True, dataformat:bool=True) -> str:
    "from `size` to size with si unit"
    base = 1024 if isdata else 1000
    logged = log(size, base)
    kmgt = int(logged)
    SIunit = ""
    if dataformat:
        match kmgt:
            case 0:
                SIunit = "  B"
            case 1:
                SIunit = "kiB" # kibibyte キビバイト
            case 2:
                SIunit = "MiB" # mebibyte メビバイト
            case 3:
                SIunit = "GiB" # gibibyte ギビバイト
            case 4:
                SIunit = "TiB" # tebibyte テビバイト
            case 5:
                SIunit = "PiB" # pebibyte ペビバイト
            case 6:
                SIunit = "EiB" # exbibyte エクスビバイト
            case 7:
                SIunit = "ZiB" # zebibyte ゼビバイト
            case 8:
                SIunit = "YiB" # yobibyte ヨビバイト
            case 9:
                SIunit = "RiB" # robibyte ロビバイト
            case 10:
                SIunit = "QiB" # quebibyte クエビバイト
            case _:
                SIunit = "Bytes"
    else:
        match kmgt:
            case 0:
                SIunit = " B"
            case 1:
                SIunit = "kB" # kilobyte キロバイト
            case 2:
                SIunit = "MB" # megabyte メガバイト
            case 3:
                SIunit = "GB" # gigabyte ギガバイト
            case 4:
                SIunit = "TB" # terabyte テラバイト
            case 5:
                SIunit = "PB" # petabyte ペタバイト
            case 6:
                SIunit = "EB" # exabyte エクサバイト
            case 7:
                SIunit = "ZB" # zettabyte ゼタバイト
            case 8:
                SIunit = "YB" # yottabyte ヨタバイト
            case 9:
                SIunit = "RB" # ronnabyte ロナバイト
            case 10:
                SIunit = "QB" # quettabyte クエタバイト
            case _:
                SIunit = "Bytes"
    return f"{size/(base**kmgt):.4f} {SIunit}"

def NoOverride(filepath:str) -> str:
    "Do Not Override with using this function"
    directory, filename = split(filepath)
    if not isdir(directory):
        raise FileNotFoundError(f"No such directory: '{directory}'")
    if filename in listdir(directory):
        idx = 0
        fn = f"{splitext(filename)[0]}_{idx}{splitext(filename)[1]}"
        while fn in listdir(directory):
            idx += 1
            fn = f"{splitext(filename)[0]}_{idx}{splitext(filename)[1]}"
        return join(directory, fn)
    else:
        return filepath
    return ""

def leftshift(s:str):
    "Input: string, Return: string with the input shifted to the left"
    return deepcopy(s[1:]+s[0])
def Burrows_Wheeler_Algorithm_encode(string:str):
    """Burrows-Wheeler変換を実行
    
    Args:
        string (str): エンコードする文字列
    
    Returns:
        tuple: (変換後の文字列, 元の文字列のインデックス)
    """
    shift_list = []
    for _ in range(len(string)):
        shift_list.append(string)
        string = leftshift(string)
    sorted_shift_list = sorted(shift_list)
    return "".join([s[-1] for s in sorted_shift_list]),sorted_shift_list.index(string)
def Burrows_Wheeler_Algorithm_decode(string:str,index:int):
    """Burrows-Wheeler変換をデコード
    
    Args:
        string (str): デコードする文字列（変換後の文字列）
        index (int): 元の文字列のインデックス
    
    Returns:
        str: デコード後の元の文字列
    """
    sorted_shift_list = [""]*len(string)
    for _ in range(len(string)):
        for i in range(len(sorted_shift_list)):
            sorted_shift_list[i] = string[i]+sorted_shift_list[i]
        sorted_shift_list = sorted(sorted_shift_list)
    return sorted_shift_list[index]