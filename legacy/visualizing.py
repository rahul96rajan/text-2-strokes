# TODO: Generalize for lines

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

super_temp_dataset = np.load('./data/100samp/dataset.npy', allow_pickle=True)

line1 = super_temp_dataset[0]

# --> ANIMATION

fig = plt.figure(figsize=(10, 2))

stroke_len = line1.shape[0]

X_data = list()
Y_data = list()
# idx_counter = count()


def animation_frame(i):
    global X_data, Y_data
    print(i)
    if line1[i, 2] != 1:
        X_data.append(line1[i, 0])
        Y_data.append(-line1[i, 1])
    else:
        X_data.extend([None])
        Y_data.extend([None])

    plt.cla()
    plt.xlim([0, 50])
    plt.ylim([-3, 3])
    plt.axis('off')
    plt.plot(X_data, Y_data)


animation = FuncAnimation(fig, func=animation_frame,
                          frames=range(line1.shape[0]), interval=40)

animation.save('animation_writing.mp4')

plt.show()
