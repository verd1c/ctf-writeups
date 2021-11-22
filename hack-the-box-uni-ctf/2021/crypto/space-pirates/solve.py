import base64
from Crypto import Random
from Crypto.Cipher import AES
from random import randint, randbytes,seed
from hashlib import md5
import math

def next_coeff(val):
	return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

def calc_coeffs(init_coeff, coeffs):
	for i in range(8):
		coeffs.append(next_coeff(coeffs[i]))

def rev_secret(init_coeff, init_x, init_y, p):
	coeffs = [init_coeff]
	calc_coeffs(init_coeff, coeffs)
	# init_y = (secret + coeffs[1] * init_x + coeffs[2] * init_x^1 + ... + coeffs[9] * init_x^9) % P
	sum = 0

	for i in range(len(coeffs)):
		init_y -= coeffs[i] * (init_x ** (i + 1))

	GCD = math.gcd(p, 1)
	secret = (GCD * (init_y)) % p
	return secret

secret = rev_secret(93526756371754197321930622219489764824, 21202245407317581090, 11086299714260406068, 92434467187580489687)

enc = '1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c'

seed(secret)
key = randbytes(16)
cipher = AES.new(key, AES.MODE_ECB)
enc_FLAG = cipher.decrypt(bytes.fromhex(enc)).decode("ascii")
print(enc_FLAG)