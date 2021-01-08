import random


class Calculation:
    @classmethod
    def _miller_rabin(cls, n: int, k: int = 100) -> bool:
        if n == 2 or n == 3:
            return True
        if not n & 1 or n <= 1:
            return False

        def _check(input_a: int, input_s: int, input_d: int, input_n: int) -> int:
            x = pow(input_a, input_d, input_n)
            if x == 1:
                return True
            for _ in range(input_s - 1):  # O(N)
                if x == input_n - 1:
                    return True
                x = pow(x, 2, input_n)
            return x == input_n - 1

        s = 0
        d = n - 1

        while d % 2 == 0:
            d >>= 1
            s += 1

        for _ in range(k):
            a = random.randint(2, n - 2)
            if not _check(a, s, d, n):
                return False
        return True

    @classmethod
    def next_prime(cls, i: int, k: int = 10) -> int:
        while not cls._miller_rabin(i, k):
            i += 1
        return i

    @classmethod
    def sel_key(cls, ls, key):
        sel = ""

        for s in ls:
            s = s.replace(" ", "")
            s = s.replace("\t", "")
            key_x = key + '="'
            sel = ""

            if s.find(key_x) > -1:
                ai = s.find(key_x)
                bi = s.rfind('"')
                sel = s[ai + len(key_x): bi]
                break
        if not sel == "":
            try:
                sel = int(sel)  # "ab123123"
            except ValueError:
                pass
        return sel

    @classmethod
    def calc_q(cls, k: int) -> int:
        q = 2 * (k // 2) + 1
        while True:
            if cls._miller_rabin(q, 5):
                p = 2 * q + 1
                if cls._miller_rabin(p, 5) and cls._miller_rabin(q, 150) and cls._miller_rabin(p, 150):
                    break
            q += 2
        return q

    @classmethod
    def calc_g(cls, q: int) -> int:
        p = 2 * q + 1
        g = random.randint(q // 10, 2 * q)
        while pow(g, q, p) == 1:
            g = random.randint(q // 10, 2 * q)
        return g
