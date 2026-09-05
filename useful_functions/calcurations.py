from collections import Counter
from copy import deepcopy
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from math import ceil, dist, factorial, isqrt, log, sqrt
from random import choices, randint, random
from typing import Callable, SupportsFloat
from warnings import catch_warnings, warn

__all__ = ['Calcurations']

class Calcurations:
    """Mathematical calculation utility class.
    
    Provides various mathematical functions and constants including:
    - PI calculation using multiple algorithms (Ramanujan, Monte Carlo, Leibniz, etc.)
    - Euler's number (E)
    - Fibonacci numbers (standard and fast method)
    - Tetration and Ackermann functions
    - Prime factorization
    - Greatest Common Divisor (GCD) calculations
    - Fraction reduction
    - And many other mathematical operations
    
    Attributes:
        PI (Decimal): Pi constant calculated using Ramanujan's method
        E (Decimal): Euler's number
        primes (list): List of prime numbers
        piCalcurator (Enum): Enumeration of different PI calculation methods
    
    数学計算ユーティリティクラス。
    
    以下のような、さまざまな数学関数や定数を提供します：
    - 複数のアルゴリズム（ラマヌジャン、モンテカルロ、ライプニッツなど）を用いた円周率（PI）の計算
    - オイラーの定数 (E)
    - フィボナッチ数（標準法および高速法）
    - テトレーション関数およびアッカーマン関数
    - 素因数分解
    - 最大公約数 (GCD) の計算
    - 分数の約分
    - その他多数の数学演算
    
    属性：
        PI (Decimal)：ラマヌジャン法を用いて計算された円周率（Pi）定数
        E (Decimal)：オイラーの定数（E）
        primes (list)：素数のリスト
        piCalculator (Enum)：さまざまな円周率計算法の列挙型
    """
    
    
    primes = [2]

    def __init__(self):
        self.PI = self.pi(self.piCalcurator.RAMANUJAN,10)
        self.E = self.e()

    class piCalcurator(Enum):
        RAMANUJAN = 0
        MONTECARLO = 1
        LEIBNIZ = 2
        TRAPEZOIDALRULE = 3
        WALLISPRODUCT = 4
        RAMANUJAN1914 = 5
        CHUDNOVSKY = 6
        BORWEIN = 7
        GAUSSLEGENDRE = 8
        EULER = 9
        BAILEYBORWEINPLOUFFE = 10
        BELLARD = 11
        高野喜久雄 = 314
    
    @staticmethod
    def fibonatti(n:int, fast:bool=False):
        if fast:
            r5 = sqrt(5)
            return int((1/r5) * (((1+r5)/2)**n - ((1-r5)/2)**n))
        a = 0
        b = 1
        for _ in range(n):
            a,b = b,a+b
        return b
    
    @staticmethod
    def tetration(a:int, n:int):
        "a↑↑n = a^a^a^a^...}←n times"
        t = 1
        for _ in range(n):
            t = a ** t
        return t
    
    @classmethod
    def ackermann(cls, m:int, n:int) -> int:
        "ackermann function. if you don't know what it was, you should google it."
        if n<0 or m<0:
            raise ValueError("n and m must be positive numbers.")
        if m==0:
            return n+1
        if n==0:
            return cls.ackermann(m-1,1)
        #_warn("This function creates huge recursion.",RecursionWarning)
        with catch_warnings(action="always",category=ResourceWarning): # ResourceWarning is set default to "ignore"
            warn("This function creates huge recursion.", ResourceWarning)
        return cls.ackermann(m-1, cls.ackermann(m, n-1))

    @classmethod
    def prime_factor(cls, n: int):
        "disassemble to prime factors"
        if n>2**50: # log(n,2)>50
            ps = [2, 3, 5, 7, 11, 13, 17, 19]
            pf = list()
            k = Fraction(n)
            for p in ps:
                if k%p==0:
                    while k%p==0:
                        pf.append(int(p))
                        k /= p
                if p*p>k:
                    if k!=1:
                        pf.append(int(p))
                    return pf
            for i in range(24, int(cls.i_root(int(k)))+12, 6):
                tp = [0, 0]
                for i,t in enumerate([i-1, i+1]):
                    for p in ps:
                        if t%p==0:
                            break
                        if p*p>t:
                            print(t)
                            if k%t==0:
                                while k%t==0:
                                    pf.append(int(t))
                                    k /= t
                            if t*t>k:
                                if k!=1:
                                    pf.append(int(k))
                                return pf
                            ps.append(int(t))
                            break
                    else:
                        print(t)
                        if k%t==0:
                            while k%t==0:
                                pf.append(int(t))
                                k /= t
                        if t*t>k:
                            if k!=1:
                                pf.append(int(k))
                            return pf
                        ps.append(int(t))
        else:
            ps = [2, 3, 5, 7, 11, 13, 17, 19]
            pf = list()
            k = n
            for p in ps:
                if k%p==0:
                    while k%p==0:
                        pf.append(int(p))
                        k /= p
                if p*p>k:
                    if k!=1:
                        pf.append(int(p))
                    return pf
            for i in range(24, int(cls.f_root(Fraction(n),2 if n<100 else ceil(log(n, 10))))+12, 6):
                tp = [0, 0]
                for i,t in enumerate([i-1, i+1]):
                    for p in ps:
                        if t%p==0:
                            break
                        if p*p>t:
                            print(t)
                            if k%t==0:
                                while k%t==0:
                                    pf.append(int(t))
                                    k /= t
                            if t*t>k:
                                if k!=1:
                                    pf.append(int(k))
                                return pf
                            ps.append(int(t))
                            break
                    else:
                        print(t)
                        if k%t==0:
                            while k%t==0:
                                pf.append(int(t))
                                k /= t
                        if t*t>k:
                            if k!=1:
                                pf.append(int(k))
                            return pf
                        ps.append(int(t))

    @staticmethod
    def myprod(l: list[int]):
        "production all of int in the list"
        ans: int = 1
        for n in l:
            ans *= n
        return int(ans)

    @classmethod
    def mygcd(cls, n1: int, n2: int):
        "Python way's greatest common divisor calc"
        f1 = cls.prime_factor(n1)
        f2 = cls.prime_factor(n2)

        c1 = Counter(f1)
        c2 = Counter(f2)
        common = c1 & c2

        common_exact = list(common.elements())
        n_gcd: int = cls.myprod(common_exact)

        return int(n_gcd)
    @staticmethod
    def my_Euclid_gcd(n1: int, n2: int):
        "euclid's greatest common divisor calcuration"
        dividee = max(n1, n2)
        divider = min(n1, n2)
        surplus = dividee % divider
        while surplus != 0:
            dividee = divider
            divider = surplus
            surplus = dividee % divider
        return divider

    @classmethod
    def fraction_reducer(cls, dividee: int, divider: int):
        "dividee / divider to compact shape"
        n_gcd = cls.mygcd(dividee, divider)

        f_dividee = cls.prime_factor(dividee)
        f_divider = cls.prime_factor(divider)
        f_gcd     = cls.prime_factor(n_gcd)

        c_dividee = Counter(f_dividee)
        c_divider = Counter(f_divider)
        c_gcd     = Counter(f_gcd)

        l_dividee = c_dividee - c_gcd
        l_divider = c_divider - c_gcd

        n_dividee = cls.myprod(list(l_dividee.elements()))
        n_divider = cls.myprod(list(l_divider.elements()))

        return n_dividee, n_divider

    @classmethod
    def choice_prime(cls, ps: list[int] = [2, 3, 5, 7, 11, 13, 17, 19]):
        exps    = [0, 1, 2, 3, 4, 5]
        weighter = [2/5, 2/5, 1/10, 1/20, 1/40, 1/40]

        expon = choices(exps, weights=weighter, k=len(ps))

        comp = cls.myprod([a**b for a,b in zip(ps, expon)])

        return comp

    @staticmethod
    def i_root(a:int,N:int|None=None):
        "sqrt(a)"
        if a==0:
            return 0
        sign = -1 if a < 0 else 1
        b = int(a*sign)
        x = 1 << ((b.bit_length() + 1) // 2)

        if N is not None:
            for _ in range(N):
                y = (x + b // x) >> 1
                if y >= x:
                    return x*sign
                x = y
            return x*sign
        else:
            while True:
                y = (x + b // x) >> 1
                if y >= x:
                    return x*sign
                x = y
    
    @staticmethod
    def f_root(a:Fraction,N:int):
        "sqrt(a)"
        if a == Fraction(0):
            return Fraction(0)
        sign = -1 if a < 0 else 1
        b = Fraction(a*sign)
        if b>10**5:
            try:
                b = Fraction(sqrt(b))
            except OverflowError:
                try:
                    b = Fraction(log(b.numerator)-log(b.denominator))
                except OverflowError:
                    b = Fraction(b.numerator.bit_length()-b.denominator.bit_length())
        for _ in range(N):
            # b = (a + b*b)/(b*2)
            b = (b + a/b) / 2
        return b*sign
    
    @staticmethod
    def aF_powby_bI(a:Fraction,b:int):
        a,b = Fraction(a), int(b)
        return Fraction(a.numerator**b,a.denominator**b)
    @classmethod
    def aI_root_bF(cls, a:int,b:Fraction,N:int, LIMITS:int=0):
        # x=b^n(1-n)-a / nb^(n-1)
        # y=at^(a-1)x+t^a(1-a)-b
        # x = t^a(1-a)-b / at^(a-1)
        a,b = int(a), Fraction(b)
        if a<=0:
            raise ValueError("a must be greater than 0")
        if a==1:
            return b
        if b==0:
            return Fraction(0)
        try:
            ans = Fraction(pow(b,1/a))
        except OverflowError:
            ans = cls.f_root(b,N)/a
        for _ in range(N):
            ans = (cls.aF_powby_bI(ans, a)*(1-a)-b)/(a*cls.aF_powby_bI(ans, a-1))
            if LIMITS>0:
                ans = ans.limit_denominator(LIMITS)
        return ans
    @classmethod
    def powFraction(cls, a:Fraction,b:Fraction,N:int, LIMITS:int=0):
        # a^b = (p/q)^(r/s) = p^(r/s)/q^(r/s) ≠ (p^r)*s√p / (q^r)*s√q = p^r/q^r * s√(p/q)
        # !!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!
        # nb^(n-1)x+b^n(1-n)-a
        # a^b = (p/q)^(r/s) = p^(r/s)/q^(r/s) = s√(p^r) / s√(q^r) = s√(p^r/q^r) = s√((p/q)^r)
        a,b = Fraction(a),Fraction(b)
        return cls.aI_root_bF(b.denominator, cls.aF_powby_bI(a,b.numerator), N, LIMITS) if LIMITS>0 else cls.aI_root_bF(b.denominator, cls.aF_powby_bI(a,b.numerator), N)
    @classmethod
    def powBinFract(cls, b:Fraction,N:int, LIMITS:int=0):
        "2^`b`"
        # 2^b = 2^(r/s) = s√(2^r)
        b=Fraction(b)
        return cls.aI_root_bF(b.denominator, Fraction(1 << b.numerator),N,LIMITS) if LIMITS>0 else cls.aI_root_bF(b.denominator, Fraction(1 << b.numerator),N)
    
    @classmethod
    def isprime(cls, n:int, speed:int=-1):
        if n<=1:
            raise ValueError("`n` must be greater than 1")
        match speed:
            case 0:
                for i in range(2,n):
                    if n%i==0:
                        return False
                return True
            case 1:
                for i in range(2,n//2):
                    if n%i==0:
                        return False
                return True
            case 2:
                for i in range(2,ceil(sqrt(n))+1):
                    if n%i==0:
                        return False
                return True
            case 3:
                if n%2==0:
                    return False
                for i in range(3,ceil(sqrt(n))+1,2):
                    if n%i==0:
                        return False
                return True
            case 4:
                smallprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349, 4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657, 4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801, 4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973, 4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107, 5113, 5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281, 5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431, 5437, 5441, 5443, 5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 5569, 5573, 5581, 5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741, 5743, 5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849, 5851, 5857, 5861, 5867, 5869, 5879, 5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 6053, 6067, 6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221, 6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353, 6359, 6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 6547, 6551, 6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691, 6701, 6703, 6709, 6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 6827, 6829, 6833, 6841, 6857, 6863, 6869, 6871, 6883, 6899, 6907, 6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991, 6997, 7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177, 7187, 7193, 7207, 7211, 7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333, 7349, 7351, 7369, 7393, 7411, 7417, 7433, 7451, 7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523, 7529, 7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 7603, 7607, 7621, 7639, 7643, 7649, 7669, 7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919, 7927, 7933, 7937, 7949, 7951, 7963, 7993, 8009, 8011, 8017, 8039, 8053, 8059, 8069, 8081, 8087, 8089, 8093, 8101, 8111, 8117, 8123, 8147, 8161, 8167, 8171, 8179, 8191, 8209, 8219, 8221, 8231, 8233, 8237, 8243, 8263, 8269, 8273, 8287, 8291, 8293, 8297, 8311, 8317, 8329, 8353, 8363, 8369, 8377, 8387, 8389, 8419, 8423, 8429, 8431, 8443, 8447, 8461, 8467, 8501, 8513, 8521, 8527, 8537, 8539, 8543, 8563, 8573, 8581, 8597, 8599, 8609, 8623, 8627, 8629, 8641, 8647, 8663, 8669, 8677, 8681, 8689, 8693, 8699, 8707, 8713, 8719, 8731, 8737, 8741, 8747, 8753, 8761, 8779, 8783, 8803, 8807, 8819, 8821, 8831, 8837, 8839, 8849, 8861, 8863, 8867, 8887, 8893, 8923, 8929, 8933, 8941, 8951, 8963, 8969, 8971, 8999, 9001, 9007, 9011, 9013, 9029, 9041, 9043, 9049, 9059, 9067, 9091, 9103, 9109, 9127, 9133, 9137, 9151, 9157, 9161, 9173, 9181, 9187, 9199, 9203, 9209, 9221, 9227, 9239, 9241, 9257, 9277, 9281, 9283, 9293, 9311, 9319, 9323, 9337, 9341, 9343, 9349, 9371, 9377, 9391, 9397, 9403, 9413, 9419, 9421, 9431, 9433, 9437, 9439, 9461, 9463, 9467, 9473, 9479, 9491, 9497, 9511, 9521, 9533, 9539, 9547, 9551, 9587, 9601, 9613, 9619, 9623, 9629, 9631, 9643, 9649, 9661, 9677, 9679, 9689, 9697, 9719, 9721, 9733, 9739, 9743, 9749, 9767, 9769, 9781, 9787, 9791, 9803, 9811, 9817, 9829, 9833, 9839, 9851, 9857, 9859, 9871, 9883, 9887, 9901, 9907, 9923, 9929, 9931, 9941, 9949, 9967, 9973]
                if n in smallprimes:
                    return True
                for sp in smallprimes:
                    if n%sp==0:
                        return False
                for i in range(smallprimes[-1], ceil(sqrt(n))+1, 2):
                    if n%i==0:
                        return False
                return True
            case 5:
                if len(cls.primes)<10000:
                    primes = [2]
                    for i in range(3,1_000_000,2):
                        for p in primes:
                            if i%p==0:
                                break
                            if p>ceil(sqrt(i))+1:
                                primes.append(i)
                                break
                        else:
                            primes.append(i)
                    cls.primes = primes
                if n in cls.primes:
                    return True
                for sp in cls.primes:
                    if n%sp==0:
                        return False
                for i in range(cls.primes[-1], ceil(sqrt(n))+1, 2):
                    if n%i==0:
                        return False
                return True
            case _:
                if n==2:
                    return True
                if n&1==0: # n の最下位ビットが0＝偶数
                    return False
                """powの実装
                def mp(base, power, mod):
                    result = 1
                    while power>0:
                        if power&1 == 1:
                            result = (result * base) % mod
                        base = (base * base) % mod
                        power >>= 1
                    return result
                """
                d = n-1
                while d&1 == 0:
                    d >>= 1
                for _ in range(20):
                    a = randint(1,n-1)
                    t = d
                    y = pow(a,t,n)
                    while t != n-1 and y != 1 and y != n-1:
                        y = (y * y) % n
                        t <<= 1
                    if y != n-1 and t&1 == 0:
                        return False
                return True    
    @staticmethod
    def generateprimesto(n:int):
        "generate prime numbers up to `n`"
        if n<=1:
            raise ValueError("`n` must be greater than 1")
        primes = [2]
        for i in range(3,n,2):
            for p in primes:
                if i%p==0:
                    break
                if p>ceil(sqrt(n))+1:
                    primes.append(i)
                    break
            else:
                primes.append(i)
        return primes
    @staticmethod
    def generateprimesby(n:int):
        "generate prime numbers `n`times"
        if n<=0:
            raise ValueError("`n` must be greater than 0")
        primes = [2]
        i = 3
        while len(primes)<n:
            for p in primes:
                if i%p==0:
                    break
                if p>ceil(sqrt(i))+1:
                    primes.append(i)
                    break
            else:
                primes.append(i)
            i+=2
        return primes
    
    @classmethod
    def pi(cls, selector:piCalcurator=piCalcurator.RAMANUJAN,N:int=10,*,ROOTS:int=10,LIMITS:int=0):
        if N<=0:
            raise ValueError("`N` must be greater than 0")
        pi = Fraction(0)
        match selector:
            case cls.piCalcurator.RAMANUJAN:
                sum = Fraction(1123,882)
                for i in range(1,N):
                    sum += Fraction((((-1)**i) * factorial(4*i) * (1123+21460*i)) , ((882**(2*i+1)) * (((4**i) * factorial(i))**4)))
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = Fraction(4*sum.denominator,sum.numerator)
            case cls.piCalcurator.MONTECARLO:
                x = [random() for _ in range(N)]
                y = [random() for _ in range(N)]
                counter = 0
                for i in range(N):
                    if dist((0,0),(x[i],y[i]))<=1:
                        counter += 1
                pi = Fraction(4 * counter, N)
            case cls.piCalcurator.LEIBNIZ:
                pi = Fraction(0)
                for i in range(N):
                    pi += Fraction(2,16*(i+1)*i+3)
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*4
            case cls.piCalcurator.TRAPEZOIDALRULE:
                h = Fraction(1,N)
                pi = Fraction(0)
                for i in range(N):
                    pi += (cls.f_root(1-(i*h)**2,ROOTS)+cls.f_root(1-(i*h+h)**2,ROOTS))*h/2
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*4
            case cls.piCalcurator.WALLISPRODUCT:
                pi = Fraction(2*2,1*3)
                for i in range(2,N+1):
                    pi *= Fraction(4*i*i,4*i*i-1)
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*2
            case cls.piCalcurator.RAMANUJAN1914:
                sum = Fraction(1103,1)
                for i in range(1,N):
                    sum += Fraction(factorial(4*i), (4**i*factorial(i))**4)*Fraction(1103+26390*i, 99**(4*i))
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = Fraction(2*cls.f_root(Fraction(2),ROOTS),9801)*sum
                pi = 1/pi
            case cls.piCalcurator.CHUDNOVSKY:
                A:int = 13591409
                B:int = 545140134
                C:int = 640320**3
                sum = Fraction(0)
                for i in range(N):
                    sum += Fraction(((-1)**i)*factorial(6*i), factorial(3*i)*((factorial(i))**3))*Fraction(A+B*i, C**i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = (12/cls.f_root(Fraction(C),ROOTS))*sum
                pi = 1/pi
            case cls.piCalcurator.BORWEIN:
                R61:Fraction = cls.f_root(61,ROOTS)
                A:Fraction = 1657145277365 + (212175710912*R61)
                B:Fraction = 107578229802750 + (13773980892672*R61)
                C:Fraction = (5280 * (236674+(30303*R61)))**3
                sum = Fraction(0)
                for i in range(N):
                    sum += Fraction(((-1)**i)*factorial(6*i), factorial(3*i)*((factorial(i))**3))*Fraction(A+B*i, C**i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = (12/cls.f_root(C.limit_denominator(LIMITS),ROOTS))*sum
                pi = 1/pi
            case cls.piCalcurator.GAUSSLEGENDRE:
                a = Fraction(1)
                b = 1/cls.f_root(Fraction(2),ROOTS)
                t = Fraction(1,4)
                p = Fraction(1)
                for i in range(N):
                    a,b,t,p = (a+b)/2, cls.f_root(a*b,ROOTS), t-p*(a-((a+b)/2))**2, 2*p
                    if LIMITS!=0:
                        a,b,t,p = a.limit_denominator(LIMITS), b.limit_denominator(LIMITS), t.limit_denominator(LIMITS), p.limit_denominator(LIMITS)
                pi = ((a + b) ** 2)/(4*t)
                pi = pi
            case cls.piCalcurator.EULER:
                sum = Fraction(1)
                for i in range(2,N+1):
                    sum += Fraction(1,i*i)
                    if LIMITS!=0:
                        sum = sum.limit_denominator(LIMITS)
                pi = sum*6
                pi = cls.f_root(pi,ROOTS)
            case cls.piCalcurator.BAILEYBORWEINPLOUFFE:
                # TODO: more efficient programming
                pi = Fraction(0)
                for i in range(N):
                    pi += Fraction(1,16**i)*(Fraction(4,8*i+1)-Fraction(2,8*i+4)-Fraction(1,8*i+5)-Fraction(1,8*i+6))
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi
            case cls.piCalcurator.BELLARD:
                # TODO: more efficient programming
                pi = Fraction(0)
                for i in range(N):
                    pi += Fraction((-1)**i,2**(10*i))*(-Fraction(2**5,4*i+1)-Fraction(1,4*i+3)+Fraction(2**8,10*i+1)-Fraction(2**6,10*i+3)-Fraction(2**2,10*i+5)-Fraction(2**2,10*i+7)+Fraction(1,10*i+9))
                    if LIMITS!=0:
                        pi = pi.limit_denominator(LIMITS)
                pi = pi*Fraction(1,2**6)
            case cls.piCalcurator.高野喜久雄:
                at49 = cls.arctan(Fraction(1,49),N)
                at57 = cls.arctan(Fraction(1,57),N)
                at239 = cls.arctan(Fraction(1,239),N)
                at110443 = cls.arctan(Fraction(1,110443),N)
                pi = 4*(12*at49 + 32*at57 - 5*at239 + 12*at110443)
            case _:
                pi = Fraction(pi)
        if LIMITS==0:
            return pi
        return pi.limit_denominator(LIMITS)
    
    @staticmethod
    def _BSm(a:Callable[[Fraction,int],Fraction],b:Callable[[Fraction,int],Fraction],p:Callable[[Fraction,int],Fraction],q:Callable[[Fraction,int],Fraction],x:Fraction,n:int):
        s = Fraction(0)
        for i in range(n):
            ans = a(x,i)/b(x,i)
            ansp = p(x,0)
            ansq = q(x,0)
            for j in range(1,i+1): # for [0,n] range function needs to be +1
                ansp *= p(x,j)
                ansq *= q(x,j)
            ans *= ansp/ansq
            s += ans
        return deepcopy(Fraction(s))
    
    @staticmethod
    def e(N:int=100):
        return sum([Fraction(1,factorial(i)) for i in range(N)])
    @classmethod
    def exp(cls, x:Fraction,N:int):
        def a(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def b(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def p(x:Fraction, n:int) -> Fraction: return Fraction(1) if n==0 else Fraction(x.numerator)
        def q(x:Fraction, n:int) -> Fraction: return Fraction(1) if n==0 else Fraction(n * x.denominator)
        return cls._BSm(a,b,p,q,x,N)

    @classmethod
    def lnp1(cls, x:Fraction,N:int):
        if x<-1:
            raise ValueError("`x` must be greater than or equal to -1")
        if x>1:
            raise ValueError("`x` must be less than or equal to 1") # Cannot be calculated for large values
        if not isinstance(x, Fraction):
            raise TypeError("`x` must be Fraction class. If you want to use other type variable, use `ln()`")
        def a(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def b(x:Fraction, n:int) -> Fraction: return Fraction(n+1)
        def p(x:Fraction, n:int) -> Fraction: return Fraction(x.numerator) if n==0 else Fraction(-1 * x.numerator)
        def q(x:Fraction, n:int) -> Fraction: return Fraction(x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    def ln(self, x:SupportsFloat,N:int):
        if x<=0 or 2<=x:
            raise ValueError("xの定義域は(0,2)です。")
        return self.lnp1(Fraction(x)-Fraction(1, 1),N)
    
    def log(self, x:Fraction,N:int, LIMITS:int=0):
        # TODO: function lnp1 can be used between -1<x<1 make this 0<x<inf
        if not isinstance(x, Fraction):
            raise TypeError("`x` must be Fraction class.")
        # 場合分けを行う
        # [1] log_eは定義域が(0,inf)なので、その外側はエラー
        if x<=0:
            raise ValueError("xの定義域は(0,inf)です。")
        # [2] (0,2)の場合はx-1をしてlnp1に渡す
        if 0<x and x<2:
            return self.lnp1(x-1, N)
        # [3] [2,?]の場合はln(x)=-ln(1/x)から求める。ln(x)はx=t+1としてt=x-1からln(1+t)=ln(1+x-1)よりlnp1にx-1を渡す
        #     つまり、2<=xに対してp,tが存在し、ln(x)=-ln(1/x)=-ln(p)=-ln(1+p-1)=-ln(1+t), p=1/x|t=p-1 => t=1/x-1
        #     したがって、ln(x)=-ln(1+ (1/x-1) )
        #     ここで、lnp1の精度を鑑みると、実際にはx=10^5程度までしか適切に演算できない
        #     よって、10<<xにおいては、log_2について考え、log_e(2)log_2(x)よりln(x)を求めるのが適する。
        if 2<=x<self.E**10:
            return -self.lnp1((1/x)-1, N)
        if self.E**10<=x:
            log2_x = Fraction(x.numerator.bit_length()-x.denominator.bit_length())
            for _ in range(N):
                #log2_x = log2_x - ((2**log2_x-x) / 2**log2_x)
                # ERROR!!! 2^log2_x = x, log2_x=log2_x-((x-x)/x)=log2_x-0 <- ???
                p2x = self.powBinFract(log2_x,N,LIMITS) if LIMITS>0 else self.powBinFract(log2_x,N)
                log2_x = log2_x - ((p2x-x)/(p2x))
                if LIMITS>0:
                    log2_x = log2_x.limit_denominator(LIMITS)
                print(p2x,"\n",log2_x)
            return -self.lnp1(Fraction(-1,2), N)*log2_x
        return None

    @classmethod
    def sin(cls, x:Fraction,N:int):
        def a(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def b(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def p(x:Fraction, n:int) -> Fraction: return Fraction(x.numerator) if n==0 else Fraction(-x.numerator*x.numerator)
        def q(x:Fraction, n:int) -> Fraction: return Fraction(x.denominator) if n==0 else Fraction(2*n*(2*n+1) * x.denominator*x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    @classmethod
    def cos(cls, x:Fraction,N:int):
        def a(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def b(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def p(x:Fraction, n:int) -> Fraction: return Fraction(1) if n==0 else Fraction(-x.numerator*x.numerator)
        def q(x:Fraction, n:int) -> Fraction: return Fraction(1) if n==0 else Fraction(2*n*(2*n-1) * x.denominator*x.denominator)
        return cls._BSm(a,b,p,q,x,N)
    @classmethod
    def arctan(cls, x:Fraction,N:int):
        def a(x:Fraction, n:int) -> Fraction: return Fraction(1)
        def b(x:Fraction, n:int) -> Fraction: return Fraction(2*n+1)
        def p(x:Fraction, n:int) -> Fraction: return x if n==0 else -x*x
        def q(x:Fraction, n:int) -> Fraction: return Fraction(1)
        return cls._BSm(a,b,p,q,x,N)

    @staticmethod
    def epsilon(t:int|float|Decimal|Fraction|SupportsFloat, c:int|float|Decimal|Fraction|SupportsFloat):
        "`t` is test value, `c` is calcurated value"
        if type(t)!=type(c):
            raise TypeError(f"Object type is not same, t:{type(t)} and c:{type(c)} was given")
        match t:
            case int():
                return (int(t) - int(c))/int(c)
            case float():
                return (float(t) - float(c))/float(c)
            case Decimal():
                return (Decimal(t) - Decimal(c))/Decimal(c)
            case Fraction():
                return (Fraction(t) - Fraction(c))/Fraction(c)
            case _:
                return (t-c)/c
        return (t-c)/c
    
    @staticmethod
    def epsilon_selector(t:str, c:str, tp:str):
        match str(tp).lower():
            case "int"|"integer":
                return (int(t) - int(c))/int(c)
            case "float"|"double":
                return (float(t) - float(c))/float(c)
            case "decimal"|"dec"|"deci"|"d":
                return (Decimal(t) - Decimal(c))/Decimal(c)
            case "fraction"|"frac"|"fract"|"f":
                return (Fraction(t) - Fraction(c))/Fraction(c)
            case _:
                raise ValueError("idk y u raise Exception")