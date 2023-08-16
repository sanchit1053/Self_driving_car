actions = {
    0:0,
    1:1,
    2:2,
    4:3,
    6:4,
}

with open("data/cricket/mine_pol.txt", 'r') as f:
    for l in f.readlines():
        print(actions[int(l)])