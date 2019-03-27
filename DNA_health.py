#!/bin/python3

import math
import os
import random
import re
import sys

parent  = 0
outlink = 1
suflink = 2
child_n = 3
dup_val = 4
trie_len = 0

def build_trie():
    n = int(input())
    genes = input().rstrip()
    health = input().rstrip()

    lib = {}
    trie = []
    root = [None, None, None, {}]
    trie.append(root)
    i = 0

    for gene, val in zip(genes.split(), health.split()):
        if gene not in lib:
            trie, lib = add_word(trie, lib, gene, i, int(val))
        else:
            node = trie[lib[gene]]
            node[dup_val][i] = int(val)
        i += 1

    trie = add_suffixes(trie)
    return trie

def add_word(trie, lib, word, pos, val):
    #init tree with root
    global trie_len
    node = trie[0]
    idx = 0

    # Add gene if not in lib
    for c in word:
        if c not in node[child_n]:
            # Create new node with pointer to parent temp_node[0]
            temp_node = [idx, None, None, {}]
            # Update Parent node's child
            trie_len += 1
            node[child_n][c] = trie_len
            trie.append(temp_node)
        
        idx = node[child_n][c]
        node = trie[idx]

    if len(node) == dup_val: # Value position doesn't exist
        node.append({pos: val})
    else:
        node[dup_val][pos] = val

    # add gene in lib
    lib[word] = idx

    return trie, lib

def add_suffixes(trie):
    q = []
    temp = trie[0]
    for key in temp[child_n]: # loop through all child nodes
        trie[temp[child_n][key]][suflink] = 0 # set nodes sufflink to root
        q.append(trie[temp[child_n][key]])

    while len(q) > 0:
        temp = q.pop(0)
        for key in temp[child_n]: # loop through all child nodes
            #Fill in Suffix Links
            temp_suff = trie[temp[suflink]]
            while True:
                if key in temp_suff[child_n]:
                    trie[temp[child_n][key]][suflink] = temp_suff[child_n][key]
                    break
                elif temp_suff[0] is None: # if Root node
                    trie[temp[child_n][key]][suflink] = 0
                    break
                else:
                    temp_suff = trie[temp_suff[suflink]]
            
            #Fill in Output Links
            temp_out = trie[trie[temp[child_n][key]][suflink]]

            if len(temp_out) is 5: # Pattern exists
                trie[temp[child_n][key]][outlink] = trie[temp[child_n][key]][suflink]
            else:
                trie[temp[child_n][key]][outlink] = temp_out[outlink]

            q.append(trie[temp[child_n][key]])
    
    return trie

def search(trie, string, start, stop):
    temp = trie[0]
    total = 0
    for c in string:
        while c not in temp[child_n]:
            if temp[parent] is None:
                break
            else:
                temp = trie[temp[suflink]]
        
        if c in temp[child_n]:
            temp = trie[temp[child_n][c]]

        if len(temp) is 5:
            for pos in temp[dup_val]:
                if pos >= start and pos <= stop:
                    total += temp[dup_val][pos]
        
        temp_out = temp
        while temp_out[outlink] is not None:
            temp_out = trie[temp_out[outlink]]
            for pos in temp_out[dup_val]:
                if pos >= start and pos <= stop:
                    total += temp_out[dup_val][pos]
        
    return total

if __name__ == '__main__':
    Tree = build_trie()

    s = int(input())
    min = sys.maxsize
    max = 0

    for s_itr in range(s):
        firstLastd = input().split()
        first = int(firstLastd[0])
        last = int(firstLastd[1])
        d = firstLastd[2]

        total = search(Tree, d, first, last)
        if total < min:
            min = total

        if total > max:
            max = total
    
    print (str(min) + " " + str(max))

