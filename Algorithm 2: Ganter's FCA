from concepts import Context
from itertools import combinations
import numpy as np

concept = Context.fromstring('''
               |bookable|rentable|driveable|rideable|joinable|
    hotel      |  X     |        |         |        |        |
    apartment  |  X     |  X     |         |        |        |
    car        |  X     |  X     |    X    |        |        |
    bike       |  X     |  X     |    X    |     X  |        |
    excursion  |  X     |        |         |        |  X     |
    trip       |  X     |        |         |        |  X     |
    ''')

o = ()
c = ()

g = len(concept.objects)
print('Number of objects',g)
#print(concept.objects[2:3])

#arr = []*g
arr = np.asarray(concept.objects)
print('Objects are:')
for a in arr:
    print('\t',a)



#print(arr[0])

def intersect(a, b):
    return list(set(a) & set(b))
def union(a, b):
    return list(set(a) | set(b))

def O_XOR_G (o, concept, g):
    interOG = intersect(o,concept.objects)
    print('\n', interOG)

    unionOGG = union(interOG, concept.objects[g:g+1])
    print(unionOGG)

    unionOGG_dash = concept.intension(list(unionOGG))
    print(unionOGG_dash)

    unionOGG_ddash = concept.extension(list(unionOGG_dash))
    print(unionOGG_ddash)

    o_xor_g = unionOGG_ddash
    #print(o_xor_g)
    return o_xor_g

def O_XOR_G_DASH (o_xor_g):
    o_xor_g_dash = concept.intension(list(o_xor_g))
    return o_xor_g_dash

#def lectic_small  

while(True):
    changed = False
    for g in range(g-1, -1, -1):
        print(g , 'element is ',arr[g])
        if (changed == False):
            oxg = (O_XOR_G(o,concept, g))
            c +=(oxg, (O_XOR_G_DASH(oxg)))
            o = O_XOR_G(o, concept, g)
            changed = True
            print('c = ',c)
            print('o = ',o)
        for g1 in range(0,g):
            print('\t' ,arr[g1])
            break

#g_set = set(concept.objects)
#print('\n', g_set)



#print(O_XOR_G(o, concept))


    


