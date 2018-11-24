import numpy as np
import matplotlib.pyplot as plt 



def loadDataSet(fileName, delim = '\t'):
	fr = open(fileName)
	stringArr = [line.strip().split(delim) for line in fr.readlines()]
	# print(stringArr)
	datArr = [list(map(float, line)) for line in stringArr]
	return mat(datArr)


def pca(dataMat, topNfeat = 9999999):
	# axis = 0, by columns; axis = 1, by rows
	meanVals = np.mean(dataMat, axis=0)
	# 去平均值
	meanRemoved = dataMat - meanVals
	# 协方差矩阵
	covMat = np.cov(meanRemoved, rowvar = 0)
	# 特征值和特征向量
	eigVals, eigVects = np.linalg.eig(mat(covMat))
	# np.argsort: return the indices that would sort an array.
	# 从小到大排序
	eigValInd = np.argsort(eigVals)
	# [start:end:step]
	# 此步骤返回N个最大的特征值
	eigValInd = eigValInd[:-(topNfeat+1):-1]
	redEigVects = eigVects[:, eigValInd]

	# 转换到新空间
	lowDDataMat = meanRemoved * redEigVects
	reconMat = (lowDDataMat * redEigVects.T) + meanVals
	return lowDDataMat, reconMat



def plotData(oldData, newData):
	fig = plt.figure(figsize=(12,12))
	ax = fig.add_subplot(111)
	ax.scatter(oldData[:, 0].flatten().A[0], oldData[:, 1].flatten().A[0], marker='^', s=25)
	ax.scatter(newData[:, 0].flatten().A[0], newData[:, 1].flatten().A[0], marker='o', s=25)
	fig.show()


def replaceNanWithMean():
	datMat = loadDataSet('secom.data', ' ')
	numFeat = np.shape(datMat)[1]
	for i in range(numFeat):
		# ~np.isnan(datMat[:, i].A)----------第i列非零的bool列向量
		# np.nonzero(a)[0] 返回a中非零（True）的元素的索引列向量
		meanVal = np.mean(datMat[np.nonzero(~np.isnan(datMat[:, i].A))[0], i])
		datMat[np.nonzero(np.isnan(datMat[:, i].A))[0], i] = meanVal
	return datMat

