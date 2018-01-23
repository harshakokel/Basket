class BinaryTree:

    def __init__(self,rootid):
      self.left = None
      self.right = None
      self.rootid = rootid
      self.positives = None
      self.negatives = None

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def setLeftChild(self, tree):
        self.left = tree

    def setRightChild(self, tree):
        self.right = tree

    def setPositiveExamples(self,value):
        self.positives = value

    def getPositiveExamples(self):
        return self.positives

    def setNegativeExamples(self,value):
        self.negatives = value

    def getNegativeExamples(self):
        return self.negatives

    def setNodeValue(self,value):
        self.rootid = value

    def getNodeValue(self):
        return self.rootid

    def isLeafNode(self):
        return (self.right is None and self.left is None)

    def printTree(self, depth=0):
        if self.left is None and self.right is None:
            print self.rootid,
        else:
            print ""
            for i in range(0, depth):
                print '|',
            print self.rootid, " = 0:",
            if self.left is not None:
                self.left.printTree(depth + 1)
            print ""
            for i in range(0, depth):
                print '|',
            print self.rootid, " = 1:",
            if self.right is not None:
                self.right.printTree(depth + 1)
