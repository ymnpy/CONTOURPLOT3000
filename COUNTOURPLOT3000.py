from pyNastran.op2.op2 import read_op2
from pyNastran.bdf.bdf import read_bdf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

def get_dispframe(bdf,op2,lcid,props):
    """
    bdf -> bdf object
    op2 -> op2 object
    lcid -> load case id
    props -> desired property ids
    """
    pid2eid=bdf.get_element_ids_dict_with_pids()
    df=op2.displacements[lcid].dataframe
    repo=[]

    for pid in props:
        for el in pid2eid[pid]:
            for nid in bdf.elements[el].nodes:
                x=bdf.nodes[nid].xyz[0]
                y=bdf.nodes[nid].xyz[1]
                z=bdf.nodes[nid].xyz[2]
                
                df_filter=df[df["NodeID"]==nid]
                dz=(float(df_filter.loc[:,"t3"])**2+\
                    float(df_filter.loc[:,"t2"])**2+\
                    float(df_filter.loc[:,"t1"])**2)**0.5
                
                repo.append((nid,x,y,z,dz))
       
    df_out=pd.DataFrame(repo,columns=["NID","X","Y","Z","DISP"])
    return df_out

def plot_contour(x,y,z,axis_off):
    """
    x -> first axis
    y -> second axis
    z -> desired field value
    axis_off -> offset value to fix visualization
    """
    plt.figure(figsize=(12,9), layout="constrained")
    contour=plt.tricontourf(x, y, z, levels=100, cmap='Spectral_r')
    plt.colorbar(contour).set_label(label=z.name,size=12,labelpad=10)
    a,b,c=min(x),np.mean(x),max(x) #assuming x > y
    plt.xlim([a,c])
    plt.ylim([a-b,c-b])
    plt.axis("off")
    plt.show()


if __name__=="__main__":
    path=r'C:/...'
    op2=read_op2(path,build_dataframe=True)
    path=r'C:/...'
    bdf=read_bdf(path,xref=False)

    given=[317,318,319]
    df=get_dispframe(bdf,op2,1,given)
    plot_contour(df["X"],df["Z"],df["DISP"],100)

