# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import ipaddress

# r2py:entity:ipFamily
def ip_family(ip_string):
    try:
        addr = ipaddress.ip_address(ip_string)
        if addr.version == 4:
            return 4
        elif addr.version == 6:
            return 6
    except ValueError:
        return -1

print(ip_family("127.0.0.1"))                # 4
# r2py:entity:ipFamily_1
print(ip_family("500.0.0.500"))              # -1
# r2py:entity:ipFamily_2
print(ip_family("500.0.0.500"))              # -1

# r2py:entity:ipFamily_3
print(ip_family("::"))                        # 6
# r2py:entity:ipFamily_4
print(ip_family("::1"))                       # 6
# r2py:entity:ipFamily_5
print(ip_family("fe80::1ff:fe23:4567:890a")) # 6