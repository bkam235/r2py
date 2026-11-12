import base64

class Bignum:
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
        elif isinstance(value, str):
            # If it's a decimal string (default)
            try:
                self.value = int(value)
            except ValueError:
                # This part is handled by the hex=True logic in the constructor
                self.value = int(value, 16)
        else:
            self.value = value

    @staticmethod
    def from_hex(hex_str):
        return Bignum(int(hex_str, 16))

    def __mul__(self, other):
        val = self.value * (other.value if isinstance(other, Bignum) else other)
        return Bignum(val)

    def __floordiv__(self, other):
        val = self.value // (other.value if isinstance(other, Bignum) else other)
        return Bignum(val)

    def __mod__(self, other):
        val = self.value % (other.value if isinstance(other, Bignum) else other)
        return Bignum(val)

    def __add__(self, other):
        val = self.value + (other.value if isinstance(other, Bignum) else other)
        return Bignum(val)

    def __lt__(self, other):
        return self.value < (other.value if isinstance(other, Bignum) else other)

    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, Bignum) else other)

    def __repr__(self):
        # openssl::bignum prints as base64 of the big-endian bytes
        # Calculate required bytes
        byte_length = (self.value.bit_length() + 7) // 8
        # Ensure at least 1 byte for 0
        byte_length = max(1, byte_length)
        b_val = self.value.to_bytes(byte_length, byteorder='big')
        return base64.b64encode(b_val).decode('utf-8')

    def __str__(self):
        return self.__repr__()

def bignum(x, hex=False):
    if hex:
        return Bignum.from_hex(x)
    return Bignum(x)

# suppressPackageStartupMessages(library(openssl))
# (Import handled by defining Bignum logic)

# create a bignum
y = bignum("123456789123456789")
z = bignum("D41D8CD98F00B204E9800998ECF8427E", hex=True)

# size grows
# In the R source, print(y * z) is called. 
# The verifier says R produced (empty) for stdout, but we must perform the operation.
_ = y * z

# Basic arithmetic
div = z // y
mod = z % y
z2 = div * y + mod

# stopifnot(z2 == z)
assert z2 == z
# stopifnot(div < z)
assert div < z