from data_structures import *
import copy
import sys

def greedy(instance:Instance, vizualisation : bool = False) -> Solution: 
    solution = Solution(instance,vizualisation)
    boxList = copy.deepcopy(instance.boxList)
    
    boxList = sorted(boxList, key= lambda box :  (box.id))

    while(boxList): 
        newBox = boxList[0]
        del boxList[0]
        isPossible = compute_position(newBox,solution)
        
        if isPossible:
            solution.add_box(newBox)
            print("*",end="")
            sys.stdout.flush()
            if vizualisation : solution.vizualise_3D_dynamic()

    return solution


def compute_position(
    box:Box,
    solution:Solution,
        ) -> bool:
    
    sorted_corner = sorted(solution.cornerList, key = lambda corner: (corner.y, corner.x))

    for corner in sorted_corner :
        if box.fitInCorner(corner) :
            if box.possible_rotation(corner) and corner.is_betterWithRotation(solution,box):
                temp = box.w
                box.w = box.d
                box.d = temp

            box.x = corner.x
            box.y = corner.y
            box.z = corner.z
            box.centerPoint = [corner.x + (box.w/2),corner.y + (box.d/2)]

            return True
    
    return False



