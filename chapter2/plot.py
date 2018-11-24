import matplotlib.pyplot as plt 
import math

from matplotlib.font_manager import FontManager, FontProperties
def getChineseFont():
	return FontProperties(fname = '/System/Library/Fonts/PingFang.ttc')


decisionNode = dict(boxstyle = "sawtooth", fc = '0.8')
leafNode = dict(boxstyle = 'round4', fc = '0.8')
arrow_args = dict(arrowstyle='<-')


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
	createPlot.ax1.annotate(nodeTxt, fontproperties = getChineseFont(), xy=parentPt, xycoords = 'axes fraction', xytext=centerPt, textcoords='axes fraction', va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


def createPlot():
	fig = plt.figure(1, facecolor = 'white')
	fig.clf()
	createPlot.ax1 = plt.subplot(111, frameon=False)
	plotNode('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
	plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
	plt.show()


# get the number of leafs to estimate x 
def getNumLeafs(myTree):
	numLeafs = 0
	# in Python3, must use list() on dict_keys() to support index
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			numLeafs += getNumLeafs(secondDict[key])
		else:
			numLeafs += 1
	return numLeafs


# get the depth of tree to estimate y
def getTreeDepth(myTree):
	maxDepth = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1 + getTreeDepth(secondDict[key])
		else:
			thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth


def retrieveTree(i):
	listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}, {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
	return listOfTrees[i]


# 在连线上添加文字
def plotMidText(cntrPt, parentPt, txtString):
	xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
	yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
	# print('cntrPt: ', cntrPt)
	# print('parentPt: ', parentPt)
	angle = 0
	if parentPt[0] != cntrPt[0]: 
		angle = math.atan((cntrPt[1] - parentPt[1]) / (cntrPt[0] - parentPt[0]))
		angle = angle * 180.0 / math.pi  
		# print('-----angle: ', angle)
	print('\n')
	createPlot.ax1.text(xMid, yMid, txtString, rotation = angle)


def plotTree(myTree, parentPt, nodeTxt):
	# print('xOff: ', plotTree.xOff)
	# print('yOff: ', plotTree.yOff)
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)

	firstStr = list(myTree.keys())[0]
	cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
	# print('cntrPt: ', cntrPt)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	# 求出下一层的y坐标
	plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			# 若为决策节点，递归调用
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			# 叶子节点，直接生成
			plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
			plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	# 此决策节点的子节点计算完毕，复原y坐标
	plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD



def createPlot(inTree):
	fig = plt.figure(1, facecolor = 'white', figsize=(12, 12))
	fig.clf()
	axprops = dict(xticks=[], yticks=[])
	createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	plotTree.xOff = -0.5 / plotTree.totalW
	plotTree.yOff = 1.0
	plotTree(inTree, (0.5, 1.0), '')
	plt.show()




