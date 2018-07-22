import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

data = pd.DataFrame({
    'x': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],
    'y': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24]
})
np.random.seed(300) #Used so that we get same results

k = 3
print('Number of clusters:', k)

# centroids[i] = [x, y] which are taken as random
centroids = {}
for i in range(k):
    centroids[i+1] = [np.random.randint(0, 80), np.random.randint(0, 80)]
    
print('Selected cluster centroids are: ', centroids)
    
#print(centroids.keys()) #1, 2, 3

def assign(data, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2) --distance
        data['distance_from_{}'.format(i)] = (
            np.sqrt(
                (data['x'] - centroids[i][0]) ** 2
                + (data['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    data['closest'] = data.loc[:, centroid_distance_cols].idxmin(axis=1)
    data['closest'] = data['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    
    return data

data = assign(data, centroids)
print(data)

old_centroids = copy.deepcopy(centroids)

def update(k):
    for i in centroids.keys():
        centroids[i][0] = np.mean(data[data['closest'] == i]['x'])
        centroids[i][1] = np.mean(data[data['closest'] == i]['y'])
    return k

centroids = update(centroids)
print(centroids)
    
data = assign(data, centroids)

i =1
while(True):
    
    print('Iteration ', i)
    closest_centroids = data['closest'].copy(deep=True)
    centroids = update(centroids)
    data = assign(data, centroids)
    i +=1
    print(closest_centroids)
    #print(centroids)
    x = data['closest']
    print(x)
    if closest_centroids.equals(data['closest']):
        break
        
print(centroids)

