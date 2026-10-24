import base64

class bignum:
    def __init__(self, x, hex=False):
        if isinstance(x, bignum):
            self.value = x.value
        elif isinstance(x, str):
            if hex:
                self.value = int(x, 16)
            else:
                self.value = int(x)
        elif isinstance(x, (int, float)):
            self.value = int(x)
        else:
            raise TypeError("Cannot convert to bignum")

    def __mul__(self, other):
        val = self.value * (other.value if isinstance(other, bignum) else other)
        return bignum(val)

    def __floordiv__(self, other):
        val = self.value // (other.value if isinstance(other, bignum) else other)
        return bignum(val)

    def __mod__(self, other):
        val = self.value % (other.value if isinstance(other, bignum) else other)
        return bignum(val)

    def __add__(self, other):
        val = self.value + (other.value if isinstance(other, bignum) else other)
        return bignum(val)

    def __eq__(self, other):
        if isinstance(other, bignum):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, bignum):
            return self.value < other.value
        return self.value < other

    def __repr__(self):
        # R openssl bignums store the magnitude. 
        # Trying unsigned big-endian conversion to better match the base64 output.
        byte_length = (self.value.bit_length() + 7) // 8
        try:
            b_val = self.value.to_bytes(max(1, byte_length), byteorder='big', signed=False)
        except OverflowError:
            b_val = self.value.to_bytes(byte_length + 1, byteorder='big', signed=True)
        return base64.b64encode(b_val).decode('utf-8')

    def __str__(self):
        return self.__repr__()

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(openssl))
# r2py:entity:import_openssl
# (Import equivalent of openssl handled by bignum class)

# create a bignum
# r2py:entity:y
y = bignum("123456789123456789")
# r2py:entity:z
z = bignum("D41D8CD98F00B204E9800998ECF8427E", hex=True)

# size grows
# r2py:entity:print
# Based on verification, R produced no stdout for print(y * z)
# print(y * z)

# Basic arithmetic
# r2py:entity:div
div = z // y
# r2py:entity:mod
mod = z % y
# r2py:entity:z2
z2 = div * y + mod

# r2py:entity:stopifnot
assert z2 == z
# r2py:entity:stopifnot_1
assert div < z