from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'paper/manuscript/figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
def save(fig,name):
 fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight');fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(10,1.8));ax.set_xlim(0,10);ax.set_ylim(0,2);ax.axis('off')
texts=['Label (d, m, a)\nm² divides d','Small integral lift\nexact chart height','Integral isometry\nP, Q in SL₂(Z)','Saturated kernel\nmaximal-minor check','Quotient lattice\nU + ⟨−2D⟩ + 2E₈(−1)']
for i,t in enumerate(texts):
 x=i*2+.02
 ax.add_patch(FancyBboxPatch((x,.65),1.75,.9,boxstyle='round,pad=0.09',facecolor='#edf3f8',edgecolor='#29567a'))
 ax.text(x+.875,1.1,t,ha='center',va='center',fontsize=8.2)
 if i<4:ax.annotate('',xy=(x+1.95,1.1),xytext=(x+1.78,1.1),arrowprops={'arrowstyle':'->','color':'#29567a'})
ax.text(5,.15,'Exact integer certificates accompany every stage; the two E₈(−1) factors are fixed.',ha='center',fontsize=9)
save(fig,'workflow')
rows=list(csv.DictReader((ROOT/'results/atlas.csv').open()))
non=[r for r in rows if int(r['m'])>1]
x=np.array([int(r['seed_height']) for r in non]);y=np.array([int(r['chart_height']) for r in non])
fig,axs=plt.subplots(1,2,figsize=(9.8,3.4))
axs[0].scatter(x,y,s=5,alpha=.25,color='#245d83',rasterized=True);axs[0].plot([1,max(x)],[1,max(x)],'--',color='#a44c35',lw=1,label='Equal height');axs[0].set(xscale='log',yscale='log',xlabel='Direct seed height',ylabel='Chart lift height');axs[0].legend(frameon=False,fontsize=8)
axs[1].hist(x/y,bins=32,color='#245d83',edgecolor='white');axs[1].set(xlabel='Direct seed / chart height',ylabel='Oriented nontrivial labels');axs[1].axvline(np.median(x/y),color='#a44c35',linestyle='--',label=f'Median {np.median(x/y):.2f}');axs[1].legend(frameon=False,fontsize=8)
fig.tight_layout();save(fig,'height_atlas')
ex=list(csv.DictReader((ROOT/'results/exact.csv').open()));family=list(csv.DictReader((ROOT/'results/sharp_family.csv').open()))
fig,axs=plt.subplots(1,2,figsize=(9.8,3.4))
axs[0].scatter([int(r['S']) for r in ex],[int(r['chart_T'])/int(r['opt_T']) for r in ex],s=7,color='#245d83',alpha=.55);axs[0].axhline(np.sqrt(2),ls='--',color='#a44c35');axs[0].set(xlabel='S = D a² (m = 3, a = 1)',ylabel='Chart / exact fixed-z minimum',ylim=(.97,1.48));axs[0].annotate('S=91: 10/7',xy=(91,10/7),xytext=(220,1.45),arrowprops={'arrowstyle':'->'},fontsize=8)
axs[1].plot([int(r['k']) for r in family],[float(r['ratio']) for r in family],lw=.9,color='#245d83');axs[1].axhline(np.sqrt(2),ls='--',color='#a44c35',label='√2');axs[1].set(xscale='log',xlabel='k in S = k(2k − 1)',ylabel='Chart / global five-coordinate minimum',ylim=(.97,1.48));axs[1].legend(frameon=False)
fig.tight_layout();save(fig,'optimality_gap')
