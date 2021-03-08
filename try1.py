import ROOT
from ROOT import TFile, TDirectory, TTree, TH1D, TCanvas, TH2C, TH2F
import numpy as np
import math as m
import sys, os

# # Disable
# def blockPrint():
#     sys.stdout = open(os.devnull, 'w')
#     # Restore
#
# def enablePrint():
#     sys.stdout = sys.__stdout__


f = TFile("NNBarAtm_hA_LFG_noCCTaus_30749278_0_20200327T220101_anatree.root","READ")# 1st file I tried
#f = TFile("NNBarAtm_hA_LFG_noCCTaus_30749284_0_20200327T220116_anatree.root", "READ")# 2nd file
#f = TFile("NNBarAtm_hA_LFG_noCCTaus_30749304_0_20200327T220104_anatree.root", "READ")# 3rd file

t = f.Get("analysistree/anatree")#get tree
n = t.GetEntries() # n = 8000, 8000 spills

c1 = TCanvas('c1', 'zenith_angle_comparison')
xbin, xmin, xmax = 100, -5, 5 # cos of angle ranges from -1 to 1, with 1 being 0 degree(particle going down)
h1 = TH1D("h1", "cosy_truth - cosy_pmtrack", xbin, xmin, xmax)
h2 = TH1D("h2", "truth_lep", xbin, xmin, xmax)
h3 = TH1D("h3", "lep_pmtrack", xbin, xmin, xmax)
hpxpy1  = TH2F( 'hpxpy', 'truth_dcosy vs lep_dcosy', 20, -1, 1, 20, -1, 1 )
hpxpy2  = TH2F( 'hpxpy', 'pmtrack_dcosy vs lep_dcosy', 20, -1, 1, 20, -1, 1 )
hpxpy3  = TH2F( 'hpxpy', 'pmtrack_dcosy vs truth_dcosy', 20, -1, 1, 20, -1, 1 )

h1.GetXaxis().SetTitle("x")
h2.GetXaxis().SetTitle("x")
h3.GetXaxis().SetTitle("x")
hpxpy1.GetXaxis().SetTitle("lep_dcosy")
hpxpy1.GetYaxis().SetTitle("truth_dcosy")
hpxpy2.GetXaxis().SetTitle("lep_dcosy")
hpxpy2.GetYaxis().SetTitle("pmtrack_dcosy")
hpxpy3.GetXaxis().SetTitle("truth_dcosy")
hpxpy3.GetYaxis().SetTitle("pmtrack_dcosy")
# blockPrint()

for i in np.arange(n): # loop over all entries
    t.GetEntry(i) # Every mcevts_truth is 1, 1 interaction in the spill
    # print()
    # print("run number: ", t.run)
    # print("event number: ", t.event)
    # print()
    #print("Number of primaries: ", t.no_primaries)
    #print("list of all geant particles: ", t.geant_list_size) # size larger than no_primaries naturally
    if t.nuPDG_truth[0] == 14 and t.ccnc_truth[0] == 0 and t.mode_truth[0]==0:
        for part in np.arange(t.no_primaries):
            # print("pdg code of particle: ", t.pdg[part])
            # print("inTPCActive: ", t.inTPCActive[part]) # whether particle passed tpc boundary? yes=1, no=0
            # print("process_primary: ", t.process_primary[part]) # primary: 1, secondary: 0
            if abs(t.pdg[part]) == 13 and t.inTPCActive[part]==1 and t.process_primary[part]==1:
                # print("Spill # ", i)
                # print("Particle # ", part)
                #
                # print("trackID: ", t.TrackId[part]) # track ID assigned by GEANT4
                #
                # print("Mother: ", t.Mother[part]) # track ID of the mother particle
                # print("MCTruthIndex: ", t.MCTruthIndex[part]) # this geant particle comes from the neutrino
                    # interaction of the _truth variables with this index
                #for j in np.arange(t.ntracks_pmtrack):
                for j in np.arange(t.ntracks_pandoraTrack):
                    #if t.trkId_pmtrack[j] ==1: # which links to the primiary muon track
                    #if t.trkId_pandoraTrack[j] == 1 and abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) < 0.3: #match
                    #if t.trkId_pandoraTrack[j] == 1 and -0.3< t.lep_dcosy_truth[0]+ t.trkstartdcosy_pandoraTrack[j] < 0.3 and abs(t.lep_dcosy_truth[0])+ abs(t.trkstartdcosy_pandoraTrack[j])>0.4: #off diagnal
                    if t.trkId_pandoraTrack[j] == 1 and -0.3 > t.lep_dcosy_truth[0] + t.trkstartdcosy_pandoraTrack[j] and 0.3 < abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) :  # off diagnal
                        # print()
                        # print('found it')
                        # print('found it')
                        # print('found it')
                        # print("trkidtruth", t.trkidtruth_pmtrack[j])
                        # print("trkorigin", t.trkorigin_pmtrack[j])
                        # print("trkpdgtruth", t.trkpdgtruth_pmtrack[j])
                        # h1.Fill(t.nu_dcosy_truth[0] - t.trkstartdcosy_pmtrack[j])
                        # h2.Fill(t.lep_dcosy_truth[0] - t.nu_dcosy_truth[0])
                        # h3.Fill(t.lep_dcosy_truth[0] - t.trkstartdcosy_pmtrack[j])
                        # hpxpy1.Fill(t.lep_dcosy_truth[0], t.nu_dcosy_truth[0])
                        ### important below
                        #hpxpy2.Fill(t.lep_dcosy_truth[0], t.trkstartdcosy_pmtrack[j])
                        print("length, want larger than 100 cm: ")
                        print(m.sqrt(t.nuvtxx_truth[0]**2 + t.nuvtxy_truth[0]**2 + t.nuvtxz_truth[0]**2))
                        hpxpy2.Fill(t.lep_dcosy_truth[0], t.trkstartdcosy_pandoraTrack[j])

                        print("run", t.run)
                        print("event", t.event)

                        ### important above
                        # hpxpy3.Fill(t.nu_dcosy_truth[0], t.trkstartdcosy_pmtrack[j])

        # print()
