from decimal import Decimal
from fractions import Fraction
from math import floor, log10, log2
from sys import float_info
from typing import Any

__all__ = [
    'digits', 
    'intstrlen', 
    'easyintlog2', 
    'intdigits', 
    'intdivision', 
    'intlog10', 
    'myaboutlog10accuracy', 
    'brlog10', 
    'compound_number', 
    'infinite_precision', 
    'infinite_precision_error', 
    'infinite_format_stringer', 
    'Fraction_to_Decimal'
    ]

def digits(n:Any) -> int:
    "Return: digitsof `n`"
    return int(log10(n))+1

def intstrlen(n:int):
    "Return: length of `n`"
    return len(str(abs(n)))

def easyintlog2(n:int) -> int:
    "Not truly log2ed, but super low calc"
    return n.bit_length()-1

def intdigits(n:int) -> int:
    "Search the digits of `n` with loop processing"
    if float_info.max<n:
        dig = 1
        lbn = easyintlog2(n)
        while(dig*log2(10)<lbn):
            dig += 1
        return dig
    else:
        dig = 1
        while(10**dig<=n):
            dig += 1
        return dig-1

def intdivision(n:int,m:int) -> int:
    "divide calculation only use int"
    return int(n // m + (0 if n%m*10/m<5 else 1))

def intlog10(n:int) -> int:
    "Not truly log10ed, but only use int for calculation"
    idig = intdigits(n)
    if(idig-float_info.max_10_exp+digits(log2(10))<0):
        return intdivision(easyintlog2(n)*(10**idig),int(log2(10)*(10**idig)))
    return intdivision(easyintlog2(n)*(10**idig),int(log2(10)*10**(float_info.max_10_exp-digits(log2(10))))*int(10**(idig-float_info.max_10_exp+digits(log2(10)))))

def myaboutlog10accuracy(n:float):
    "for `intlog10()` function to check accuracy rate"
    if n==1:
        return 100
    return (intlog10(int(n))-log10(n))/log10(n)*100

def brlog10(n):
    "log10 selector for big range of n"
    if(type(n)==float):
        return log10(n)
    elif(type(n)==int):
        if(intlog10(n)<(10**float_info.max_10_exp)):
            return log10(n)
        else:
            return intlog10(int(n))
    else:
        return None
    
def compound_number(frac:Fraction) -> tuple[int,Fraction]:
    """Separate a fraction into integer and fractional parts.
    
    Given a fraction, separate it into an integer part and a fractional part
    (a fraction greater than or equal to 0 and less than 1), and return as a tuple.
    
    Keyword arguments:
    frac -- The fraction to be split
    
    Return: (integer part, fractional part)
    
    分数を整数部と小数部に分離する
    
    与えられた分数を整数部と小数部（0以上1未満の分数）に分割し、
    タプルで返す。
    
    Keyword arguments:
    frac -- 分割対象の分数
    
    Return: (整数部, 小数部)
    """
    if frac==Fraction(1):
        return 1,Fraction(0)
    if frac.numerator<frac.denominator:
        return 0,frac
    # n>d(n/d)
    base = floor(frac)
    return base,frac-base
def infinite_precision(frac:Fraction, precision:int=1000) -> tuple[int,int]:
    """Convert a fraction to mantissa and exponent with specified precision.
    
    Perform decimal expansion on the given fraction and express it as mantissa and exponent.
    The precision can limit the number of decimal places.
    
    Keyword arguments:
    frac -- The fraction to be converted
    precision -- Number of significant digits after the decimal point (default: 1000)
    
    Return: Returns in the format (mantissa, exponent)
    
    分数を指定精度で仮数部と指数部に変換する
    
    与えられた分数を小数展開し、仮数部と指数部として表現する。
    精度により小数点以下の桁数を制限できる。
    
    Keyword arguments:
    frac -- 変換対象の分数
    precision -- 小数点以下の有効桁数（デフォルト1000）
    
    Return: (仮数部, 指数部) の形式で返す
    """
    sign = -1 if frac<0 else 1
    frac = abs(frac)
    mantissa, cp_frac = compound_number(frac)
    expo = 0
    while cp_frac!=Fraction(0):
        mantissa *= 10
        cp_frac *= 10
        b, cp_frac = compound_number(cp_frac)
        mantissa += b
        expo += 1
        if 0<precision and precision<=expo:
            break
    return (sign*mantissa,expo)
def infinite_precision_error(frac:Fraction, precision:int=1000) -> Fraction:
    """Calculate the error due to precision limitation.
    
    Returns the remaining fractional part as a fraction when truncated at the specified precision.
    Represents the difference between the original value and the value after precision limitation.
    
    Keyword arguments:
    frac -- The fraction for which the error is to be calculated
    precision -- The number of significant digits after the decimal point (default: 1000)
    
    Returns: The fraction representing the error
    
    精度制限による誤差を計算する
    
    指定精度で打ち切られた場合の残りの小数部分を分数として返す。
    元の値と精度制限後の値の差を表す。
    
    Keyword arguments:
    - frac -- 誤差計算対象の分数
    - precision -- 小数点以下の有効桁数（デフォルト1000）
    
    Returns: 誤差に相当する分数
    """
    frac = abs(frac)
    _, cp_frac = compound_number(frac)
    expo = 0
    while cp_frac!=Fraction(0):
        cp_frac *= 10
        _, cp_frac = compound_number(cp_frac)
        expo += 1
        if 0<precision and precision<=expo:
            break
    return cp_frac
def infinite_format_stringer(mantissa:int, expo:int):
    """Generate a decimal notation string from mantissa and exponent.
    
    Takes mantissa and exponent (in the form mantissa * 10^-expo),
    and converts it to a string representation including decimal point.
    
    Keyword arguments:
    mantissa -- mantissa (integer)
    expo -- exponent (represents a negative power of 10)
    
    Returns: A string representing the number in decimal notation
    
    仮数部と指数部から小数表記の文字列を生成する
    
    仮数部と指数部（mantissa * 10^-expo の形式）を受け取り、
    小数点記号を含む文字列表現に変換する。
    
    Keyword arguments:
    mantissa -- 仮数部（整数）
    expo -- 指数部（10の負の累乗を示す）
    
    Return: 小数表記の文字列
    """
    # mantissa*10^-expo
    mstring = str(mantissa)
    mdigits = len(mstring)
    string = ""
    if expo==0:
        return mstring
    if mdigits>expo:
        string = mstring[:mdigits-expo] + "." + mstring[mdigits-expo:]
    elif mdigits==expo:
        string = "0." + mstring
    else:
        string = "0." + "0"*(expo-mdigits) + mstring
    return string
def Fraction_to_Decimal(frac:Fraction, precision:int=1000):
    """Convert a fraction to Decimal type with specified precision.
    
    Convert the given fraction to Decimal type for arbitrary precision arithmetic.
    The precision can limit the number of significant digits after the decimal point.
    
    Keyword arguments:
    frac -- The fraction to be converted
    precision -- Number of significant digits after the decimal point (default: 1000)
    
    Return: The value converted to the Decimal type
    
    分数を指定精度のDecimal型に変換する
    
    与えられた分数を無限精度演算用のDecimal型に変換する。
    精度により小数点以下の有効桁数を制限できる。
    
    Keyword arguments:
    frac -- 変換対象の分数
    precision -- 小数点以下の有効桁数（デフォルト1000）
    
    Return: Decimal型に変換された値
    """
    return Decimal(infinite_format_stringer(*infinite_precision(frac=frac, precision=precision)))
