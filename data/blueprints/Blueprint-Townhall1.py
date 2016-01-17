blueprint = []

h = 10
w = 8
ID = 1

roofSize = 3
for wi in range(w+1):
    blueprint.append((0,wi,5,6))
    
for hi in range(1,4):
    for wi in range(1,w):
        blueprint.append((hi,wi,16,8))

blueprint.append((hi,0,20,10))
blueprint.append((hi,w,20,10))

for hi in range(4,h-roofSize):
    blueprint.append((hi,0,5,6))
    for wi in range(1,w):
        blueprint.append((hi,wi,16,8))
    blueprint.append((hi,wi+1,5,6))

off = 2
for roof in range(hi+1,h):
    for wi in range(off//2,(w- (off//2)) + 1):
        blueprint.append((roof,wi,5,6))
    off += 2
