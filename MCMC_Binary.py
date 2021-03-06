__author__ = 'mhjang'

import numpy as np
import math
#import matplotlib.pyplot as plt
#from matplotlib import cm
import random


#original_img = np.genfromtxt('stripes.txt')
#noisy_img = np.genfromtxt('stripes-noise.txt')

original_img = np.genfromtxt('swirl.txt')
noisy_img = np.genfromtxt('swirl-noise.txt')

np.set_printoptions(threshold='nan')

def generateSample(t, W_p, W_l):
    # initialize with y_ij = x_ij
    samples = list()
    maes = list()
    iteration = 0
    cur_mae = 0.0
    prev_mae = 0.0
  #  calMAE(noisy_img)
    y = np.copy(noisy_img)

    while(1):
 #   for iteration in range(100):
        y = np.copy(y)
        for i in range(100):
            for j in range(100):
                neighbors = get_neighbors((i,j))
                # len([y_lk = 0]
                neighbors_zero = len(neighbors) - sum([y[k][l] for (k, l) in get_neighbors((i,j))])
                norm = math.exp(W_p*(len(neighbors) - neighbors_zero) + W_l * noisy_img[i][j])
                denorm = math.exp(W_p * neighbors_zero + W_l * (1-noisy_img[i][j])) + norm
                prob_y_ij = norm / denorm
         #       alpha = 0.3
                alpha = random.uniform(0, 1)
                if alpha < prob_y_ij:
                    y[i][j] = 1
                else:
                    y[i][j] = 0
        samples.append(y)
        prev_mae = cur_mae
        cur_mae = calMAE(sum(samples)/(len(samples)))
        maes.append(cur_mae)
      #  print(len(samples))
   #     iteration += 1
  #      print(abs((cur_mae - prev_mae)))
        if abs((cur_mae - prev_mae)) < 0.0001:
            break
#        print(y)
  #      print(sum(samples)/((k+1)))
  #  print(maes)
    # plotting the error
   # print("done")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title("Error rate")
    ax1.plot(range(len(maes)), maes)
    ax1.set_ylabel("MAE")

    plt.show()
  #  print(sum(samples))
    return sum(samples)/(len(samples))



def gaussianModel(w_p, w_l):
    y = np.copy(noisy_img)
    samples = list()
    maes = list()
    curmae = 0.0
    prevmae= 0.0
    while(1):
  #  for iteration in range(100):
        y = np.copy(y)
        for i in range(100):
            for j in range(100):
                neighbors = get_neighbors((i, j))
                variance = 1.0/(2.0*(w_p*len(neighbors) + w_l))
                mu = (1.0/((w_p*len(neighbors) + w_l)))*((w_l*noisy_img[i][j] + sum([w_p * y[k][l] for (k, l) in neighbors])))
                z = np.random.normal(0, 1)
                y[i][j] = mu + z*math.sqrt(variance)
        samples.append(y)
        prevmae = curmae
        curmae = calMAE((sum(samples)/(len(samples))))
        maes.append(curmae)
        if math.fabs(curmae - prevmae) < 0.0001:
            break
    #    print(len(samples))
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title("Error rate")
    ax1.plot(range(len(maes)), maes)
    ax1.set_ylabel("MAE")
    return sum(samples)/(len(samples))


def gaussianModel2(w_p, w_l):
    y = np.copy(noisy_img)
    samples = list()
    for iteration in range(100):
        y = np.copy(y)
        for i in range(100):
            for j in range(100):
                neighbors = get_neighbors((i, j))
                w_p_neighborSum = sum([(w_p/(0.01 + math.pow((noisy_img[i][j] - noisy_img[k][l]), 2))) for (k,l) in neighbors])
                variance = 1.0/(2.0*(w_p_neighborSum + w_l))
                mu = (1.0/(w_p_neighborSum + w_l))*((w_l*noisy_img[i][j] +
                    sum([(w_p/(0.01 + math.pow((noisy_img[i][j] - noisy_img[k][l]), 2))) * y[k][l] for (k, l) in neighbors])))
                z = np.random.normal(0, 1)
                y[i][j] = mu + z*math.sqrt(variance)
        samples.append(y)
        calMAE((sum(samples)/len(samples)))
        print(len(samples))




def plot(y):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title("Original data (greyscale)")
    ax1.imshow(y, interpolation='nearest', cmap='gray')
    plt.show()



# given a pixel coordinate (i, j), return a list of coordinates of its neighbors
def get_neighbors(coord):
    i = coord[0]
    j = coord[1]
    # if it's on the border of the top
    # (i, j-1), (i-1, j), (i, j+1), (i+1, j)
    neighbors = list()
    if is_in_range(i):
        if is_in_range(j-1):
            neighbors.append((i, j-1))
        if is_in_range(j+1):
            neighbors.append((i, j+1))
    if is_in_range(j):
        if is_in_range(i-1):
            neighbors.append((i-1, j))
        if is_in_range(i+1):
            neighbors.append((i+1, j))
    return neighbors
def is_in_range(i):
    if i>=0 and i<100:
        return True
    else:
        return False


def calMAE(y):
    error = 0
    for i in range(100):
        for j in range(100):
            error += math.fabs(y[i][j] - original_img[i][j])
    print("error: " + str(error / (100*100)))
  #  print(error)
    return error/(100*100)

def main():
    W_p = 70
    W_l = 15

#    s = gaussianModel(W_p, W_l)
    gaussianModel2(W_p, W_l)
#    s = generateSample(100, W_p, W_l)
  #  plot(s)
   # print(str(W_p) + ", " + str(w_l))
    calMAE(s)
#    print(s)
  #  s = generateSample(100, 0, 178)
  #  calMAE(s)


if __name__ == '__main__':
    main()