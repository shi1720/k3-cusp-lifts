"""Reproduce exact audits, deterministic datasets and descriptive benchmarks."""
import sys,json,csv,random,time,platform,statistics,copy,hashlib
from pathlib import Path
from math import gcd,isqrt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cusp_lifts import certificate,labels,threshold,height,exact_fixed_z
from verify import verify
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
summary={'python':sys.version,'platform':platform.platform(),'seed':6052026}
rows=[]; total=0
start=time.perf_counter()
with (OUT/'certificates.jsonl').open('w') as f:
 for d in range(1,4097):
  expected={k for k in range(2*d) if k*k%(4*d)==0}
  got=set()
  for m,a in labels(d):
   C=certificate(d,m,a)
   assert verify(C),(d,m,a)
   got.add((2*d*a//m)%(2*d))
   total+=1
   f.write(json.dumps(C,separators=(',',':'))+'\n')
   rows.append([d,m,a,C['S'],height(C['seed']),height(C['c'])])
  assert got==expected,d
summary.update(atlas_degrees=4096,atlas_certificates=total,atlas_seconds=time.perf_counter()-start)
# Independent chart optimization: free x,y and solve w=S-x*y.
for S in range(1025):
 B=isqrt(S)+2
 direct=min(max(1,abs(x),abs(y),abs(S-x*y)) for x in range(-B,B+1) for y in range(-B,B+1))
 assert direct==threshold(S),(S,direct)
summary['independent_chart_cases']=1025
# Independently enumerate all four normalized coordinates (product table).
exact=[]
for S in range(1,1025):
 H,v=exact_fixed_z(9*S,3,1)
 C=certificate(9*S,3,1)
 assert verify(C)
 assert 2*(H//3)**2>=S and H<=height(C['c'])
 exact.append([S,height(C['c'])//3,H//3,*v])
summary['unrestricted_fixed_z_cases']=1024
# Asymptotically tight explicit family, with an independent lower bound.
family=[]
for k in range(2,1001):
 S=k*(2*k-1)
 C=certificate(9*S,3,1)
 v=[3*k,3*k,3*(k-1),3*k,1]
 assert sum([v[0]*v[1],v[2]*v[3],-9*S*v[4]**2])==0
 assert gcd(gcd(gcd(v[0],v[1]),gcd(v[2],v[3])),18*S)==3
 assert 2*(k-1)**2<S
 family.append([k,S,C['T'],k,C['T']/k])
summary['sharp_family_cases']=999
# Larger integer certificates, no floating square roots or factorization.
rng=random.Random(summary['seed']); stress=[]
for i in range(500):
 m=rng.randrange(2,250)
 a=rng.randrange(1,m)
 while gcd(a,m)!=1:a=rng.randrange(1,m)
 D=rng.getrandbits(256)+1
 C=certificate(m*m*D,m,a)
 assert verify(C)
 stress.append(C)
summary['large_integer_cases']=500
(OUT/'stress_certificates.jsonl').write_text(''.join(json.dumps(C,separators=(',',':'))+'\n' for C in stress))
# Meaningful rejection checks: norm, label, divisibility, saturation, isometry.
base=certificate(819,3,1); mutations=[]
for key,index in [('c',0),('c',4),('kernel_basis',None),('Q',None)]:
 C=copy.deepcopy(base)
 if key=='kernel_basis':C[key][1]=[2*x for x in C[key][1]]
 elif key=='Q':C[key][0][0]+=1
 else:C[key][index]+=1
 assert not verify(C)
 mutations.append(key)
C=copy.deepcopy(base);C['m']=6
assert not verify(C);mutations.append('m')
summary['rejected_mutations']=len(mutations)
# Separate producer/verifier timings; repeated calls are not independent observations.
bench=[]
for bits in [16,64,128,256,512,1024]:
 Ds=[rng.getrandbits(bits)|(1<<(bits-1)) for _ in range(40)]
 cs=[]; prod=[]; ver=[]
 for D in Ds:
  t=time.perf_counter_ns();C=certificate(49*D,7,3);prod.append(time.perf_counter_ns()-t)
  t=time.perf_counter_ns();ok=verify(C);ver.append(time.perf_counter_ns()-t)
  assert ok
 bench.append([bits,40,statistics.median(prod)/1000,statistics.median(ver)/1000])
for filename,header,data in [('atlas.csv',['d','m','a','S','seed_height','chart_height'],rows),('exact.csv',['S','chart_T','opt_T','x1','y1','x2','y2','z'],exact),('sharp_family.csv',['k','S','chart_T','opt_T','ratio'],family),('timing.csv',['D_bits','n','producer_median_us','verifier_median_us'],bench)]:
 with (OUT/filename).open('w') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(data)
nontrivial=[r for r in rows if r[1]>1]
ratios=[r[4]/r[5] for r in nontrivial]
summary.update(nontrivial_labels=len(nontrivial),strict_reductions=sum(r[4]>r[5] for r in nontrivial),median_height_reduction=statistics.median(ratios),max_height_reduction=max(ratios),max_small_chart_to_opt_ratio=max(r[1]/r[2] for r in exact),benchmark=bench)
summary['result_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*') if p.name!='summary.json'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
