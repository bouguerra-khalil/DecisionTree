from utilities import *


############################## Generalization_Error ##########################################

def Generalization_Error(root,data,alpha,attributes_possible_values):
    #we calculate the generalization error  by computing the  nbr of diffrences between the predictied target class and
    #the real target class and we add to that the nbr of leafs multiplied by a coeff alpha    
    nbr_err=0
    for line in data: 
        current_node=root
        while(not current_node.leaf):
            decision_att=current_node.constraint[0]
            decision_set=attributes_possible_values[decision_att][:current_node.constraint[1]]
            if(line[decision_att] in decision_set):
                current_node=current_node.children[0]
            else:
                current_node=current_node.children[1]
        if(line[-1]!=current_node.my_class):
            nbr_err+=1
    return nbr_err+alpha*get_nbr_leafs(root)
    
