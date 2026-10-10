#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:37:32 2021

@author: kendrick shepherd
"""

import sys

import Geometry_Operations as geom

# Determine the unknown bars next to this node
def UnknownBars(node):
    bars_next_to_this_node = node.bars
    unknown_bars = []
    for bar in bars_next_to_this_node:
        if not bar.is_computed:
            unknown_bars.append(bar)
    return unknown_bars

# Determine if a node if "viable" or not
def NodeIsViable(node):
    unk_bars = UnknownBars(node)
    if 0 < len(unk_bars) and len(unk_bars) <= 2:
        return True
    else:
        return False
    
def UnitVector(node, bar):
    vector = geom.BarNodeToVector(node, bar)
    length = geom.VectorTwoNorm(vector)

    if length == 0:
        raise ValueError(f"Zero-length bar {bar.idx}")

    return vector[0] / length, vector[1] / length


# Sum all known forces acting on a node
def KnownForces(node):
    fx = node.GetNetXForce()
    fy = node.GetNetYForce()

    for bar in node.bars:
        if bar.is_computed:
            ux, uy = UnitVector(node, bar)

            fx += bar.axial_load * ux
            fy += bar.axial_load * uy

    return fx, fy


# Solve a node with one unknown bar
def SumOfForcesInLocalX(node, local_x_bar):
    fx, fy = KnownForces(node)

    ux, uy = UnitVector(node, local_x_bar)

    # Project the known forces onto the unknown bar
    force = -(fx * ux + fy * uy)

    local_x_bar.SetAxialLoad(force)
    local_x_bar.is_computed = True

    return force


# Solve a node with two unknown bars
def SumOfForcesInLocalY(node, unknown_bars):
    fx, fy = KnownForces(node)

    bar1, bar2 = unknown_bars

    ux1, uy1 = UnitVector(node, bar1)
    ux2, uy2 = UnitVector(node, bar2)

    # Solve the x and y equilibrium equations
    determinant = ux1 * uy2 - uy1 * ux2

    if abs(determinant) < 1e-12:
        raise ValueError(
            f"Cannot solve joint {node.idx}: "
            "unknown bars are parallel"
        )

    force1 = (-fx * uy2 + fy * ux2) / determinant
    force2 = (fx * uy1 - fy * ux1) / determinant

    bar1.SetAxialLoad(force1)
    bar1.is_computed = True

    bar2.SetAxialLoad(force2)
    bar2.is_computed = True

    return force1, force2


# Perform the method of joints on the structure
def IterateUsingMethodOfJoints(nodes, bars):

    while any(not bar.is_computed for bar in bars):
        progress = False

        for node in nodes:
            unknown_bars = UnknownBars(node)

            if len(unknown_bars) == 1:
                SumOfForcesInLocalX(
                    node, unknown_bars[0]
                )
                progress = True

            elif len(unknown_bars) == 2:
                SumOfForcesInLocalY(
                    node, unknown_bars
                )
                progress = True

        if not progress:
            unresolved = [
                bar.idx for bar in bars
                if not bar.is_computed
            ]

            raise ValueError(
                f"Could not solve bars {unresolved}"
            )

    return