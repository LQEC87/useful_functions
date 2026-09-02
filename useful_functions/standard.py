from datetime import timedelta
from fractions import Fraction
from math import log, log10

from .algorithms import infinite_precision

__all__ = [
    'float_error', 
    'to_ieee754', 
    'from_ieee754', 
    'to_ieee754_bytes', 
    'from_ieee754_bytes', 
    'get_dhmsu', 
    'y2d', 
    'timestamp2ISO8601'
    ]

def float_error(*,zeropoint:int) -> float:
    "Input:0.[zeropoint:int] Return: error of floating point number"
    fi = infinite_precision(Fraction(float(f"0.{zeropoint}")))
    ex2 = 0
    ex5 = 0
    for i in range(int(log(zeropoint, 2))+1):
        if zeropoint%2**i==0:
            ex2 = i
    for i in range(int(log(zeropoint, 5))+1):
        if zeropoint%5**i==0:
            ex5 = i
    truezeropoint = int(zeropoint/10**min(ex2,ex5))
    return (fi[0] - truezeropoint * 10**(fi[1]-int(log10(truezeropoint)+1))) / 10**fi[1]

def to_ieee754(x:float): # 'bias': 1023, 'exp_bits': 11, 'mantissa_bits': 52, 8bytes = 64bits
    "From `float` to representation of IEEE754"
    if x==0:
        if str(x)[0]=="0":
            return "0"*64
        else:
            return "1"+"0"*63
    sign = 0 if x>=0 else 1
    x = abs(x)
    itx = int(x)
    flx = x-itx
    bitx = bin(itx)[2:]
    i = 1
    bflx = ""
    while flx!=0.0:
        if not 2**-i<=flx:
            bflx += "0"
            i+=1
        else:
            bflx += "1"
            flx -= 2**-i
            i+=1
    bnx = f"{bitx}.{bflx}"
    pp = bnx.find('.')
    fo = bnx.find('1')
    exponent = pp-fo-1
    if fo>pp:
        exponent = pp-fo
    exponent += 1023 # bias
    mantissa = (bitx+bflx)[((bitx+bflx).find('1'))+1:]
    ieee754 = f"{sign}{("0"*11+bin(exponent)[2:])[-11:]}{(mantissa+"0"*52)[:52]}"
    return ieee754
def from_ieee754(s:str):
    "From representation of IEEE754 to `float`"
    if len(s)!=64:
        raise ValueError("Not Correct Value")
    if s == "0"*64:
        return 0.0
    elif s == "1"+"0"*63:
        return -0.0
    sign, exponent, mantissa = int(s[0]), int(s[1:11+1],2), s[11+1:]
    fl = 1.0
    for i in range(len(mantissa)):
        fl += int(mantissa[i])*2**-(i+1)
    fl *= 2**(exponent-1023)
    fl *= (-1)**sign
    return fl
def to_ieee754_bytes(x:float):
    "`to_ieee` output bytes type"
    return int(to_ieee754(x),2).to_bytes(8)
def from_ieee754_bytes(x:bytes):
    "`from_ieee` input bytes type"
    return from_ieee754(bin(int.from_bytes(x))[2:])

def get_dhmsu(sec:float):
    "Convert seconds to days, hours, minutes, seconds, and microseconds"
    td = timedelta(seconds=sec)
    m,s = divmod(td.seconds, 60)
    h,m = divmod(m, 60)
    return td.days, h, m, s, td.microseconds

def y2d(y:int) -> int:
    "from year to days"
    return 365*y+int(y/4)-int(y/100)+int(y/400)

def timestamp2ISO8601(t:float):
    "From timestamp to ISO8601 format of date"
    year = int(t//(60*60*24*365.25))+1970
    year = year if y2d(year-1)-y2d(1969)<=t/(60*60*24)<y2d(year)-y2d(1969) else (year-1 if t/(60*60*24)<=y2d(year)-y2d(1969) else year+1)
    days = int(t)//(60*60*24)-(y2d(year-1)-y2d(1970-1))+1
    # print(days)
    endofmonth = [31,29 if year%4==0 and ( year%100!=0 or year%400==0 ) else 28,31,30,31,30,31,31,30,31,30,31]
    month = sum([1 for i in range(1,12+1) if sum(endofmonth[:i])<days])+1
    endofbeforelast = sum(endofmonth[:month-1])
    # print(days,endofbeforelast)
    day = int(days-endofbeforelast)
    total_seconds = t%int(60*60*24)
    hour = int(total_seconds//(60*60))
    minute = int(total_seconds%(60*60)//60)
    sec = int(total_seconds%60)
    nosec = int(t*1000000)%1000000
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{sec:02d}.{nosec:06d}"
