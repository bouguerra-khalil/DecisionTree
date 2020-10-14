


###################################################################
##                                                               ##
##                  DECISION TREE IMPLEMENTATION                 ##
##             Project realised by KHALIL BOUGUERRA              ##
##      You can check the files utilities, BuildDecisionTree,    ##
##      Generalization_Error and Post_Prun for Help or comments  ##
##                                                               ##
###################################################################

####################### Imports ###################################
from utilities import log2
from BuildDecisionTree import *
from Generalization_Error import *
from Post_Prun import *


######################### Setup ###################################
path_input_file="/Graphs/2.txt" # input file path 
minNum=1 # min number of records in a node 
default_class=0 #The default target  class
alpha=0.5 # Alpha The pruning Coeff 

#extract  the variable needed to run the main program 
attributes_names=[] #name of features in the input file , optional 
(data,nbr_of_feature,attributes_possible_values,attributes_names)= import_data(path_input_file,attributes_names) 
    # data: 2D array holding all the records in the input file
    # nbr_of_features : number of features used in the decision tree 
    # attributes_possible_values : Dict containing for each variable the possible values 
    #                              {key= attribute or feature index , value= list[possible_values_ of_ that_attribue]}
attributes_indexes_root=list(range(nbr_of_feature)) # list of indexes of the features that will be used.




############################ Main Program ###########################

#create the root of the tree.
#a tree is defined by it is root.
root=Node(minNum,default_class,1,attributes_indexes_root,data,attributes_possible_values,attributes_possible_values)
#build The Tree (node , level_of_the_node )
BuildDecisionTree(root,1)
#Prune the tree 
pruned_tree_root=Post_Prune(root,data,minNum,default_class,alpha,attributes_possible_values)


########################### PRINTING ################################

#print Generalization_Error for the non-prunned tree( original )
print("Generalization Error Non-pruned Tree =",Generalization_Error(root,data,alpha,attributes_possible_values))
#print original tree, non-prunned tree
print_tree(root,attributes_possible_values,attributes_names)
#print Generalization_Error for the  prunned tree
print("Generalization Error pruned Tree =",Generalization_Error(pruned_tree_root,data,alpha,attributes_possible_values))
#print prunned tree
print_tree(pruned_tree_root,attributes_possible_values,attributes_names)
