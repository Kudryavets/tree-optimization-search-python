# Tree-Optimization-Search-Python

----

This is the attempt to solve [optimizing look-up problem](https://www.hackerrank.com/contests/quora-haqathon/challenges/ontology) in python 
via trees and recursion.

## Problem
There is a corpus of topics represented hierarchically. Each topic has a number of questions associated with it. In the same time each topic is 
a generalization of it's children topics and all their questions can be considered as its own questions. The task is to find how many 
questions among questions of a certain topic match a pattern.

## Solution
The tested solution is to build a tree of topics with questions tied to nodes. Then traverse a tree recursively to find needed topic
and recursively count matching questions from this topic and it's children. Trees are implemented in Python without using external libraries.
All computations are consecutive.

The algorithm has three parts:
1. Building a tree of topics
2. Filling the tree with questions for topics
3. Querying the tree about the patterns for certain topics

Let's consider them one by one.
To **build a tree** we should:
1. parse flat representation of topic hierarchy in python objects via coercing to json and parsing to dict
2. get the name of the root topic and json object of it's children
3. create a node with topic name and all children names in the branch
4. iterate by children creating a tree node for every one of them
5. Repeat steps 3 and 4 while topic has children

To **fill a tree** with questions we need to find a node associated with certain question and add question to it:
1. ask if node is the target one by comparing their names
2. iterate by children asking if child's branch contains target topic until find one
3. repeat steps 1 and 2 until find the needed node
4. attach question to it

To **query a tree** we need to find a node stated in the query and count matching the pattern questions from this node and it's children:
1. find needed node using steps 1 to 3 from the previous part
2. count questions matching the pattern in this node
3. iterate by children counting questions matching the pattern in the child node
4. repeat steps 2 and 3 while node has children
5. sum all counts

## Results
Results of testing are not the best. Solution works pretty fast on 20000 topics / 20000 questions / 20000 queries. 
But 100000 topics / 100000 questions / 100000 queries make one wait for near ten seconds on my laptop. I also found out that python is not 
optimized for tail recursion functions. In several cases of very deep nested trees I have experienced 
`RecursionError: maximum recursion depth exceeded`. Most of the found advices suggest not to use recursion at all or increase recursion limit 
which is not working for me.
