import heapq

codeBook = {}

class Node:
    def __init__(self, value, symbol = None, rchild = None, lchild = None, code = None):
        self.symbol = symbol 
        self.value = value
        
        self.leftChild = lchild
        self.rightChild = rchild

    def __le__(self, other):
        return self.value <= other.value
    
    def __lt__(self, other):
        return self.value < other.value

def huffmanCode(symbolFrequancy):

    #Ctreats huffman tree
    def createTree():
        minHeap = []

        # Adding Symbol nodes to the heap
        for s in symbolFrequancy:
            heapq.heappush(minHeap, Node(symbolFrequancy[s], symbol = s))

        while (True):

            if len(minHeap) >= 2:
                n1 = heapq.heappop(minHeap)
                n2 = heapq.heappop(minHeap)
                heapq.heappush(minHeap, Node(n1.value + n2.value, lchild = n1, rchild = n2))

            else:
                return heapq.heappop(minHeap)

    # Wrtie the codes of each symbol using the preorder traversal
    def writeCodes(node, codeStr):

        if node != None:
            if node.symbol != None:
                codeBook[node.symbol] = codeStr

            writeCodes(node.leftChild, codeStr + '0')

            writeCodes(node.rightChild, codeStr + '1')
        
    treeRoot = createTree()
    
    writeCodes(treeRoot, "")

    return (codeBook, treeRoot)

# Returns the decoded data as a binary array
def huffmanDecode(treeRoot, code) -> bytearray:
    if not isinstance(treeRoot, Node): 
        return
    
    currentNode = treeRoot
    binary_data = bytearray()

    for bit in code:
        if bit == '0':
            currentNode = currentNode.leftChild
        elif bit == '1':
            currentNode = currentNode.rightChild
        else:
            raise ValueError("Code must be a string of '0's and '1's")

        if currentNode.symbol != None:
            binary_data.append(currentNode.symbol)
            currentNode = treeRoot

    return binary_data