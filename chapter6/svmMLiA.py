from numpy import *
from time import sleep



def loadDataSet(fileName):
	dataMat = []; labelMat = []
	fr = open(fileName)
	for line in fr.readlines():
		lineArr = line.strip().split('\t')
		dataMat.append([float(lineArr[0]), float(lineArr[1])])
		labelMat.append(float(lineArr[2]))
	return dataMat, labelMat


def selectJrand(i, m):
	j = i
	while (j == i):
		# random.uniform: return a real between 0 and m
		j = int(random.uniform(0, m))
	return j


def clipAlpha(aj, H, L):
	if aj > H:
		aj = H
	if L > aj:
		aj = L
	return aj


# SMO(Sequential Minimal Optimization)-------Simple
# toler: fault-tolerance
# maxIter: max-iteration
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
	dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
	b = 0; m, n = shape(dataMatrix)
	alphas = mat(zeros((m, 1)))
	# 如果alphas一直不改变直到maxIter次，就return
	iter = 0
	while(iter < maxIter):
		# alphaPairsChanged 用于记录alpha是否被优化
		alphaPairsChanged = 0
		for i in range(m):
			# multiply: 对应相乘
			# fXi: 预测的类别
			fXi = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
			# Ei: 误差
			Ei = fXi - float(labelMat[i])
			if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
				j = selectJrand(i, m)
				fXj = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[j, :].T)) + b
				Ej = fXj - float(labelMat[j])
				alphaIold = alphas[i].copy()
				alphaJold = alphas[j].copy()
				# if用于将alpha[j]调整到0到C之间
				if (labelMat[i] != labelMat[j]):
					L = max(0, alphas[j] - alphas[i])
					H = min(C, C + alphas[j] - alphas[i])
				else:
					L = max(0, alphas[j] + alphas[i] - C)
					H = min(C, alphas[j] + alphas[i])
				if L == H: 
					print('H == L')
					continue
				# eta为alpha[j]的最优修改量
				eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - dataMatrix[i, :] * dataMatrix[i, :].T - dataMatrix[j, :] * dataMatrix[j, :].T
				if eta >= 0:
					print('eta >= 0')
					continue
				alphas[j] -= labelMat[j] * (Ei - Ej) / eta
				alphas[j] = clipAlpha(alphas[j], H, L)
				if (abs(alphas[j] - alphaJold) < 0.00001): 
					print('j not moving enought')
					continue
				# 对于i的修改，幅度等于j，但是反向相反
				alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])

				b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T
				b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
				if (0 < alphas[i]) and (C > alphas[i]):
					b = b1
				elif (0 < alphas[j]) and (C > alphas[j]):
					b = b2
				else:
					b = (b1 + b2) / 2.0
				alphaPairsChanged += 1
				print('iter: %d i: %d, pairs changed: %d'%(iter, i, alphaPairsChanged))
		if (alphaPairsChanged == 0):
			iter += 1
		else:
			iter = 0
		print('iteration number: %d' % iter)
	return b, alphas

