#!/usr/bin/env python 

import ROOT
from ROOT import VHBBEvent, ThinEvent, ExtEvent
from ROOT import TChain, BasicSelector,  vector
from ROOT import TH1, TFile

from di_higgs.hh2bbbb.samples_25ns import mc_samples

thinEvent = True 
thinEventPath = "skim/"

base_dir = "signal_region/"

max_events = -100
inEllipse = True 
freeJetTagged = True 
isMC = True

TH1.AddDirectory(False)

hlt_paths = ["HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v",
             "HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v",
             "HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v",
             "HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v",
             "HLT_HH4bAll"]

hlt_paths_v = vector("string")()
for hlt_path in hlt_paths: hlt_paths_v.push_back(hlt_path)

hlt_paths_or = hlt_paths[0:1] +  hlt_paths[2:3] 
hlt_paths_or_v = vector("string")()
for hlt_path in hlt_paths_or: hlt_paths_or_v.push_back(hlt_path)

mc_names = mc_samples.keys()
mc_names=[mc_name for mc_name in mc_names if 'HH' in mc_name]
for name in mc_names:
    isHH = False
    if "HH" in name: isHH = True
    if thinEvent:
        selector = BasicSelector(ExtEvent(ThinEvent))(0, hlt_paths_v, isHH,
                                                  hlt_paths_or_v, inEllipse,
                                                  freeJetTagged)
        tchain = TChain("tree")
        n_added = tchain.Add(thinEventPath+name+".root")
    else:    
        selector = BasicSelector(ExtEvent(VHBBEvent))(0, hlt_paths_v, isHH,
                                                  hlt_paths_or_v, inEllipse,
                                                  freeJetTagged)
        tchain = TChain("tree")
        n_added = tchain.Add(mc_samples[name]["lustre_path"])
    print "processing {} sample ( {} files)".format(name, n_added)
    if max_events > 0:
        tchain.Process(selector, "ofile="+base_dir+name+".root", max_events)
    else:
        tchain.Process(selector, "ofile="+base_dir+name+".root")

