from utilities import *


############################## BuildDecisionTree #############################################


def BuildDecisionTree(node,level):
    if(node.leaf):
        #if leaf node terminate
        return 
    else:
        attributes=node.attributes.copy() # get a copy of the current node attributes
        attributes.remove(node.constraint[0])  # remove the decision attribute from the list because we used it for this split 
        (records_left,records_right)=node.best_split_records # get records of the left/right children after the best split ( that max Gain_info)
        node_L=Node(node.minNum,node.default_class,level+1,attributes,records_left,node.attributes_possible_values) #Create Node_L with level+1 and records_left 
        node_R=Node(node.minNum,node.default_class,level+1,attributes,records_right,node.attributes_possible_values,right=1) #Create Node_R with level+1 and records_right
        node.children.append(node_L) # current node children[0]<=node_L  ( left child)
        node.children.append(node_R) # current node children[1]<=node_R  ( right child)
        BuildDecisionTree(node_L,level+1) # recursively build  the left subtree
        BuildDecisionTree(node_R,level+1) # recursively build  the right subtree
