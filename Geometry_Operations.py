#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:25:01 2021

@author: kendrick shepherd
"""

import math
import numpy as np
import sys

# length of the beam
def Length(bar):
    vector = BarNodeToVector(bar.init_node, bar)
    length = VectorTwoNorm(vector)
    
    return length

# Find two norm (magnitude) of a vector
def VectorTwoNorm(vector):
    value=0
    for val in vector:
        value = value + val**2
    
    #returning the norm of the vector
    return math.sqrt(value)

# Find a shared node between two bars
def FindSharedNode(bar_1,bar_2):
    if(bar_1.init_node==bar_2.init_node):
        return bar_1.init_node
    elif(bar_1.init_node==bar_2.end_node):
        return bar_1.init_node
    elif(bar_1.end_node==bar_2.end_node):
        return bar_2.end_node
    else:
        sys.exit("Error: No shared nodes")

# Given a bar and a node on that bar, find the other node
def FindOtherNode(node,bar):
    if (bar.end_node == node):
        return bar.init_node
    elif (bar.init_node == node):
        return bar.end_node
    else:
        sys.exit("Node on bar doesn't exist")

# Find a vector from input node (of the input bar) in the direction of the bar
def BarNodeToVector(origin_node,bar):
    #getting the locations of the origin and other nodes from classes for use
    #of finding the vector of the bar
    [origin_x,origin_y] = origin_node.location
    other_node = FindOtherNode(origin_node, bar)
    [other_x,other_y] = other_node.location
    
    #getting the vector from the nodes and returning it
    vec = [other_x-origin_x, other_y-origin_y]
    return vec

# Convert to bars that meet at a node into vectors pointing away from that node
def BarsToVectors(bar_1,bar_2):
    shared_node = FindSharedNode(bar_1,bar_2)
    vec_1 = BarNodeToVector(shared_node,bar_1)
    vec_2 = BarNodeToVector(shared_node,bar_2)
    return vec_1,vec_2

# Cross product of two vectors
def TwoDCrossProduct(vec1,vec2):
    #using numpy we can use a simple np.cross
    cross = np.cross(vec1,vec2)
    return cross

# Dot product of two vectors
def DotProduct(vec1,vec2):
    #using numpy we can use np.dot()
    dot = np.dot(vec1,vec2)
    return dot

# Cosine of angle from local x vector direction to other vector
def CosineVectors(local_x_vec,other_vec):
    dot = DotProduct(local_x_vec,other_vec)
    normLocal = VectorTwoNorm(local_x_vec)
    normOther = VectorTwoNorm(other_vec)
    cos = (dot/(normLocal*normOther))
    return cos

# Sine of angle from local x vector direction to other vector
def SineVectors(local_x_vec,other_vec):
    cross = TwoDCrossProduct(local_x_vec,other_vec)
    normLocal = VectorTwoNorm(local_x_vec)
    normOther = VectorTwoNorm(other_vec)
    sin = (cross/(normLocal*normOther))
    return sin

# Cosine of angle from local x bar to the other bar
def CosineBars(local_x_bar,other_bar):
    vec_1,vec_2 = BarsToVectors(local_x_bar,other_bar)
    cos = CosineVectors(vec_1,vec_2)
    return cos

# Sine of angle from local x bar to the other bar
def SineBars(local_x_bar,other_bar):
    vec_1,vec_2 = BarsToVectors(local_x_bar,other_bar)
    sin = SineVectors(vec_1,vec_2)
    return sin