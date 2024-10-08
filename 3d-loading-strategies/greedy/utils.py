import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_cube(w,d,h, x,y,z, ax,op, face_color):
    # corners of the cube
    corners = [
        [x, y, z],
        [x + w, y, z],
        [x + w, y + d, z],
        [x, y + d, z],
        [x, y, z + h],
        [x + w, y, z + h],
        [x + w, y + d, z + h],
        [x, y + d, z + h]
    ]

    # faces of the cube 
    faces = [
        [corners[0], corners[1], corners[2], corners[3]],
        [corners[4], corners[5], corners[6], corners[7]],
        [corners[0], corners[1], corners[5], corners[4]],
        [corners[2], corners[3], corners[7], corners[6]],
        [corners[1], corners[2], corners[6], corners[5]],
        [corners[0], corners[3], corners[7], corners[4]]
    ]
    # color of the cube
    #face_color = colors_dict[cube_id]
    # display the cube
    ax.add_collection3d(Poly3DCollection(faces, facecolors=[face_color]*6, linewidths=1, edgecolors='black', alpha=op))
    # ax.add_collection3d(Poly3DCollection(faces, facecolors=[(random.random(), random.random(), random.random())]*6, linewidths=1, edgecolors='black', alpha=op))

    return ax
