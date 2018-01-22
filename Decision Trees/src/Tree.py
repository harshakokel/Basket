class BinaryTree:

    def __init__(self,rootid):
      self.left = None
      self.right = None
      self.rootid = rootid

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def setLeftChild(self, tree):
        self.left = tree

    def setRightChild(self, tree):
        self.right = tree

    def setNodeValue(self,value):
        self.rootid = value

    def getNodeValue(self):
        return self.rootid

    def printTree(self, depth):
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
