from utilities import *
from Generalization_Error import *


######################################## Post_Prune ##########################################


def Post_Prune(root,data,minNum,default_class,alpha,attributes_possible_values):
    #root: the root node of the tree to be prunned 
    #data: 
    import copy
    root_final_purn = copy.deepcopy(root) #The root of the prunned tree
    root_current_purn= copy.deepcopy(root) #the root of the original tree

    for level in range(Node.max_level, 1, -1): 
        queue=[]
        queue.append(root_current_purn)
        while(queue):
            current_node=queue.pop(0)
            if(current_node.level==level and not current_node.leaf):
                current_node.leaf=True
                current_node.children=[]
                if(len(current_node.records)<minNum):
                    current_node.my_class=default_class
                else:
                    current_node.my_class=current_node.major_class()
            if(not current_node.leaf):
                queue.append(current_node.children[0])
                queue.append(current_node.children[1])
        if(Generalization_Error(root_current_purn,data,alpha,attributes_possible_values)<Generalization_Error(root_final_purn,data,alpha,attributes_possible_values)):
            root_final_purn=copy.deepcopy(root_current_purn)
        else: 
            root_current_purn=copy.deepcopy(root_final_purn)
            
    return root_final_purn
