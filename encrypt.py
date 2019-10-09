
def modadd(a, b):
    return (a+b) % (2**16)


def modmultiply(a, b):
    return (a*b) % ((2**16) + 1)


def plainsplit(x):
    p1 = (x & (0xffff000000000000)) >> 48
    p2 = (x & (0x0000ffff00000000)) >> 32
    p3 = (x & (0x00000000ffff0000)) >> 16
    p4 = (x & (0x000000000000ffff))
    return p1, p2, p3, p4


def round(p, k1, k2, k3, k4, k5, k6):
    p1, p2, p3, p4 = plainsplit(p)
    print(hex(p1), hex(p2), hex(p3), hex(p4))
    s1 = modmultiply(p1, k1)
    s2 = modadd(p2, k2)
    s3 = modadd(p3, k3)
    s4 = modmultiply(p4, k4)
    s5 = s1 ^ s3
    s6 = s2 ^ s4
    s7 = modmultiply(s5, k5)
    s8 = modadd(s6, s7)
    s9 = modmultiply(s8, k6)
    s10 = modadd(s7, s9)
    r1 = s1 ^ s9
    r3 = s3 ^ s9
    r2 = s2 ^ s10
    r4 = s4 ^ s10
    print(hex(r1), hex(r2), hex(r3), hex(r4))


round(0x05320a6414c819fa, 0x0064, 0x00c8, 0x012c, 0x0190, 0x01f4, 0x0258)
