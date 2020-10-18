
<h1 style="text-align:center">Decision Tree Implementation : 
</h1>
<img style="display: block; margin: auto;" alt="photo"  width="400" src="./images/Decision tree.png">
A Decision tree is a supervised machine learning tool used in classification problems to predict the class of an instance. It is a tree-like structure where internal nodes of the decision tree test an attribute of the instance and each subtree indicates the outcome of the attribute split. Leaf nodes indicate the class of the instance based on the model of the decision tree.

- Splits score: the splitting in each node can be based on : 
	- GINI score 
	- Entropy
	- Gain

- The best split is chosen based on the generelazation error of the tree , which we will use  to chose the best prune too.
 

- We implemented pruning  which  is compressing and optimizing a decision tree by removing subtrees that are uncritical and redundant to classify instances.




## Usage 
Open  ```Main.py``` and set the values of these variables : 
```
	- path_input_file	:Input file path 
	- attributes_names	:Namee of features in the input file (optional) 
	- minNum	 			:Min number of records in a node 
	- default_class		:The default target class
	- alpha 				:The pruning coefficient  
```
save ```main.py``` and run it 
```console 
$ python3 main.py 
```
## Output 
The decision tree is printed in the order of Breadth-first traversal following this format for each node :

		-Type	 : [Root,Intermediate,Leaf]
		-Level	 : Shortest  distance to the root 
		-Feautre : Feature name,Feature threshold 
		-Score	 : [Gini Score,Gain Score,Entropy]


