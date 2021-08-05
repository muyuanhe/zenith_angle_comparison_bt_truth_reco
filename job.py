import ROOT
from ROOT import TFile, TDirectory, TTree, TH1D, TCanvas, TH2C, TH2F, TH3F, TH3C
import numpy as np
import math as m
import sys, os
import time


#f = TFile("/pnfs/dune/tape_backed/dunepro/fardet-sp/root-tuple/2020/mc/out1/MC_Fall2019/30/28/13/01/NNBarAtm_hA_BR_kaonspm_noCCTaus_30796263_0_20200401T002940_anatree.root","READ")
f = TFile("/pnfs/dune/tape_backed/dunepro/fardet-sp/root-tuple/2020/mc/out1/MC_Fall2019/30/22/64/97/NNBarAtm_hA_BR_noCCTaus_30749665_0_20200327T220102_anatree.root", "READ")
#f = TFile("/pnfs/dune/tape_backed/dunepro/fardet-sp/root-tuple/2020/mc/out1/MC_Fall2019/30/28/13/01/NNBarAtm_hA_BR_kaonspm_noCCTaus_30662659_0_20200325T032037_anatree.root", "READ")
#f = TFile("/pnfs/dune/tape_backed/dunepro/fardet-sp/root-tuple/2020/mc/out1/MC_Fall2019/30/28/13/01/NNBarAtm_hA_BR_kaonspm_noCCTaus_30662702_0_20200325T032256_anatree.root", "READ")


t = f.Get("analysistree/anatree") #get tree

n = t.GetEntries()
#print("# of entries: ", n, "\n")

c1 = TCanvas('c1', 'zenith_angle_comparison')

xbin, xmin, xmax = 100, -5, 5 # cos of angle ranges from -1 to 1, with 1 being 0 degree(particle going down)

hpxpy3  = TH2F( 'hpxpy', 'pandora_lep_dcosy vs truth_dcosy', 20, -1, 1, 20, -1, 1 )

hpxpy3.GetXaxis().SetTitle("truth_dcosy")
hpxpy3.GetYaxis().SetTitle("pandora_lep_dcosy")

for i in np.arange(n): # loop over all entries
#	print(i, "th entry")
	t.GetEntry(i) # Every mcevts_truth is 1, 1 interaction in the spill
#	print("entry get")
#	print("PDG code: ", t.nuPDG_truth[0])
#	print("ccnc_truth: ", t.ccnc_truth[0])
		
	if t.nuPDG_truth[0] != 14 or t.ccnc_truth[0] != 0 or t.mode_truth[0]!=0: # Event: numuCC, Quasi-elastic/elastic
#		print(i, "\n")
		
		continue
#	print("first if continue  passed \n")
	for part in np.arange(t.no_primaries): # for each particle in this numuCC event)
		if abs(t.pdg[part]) != 13 or t.inTPCActive[part]!=1 or t.process_primary[part]!=1:
#			print("2")
			continue
#		print("second IF passed")
		for j in np.arange(t.ntracks_pandoraTrack):
			L = t.pathlen[part]
#			print("partlen: ", L, "\n")
			if t.trkId_pandoraTrack[j] != 1 or L < 50:
				continue
#			print("j: ", j, "\n")
#			print("third IF passed")
########################################## group selection ###########################################################
            ### not on diagnol
            # if abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) < 0.3: #match
            #     continue
            # if -0.3< t.lep_dcosy_truth[0]+ t.trkstartdcosy_pandoraTrack[j] < 0.3 and abs(t.lep_dcosy_truth[0])+ abs(t.trkstartdcosy_pandoraTrack[j])>0.4: #off diagnal
            #     continue
            # else:
            ###

            ### Right diagnol
            # if abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) < 0.3:
            ###

            ### wrong diagnol
            # if -0.3 < t.lep_dcosy_truth[0] + \
            #         t.trkstartdcosy_pandoraTrack[j] < 0.3 and abs(t.lep_dcosy_truth[0]) + abs(
            #         t.trkstartdcosy_pandoraTrack[j]) > 0.4:  # off diagnal
            ###

            ### In TPC length
            # if L_in_TPC > 400:
########################################################################################################################
				
#			print(j)
			#print(t.lep_dcosy_truth[0], "\n")
			hpxpy3.Fill(t.lep_dcosy_truth[0], t.trkstartdcosy_pandoraTrack[j])



hpxpy3.Draw("colz") #can also try option "E"
c1.Update()
c1.SaveAs("pandora_lep_dcosy_vs_truth_dcosy_2.root")
f2 = TFile('output.root', 'recreate')
hpxpy3.Write()
