#!/usr/bin/env python
import math
import random
import hashlib
import socket


def fastModularExponentiation(base, exponent, prime):
	answer = base

	sizeofexp = int(math.floor(math.log(exponent, 2)) + 1)
	for i in range(sizeofexp-2, -1, -1):
		answer = (answer * answer) % prime
		if (exponent >> i) % 2 == 1:
			answer = (base * answer) % prime
	return answer


def primeFactorization(number):
	primefactors = []
	if number % 2 == 0:
		primefactors.append(2)
	while number % 2 == 0:
		number = number // 2
	for i in range(3, int(math.sqrt(number)) + 1):
		if number % i == 0:
			primefactors.append(i)
		while number % i == 0:
			number = number // i
	if number > 2:
		primefactors.append(number)
	return primefactors


def millerrabin(number, q, k, base):
	if fastModularExponentiation(base, q, number) == 1:
		return "inconclusive"
	for j in range(k):
		if fastModularExponentiation(base, (1 << j) * q, number) == (number-1):
			return "inconclusive"
	return "composite"


def isPrime(number):
	if number % 2 == 0:
		return "Not a Prime"
	k = 0
	q = 0
	for k in range(1, int(math.log(number-1, 2)) + 1):
		if (number-1) % (1 << k) == 0:
			q = (number-1) // (1 << k)
			if q % 2 == 1:
				break
	base = random.randint(2, 10000)
	base = base % (number-1)
	if base == 0:
		base = 2
	if millerrabin(number, q, k, base) == "composite":
		return "Not a Prime"
	else:
		return "Prime with High Probablity"


def gcd(a, b):
	if a == 0:
		return b
	return gcd(b % a, a)


def moduloMultiplicativeInverse(alpha, p):
	if gcd(alpha, p) != 1:
		return -1
	return fastModularExponentiation(alpha, p-2, p)


sock = socket.socket()
portnumber = input("Enter Port Number:")
hostname = socket.gethostname()
sock.connect((hostname, portnumber))

while True:
	testnumber = random.randint(10001, 100000000000)
	print("Testing on")
	print(testnumber)
	flag = 0
	for i in range(10):
		if isPrime(testnumber) == "Not a Prime":
			flag = 1
	if flag == 1:
		print("Not a Prime")
	else:
		print("Prime with High Prob")
		break
factorlist = primeFactorization(testnumber - 1)
q = factorlist[len(factorlist) - 1]
p = testnumber

g = random.randint(2, p-2)
alpha = 1
modinvalpha = 0
while alpha == 1:
	g = random.randint(2, p-2)
	alpha = fastModularExponentiation(g, (p-1) // q, p)
	modinvalpha = moduloMultiplicativeInverse(alpha, p)
	if modinvalpha == -1:
		alpha = 1
a = random.randint(1, q-1)
y = fastModularExponentiation(alpha, a, p)
print "P = ", p
print "Q = ", q
print "G = ", g
print "Alpha = ", alpha
print "Y = ", y
print "A = ", a
publickey = str(p) + ":" + str(q) + ":" + str(alpha) + ":" + str(y) + ":" + "SHA-1"
sock.send(publickey)


m = random.randint(1, 10000)
mbin = bin(m)
mbin = mbin[2:]


k = random.randint(1, q-1)
r = fastModularExponentiation(alpha, k, p)
rbin = bin(r)
rbin = rbin[2:]
mrbin = mbin + rbin

e = int(hashlib.sha1(mrbin).hexdigest(), 16)
s = (((a % q) * (e % q)) % q + k % q) % q

# v = 0
# e = 0
# edash = 1
# while edash != e - v:
u = random.randint(1, q-1)
v = random.randint(1, q-1)
rdash = ((r % p) * ((fastModularExponentiation(y, v, p)) * (fastModularExponentiation(modinvalpha, u, p))) % p) % p

rdashbin = bin(rdash)
rdashbin = rdashbin[2:]
mrdashbin = mbin + rdashbin
edoubledash = int(hashlib.sha1(mrdashbin).hexdigest(), 16)
sdash = s - u
edash = e - v

print "M = ", mbin
print "K = ", k
print "R = ", r
print "R in binary = ", rbin
print "M || R =", mrbin
print "S = ", s
print "E = ", e
print "U = ", u
print "V = ", v
print "Rdash = ", rdash
print "Rdash in binary = ", rdashbin
print "M || Rdash = ",  mrdashbin
print "Edash = ", edash
print "Edoubledash = ", edoubledash
print "Sdash = ", sdash

signedmsg = str(m) + ":" + str(edash) + ":" + str(edoubledash) + ":" + str(sdash)
sock.send(signedmsg)
result = sock.recv(10)
print "VERIFICATION STATUS : ", result
sock.close()
