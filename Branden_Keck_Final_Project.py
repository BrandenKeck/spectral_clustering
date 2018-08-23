##############################################################################################
####################### Spectral Clustering via Diffusion Maps: ##############################
##### Algorithm Optimization and Applications in Predictive Analysis of Weather Patterns #####
######### By: Branden Keck, JHU 625.714: Intro. To Stochastic Differential Equations #########
################################## 22 August 2018 ############################################
##############################################################################################

# Construction of the Diffusion Map via Nystrom Approximation
def diffusionMap(x, n, m, t, sig):
	
	# Create the affinity matrix with Nystrom
	nystroem = ka.Nystroem(kernel="rbf", n_components=n, gamma=sig**2)
	W = nystroem.fit_transform(x)
		
	# Faster Approximation Algorithm:
	# x = np.array(x)
	# W = np.ones([n, n])
	# for i in range(0, n):
		# j = i
		# while j<n:
			# if(x[i].all != x[j].all):
				# W[i,j] = np.exp(-1*np.linalg.norm(np.subtract(x[i],x[j]))/2*sig**2)
			# j = j + 1
		# if(i%1000==0):print(str(100*i/n)+"%")
	# W = tf.convert_to_tensor(W)
	
	# Computation the diagonal matrix of row sums
	d = tf.reduce_sum(W, 1)
	Dinv = tf.matrix_inverse(tf.diag(d))
	
	# Creation of stochastic matrix M and its eigenfunctions
	M = tf.matmul(Dinv, W)
	M = tf.Session().run(M)
	lam, evA = np.linalg.eig(M)
	
	# Final diffusion map computation
	DM = []
	for i in range(1,m+1):
		DM.append(lam[i]**t * np.array(evA[:,i]))
	DM = np.transpose(np.array(DM))
	
	return DM

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def kMeans(k, DM, n):
	
	# KMeans clustering algorithm
	km = clus.KMeans(n_clusters=k, init="k-means++", n_init=10, max_iter=300, tol=0.0001).fit(DM)
	clusterMe = km.labels_

	# Test colors
	colors = [[0,0,0],[20,20,20],[50,50,50],[100,100,100],[140,140,140],[180,180,180],[230,230,230]]
		
	# Construction of test image
	l = []
	clusterMe = clusterMe.astype(int)

	for col in range(n):
		l.append(colors[clusterMe[col]])
	l = np.array(l, dtype='f').reshape(shape)
	
	# Also for the testing phase
	plt.imshow(l)
	plt.show()
	
	# return [clusterMe, error] # Come back to this?
	return clusterMe
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def analyzeClusters(k, d, c, shape):
	c = c.reshape([shape[0], shape[1]])
	d = np.array(d).reshape(shape[0], shape[1], 5)
	
	# Gather info from the mean and variance of data in each dimention
	bg = c[0,0]
	bgcolor = d[0,0]
	
	X = [[] for i in range(0,k)]
	Y = [[] for i in range(0,k)]
	R = [[] for i in range(0,k)]
	G = [[] for i in range(0,k)]
	B = [[] for i in range(0,k)]
	
	for i in range(0, shape[0]):
		for j in range(0, shape[1]):
			if(c[i,j]) != bg:
				X[c[i,j]].append(i)
				Y[c[i,j]].append(j)
				R[c[i,j]].append(d[i,j,2])
				G[c[i,j]].append(d[i,j,3])
				B[c[i,j]].append(d[i,j,4])
	
	mX = [[] for i in range(0,k)]
	mY = [[] for i in range(0,k)]
	mR = [[] for i in range(0,k)]
	mG = [[] for i in range(0,k)]
	mB = [[] for i in range(0,k)]
	vX = [[] for i in range(0,k)]
	vY = [[] for i in range(0,k)]
	vR = [[] for i in range(0,k)]
	vG = [[] for i in range(0,k)]
	vB = [[] for i in range(0,k)]
	for i in range(0, k):
		if(X[i]!=[]):
			mX[i] = np.mean(np.array(X[i]))
			mY[i] = np.mean(np.array(Y[i]))
			mR[i] = np.mean(np.array(R[i]))
			mG[i] = np.mean(np.array(G[i]))
			mB[i] = np.mean(np.array(B[i]))
			vX[i] = np.var(np.array(X[i]))
			vY[i] = np.var(np.array(Y[i]))
			vR[i] = np.var(np.array(R[i]))
			vG[i] = np.var(np.array(G[i]))
			vB[i] = np.var(np.array(B[i]))
			
	m = [mX, mY, mR, mG, mB]
	v = [vX, vY, vR, vG, vB]
			
	return [bgcolor, X, Y, m, v]
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def importData(file):

	# Data import
	file = os.path.join(file)
	lenna = io.imread(file)
	shape = lenna.shape

	# Contruction of data vectors to be used in the Diffusion Map
	x = []
	for i in range(0, shape[0]):
		for j in range(0, shape[1]):
			x.append([lenna[i,j][0], lenna[i,j][1], lenna[i,j][2]])
			
	return [x, lenna, len(x), shape]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def drawPredictions(pm):
	x = 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	
