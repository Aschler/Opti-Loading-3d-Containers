import numpy as np 
cimport numpy as np
import matplotlib.pyplot as plt 
from utils import create_cube
import time, sys, random

cdef class Container:
    cdef int W, H, D, Wgt

    def __cinit__(self, int W, int H, int D, int Wgt):
        self.W = W
        self.H = H
        self.D = D
        self.Wgt = Wgt

    def __reduce__(self):
        # Retourne un tuple contenant une fonction de réduction et un tuple d'arguments
        return (self.__class__, (self.W, self.H, self.D, self.Wgt))
    
    # Méthode pour recréer l'objet Cython à partir de ses états
    @staticmethod
    cdef create_from_states(cls, W, H, D, Wgt):
        obj = cls.__new__(cls,W, H, D, Wgt)
        return obj

    cpdef int get_W(self):
        return self.W

    cpdef int get_H(self):
        return self.H

    cpdef int get_D(self):
        return self.D

    cpdef int get_Wgt(self):
        return self.Wgt

cdef class Corner:
    cdef int x, y, z, w, d, h

    def __cinit__(self, int x, int y, int z, int w, int d, int h):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.d = d
        self.h = h

    def __reduce__(self):
        return (self.__class__, (self.x, self.y, self.z, self.w, self.d, self.h))
    
    @staticmethod
    cdef create_from_states(cls, ty, x, y, z, w, d, h):
        obj = cls.__new__(cls, ty, x, y, z, w, d, h)
        return obj

    cpdef int get_x(self):
        return self.x
    cpdef int get_y(self):
        return self.y
    cpdef int get_z(self):
        return self.z
    cpdef int get_w(self):
        return self.w
    cpdef int get_h(self):
        return self.h
    cpdef int get_d(self):
        return self.d

    cpdef int test_loading_meters(self, solution, x,y,w,d):
        cdef int res
        res = max(solution.get_totalWidth(), x + w) + max(solution.get_totalDeep(), y + d)
        return res

    cpdef bint is_betterOnRight(self, solution, box):
        return (self.test_loading_meters(solution, box.get_x(), box.get_y(), box.get_w(), box.get_d()) 
            < self.test_loading_meters(solution, (self.x + self.w - box.get_w()), box.get_y(), box.get_w(), box.get_d()))

    cpdef bint is_betterWithRotation(self, solution, box):
        return ((max(solution.get_totalDeep(), box.get_y() + box.get_w()) + max(solution.get_totalWidth(), box.get_x() + box.get_d())) 
                < (max(solution.get_totalDeep(), box.get_y() + box.get_d())+ max(solution.get_totalWidth(), box.get_x() + box.get_w())))

