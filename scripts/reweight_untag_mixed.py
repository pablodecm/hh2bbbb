#!/usr/bin/env python 

import ROOT
from ROOT import ExtEvent as Event
from ROOT import TChain, BasicSelector,  vector
from ROOT import TH1, TFile

from di_higgs.hh2bbbb.samples_25ns import mc_samples

base_dir = "reweight_untag_mixed/"

inEllipse = True 
freeJetTagged = False 
isMC = True

tfile = TFile("estimate_btag_prob_mixed/ratio.root")
h_ratio = tfile.Get("ratio")

TH1.AddDirectory(False)

hlt_paths_data = ["HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v",
                  "HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v",
                  "HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v",
                  "HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v",
                  "HLT_HH4bAll"]

hlt_paths_mc = ["HLT_BIT_HLT_QuadJet45_TripleCSV0p5_v",
                "HLT_BIT_HLT_QuadJet45_DoubleCSV0p5_v",
                "HLT_BIT_HLT_DoubleJet90_Double30_TripleCSV0p5_v",
                "HLT_BIT_HLT_DoubleJet90_Double30_DoubleCSV0p5_v",
                "HLT_HH4bAll"]

hlt_paths = hlt_paths_mc if isMC else hlt_paths_data
hlt_paths_v = vector("string")()
for hlt_path in hlt_paths: hlt_paths_v.push_back(hlt_path)

hlt_paths_or = hlt_paths[0:1] +  hlt_paths[2:3] 
hlt_paths_or_v = vector("string")()
for hlt_path in hlt_paths_or: hlt_paths_or_v.push_back(hlt_path)

to_process = [("HHTo4B_SM", 25000),("TTJets", -1 )]
for name, n_events in to_process:
    isHH = False
    selector = BasicSelector(Event)(0, hlt_paths_v, isHH,
                                    hlt_paths_or_v, inEllipse,
                                    freeJetTagged, h_ratio)
    tchain = TChain("tree")
    tchain.Add(mc_samples[name]["lustre_path"])
    print "processing {} sample".format(name)
    if (n_events < 0):
        tchain.Process(selector, "ofile="+base_dir+name+".root")
    else:
        tchain.Process(selector, "ofile="+base_dir+name+".root", n_events)
