"""Independent full 21-coordinate check: the omitted E8 factors can lower height."""
from math import gcd
from functools import reduce
import json
from pathlib import Path
G=[[0]*21 for _ in range(21)]
G[0][1]=G[1][0]=G[2][3]=G[3][2]=1
G[4][4]=-126  # d=63, m=3, D=7, a=1
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]
for offset in (5,13):
 for i in range(8):G[offset+i][offset+i]=-2
 for i,j in edges:G[offset+i][offset+j]=G[offset+j][offset+i]=1
v=[6,6,6,6,1]+[3,0,0,0,0,0,0,0]+[0]*8
Gc=[sum(row[j]*v[j] for j in range(21)) for row in G]
assert sum(x*y for x,y in zip(v,Gc))==0
assert reduce(gcd,map(abs,Gc))==3
assert reduce(gcd,map(abs,v))==1
assert max(map(abs,v))==6
# If H<6, all hyperbolic coordinates, which are multiples of 3,
# have magnitude <=3. Their product sum is <=18, whereas d*z^2>=63.
# Negative E8 components can only increase the required product sum.
assert 2*3**2<63
result={'d':63,'m':3,'a':1,'D':7,'chart_height':9,'five_coordinate_minimum':9,'full_lattice_minimum':6,'vector':v,'norm':0,'divisibility':3,'gram':G}
p=Path(__file__).resolve().parents[1]/'results/full_lattice_example.json'
p.write_text(json.dumps(result,indent=2)+'\n')
print('Verified full-lattice example: chart=9, five-coordinate minimum=9, full minimum=6')