cdef class Box:
    cdef int x, y, z, w, h, d, wgt, id
    cdef list centerPoint

    def __cinit__(self, int x, int y, int z, int w, int h, int d, int wgt, int id):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.wgt = wgt
        self.id = id
        self.centerPoint = [w // 2, d // 2]

    def __reduce__(self):
        # Retourne un tuple contenant la classe de l'objet et un tuple d'arguments
        return (self.__class__, (self.x, self.y, self.z, self.w, self.h, self.d, self.wgt, self.id))  # Remplacez attr1, attr2 par vos attributs nécessaires

    @staticmethod
    cdef create_from_states(cls, int x, int y, int z, int w, int h, int d, int wgt, int id):
        return Box(x, y, z, w, h, d, wgt, id)

    cpdef void set_x(self, int x):
        self.x = x
    cpdef void set_y(self, int y):
        self.y = y
    cpdef void set_z(self, int z):
        self.z = z
    
    cpdef void set_w(self, int w):
        self.w = w
    cpdef void set_h(self, int h):
        self.h = h
    cpdef void set_d(self, int d):
        self.d = d

    cpdef void set_centerPoint(self, list centerPoint):
        self.centerPoint = centerPoint

    cpdef int get_w(self):
        return self.w
    cpdef int get_d(self):
        return self.d
    cpdef int get_h(self):
        return self.h
    cpdef int get_x(self):
        return self.x
    cpdef int get_y(self):
        return self.y
    cpdef int get_z(self):
        return self.z
    cpdef int get_id(self):
        return self.id

    cpdef bint fitInCorner(self, corner) except *:
        cdef Corner c = <Corner>corner
        return (self.w <= c.w) and (self.d <= c.d) and (self.h <= c.h)

    cpdef bint possible_rotation(self, corner) except *:
        cdef Corner c = <Corner>corner
        return (self.w <= c.d) and (self.d <= c.w)


cdef class Instance:
    cdef int n
    cdef list boxList
    cdef Container container

    def __cinit__(self, int n, list w, list h, list d, list wgt, list ids, int W, int H, int D, int Wgt):
        self.n = n
        self.boxList = []
        self.container = Container(W, H, D, Wgt)

        cdef int i
        for i in range(n):
            self.boxList.append(Box(0, 0, 0, w[i], h[i], d[i], wgt[i], ids[i]))

    cpdef int get_n(self):
        return self.n

    cpdef list get_boxList(self):
        return self.boxList
    
    cpdef Container get_container(self):
        return self.container

    def init_example(cls):
        cdef int W = 2550
        cdef int H = 2700
        cdef int D = 3950
        cdef int Wgt = 30000

        cdef list w = []
        cdef list h = []
        cdef list d = []
        cdef list wgt = []
        cdef list ids = []
        for j in range(4): 
            d.append(900); w.append(620); h.append(1300); wgt.append(450); ids.append(1)
        for j in range(5): 
            d.append(860); w.append(570); h.append(1060); wgt.append(512); ids.append(2)
        for j in range(8): 
            d.append(970); w.append(600); h.append(1150); wgt.append(470); ids.append(3)
        for j in range(4): 
            d.append(910); w.append(590); h.append(1200); wgt.append(470); ids.append(4)
        for j in range(6): 
            d.append(1040); w.append(740); h.append(1260); wgt.append(710); ids.append(5)
        for j in range(4): 
            d.append(1040); w.append(740); h.append(1180); wgt.append(420); ids.append(6)
        for j in range(15): 
            d.append(600); w.append(800); h.append(500); wgt.append(195); ids.append(7)
        for j in range(7): 
            d.append(1200); w.append(1200); h.append(900); wgt.append(923); ids.append(8)
        for j in range(4): 
            d.append(1000); w.append(1000); h.append(800); wgt.append(870); ids.append(9)

        cdef int n = len(w)
        print(len(w),"-",n)
        return cls(n, w, h, d, wgt, ids, W, H, D, Wgt)

cdef class Solution:
    cdef int nTotalBox
    cdef Container container
    cdef int totalWeight
    cdef int totalHeight
    cdef int totalDeep
    cdef int totalWidth
    cdef list boxList
    cdef list cornerList
    cdef list coordonateCornerList
    cdef dict colors_dict
    cdef list gravityCenter
    cdef heightMatrix
    cdef weightMatrix

    def __cinit__(self, int n, Container container):
        self.nTotalBox = n
        self.container = container
        self.totalWeight = 0
        self.totalHeight = 0
        self.totalDeep = 0
        self.totalWidth = 0
        self.boxList = []
        self.heightMatrix = np.zeros((self.container.D, self.container.W), dtype=np.float64)
        self.weightMatrix = np.zeros((self.container.D, self.container.W), dtype=np.float64)
        self.cornerList = [Corner(
            x=0, y=0, z=0,
            w=self.container.W, d=self.container.D, h=self.container.H)]
        self.coordonateCornerList = []
        self.colors_dict = {} 

        self.gravityCenter = [np.array([0, 0], dtype=np.float64), 0]
        

    cpdef void set_heightMatrix(self, value):
        self.heightMatrix = value 
    
    cpdef void set_weightMatrix(self, value):
        self.weightMatrix = value 

    cpdef void set_totalWeight(self, value):
        self.totalWeight = value

    cpdef void set_totalHeight(self, value):
        self.totalHeight = value

    cpdef void set_totalDeep(self, value):
        self.totalDeep = value

    cpdef void set_totalWidth(self, value):
        self.totalWidth = value

    cpdef void set_boxList(self, value):
        self.boxList = value

    cpdef void set_cornerList(self, value):
        self.cornerList = value

    cpdef void set_coordonateCornerList(self, value):
        self.coordonateCornerList = value

    cpdef void set_colors_dict(self, value):
        self.colors_dict = value

    cpdef void set_gravityCenter(self, value):
        self.gravityCenter = value

    cpdef int get_totalWeight(self):
        return self.totalWeight

    cpdef int get_totalHeight(self):
        return self.totalHeight

    cpdef int get_totalDeep(self):
        return self.totalDeep

    cpdef int get_totalWidth(self):
        return self.totalWidth

    cpdef list get_boxList(self):
        return self.boxList

    cpdef list get_cornerList(self):
        return self.cornerList

    cpdef list get_coordonateCornerList(self):
        return self.coordonateCornerList

    cpdef dict get_colors_dict(self):
        return self.colors_dict

    cpdef list get_gravityCenter(self):
        return self.gravityCenter

    cpdef get_heightMatrix(self):
        return self.heightMatrix

    cpdef get_weightMatrix(self):
        return self.weightMatrix
    
    cpdef double evaluate(self) :
        return -len(self.boxList)
        return self.totalHeight * self.totalWidth * self.totalDeep
        cdef double[:] goodCenterPoint = np.array([self.container.W / 2, self.container.D / 2], dtype=float)
        cdef double[:] gravityCenterPoint = self.gravityCenter[0]
        return np.linalg.norm([goodCenterPoint[0] - gravityCenterPoint[0], goodCenterPoint[1] - gravityCenterPoint[1]])
    
    def __reduce__(self):
        return (self.__class__, (
            self.nTotalBox,
            self.container,
            self.totalWeight,
            self.totalHeight,
            self.totalDeep,
            self.totalWidth,
            self.heightMatrix,
            self.weightMatrix,
            self.cornerList,
            self.coordonateCornerList,
            self.colors_dict,
            self.gravityCenter,
            ))



    @staticmethod
    cdef create_from_states(cls,
        nTotalBox,
        container,
        totalWeight,
        totalHeight,
        totalDeep,
        totalWidth,
        heightMatrix,
        weightMatrix,
        cornerList,
        coordonateCornerList,
        colors_dict,
        gravityCenter,
    ):
        obj = cls.__new__(cls)
        obj.container = container
        obj.set_totalWeight(totalWeight)
        obj.set_totalHeight(totalHeight)
        obj.set_totalDeep(totalDeep)
        obj.set_totalWidth(totalWidth)
        obj.set_heightMatrix(heightMatrix)
        obj.set_weightMatrix(weightMatrix)
        obj.set_cornerList(cornerList)
        obj.set_coordonateCornerList(coordonateCornerList)
        obj.set_colors_dict(colors_dict)
        obj.set_gravityCenter(gravityCenter)
        return obj


    cdef void computeCorner(self, int x_start, int y_start):
        cdef int ground_level, w, d1, d2, d_min
        cdef int x_end, y_end
 
        ground_level = self.heightMatrix[y_start, x_start]
        w = 0
        d1 = 0
        d2 = 0
        d_min = self.container.D
        x_end = self.container.W 
        y_end = self.container.D

        while (x_start + w) < x_end and self.heightMatrix[y_start, x_start + w] == ground_level:
            w += 10
        
        while (y_start + d1) < y_end and self.heightMatrix[y_start + d1, x_start] == ground_level:
            d1 += 10

        new_start = x_start + w - 1
        while (y_start + d2) < y_end and self.heightMatrix[y_start + d2, new_start] == ground_level:
            d2 += 10
 
        d_min = min(d1, d2)
        self.cornerList.append(Corner(x_start, y_start, ground_level, w, d_min, self.container.H - ground_level))
        
    cdef void update_heightMatrix(self, Box box):
        cdef int x_start = box.x 
        cdef int x_end = x_start + box.w 
        cdef int y_start = box.y 
        cdef int y_end = y_start + box.d 
        cdef int height = box.z + box.h 

        self.heightMatrix[y_start:y_end,x_start:x_end] = max(height,self.heightMatrix[y_start,x_start])
        self.weightMatrix[y_start:y_end,x_start:x_end] += box.wgt

    cdef void recompute_cornerList(self):
        cdef int i, x, y
        self.cornerList = []

        for (x,y) in self.coordonateCornerList:
            if (y < self.container.D and x < self.container.W):
                self.computeCorner(x, y)  

    cpdef void add_box(self, Box box):
        cdef int x, y
        
        self.boxList.append(box)

        self.totalWeight += box.wgt
        self.totalDeep = max(self.totalDeep, box.y + box.d)
        self.totalWidth = max(self.totalWidth, box.x + box.w)
        self.totalHeight = max(self.totalHeight, box.z + box.h)

        self.gravityCenter[1] += box.wgt
        self.gravityCenter[0] = ((self.gravityCenter[0] * (self.gravityCenter[1] - box.wgt)) + (np.array(box.centerPoint) * box.wgt)) / self.gravityCenter[1]

        if box.id not in self.colors_dict:
            self.colors_dict[box.id] = (random.random(), random.random(), random.random())

        x = box.x
        y = box.y

        if (x,y) not in self.coordonateCornerList:
            self.coordonateCornerList.append((x,y))
        if (x + box.w,y) not in self.coordonateCornerList:
            self.coordonateCornerList.append((x + box.w,y))
        if (x,y + box.d) not in self.coordonateCornerList:
            self.coordonateCornerList.append((x,y + box.d))
        if (x + box.w,y + box.d) not in self.coordonateCornerList:
            self.coordonateCornerList.append((x + box.w,y + box.d))
        
        self.update_heightMatrix(box)
        self.recompute_cornerList()

    cpdef void vizualise_3D(self):
        cdef int W = self.container.W
        cdef int D = self.container.D
        cdef int H = self.container.H
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        cdef int l = max(W, D, H)
        ax.auto_scale_xyz([0, l], [0, l], [0, l])
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        for box in self.boxList:
            ax = create_cube(box.get_w(), box.get_d(), box.get_h(), box.get_x(), box.get_y(), box.get_z(), ax, 0.9, self.colors_dict[box.get_id()])

        ax = create_cube(W, D, H, 0, 0, 0, ax, 0, (0, 0, 0))

        plt.show()

    def __str__(self):
        cdef str result = "Solution:\n"
        cdef int nTotalBox = self.nTotalBox
        cdef int totalWeight = self.totalWeight
        cdef int containerWgt = self.container.Wgt
        cdef int len_boxList = len(self.boxList)

        result += "Total Boxes: {}\n".format(nTotalBox)
        result += "Total Weight: {}/{}\n".format(totalWeight, containerWgt)
        result += "Number of Boxes Taken: {}\n".format(len_boxList)

        return result

