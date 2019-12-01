
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


def addInverse(k):
    n = 2**16
    inv = n - k
    return inv

def multiplyInverse(a) : 
    m = (2**16) + 1
    g = gcd(a, m) 
      
    if (g != 1) : 
        print("Inverse doesn't exist") 
          
    else : 
        return power(a, m - 2, m)
      
def power(x, y, m) :       
    if (y == 0) : 
        return 1
          
    p = power(x, y // 2, m) % m 
    p = (p * p) % m 
  
    if(y % 2 == 0) : 
        return p  
    else :  
        return ((x * p) % m) 
  
def gcd(a, b) : 
    if (a == 0) : 
        return b 
          
    return gcd(b % a, a)


def invKeyGeneration(k):
    invk = k
    p = 0
    i = 48
    invk[i] = multiplyInverse(k[p])
    p = p + 1
    invk[i+1] = multiplyInverse(k[p])
    p = p + 1
    invk[i+2] = multiplyInverse(k[p])
    p = p + 1
    invk[i+3] = multiplyInverse(k[p])

    for r in range(7, 0, -1):
        i = r * 6
        invk[i+4] = k[p]
        p = p + 1
        invk[i+5] = k[p]
        p = p + 1
        invk[5]   = multiplyInverse(k[p])
        p = p + 1
        invk[i+2] = addInverse(k[p])
        p = p + 1
        invk[i+1] = addInverse(k[p])
        p = p + 1
        invk[i+3] = multiplyInverse(k[p])
        p = p + 1

    invk[4] = k[p]
    p = p + 1
    invk[5] = k[p]
    p = p + 1
    invk[0] = multiplyInverse(k[p])
    p = p + 1
    invk[1] = addInverse(k[p])
    p = p + 1
    invk[2] = addInverse(k[p])
    p = p + 1
    invk[3] = multiplyInverse(k[p])
    return invk



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
        print(hex(p))
    p = finalRound(p, sk[48], sk[49], sk[50], sk[51])
    return p

def decrypt(c, k):
    sk = keyGeneration(k)
    sk = invKeyGeneration(sk)
    for i in range(0, 8):
        p = round(p, sk[i*6], sk[i*6+1], sk[i*6+2],
                  sk[i*6+3], sk[i*6+4], sk[i*6+5])
        print(hex(p))
    p = finalRound(p, sk[48], sk[49], sk[50], sk[51])
    return p



cipher = encrypt(int(sys.argv[1], 16), int(sys.argv[2], 16))
print(hex(cipher))
