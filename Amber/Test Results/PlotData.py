import matplotlib.pyplot as plt, numpy as np

cloud = {0.1: [28.737525, 35.294157, 37.251017, 37.247285, 37.220542, 37.126950, 37.187707, 37.140114],\
         0.5: [8.796554, 9.205409, 9.286810, 9.326784, 9.367543, 9.372415, 9.347731, 9.348159, 9.348332, 9.325010, 9.297519],\
         1  : [6.726414, 6.798498, 6.937224, 6.878832, 6.828630, 6.822782, 6.770715, 6.766120, 6.765100, 6.738865, 6.696692],\
         5  : [4.858181, 3.887907, 3.888458, 3.925361, 3.925478, 3.924713, 3.932744, 3.938251, 3.969049, 3.938612, 3.930301, 3.932361],\
         10 : [3.548206, 3.536180, 3.515200, 3.522238, 3.530696, 3.560360, 3.583819, 3.584272, 3.563212, 3.556843, 3.576291, 3.560071]}

hybrid = {0.1: [32.247003, 41.635468, 42.604175, 42.441479, 42.647158, 43.356084, 43.367705, 43.388867, 43.457216, 42.894894],\
          0.5: [13.919500, 14.159425, 14.562314, 14.375902, 14.640490, 14.502664, 14.495209, 15.218466, 15.691716, 15.688786, 15.142892],\
          1  : [10.077460, 11.347455, 11.926654, 11.908882, 11.900213, 11.711689, 11.741287, 11.731933, 12.409190, 13.069323, 12.994066],\
          5  : [6.077563, 7.818010, 8.199321, 9.859004, 9.610990, 9.357674, 9.368867, 9.156163, 8.950741, 9.127098, 9.099534, 10.543003],\
          10 : [7.458483, 7.712030, 9.625562, 8.436493, 8.538699, 8.547045, 8.530429, 8.534606, 8.693237, 9.825369, 9.670858]}

local = {0.1: [32.315506, 38.564228, 41.222073, 40.875343, 40.316252],\
         0.5: [11.472450, 11.805248, 11.569088, 11.457014, 11.465871, 11.597523, 11.553536, 11.550935, 11.464650, 11.366190],\
         1  : [8.076799, 8.029537, 7.961660, 7.895948, 7.904000, 8.046691, 8.038584, 8.036822, 8.037481, 7.907447],\
         5  : [5.022460, 4.949500, 5.120481, 5.134944, 5.144536, 5.213707, 5.211734, 5.196800, 5.196846, 5.161212, 5.053142],\
         10 : [4.673613, 4.599289, 4.768661, 4.800531, 4.810185, 4.872973, 4.869621, 4.854938, 4.855751, 4.819260, 4.710414]}

local_avg = {0.1 : np.mean(local[0.1]), 0.5 : np.mean(local[0.5]), 1 : np.mean(local[1]), 5 : np.mean(local[5]), 10 : np.mean(local[10])}
cloud_avg = {0.1 : np.mean(cloud[0.1]), 0.5 : np.mean(cloud[0.5]), 1 : np.mean(cloud[1]), 5 : np.mean(cloud[5]), 10 : np.mean(cloud[10])}
hybrid_avg = {0.1 : np.mean(hybrid[0.1]), 0.5 : np.mean(hybrid[0.5]), 1 : np.mean(hybrid[1]), 5 : np.mean(hybrid[5]), 10 : np.mean(hybrid[10])}

plt.plot([0.1 for i in local[0.1]], [0.1*i for i in local[0.1]], 'ro',\
         [0.5 for i in local[0.5]], [0.5*i for i in local[0.5]], 'ro',\
         [1 for i in local[1]], [i for i in local[1]], 'ro',\
         [5 for i in local[5]], [5*i for i in local[5]], 'ro',\
         [10 for i in local[10]], [10*i for i in local[10]], 'ro',\
         [0.1 for i in cloud[0.1]], [0.1*i for i in cloud[0.1]], 'go',\
         [0.5 for i in cloud[0.5]], [0.5*i for i in cloud[0.5]], 'go',\
         [1 for i in cloud[1]], [i for i in cloud[1]], 'go',\
         [5 for i in cloud[5]], [5*i for i in cloud[5]], 'go',\
         [10 for i in cloud[10]], [10*i for i in cloud[10]], 'go',\
         [0.1 for i in hybrid[0.1]], [0.1*i for i in hybrid[0.1]], 'bo',\
         [0.5 for i in hybrid[0.5]], [0.5*i for i in hybrid[0.5]], 'bo',\
         [1 for i in hybrid[1]], [i for i in hybrid[1]], 'bo',\
         [5 for i in hybrid[5]], [5*i for i in hybrid[5]], 'bo',\
         [10 for i in hybrid[10]], [10*i for i in hybrid[10]], 'bo')
plt.errorbar([0.1, 0.5, 1, 5, 10], [0.1*np.mean(local[0.1]), 0.5*np.mean(local[0.5]), np.mean(local[1]), 5*np.mean(local[5]), 10*np.mean(local[10])],\
    [np.std([0.1*i for i in local[0.1]]), np.std([0.5*i for i in local[0.5]]), np.std(local[1]), np.std(5*local[5]), np.std(10*local[10])], linestyle=None, marker='^', color='r')
plt.errorbar([0.1, 0.5, 1, 5, 10], [0.1*np.mean(cloud[0.1]), 0.5*np.mean(cloud[0.5]), np.mean(cloud[1]), 5*np.mean(cloud[5]), 10*np.mean(cloud[10])],\
    [np.std([0.1*i for i in cloud[0.1]]), np.std([0.5*i for i in cloud[0.5]]), np.std(cloud[1]), np.std(5*cloud[5]), np.std(10*cloud[10])], linestyle=None, marker='^', color='g')
plt.errorbar([0.1, 0.5, 1, 5, 10], [0.1*np.mean(hybrid[0.1]), 0.5*np.mean(hybrid[0.5]), np.mean(hybrid[1]), 5*np.mean(hybrid[5]), 10*np.mean(hybrid[10])],\
    [np.std([0.1*i for i in hybrid[0.1]]), np.std([0.5*i for i in hybrid[0.5]]), np.std(hybrid[1]), np.std(5*hybrid[5]), np.std(10*hybrid[10])], linestyle=None, marker='^', color='b')
plt.text(9, 50, 'Local', color='r')
plt.text(5.5, 20, 'Cloud', color='g')
plt.text(5.5, 55, 'Hybrid', color='b')
plt.xlabel('FPS')
plt.ylabel('Performance')
plt.title('Performance vs. FPS (600MHz, 1080p)')
plt.grid(True)
plt.show()
