#!/usr/bin/env python
# coding: utf-8

# In[132]:


# Theta 2 overestimate
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def fun(theta_1, theta_2):
    return np.tan(np.radians(theta_2*1.1))*np.tan(np.radians(theta_1))/(np.tan(np.radians(theta_2*1.1))-np.tan(np.radians(theta_1)))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
theta1_range = np.arange(31.0, 5.0, -0.9)
theta2_range = np.arange(55.0, 35.0, -0.9)
theta1, theta2 = np.meshgrid(theta1_range, theta2_range)
ds = np.array(fun(np.ravel(theta1), np.ravel(theta2)))
d = ds.reshape(theta1.shape)

ax.plot_surface(theta2, theta1, d)

ax.set_xlabel('Theta 2')
ax.set_ylabel('Theta 1')
ax.set_zlabel('d')
ax.set_zlim(0,11)

plt.show()


# In[131]:


# Theta 2 underestimate
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def fun(theta_1, theta_2):
    return np.tan(np.radians(theta_2*0.9))*np.tan(np.radians(theta_1))/(np.tan(np.radians(theta_2*0.9))-np.tan(np.radians(theta_1)))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
theta1_range = np.arange(31.0, 5.0, -0.9)
theta2_range = np.arange(55.0, 35.0, -0.9)
theta1, theta2 = np.meshgrid(theta1_range, theta2_range)
ds = np.array(fun(np.ravel(theta1), np.ravel(theta2)))
d = ds.reshape(theta1.shape)

ax.plot_surface(theta2, theta1, d)

ax.set_xlabel('Theta 2')
ax.set_ylabel('Theta 1')
ax.set_zlabel('d')
ax.set_zlim(0,11)

plt.show()


# In[133]:


# Theta 1 overestimate
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def fun(theta_1, theta_2):
    return np.tan(np.radians(theta_2))*np.tan(np.radians(theta_1*1.1))/(np.tan(np.radians(theta_2))-np.tan(np.radians(theta_1*1.1)))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
theta1_range = np.arange(31.0, 5.0, -0.9)
theta2_range = np.arange(55.0, 35.0, -0.9)
theta1, theta2 = np.meshgrid(theta1_range, theta2_range)
ds = np.array(fun(np.ravel(theta1), np.ravel(theta2)))
d = ds.reshape(theta1.shape)

ax.plot_surface(theta2, theta1, d)

ax.set_xlabel('Theta 2')
ax.set_ylabel('Theta 1')
ax.set_zlabel('d')
ax.set_zlim(0,11)

plt.show()


# In[134]:


# Theta 1 underestimate
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def fun(theta_1, theta_2):
    return np.tan(np.radians(theta_2))*np.tan(np.radians(theta_1*0.9))/(np.tan(np.radians(theta_2))-np.tan(np.radians(theta_1*0.9)))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
theta1_range = np.arange(31.0, 5.0, -0.9)
theta2_range = np.arange(55.0, 35.0, -0.9)
theta1, theta2 = np.meshgrid(theta1_range, theta2_range)
ds = np.array(fun(np.ravel(theta1), np.ravel(theta2)))
d = ds.reshape(theta1.shape)

ax.plot_surface(theta2, theta1, d)

ax.set_xlabel('Theta 2')
ax.set_ylabel('Theta 1')
ax.set_zlabel('d')
ax.set_zlim(0,11)

plt.show()

