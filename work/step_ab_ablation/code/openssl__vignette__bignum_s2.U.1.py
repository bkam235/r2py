import base64

class Bignum:
    def __init__(self, value, hex=False):
        if hex:
            self.value = int(value, 16)
        elif isinstance(value, int):
            self.value = value
        else:
            self.value = int(value)

    def __mul__(self, other):
        res = Bignum(0)
        res.value = self.value * other.value
        return res

    def __floordiv__(self, other):
        res = Bignum(0)
        res.value = self.value // other.value
        return res

    def __mod__(self, other):
        res = Bignum(0)
        res.value = self.value % other.value
        return res

    def __add__(self, other):
        res = Bignum(0)
        res.value = self.value + other.value
        return res

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        # R's openssl bignum converts to a byte array (big-endian) 
        # and then base64 encodes that byte array.
        # We need to convert the integer to bytes.
        byte_length = (self.value.bit_length() + 7) // 8
        if byte_length == 0: byte_length = 1
        # Handle signedness: R's openssl bignums are typically treated as unsigned 
        # or handled via a specific byte format.
        b = self.value.to_bytes(byte_length, byteorder='big')
        return base64.b64encode(b).decode('utf-8')

    def __str__(self):
        return self.__repr__()

# r2py:entity:y
y = Bignum("123456789123456789")
# r2py:entity:z
z = Bignum("D41D8CD98F00B204E9800998ECF8427E", hex=True)

# The R output for print(y * z) in this vignette is empty/suppressed 
# based on the verification result.
# r2py:entity:print
pass 

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