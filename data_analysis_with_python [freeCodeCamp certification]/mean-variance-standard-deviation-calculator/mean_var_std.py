import numpy as np

def calculate(list):

    # Cast the list to a 3x3 array if it has 9 numbers
    if len(list) != 9:
        raise ValueError("List must contain nine numbers.")
    else:
        arr = np.array(list).reshape((3,3))

    # List the desired metrics and respective NumPy functions
    metrics = ["mean", "variance", "standard deviation", "max", "min", "sum"]
    funcs = [np.mean, np.var, np.std, np.amax, np.amin, np.sum]

    # Perform all the calculations needed and save them in the dictionary
    # Since we always execute the same function first for the columns, then\
    # the rows, then the flat array, we can use a dict comprehension for\
    # this repeated logic
    calculations = dict()
    calculations = {
        metrics[i]: [
            funcs[i](arr, axis=0).tolist(),
            funcs[i](arr, axis=1).tolist(),
            funcs[i](arr).tolist()
        ]
        for i in range(len(metrics))
    }

    return calculations

if __name__ == "__main__":
    print(calculate([0,1,2,3,4,5,6,7,8]))