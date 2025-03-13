import os
import numpy as np
from ModelTests import TestModel

directory = "Tests"
extension = ".txt" 

files = ["Tests/" + f for f in os.listdir(directory) if f.endswith(extension)]
eps_range = np.arange(10000, 10000000.01, 0.1)  # .01 -> 10
samples = np.arange(1,31) # 1 -> 30
with open("Weights.csv", "a") as output:
    with open("FalsePositives.txt", "a") as falses:
        output.write("-----------------\n")
        output.flush()
        falses.write("-----------------\n")
        falses.flush()
        counter = 0
        for f in files:
            for i in eps_range:
                    for j in samples:
                        counter += 1
                        a, b, c = TestModel(f,i,j,"euclidean")
                        # ? id, noise, newsInclusion, samples, eps_range, filePath, metric
                        output.write(f"{counter},{a:.3f},{b:.3f},{i},{j},{f}\n")
                        output.flush()
                        falses.write(f"{counter} | {"|".join(c)} \n")
                        falses.flush()