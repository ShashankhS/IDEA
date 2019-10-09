
import sys


def modAdd(a, b):
    return (a+b) % (2**16)


def modMultiply(a, b):
    return (a*b) % ((2**16) + 1)


def plainSplit(x):
    p1 = (x & (0xffff000000000000)) >> 48
    p2 = (x & (0x0000ffff00000000)) >> 32
    p3 = (x & (0x00000000ffff0000)) >> 16
    p4 = (x & (0x000000000000ffff))
    return p1, p2, p3, p4


def keyGeneration(k):
    key = []
    key.append(k)
    for i in range(0, 6):
        key.append(
            ((key[i] * (2 ** 25)) & 0xffffffffffffffffffffffffffffffff) + (key[i] >> 103))
    subkeys = []
    for sk in key:
        subkeys.append((sk & (0xffff0000000000000000000000000000)) >> 112)
        subkeys.append((sk & (0x0000ffff000000000000000000000000)) >> 96)
        subkeys.append((sk & (0x00000000ffff00000000000000000000)) >> 80)
        subkeys.append((sk & (0x000000000000ffff0000000000000000)) >> 64)
        subkeys.append((sk & (0x0000000000000000ffff000000000000)) >> 48)
        subkeys.append((sk & (0x00000000000000000000ffff00000000)) >> 32)
        subkeys.append((sk & (0x000000000000000000000000ffff0000)) >> 16)
        subkeys.append((sk & (0x0000000000000000000000000000ffff)))
    subkeys = subkeys[:-4]
    return subkeys


def round(p, k1, k2, k3, k4, k5, k6):
    p1, p2, p3, p4 = plainSplit(p)
    s1 = modMultiply(p1, k1)
    s2 = modAdd(p2, k2)
    s3 = modAdd(p3, k3)
    s4 = modMultiply(p4, k4)
    s5 = s1 ^ s3
    s6 = s2 ^ s4
    s7 = modMultiply(s5, k5)
    s8 = modAdd(s6, s7)
    s9 = modMultiply(s8, k6)
    s10 = modAdd(s7, s9)
    r1 = s1 ^ s9
    r2 = s3 ^ s9
    r3 = s2 ^ s10
    r4 = s4 ^ s10
    r = (r1 << 48) + (r2 << 32) + (r3 << 16) + r4
    return r


def finalRound(p, k1, k2, k3, k4):
    p1, p3, p2, p4 = plainSplit(p)
    r1 = modMultiply(p1, k1)
    r2 = modAdd(p2, k2)
    r3 = modAdd(p3, k3)
    r4 = modMultiply(p4, k4)
    r = (r1 << 48) + (r2 << 32) + (r3 << 16) + r4
    return r


def encrypt(p, k):
    sk = keyGeneration(k)
    for i in range(0, 8):
        p = round(p, sk[i*6], sk[i*6+1], sk[i*6+2],
                  sk[i*6+3], sk[i*6+4], sk[i*6+5])
    p = finalRound(p, sk[48], sk[49], sk[50], sk[51])
    return p


cipher = encrypt(ord(sys.argv[1]), ord(sys.argv[2]))
print(hex(cipher))
