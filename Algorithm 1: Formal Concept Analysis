from concepts import Context
from itertools import combinations

def FCA(concept):
	c = set()
	g = len(concept.objects)
	m = len(concept.properties)
	if(g<m):
		all_tuples = ()
		for idx in range(1,g):
			all_tuples += tuple(combinations(concept.objects,idx))
		for object_tuple in all_tuples:
			o_dash = concept.intension(list(object_tuple))
			o_ddash = concept.extension(list(o_dash)) 
			c.add((o_ddash,o_dash))
				
	else:
		all_tuples = ()
		for idx in range(1,m):
			all_tuples += tuple(combinations(concept.properties,idx))
		for attrib_tuple in all_tuples:
			a_dash = concept.extension(list(attrib_tuple))
			a_ddash = concept.intension(list(a_dash))
			c.add((a_dash,a_ddash))
			
	return c

formalContext = Context.fromstring('''
               |bookable|rentable|driveable|rideable|joinable|
    hotel      |  X     |        |         |        |        |
    apartment  |  X     |  X     |         |        |        |
    car        |  X     |  X     |    X    |        |        |
    bike       |  X     |  X     |    X    |     X  |        |
    excursion  |  X     |        |         |        |  X     |
    trip       |  X     |        |         |        |  X     |
    ''')
print(FCA(formalContext))
print('\n')
formalContext2 = Context.fromstring('''
               |bookable|rentable|driveable|rideable|joinable|
    
    apartment  |  X     |  X     |         |        |        |
    
    bike       |  X     |  X     |    X    |     X  |        |
    excursion  |  X     |        |         |        |  X     |
    trip       |  X     |        |         |        |  X     |
    ''')
print(FCA(formalContext2))

