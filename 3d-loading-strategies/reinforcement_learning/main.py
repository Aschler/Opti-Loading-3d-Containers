import matplotlib.pyplot as plt 
import numpy as np 
import time
import data_structures as ds
from ACO import ant_colony
from utils import visualize_3D_boxList

def create_random_instance(nb_boxes):
    # Generate random dimensions and weights for boxes
    d = 10*np.random.randint(2, 5, nb_boxes)
    w = 10*np.random.randint(2, 5, nb_boxes)
    h = 10*np.random.randint(2, 5, nb_boxes)
    wgt = 10*np.random.randint(2, 5, nb_boxes)
    ids = np.random.randint(2, 5, nb_boxes)

    # Define container dimensions and weight
    W = 100
    H = 120
    D = 100
    Wgt = 3000

    return list(d),list(h),list(w),list(ids),list(wgt),D,H,W,Wgt

def main():
    """
    This program is an optimization algorithm of a loading strategie in 3-Dimensional Truck Containers based on an Ant Colony Algorithm
      To launch the program and choose the parameters use main(maxIter, maxAnt, rE, rD) :
        - maxIter : The number of iteration of maxAnt ants (10 by default)
        - maxAnt : The number of ant for each iteration (10 by default)
        - rE : Rate of evaporation of the pheromones after each iteration (0.8 by default)
        - rD : Rate of deposition of the pheromones after each iteration (1.2 by default)")
    """
    # Choose an instance to solve
    
    # instance = create_random_instance(nb_boxes = 50)
    instance = ds.Instance.init_example(ds.Instance)

    # Define parameters for reinforcement learning
    maxIter = 10
    maxAnt = 10
    rE = 0.8
    rD = 1.2

    print(f"Parameters :\n\t- maxIter = {maxIter}\n\t- maxAnt = {maxAnt}\n\t- rE = {rE}\n\t- rD = {rD}")
    # Run reinforcement learning and measure time
    t = time.time()
    solution_boxList, colors_dict, allZ, allBestZ, bestZ = ant_colony(instance,maxIter,maxAnt,rE,rD)
    print("----------------------------------------")
    print("bestZ = ", bestZ)
    print("total time = ", time.time() - t)

    # Visualize solution and plot evolution of best Z value
    visualize_3D_boxList(instance.get_container(),solution_boxList,colors_dict)
    plt.plot(range(len(allZ)), allZ, marker='o', linestyle='-')
    plt.title(f'Evolution of the Z value, Iterations = {maxIter}, Ants = {maxAnt}, rho_E = {rE}, rho_D = {rD}')
    plt.show()

main()