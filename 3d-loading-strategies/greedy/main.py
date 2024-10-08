import numpy as np 
import time
from data_structures import *
from greedy import greedy

def create_instance(nb_boxes):
    d = np.array([10,30,20,20])
    w = np.array([20,20,20,20])
    h = np.array([30,20,40,40])
    wgt = np.array([10,10,10,10])
    ids = np.array([1,2,3,4])
    W = 60
    H = 60
    D = 70
    Wgt = 3000
    ##########################
    
    ########################## 
    return Instance(nb_boxes,w,h,d,wgt,ids,W,H,D,Wgt)


def main():
    # Choose an instance to solve
    instance = create_instance(nb_boxes=4)
        # or
    instance = Instance.init_example()

    vizualisation = True
    
    print("Solving instance :")
    print(" > ",end="")
    
    t = time.time()
    solution = greedy(instance, vizualisation)
    t = time.time() - t
    
    if not vizualisation :
        print("\nTotal time : ", t)
        
    solution.vizualise_3D()

main()
