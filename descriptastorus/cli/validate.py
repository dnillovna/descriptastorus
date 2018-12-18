#!/usr/bin/env python
"""storus
see Description below
"""
from __future__ import print_function
from descriptastorus import DescriptaStore
from descriptastorus.descriptors import MakeGenerator
import argparse, os, shutil, time, random

import math, sys
from rdkit import rdBase
rdBase.DisableLog("rdApp.*")


parser = argparse.ArgumentParser()
parser.add_argument("storage",
                    help="directory in which to store the descriptors")

parser.add_argument("--samples", default=1000, type=int)

def main():
    opts = parser.parse_args()
    store = DescriptaStore(opts.storage)
    
    N = len(store)
    gen = store.getDescriptorCalculator()
    
    
    randomize=True
    if opts.samples == -1:
        randomize=False
        opts.samples = len(store)
    
    next = .05
    for i in range(opts.samples):
        if i and float(i)/opts.samples > next:
            print("Validated %2.2f%%"%(next*100))
            next += .05
        if randomize:
            idx = random.randint(0,N-1)
        else:
            idx = i
        
        v = store.descriptors().get(idx)
        smiles = store.molIndex().getMol(idx)
        name = None
        try:
            name = store.molIndex().getName(idx)
        except:
            pass
        
        res = gen.process(smiles)
        if res is None:
            assert v == tuple([0]*len(v))
            continue
        
        data = []
        
        for x in gen.process(smiles):
            if math.isnan(x): data.append(None)
            else: data.append(x)
        v2 = []
        for x in v:
            if math.isnan(x): v2.append(None)
            else: v2.append(x)
        assert v2 == data, "idx:%s smiles:%s name:%s \n%r\n\t%r"%(idx, smiles, name,
                                                                  v, data)
    
            
                
                
    
    
    
