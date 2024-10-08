from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def create_cube(w, d, h, x, y, z, ax, op, face_color):
    """Create a 3D cube on a given axes."""
    # Define corners of the cube
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

    # Define faces of the cube 
    faces = [
        [corners[0], corners[1], corners[2], corners[3]],
        [corners[4], corners[5], corners[6], corners[7]],
        [corners[0], corners[1], corners[5], corners[4]],
        [corners[2], corners[3], corners[7], corners[6]],
        [corners[1], corners[2], corners[6], corners[5]],
        [corners[0], corners[3], corners[7], corners[4]]
    ]

    # Add the cube to the axes
    ax.add_collection3d(Poly3DCollection(faces, facecolors=[face_color]*6, linewidths=1, edgecolors='black', alpha=op))

    return ax

def visualize_3D_boxList(container, boxList, colors_dict):
    """Visualize a list of 3D boxes in a container."""
    W, D, H = container.get_W(), container.get_D(), container.get_H()
    
    # Create figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Set axes limits and labels
    l = max(W, D, H)
    ax.auto_scale_xyz([0, l], [0, l], [0, l])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Create container
    ax = create_cube(W, D, H, 0, 0, 0, ax, 0, (0, 0, 0))

    # Create each box
    for i, box in enumerate(boxList):
        ax = create_cube(box.get_w(), box.get_d(), box.get_h(), box.get_x(), box.get_y(), box.get_z(), ax, 0.9, colors_dict[box.get_id()])
        plt.show(block=False)
        plt.pause(0.5)
        # if i < len(boxList) - 1:
        #     input("Press Enter to add the next box...")
        # else:
        plt.waitforbuttonpress()
        if i == len(boxList) - 1:
            plt.close()

    # Show plot
    plt.show()