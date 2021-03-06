'''
Overfitting in Linear Regression
Author: Rowel Atienza
Project: https://github.com/roatienza/Deep-Learning-Experiments
'''
# On command line: python3 overfit_regression.py
# Prerequisite: tensorflow 1.0 (see tensorflow.org)
#             : matplotlib (http://matplotlib.org/)

from __future__ import print_function

import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math

# Tunable parameters (Try changing the values and see what happens)
samples = 100
learning_rate = 0.0001

# xcoeff should be predicted by the model, yp
xcoeff = tf.transpose(tf.constant([[1., 1., 1.]]))

# a = tf.random_uniform([1, samples],-2.5,2.5)
a = tf.linspace(-2.5,2.5,samples)
# Correct the shape
a = tf.reshape(a,[samples,1])

# In theory, polynomial degree greater than 2 will overfit but the training is still able to guess the weights
# correctly for 3rd and 4th degree polynomials
# Inputs to form yp = a*a*a*a*xp[0] + a*a*a*xp[1] + a*a*xp[2] + a*xp[3] + xp[4], xp[] are the weights
# Overfit since our data generating model is quadratic
Ap = tf.concat([tf.concat([tf.concat([tf.concat([a*a*a*a*a*a,a*a*a*a],1),a*a],1),a],1),tf.ones_like(a)],1)

# Inputs to form yp = a*a*a*xp[0] + a*a*xp[1] + a*xp[2] + xp[3], xp[] are the weights
# Overfit since our data generating model is quadratic
# Ap = tf.concat(1,[tf.concat(1,[tf.concat(1,[a*a*a,a*a]),a]),tf.ones_like(a)])

# Inputs to form y = a*a*xcoeff[0] + a*xcoeff[1] + xcoeff[2]
A = tf.concat([tf.concat([a*a,a],1),tf.ones_like(a)],1)

# Initial guess on coefficients of predicted linear model
xp = tf.Variable(tf.random_uniform([5,1], -1.0, 1.0))

# xp = tf.Variable(tf.random_uniform([4,1], -1.0, 1.0))

# Predicted Model
yp = tf.matmul(Ap,xp)

# Observed outputs
y = tf.matmul(A,xcoeff)
# noise = tf.random_normal(y.get_shape(),stddev=0.8)
noise = tf.sin(math.pi*a)
y = tf.add(y,noise)

# The smaller the loss, the closer our prediction to the observed outputs
# The loss model used is square of error (yp - y)
# Miinimization of loss is done by Gradient Descent
loss = tf.reduce_mean(tf.square(yp - y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_step = optimizer.minimize(loss)

init = tf.global_variables_initializer()
with tf.Session() as session:
    session.run(init)
    for i in range(10000):
        session.run(train_step)
        if ((i+1) % 100) == 0:
            print("%d : Loss=%0.1lf,  Predicted Parameters = %s" % (i+1, loss.eval(), session.run(xp)))
    # Let's plot
    a = np.array(a.eval())
    plt.plot(a, y.eval(), 'ro', a, yp.eval(), 'b')
    red = mpatches.Patch(color='red', label='Data')
    blue = mpatches.Patch(color='blue', label='Model')
    plt.legend(handles=[red,blue])
    plt.show()