if __name__ == "__main__":

	# Start time for benchmarking the code
	import time
	start_me = time.time()
	
	
	# Suppress warnings due to complex eigenvalues
	import warnings
	warnings.filterwarnings('ignore')
	
	
	# Python Library Imports
	import os
	import sklearn.metrics.pairwise as sk
	import sklearn.kernel_approximation as ka
	import sklearn.cluster as clus
	import tensorflow as tf
	import numpy as np
	from skimage import io
	from matplotlib import pyplot as plt
	from copy import deepcopy
	
	# Define the dataset
	#files = ['_data/Set0/1.png', '_data/Set0/2.png', '_data/Set0/3.png', '_data/Set0/4.png', '_data/Set0/5.png', '_data/Set0/6.png', '_data/Set0/7.png']
	#files = ['_data/Set1/1.png', '_data/Set1/2.png', '_data/Set1/3.png', '_data/Set1/4.png', '_data/Set1/5.png']
	#files = ['_data/Set0/1.png', '_data/Set0/2.png']
	#files = ["_data/Set1_min/1.png"]
	files = ["_data/_test/30.png"]
	
	# Adjustable model parameters
	sig = 0.01 # Scaling parameter for Diffusion Map kernel
	m = 3 # Number of eigenvalues to be included in Diffusion Map
	t = 2 # Diffusion Map time step
	k = 4 # K-Means Clustering constant
	numP = 1 # Number of future prediction images
	
	counter = 1
	predictMe = []
	imgs = []
	for file in files:
		print("Calculating for file #" + str(counter))
	
		# Gather the dataset and Nystrom approximation parameter
		[x, img, n, shape] = importData(file)
		imgs.append(img)
		
		# Update screen with current time
		print("")
		print("Time for Imports:")
		print(time.time() - start_me)
		
		# Compute a diffusion map from the data
		DM = diffusionMap(x, n, m, t, sig)
		
		# Update screen with current time
		print("")
		print("Time for Diffusion Map Calculation:")
		print(time.time() - start_me)
		
		
		# Calculate "k" and clusters via k means
		clusters = kMeans(k, DM, n)
		
		# Update screen with current time
		print("")
		print("Time for K Means Calculation:")
		print(time.time() - start_me)
		
		continue
		
		# Get data cluster centers
		data = analyzeClusters(k, x, clusters, shape)
		predictMe.append(data)
		
		counter = counter + 1
		
	for i in range(0, numP):
		lol = 0
		#[predictMe img] = drawPredictions(predictMe)
		#imgs.append(img)
		
	plt.figure(1)
	for i in range(0, len(imgs)):
		plt.subplot(1,len(imgs)+1, i+1)
		plt.imshow(imgs[i])
	
	plt.show()
	
	print("")
	print("-------------------")
	print("SIMULATION COMPLETE")
	