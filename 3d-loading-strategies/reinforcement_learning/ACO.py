import data_structures as ds
import matplotlib.pyplot as plt 

import numpy as np
import copy, random, math, time

def ant_colony(
    instance: ds.Instance, 
    maxIter : int,
    maxAnt : int,
    rE : float,
    rD : float,
        ) -> ds.Solution: 
    """
    This function implements the ant colony optimization algorithm to solve the given instance.
    
    Parameters:
    - instance: The instance of the problem to be solved.
    - maxIter: The maximum number of iterations.
    - maxAnt: The maximum number of ants.
    - rE: The evaporation rate for the pheromone.
    - rD: The deposition rate for the pheromone.
    
    Returns:
    - bestSolution_boxList: The list of boxes in the best solution found.
    - bestSolution_color_dict: The dictionary mapping box IDs to their corresponding colors in the best solution.
    - allZ: The list of objective function values for each iteration.
    - allBestZ: The list of best objective function values for each iteration.
    - bestZ: The best objective function value found.
    """
    bestZ = np.inf
    stepList = []
    n = instance.get_n()
    phi_box = np.full((n, n), 1/n)
    
    allZ = []
    allBestZ = []
    for i in range(maxIter):
        
        for ant in range(maxAnt):
            print("*",end="", flush=True)
            solution,stepList = generate_solution(instance,phi_box,i+1,maxIter)
            z = solution.evaluate()
            allZ.append(z)
            if z <= bestZ :
                bestZ = z
                bestStepList = list(stepList)
                bestSolution_boxList = copy.deepcopy(solution.get_boxList())
                bestSolution_color_dict = copy.deepcopy(solution.get_colors_dict())

        managePhi(n,phi_box,bestStepList,rE,rD)
        phi_box = normalize(phi_box)
        
    print()
    print(bestStepList)
    return bestSolution_boxList, bestSolution_color_dict, allZ, allBestZ, bestZ

def managePhi(n, phi_box, bestStepList, rE, rD):
    """
    This function manages the pheromone update for the ant colony optimization algorithm.
    
    Parameters:
    - n: The number of boxes.
    - phi_box: The pheromone matrix for the boxes.
    - bestStepList: The list of best steps taken by the ants.
    - rE: The evaporation rate for the pheromone.
    - rD: The deposition rate for the pheromone.
    """
    for i in range(n):
        # Evaporation of box pheromone
        phi_box[i] *= rE
        
        # Deposition of box pheromone for the best step taken
        phi_box[i, bestStepList[i][0]] /= rE
        phi_box[i, bestStepList[i][0]] *= rD
        
def normalize(phi):
    """
    Normalize the input matrix phi by dividing each element by the sum of its corresponding row.

    Parameters:
    phi (numpy.ndarray): The input matrix to be normalized.

    Returns:
    numpy.ndarray: The normalized matrix.
    """
    # Calculate the sum of each row
    sum_lines = np.sum(phi, axis=1, keepdims=True)

    # Divide each element by the sum of its corresponding row
    phi = phi / sum_lines
    return phi

def generate_solution(
    instance, phi_box, iter, maxIter
        ) -> ds.Solution:
    """
    This function generates a solution using the ant colony optimization algorithm.
    
    Parameters:
    - instance: The instance of the problem.
    - phi_box: The pheromone matrix for the boxes.
    - iter: The current iteration number.
    - maxIter: The maximum number of iterations.
    
    Returns:
    - solution: The generated solution.
    - stepList: The list of steps taken by the ants.
    """
    temp_phi = copy.copy(phi_box)
    stepList = []
    solution = ds.Solution(instance.get_n(), instance.get_container())
    boxList = list(instance.get_boxList())
    
    P = math.log10(iter) / math.log10(maxIter)

    for i in range(instance.get_n()):
    
        isRandom = random.random() > P
        step = next_step(temp_phi[i], isRandom)
    
        newBox = boxList[step[0]]
        temp_phi[i+1:, step[0]] = 0   
        temp_phi = normalize(temp_phi)

        isPossible, isRight = compute_position(newBox, solution)
        step.append(isPossible)
        step.append(isRight)
        stepList.append(step)
        if isPossible:
            solution.add_box(newBox)

    return solution, stepList

def next_step(
    phi_box,
    isRandom
) :
    step = []
    box_index = choose_box(phi_box, isRandom)
    step.append(box_index)
    return step


def choose_box(
    phi_box : list, 
    isRandom : bool):
    """
    Choose a box based on the given probabilities.

    Parameters:
    phi_box (list): A list of probabilities for each box.
    isRandom (bool): If True, choose a box randomly based on the probabilities. 
                     If False, choose the box with the highest probability.

    Returns:
    int: The index of the chosen box.

    """
    if isRandom:
        prob_cumulatives = [sum(phi_box[:i+1]) for i in range(len(phi_box))]
        rand_num = random.random()

        for i, prob_cumulative in enumerate(prob_cumulatives):
            if rand_num <= prob_cumulative:
                return i
    else:
        return np.argmax(phi_box)




def compute_position(
    box: ds.Box,
    solution: ds.Solution,
) -> bool:
    """
    Computes the position of a box within a solution by finding the best corner to place it.

    Parameters:
        box (ds.Box): The box to be positioned.
        solution (ds.Solution): The solution in which the box will be placed.

    Returns:
        tuple: A tuple containing two boolean values. The first value indicates whether a suitable position was found
        for the box, and the second value indicates whether the box was placed on the right side of the corner.

    """
    # Iterate over each corner in the solution
    for corner in solution.get_cornerList():

        if box.fitInCorner(corner):
            isRight = False
            if box.possible_rotation(corner) and corner.is_betterWithRotation(solution, box):
                # Rotate the box if it provides a better fit with rotation
                temp = box.get_w()
                box.set_w(box.get_d())
                box.set_d(temp)

            # Check if the box provides a better fit on the right side of the corner
            if corner.is_betterOnRight(solution, box) :#or True:
                # Set the position of the box on the right side of the corner
                box.set_x(corner.get_x())
                box.set_y(corner.get_y())
                box.set_z(corner.get_z())
                box.set_centerPoint([corner.get_x() + (box.get_w() / 2), corner.get_y() + (box.get_d() / 2)])
                isRight = True
            else:
                # Set the position of the box on the left side of the corner
                box.set_x(corner.get_x() + corner.get_w() - box.get_w())
                box.set_y(corner.get_y())
                box.set_z(corner.get_z())
                box.set_centerPoint([corner.get_x() + (box.get_w() / 2), corner.get_y() + (box.get_d() / 2)])

            return True, isRight

    return False, False