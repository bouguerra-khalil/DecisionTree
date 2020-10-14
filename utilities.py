############################# Utilties Functions ###########################

def log2(x):
    #return value is x*log2(x) ( to avoid the exception in log(0) )
    if(x==0):
        return 0
    import math  
    return math.log2(x)

def import_data(file_path,attributes_names=[]): 
    #file_path: path to the input
    #attributes_name = list of names of attributes of size (nbr_of features) 
    #optional parameter => by default values are [A,B,C,D,...]
    data=[]
    # data is 2D array [columns=(Features + target attribute)[rows=records]
    nbr_of_feature=0 # number of features in the data 
    attributes_possible_values={}
    #we will be using the index of the Feature rather than it's name to simplify things
    #attributes_possible_values is a dictionnary of key = index for attribute in attributes_name table 
    #and as value a list of the ordered possible values of this attribute
    #WE SUPPOSE ALL THE VALUES are in the form [0,1...,n] 
    with open(file_path) as file:
        data=[[int(element) for element in line.strip().split(" ") ] for line in file.readlines()]
    if(data): 
        nbr_of_feature=len(data[0])-1
        for line in data: 
            for att in range(nbr_of_feature):
                if(att in attributes_possible_values):
                    attributes_possible_values[att].append(line[att])
                else:
                    attributes_possible_values[att]=[line[att]]
        for att in range(nbr_of_feature):
             attributes_possible_values[att]=list(set( attributes_possible_values[att]))
    if(attributes_names==[]):
        attributes_names=[chr(ord('A')+i) for i in range(nbr_of_feature)]
    return(data,nbr_of_feature,attributes_possible_values,attributes_names)

    
def print_node(node,attributes_possible_values,attributes_names):
    #print The data of a single node 
    if(node.root):
        print("Root")
    elif(node.leaf):
        print("Leaf")
    else: 
        print("Intermediate")
    print("Level",node.level)
    if(not node.leaf):
        range_of_values=' '.join(map(lambda x:str(x),attributes_possible_values[node.constraint[0]][:node.constraint[1]]))
        #we concatinate the values less than the (constraint[1]=delimter=values of the split) from the range of possible values for that feature  
        print("Feature",attributes_names[node.constraint[0]],range_of_values)
    print("Gini",node.Gini)
    return

def print_tree(root,attributes_possible_values,attributes_names):
    #root = the root node of the tree define the tree
    #print The Whole Tree in BFS style 
    queue=[]
    queue.append(root)
    while(queue):
        current_node=queue.pop(0)
        print_node(current_node,attributes_possible_values,attributes_names)
        if(not current_node.leaf):
            queue.append(current_node.children[0])
            queue.append(current_node.children[1])
    
def get_nbr_leafs(root): 
    #root = the root node of the tree define the tree
    #return number of leafs in a tree 
    #BFS traversal  if leaf, count it , else add the children in the queue 
    nbr_leafs=0
    queue=[]
    queue.append(root)
    while(queue):
        current_node=queue.pop(0)
        if(not current_node.leaf):
            queue.append(current_node.children[0])
            queue.append(current_node.children[1])
        else:
            nbr_leafs+=1
    return nbr_leafs





