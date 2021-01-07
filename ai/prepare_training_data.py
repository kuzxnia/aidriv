import numpy as np
import cv2
import time
import os


def concat_path(*paths):
    return os.path.join(*paths)


input_size = 120 * 320
base_path = concat_path(os.path.expanduser('~'), 'screens/')

# create labels
k = np.zeros((4, 4), 'float')
for i in range(4):
    k[i, i] = 1

direct = {
    'L_': k[0],
    'R_': k[1],
    'U_': k[2],
    'D_': k[3],
    'UL': k[0],
    'UR': k[1],
}


def collect():
    total = 0
    X = np.empty((0, input_size))
    y = np.empty((0, 4))

    for filename in os.listdir(base_path):
        path = concat_path(base_path, filename)
        if not os.path.isfile(path):
            continue

        print('reading image' + path)
        image = cv2.imread(path, 0)
        height, width = image.shape

        print(height, width)
        cv2.imshow('image', image)

        # reshape the roi image into a vector
        temp_array = image.reshape(1, input_size).astype(np.float32)

        X = np.vstack((X, temp_array))
        y = np.vstack((y, direct[filename[:2]]))
        total += 1

    # save data as a numpy file
    file_name = str(int(time.time()))
    directory = "training_data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
    except IOError as e:
        print(e)

    print(X.shape)
    print(y.shape)


if __name__ == '__main__':
    collect()
