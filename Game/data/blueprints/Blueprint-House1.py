blueprint = []
h = 7
w = 6
ID = 0

for wi in range(w+1):
    blueprint.append((0,wi,0,0))

for hi in range(1,h):
    blueprint.append((hi,0,0,0))
    for wi in range(1,w):
        blueprint.append((hi,wi,16,8))
    blueprint.append((hi,wi+1,0,0))

for wi in range(w+1):
    blueprint.append((hi+1,wi,0,0))
