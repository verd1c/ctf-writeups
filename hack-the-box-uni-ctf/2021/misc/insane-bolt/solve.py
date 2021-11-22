from pwn import *

PLAYER = b'\xf0\x9f\xa4\x96'
FIRE = b'\xf0\x9f\x94\xa5'
MINE = b'\xe2\x98\xa0\xef\xb8\x8f'
WRENCH = b'\xf0\x9f\x94\xa9'
DIAMOND = b'\xf0\x9f\x92\x8e'


conn = remote('167.172.51.245', '30766')

print(conn.recvuntil('> '))

conn.send(b'2\n')

diamonds = 0
wrenches = 0

while True:
    given = conn.recvuntil('> ')


    game_parse = []
    lines = given.split(b'\n')
    initX = 0
    initY = 0
    i = -1
    j = 0
    for l in lines:
        ll = ''
        line = []
        emojis = l.split(b' ')
        j = 0
        for e in emojis:
            if e == FIRE:
                line.append('F')
            elif e == MINE:
                line.append('B')
            elif e == WRENCH:
                line.append('W')
            elif e == PLAYER:
                line.append('P')
                initX = j
                initY = i
            elif e == DIAMOND:
                line.append('D')
            else:
                j = j - 1
            j = j + 1
        game_parse.append(line)
        i = i + 1

    game = [x for x in game_parse if x != []]
    for l in game:
        ll = ''
        for e in l:
            ll = ll + e + ' '
        print(ll)

    sol = []
    print('MaxX : ' + str(len(game[0])) + ' MaxY: ' + str(len(game)))

    def solve(G, curX, curY, orig, path):
        if curX < 0 or curX >= len(G[0]) or curY < 0 or curY >= len(G):
            return 9999
        cur = G[curY][curX]
        if cur == 'F' or cur == 'B':
            return 9999

        if cur == 'D':
            sol.append(path)
            return 0

        left = 9999
        right = 9999
        down = 9999
        if orig != 'l':
            left = solve(G, curX - 1, curY, 'r', path + 'L')
        if orig != 'r':
            right = solve(G, curX + 1, curY, 'l', path + 'R')
        down = solve(G, curX, curY + 1, 'u', path + 'D')
        return min(left, right, down) + 1


    minpath = solve(game, initX, initY, 'u', '')
    print(sol)
    conn.sendline(sol[0])

    diamonds = diamonds + 1
    wrenches = wrenches + minpath
    if diamonds >= 500 and wrenches >= 5000:
        break


    print(conn.recvline())
    print(conn.recvline())

conn.interactive()