################################### NODE CLASS ################################################
class Node:
    max_level=0 #max level in the tree 

    def __init__(self,minNum,default_class,level,attributes,records,attributes_possible_values,root=0,right=0):
        self.id=level*2+right
        self.records=records #records of this nodes ( line of input file that fit the constraints till this node )
        self.root=root #Boolean if root or not 
        self.leaf=False #boolean if leaf or not 
        self.attributes_possible_values=attributes_possible_values
        self.constraint=[] #list of 2 element [decision Attribute index, delimiter (split value)]
        self.children=[] #list of 2 node objects if the node not leaf 
        self.gain_info=0 #the max Gain info we achieve with best split 
        self.minNum = minNum #minimum number of recored per node
        self.attributes=attributes  #remaining attributes to use as decision attributes to split 
        self.default_class = default_class #the default class value 
        self.entropy=0 #Entropy  value of the node 
        self.best_split_records=[] #list of 2 elements, each is a list of records of the 1st class and 2nd class after the split  
                                   #best_split_records=[[left_class_records],[right_class_records]]
        self.my_class=self.default_class # node class (we need it only if leaf )
        self.level=level# node level 
        Node.max_level=max(level,Node.max_level)#we always update the class Attribute max_level everytime we add a new node 
        
        self.class_cardinal=[0,0] #a list of 2 int values , representing the cardinal of records of this node of the two classes of the target  
        for line in self.records: 
            if (line[-1]==0): 
                #if target class = 0 
                self.class_cardinal[0]+=1
            else:
                #if target class = 1 
                self.class_cardinal[1]+=1
        
        if(not records):
            self.Gini=None
            self.entropy=None
        else:
            self.Gini=1-((self.class_cardinal[0]/len(self.records))**2+(self.class_cardinal[1]/len(self.records))**2)
            self.entropy=-(self.class_cardinal[0]/len(self.records)*log2(self.class_cardinal[0]/len(self.records))+self.class_cardinal[1]/len(self.records)*log2(self.class_cardinal[1]/len(self.records)))

        ####Check the type of node 
        if(len(self.records)<self.minNum ): 
            #if nbr_of records < minNum  => class of the node is the majorty class
            self.leaf=True
            self.my_class=self.major_class()
        elif(self.all_records_same_class()):
            #if all records has the same class  => class of the node that same class 
            self.leaf=True
            self.my_class=self.records[0][-1]
        elif(len(self.attributes)==0):
            #if attributes list is empty => class of the node is the majorty class
            self.leaf=True
            self.my_class=self.major_class()
        elif(self.leaf==False):
            if(records):
                self.best_split_records=self.find_best_split()
            #self.find_best_split() update the self.constraint and return records of the left node 
            #and right node after the split that maximize the information gain 


    def find_best_split(self):
        #Take as input the current node (self)
        #return  the records of the right/left node after splitting the records on to fit the constraint that maximizes the gain_info  
        #(this function update the constraint too)
        best_split_att=-1 #best spliting attribute = best decision attribute eg: Feature A 
        best_split_delimiter=-1 # best splitting value  eg: if A take values in [0,1,2,3,4,5] we can say A<=2 and  2 is the delimiter 
        best_gain_info=-1 #best gain of information achieved after trying all possible  desicion attribute and all the correspending spliting values  
        class_1_records=[] # records of left child (class 1 eg A<=2) 
        class_2_records=[] #records of right child (class 2 eg A>2)
        for attribute in self.attributes:
            for delimiter in range(1,max(2,len(self.attributes_possible_values[attribute]))):
                Att_class_1=self.attributes_possible_values[attribute][:delimiter] #eg att_class1= [0,1,2] in the case of A<=2
                records_class_1=[] # will contain records fitting the constraint (A<=2)
                cardinal_target_class_1=[0,0] # number of  0 and 1 in the traget attribute of records of the first class (A<=2)
                Att_calss_2=self.attributes_possible_values[attribute][delimiter:]#eg att_class2= [3,4,5] in the case of A<=2
                records_class_2=[] # will contain records not fitting the constraint (A<=2)
                cardinal_target_class_2=[0,0] # number of  0 and 1 in the traget attribute of records of the second class (A>2)
                for line in self.records:
                    if(line[attribute] in Att_class_1):
                        records_class_1.append(line)
                        if(line[-1]==0):
                            cardinal_target_class_1[0]+=1
                        else:
                            cardinal_target_class_1[1]+=1
                    else:
                        records_class_2.append(line)
                        if(line[-1]==0):
                            cardinal_target_class_2[0]+=1
                        else:
                            cardinal_target_class_2[1]+=1
                entropy_class_1=0 # will remain zero if the split genrate a left child with no records else it will be updated if we have records on the left child 
                entropy_class_2=0 # will remain zero if the split genrate a  right child with no records else it will be updated if we have records  on the right child 

                if(records_class_1):
                    entropy_class_1=-(cardinal_target_class_1[0]/len(records_class_1)*log2(cardinal_target_class_1[0]/len(records_class_1))+cardinal_target_class_1[1]/len(records_class_1)*log2(cardinal_target_class_1[1]/len(records_class_1)))
                if(records_class_2):
                    entropy_class_2=-(cardinal_target_class_2[0]/len(records_class_2)*log2(cardinal_target_class_2[0]/len(records_class_2))+cardinal_target_class_2[1]/len(records_class_2)*log2(cardinal_target_class_2[1]/len(records_class_2)))
                entropy_split=self.entropy-(len(records_class_1)/len(self.records)*entropy_class_1+len(records_class_2)/len(self.records)*entropy_class_2)
                #print("##########",self.level,self.id,attribute,delimiter,entropy_split)
                if(entropy_split>=best_gain_info):
                    best_split_att=attribute
                    best_split_delimiter=delimiter
                    best_gain_info=entropy_split
                    class_1_records=records_class_1
                    class_2_records=records_class_2
        #update node attributes after determining the best split.
        self.constraint.append(best_split_att) 
        self.constraint.append(best_split_delimiter)
        self.gain_info=best_gain_info
        
        #return records of the left/right Child node 
        return(class_1_records,class_2_records)
                

    def all_records_same_class(self):
        #return if all the records in a node are of the same target class
        target_attribute=[line[-1] for line in self.records]
        return len(set(target_attribute))==1
    def major_class(self):
        #return the major target class in the records of a node if tie return default value 
        if(self.class_cardinal[0] == self.class_cardinal[1]):
            return self.default_class
        elif(self.class_cardinal[0] > self.class_cardinal[1]):
            return 0
        else:
            return 1
