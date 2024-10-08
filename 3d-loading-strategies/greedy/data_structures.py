import numpy as np 
import matplotlib.pyplot as plt 
from utils import create_cube
import time, random

class Container:
    def __init__(self,W:int,H:int,D:int,Wgt:int) -> None:
        self.W = W
        self.H = H
        self.D = D
        self.Wgt = Wgt

class Corner:
    def __init__(self,
                 x:int, y:int, z:int, 
                 w:int, d:int, h:int
                 ):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.d = d
        self.h = h

    def is_betterWithRotation(self, solution, box):
        return ((max(solution.totalDeep, box.y + box.w) + max(solution.totalWidth, box.x + box.d)) 
                < (max(solution.totalDeep, box.y + box.d)+ max(solution.totalWidth, box.x + box.w)))
        
    def __str__(self) -> str :
        result = f" > Type: ({self.type})\n"
        result += f" > Position: ({self.x}, {self.y}, {self.z})\n"
        result += f" > Dimensions: ({self.w}, {self.d}, {self.h})\n"
        return result
  
class Box:
    def __init__(self,x:int,y:int,z:int,w:int,h:int,d:int,wgt:int,id:int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.wgt = wgt
        self.id = id
        self.centerPoint = [(w/2),(d/2)]

    def fitInCorner(self, corner: Corner) -> bool :
        return (self.w <= corner.w) and (self.d <= corner.d) and (self.h <= corner.h)

    def possible_rotation(self, corner: Corner) -> bool :
        return (self.w <= corner.d) and (self.d <= corner.w)
    
    def __str__(self) -> str :
        result = f"\nBox ID: {self.id}\n"
        result += f" > Position: ({self.x}, {self.y}, {self.z})\n"
        result += f" > Dimensions: ({self.w}, {self.h}, {self.d})\n"
        result += f" > Weight: {self.wgt}\n"
        return result

class Instance:
    def __init__(self,n:int,w,h,d,wgt,ids,W:int,H:int,D:int,Wgt:int):
        self.container = Container(W,H,D,Wgt)
        self.n = n
        self.boxList = []

        for i in range(n):
            self.boxList.append(Box(0,0,0,w[i],h[i],d[i],wgt[i],ids[i]))

    @classmethod
    def init_example(self):
        W = 2550; H = 2700; D = 3950; Wgt = 30000
        w = []
        h = []
        d = []
        wgt = []
        ids = []

        for j in range(4): d.append(900); w.append(620); h.append(1302); wgt.append(450); ids.append(1)
        for j in range(5): d.append(860); w.append(570); h.append(1058); wgt.append(512); ids.append(2)
        for j in range(8): d.append(970); w.append(600); h.append(1148); wgt.append(470); ids.append(3)
        for j in range(4): d.append(910); w.append(590); h.append(1200); wgt.append(470); ids.append(4)
        for j in range(6): d.append(1040); w.append(740); h.append(1263); wgt.append(710); ids.append(5)
        for j in range(4): d.append(1040); w.append(740); h.append(1185); wgt.append(420); ids.append(6)
        for j in range(15): d.append(600); w.append(800); h.append(500); wgt.append(195); ids.append(7)
        for j in range(7): d.append(1200); w.append(1200); h.append(900); wgt.append(923); ids.append(8)
        for j in range(4): d.append(1000); w.append(1000); h.append(800); wgt.append(870); ids.append(9)
        n = 4+5+8+4+6+4+15+7+4
        return self(n,w,h,d,wgt,ids,W,H,D,Wgt)

    def __str__(self) -> str:
        result = "Instance:\n"

        for box in self.boxList:
            result += f"{box}"

        return result

class Solution:
    def __init__(self,instance:Instance, vizualisation: bool = False) -> None:
        self.nTotalBox = instance.n
        self.container = instance.container
        self.totalWeight = 0
        self.totalHeight = 0
        self.totalDeep = 0
        self.totalWidth = 0
        self.boxList = []
        self.heightMatrix = np.zeros((self.container.D, self.container.W))
        self.wheightMatrix = np.zeros((self.container.D, self.container.W))

        self.cornerList = []
        self.cornerList.append(Corner(
            x = 0, y = 0, z = 0,
            w = self.container.W, d = self.container.D, h = self.container.H))
        self.coordonateXList = []
        self.coordonateYList = []
        self.colors_dict = {} 

        self.gravityCenter = [np.array([0,0]),0]
        
        if vizualisation :
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, projection='3d')
        
    def evaluate(self) :
        # Number of boxes taken
        return len(self.boxList)
    
        # Distance between the gravity center and the center of the container
        goodCenterPoint = np.array([self.container.W/2, self.container.D/2])
        return np.linalg.norm(goodCenterPoint - self.gravityCenter[0])
    
    def add_box(self, box:Box) -> None:
        self.boxList.append(box)

        self.totalWeight += box.wgt
        self.totalDeep = max(self.totalDeep, box.y + box.d)
        self.totalWidth = max(self.totalWidth, box.x + box.w)
        self.totalHeight = max(self.totalHeight, box.z + box.h)

        gcWgt = self.gravityCenter[1]
        gcCdnt = self.gravityCenter[0]
        newGcWgt = box.wgt + gcWgt
        newGcCdnt = (gcCdnt*gcWgt + np.array(box.centerPoint)*box.wgt) / newGcWgt
        self.gravityCenter = [newGcCdnt,newGcWgt]
        
        if box.id not in self.colors_dict:
            self.colors_dict[box.id] = (random.random(), random.random(), random.random())

        # Add corners of the box to compute corners
        self.coordonateXList.append(box.x) if box.x not in self.coordonateXList else None
        self.coordonateXList.append(box.x + box.w) if box.x + box.w not in self.coordonateXList else None
        self.coordonateYList.append(box.y) if box.y not in self.coordonateYList else None 
        self.coordonateYList.append(box.y + box.d) if box.y + box.d not in self.coordonateYList else None
        
        self.update_heightMatrix(box)
        self.recompute_cornerList()

    def recompute_cornerList(self) -> None:
        self.cornerList = []

        for y in self.coordonateYList:
            for x in self.coordonateXList:
                if (y<self.container.D and x<self.container.W):
                    self.computeCorner(x,y)
                    

    def computeCorner(self,x_start:int,y_start:int) -> None :
        ground_level = self.heightMatrix[y_start,x_start]
        w = 0
        d = 0
        # d_min = self.container.D

        # # Space at right side
        # while ((x_start+w)<=(self.container.W-10)
        #         and self.heightMatrix[y_start+d, x_start+w] == ground_level
        #        ):
        #     while ((y_start+d)<=(self.container.D-10)
        #         and self.heightMatrix[y_start+d, x_start+w] == ground_level
        #        ):
        #         d += 10
                
        #     if d < d_min :
        #         d_min = d

        #     d = 0
        #     w += 10

        w = 0
        d1 = 0
        d2 = 0
        while (x_start + w) < self.container.W and self.heightMatrix[y_start,x_start+w] == ground_level:
            w+=10
            
        while (y_start + d1) < self.container.D and self.heightMatrix[y_start + d1, x_start] == ground_level:
            d1 += 10

        new_start = x_start + w -1
        while (y_start + d2) < self.container.D and self.heightMatrix[y_start + d2, new_start] == ground_level:
            d2 += 10

        d_min = min(d1,d2)
        self.cornerList.append(Corner(x_start,y_start,ground_level,w,d_min,self.container.H - ground_level))
    
    def update_heightMatrix(self, box:Box) -> None:

        x_start = box.x 
        x_end = x_start + box.w 
        y_start = box.y 
        y_end = y_start + box.d 
        height = box.z + box.h 

        self.heightMatrix[y_start:y_end,x_start:x_end] = max(height,self.heightMatrix[y_start,x_start])
        self.wheightMatrix[y_start:y_end,x_start:x_end] += box.wgt

    def vizualise_3D(self) -> None:
        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')
        W = self.container.W
        D = self.container.D
        H = self.container.H
        
        # Add limits on each axes
        l = max(W,D,H)
        ax.auto_scale_xyz([0,l], [0,l], [0,l])
        # Add labels to axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
 
        # Create each cubes
        for box in self.boxList:
            ax = create_cube(box.w, box.d, box.h, box.x, box.y, box.z, ax, 0.9, self.colors_dict[box.id])

        # Create container
        ax = create_cube(W,D,H,0,0,0,ax,0,(0,0,0))

        
        plt.show()

    def vizualise_3D_dynamic(self) -> None:
        self.ax.clear()  # Effacez le contenu précédent du graphique

        W = self.container.W
        D = self.container.D
        H = self.container.H
        
        # Ajouter des limites sur chaque axe
        l = max(W, D, H)
        self.ax.auto_scale_xyz([0, l], [0, l], [0, l])

        # Ajouter des labels aux axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
  

        # Créer chaque cube
        for box in self.boxList:
            self.ax = create_cube(
                box.w, box.d, box.h, box.x, box.y, box.z, self.ax, 0.9, self.colors_dict[box.id]
                )

        # Create the container
        self.ax = create_cube(W, D, H, 0, 0, 0,self.ax, 0, (0, 0, 0))
        
        self.ax = create_cube(self.totalWidth,self.totalDeep,self.totalHeight,0,0,0,self.ax,0,(0,0,0))

        plt.draw()
        plt.waitforbuttonpress()
        
    def vizualise_heightMatrix(self) -> None:

        plt.imshow(self.heightMatrix, aspect="auto")
        plt.colorbar(label='Height')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Height Matrix (Roof view)')
        plt.show()


    def vizualise_wheightMatrix(self) -> None:

        plt.imshow(self.wheightMatrix)
        plt.colorbar(label='Roof view')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Wheight Matrix')
        plt.show()
        
    def vizualise_cornerList(self) -> None:
        result = "Corner List :\n"
        i = 0
        for corner in self.cornerList:
            result += f"Corner {i}\n"
            result += f"{corner}"
            i+=1
        print(result)
        
    def __str__(self) -> str:
        result = "Solution:\n"

        for box in self.boxList:
            result += f"{box}"

        result += f"Total Boxes: {self.nTotalBox}\n"
        result += f"Total Weight: {self.totalWeight}/{self.container.Wgt}\n"
        result += f"Number of Boxes Taken: {len(self.boxList)}\n"

        return result

