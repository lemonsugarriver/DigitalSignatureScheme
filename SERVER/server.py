#!/usr/bin/env python
import math
import random
import hashlib
import socket


def fastModularExponentiation(base, exponent, prime):  #快速模幂
	answer = base

	sizeofexp = int(math.floor(math.log(exponent, 2)) + 1)
	for i in range(sizeofexp-2, -1, -1):
		answer = (answer * answer) % prime
		if (exponent >> i) % 2 == 1:
			answer = (base * answer) % prime
	return answer


def primeFactorization(number): #素因子分解
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


def millerrabin(number, q, k, base):  #miller rabin
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


def moduloMultiplicativeInverse(alpha, p): #逆乘
	if gcd(alpha, p) != 1:
		return -1
	return fastModularExponentiation(alpha, p-2, p)


sock = socket.socket()
portnumber = input("Enter Port Number:")
hostname = socket.gethostname()
sock.bind((hostname, portnumber))

sock.listen(3)
connection, address = sock.accept()
publickey = connection.recv(8000)
p, q, alpha, y, hf = publickey.split(":")
print(int(p), int(q), int(alpha), int(y), hf)
p = int(p)
q = int(q)
alpha = int(alpha)
y = int(y)

print "P = ", p
print "Q = ", q
print "Alpha = ", alpha
print "Y = ", y


signedmsg = connection.recv(8000)
m, edash, edoubledash, sdash = signedmsg.split(":")
m = int(m)
edash = int(edash)
edoubledash = int(edoubledash)
sdash = int(sdash)

mbin = bin(m)
mbin = mbin[2:]


print "M = ", mbin
print "Edash = ", edash
print "Edoubledash = ", edoubledash
print "Sdash = ", sdash


modinvalpha = moduloMultiplicativeInverse(alpha, p)
yinv = moduloMultiplicativeInverse(y, p)
if sdash >= 0:
	rstar = (((fastModularExponentiation(yinv, edash, p)) * (fastModularExponentiation(alpha, sdash, p))) % p) % p
else:
	rstar = (((fastModularExponentiation(yinv, edash, p)) * (fastModularExponentiation(modinvalpha, -sdash, p))) % p) % p

rstarbin = bin(rstar)
rstarbin = rstarbin[2:]
rstarhash = int(hashlib.sha1(mbin+rstarbin).hexdigest(), 16)

print "Rstar = ", rstar
print "Rstar in binary = ", rstarbin
print "M || Rstar = ", mbin+rstarbin
print "Hash value = ", rstarhash
print("FI")
if rstarhash == edoubledash:
	connection.send("TRUE")
else:
	connection.send("FALSE")