'''
    if t.nuPDG_truth[0] == 14 and t.ccnc_truth[0] == 0: # the first(only) event, 14: V_mu, 0: cc -> V_muCC for all selected events
        print(i, "th spills:\n")
        print("ntracks_pmtrack: ", t.ntracks_pmtrack)
        print("ntracks_pandoraTrack: ", t.ntracks_pandoraTrack)
        print("length of TrackId(ntracks): ", len(t.TrackId)) # why is the length 15 or so ???????????
        print("no_primaries", t.no_primaries)
        #print("TrackId", t.TrackId[1]) # TrackId has only 1 track for VuCC
        #print("TrackId", t.TrackId[0]) # TrackId == 1
        truth_list = []
        pm_list = []
        pandora_list = []
        for i in np.arange(t.ntracks_pmtrack):
            print("pmtrack_id: ", t.trkId_pmtrack[i]) # primiary muon will always be ==1
            print("trkidtruth_pmtrack", t.trkidtruth_pmtrack[i])
            dy = t.trkenddcosy_pmtrack[i] - t.trkstartdcosy_pmtrack[i]
            #pm_list.append([t.trkidtruth_pmtrack[i], dy])
            #print("pmtrack", dy)
            print("trkpdgtruth_pmtrack: ", t.trkpdgtruth_pmtrack[i]) # pdg == 13: Muon track
        # for j in np.arange(len(t.TrackId)): # only 1 track, no need to loop
        print("\n")
        print("TrackId", t.TrackId[0])
        print("\n")
        #print("truth", t.nu_dcosy_truth[0])
        for k in np.arange(t.ntracks_pandoraTrack):
            dy = t.trkenddcosy_pandoraTrack[k] - t.trkstartdcosy_pandoraTrack[k]
            #print(dy)
            print("trkpdgtruth_pandoraTrack", t.trkpdgtruth_pandoraTrack[k]) # pdg == 13: Muon track
            print("pandoratrack_id: ", t.trkId_pandoraTrack[k])
            print("trkidtruth_pandoraTrack: ", t.trkidtruth_pandoraTrack[k])
        print("\n")

'''









# h1.Draw()
# h1.SetLineColor(ROOT.kRed)
# h2.Draw("same")
# h2.SetLineColor(ROOT.kBlue)
# h3.Draw("same")
# h3.SetLineColor(ROOT.kBlack)
#hpxpy1.Draw("colz")
hpxpy2.Draw("colz")
#hpxpy3.Draw("colz")
c1.Update()
#c1.SaveAs("lepton_vs_truth.png") # for hpxpy1
c1.SaveAs("file1_lepton_vs_pandoraTrack.png") # for hpxpy2
#c1.SaveAs("pmtrack_dcosy_vs_truth_dcosy.png")