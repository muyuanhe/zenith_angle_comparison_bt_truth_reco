import ROOT
from ROOT import TFile, TDirectory, TTree, TH1D, TCanvas, TH2C, TH2F, TH3F, TH3C
import numpy as np
import math as m
import sys, os
import time
#from multiprocessing import Process

time_start = time.perf_counter()

def program(file):
    f = TFile(file,"READ")
    t = f.Get("analysistree/anatree") #get tree
    n = t.GetEntries()

    for i in np.arange(n): # loop over all entries
        t.GetEntry(i) # Every mcevts_truth is 1, 1 interaction in the spill
        if t.nuPDG_truth[0] != 14 or t.ccnc_truth[0] != 0 or t.mode_truth[0]!=0: # Event: numuCC, Quasi-elastic/elastic
            continue
        for part in np.arange(t.no_primaries): # for each particle in this numuCC event)
            if abs(t.pdg[part]) != 13 or t.inTPCActive[part]!=1 or t.process_primary[part]!=1:
                continue
            for j in np.arange(t.ntracks_pandoraTrack):
                L = t.pathlen[part]
                # L_pandora = m.sqrt((t.trkendx_pandoraTrack[j] - t.trkstartx_pandoraTrack[j])**2 + (t.trkendy_pandoraTrack[j] - t.trkstarty_pandoraTrack[j])**2 + (t.trkendz_pandoraTrack[j] - t.trkstartz_pandoraTrack[j])**2)
                if t.trkId_pandoraTrack[j] != 1 or L < 50:
                    continue
    ########################################## group selection ###########################################################
                ### not on diagnol
                # if abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) < 0.3: #match
                #     continue
                # if -0.3< t.lep_dcosy_truth[0]+ t.trkstartdcosy_pandoraTrack[j] < 0.3 and abs(t.lep_dcosy_truth[0])+ abs(t.trkstartdcosy_pandoraTrack[j])>0.4: #off diagnal
                #     continue
                # else:
                ###

                ### Right diagnol
                if abs(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j]) < 0.3:
                ###

                ### wrong diagnol
                # if -0.3 < t.lep_dcosy_truth[0] + \
                #         t.trkstartdcosy_pandoraTrack[j] < 0.3 and abs(t.lep_dcosy_truth[0]) + abs(
                #         t.trkstartdcosy_pandoraTrack[j]) > 0.4:  # off diagnal
                ###

                ### In TPC length
                # if L_in_TPC > 400:
    ########################################################################################################################

                    hpxpy3.Fill(t.lep_dcosy_truth[0], t.trkstartdcosy_pandoraTrack[j])
                    hpxpy4.Fill(t.lep_dcosy_truth[0] - t.trkstartdcosy_pandoraTrack[j])


                    # print("run", t.run) # Run Number All The Same: 30225954
                    # print("event: ", t.event) # Use event number to track ***
                    # print("lep_dcosy_truth vs pandoraTrack: ", t.lep_dcosy_truth[0], t.trkstartdcosy_pandoraTrack[j])

###################################     Main     #######################################################################

# c1 = TCanvas('c1', 'zenith_angle_comparison')
# hpxpy3 = TH2F('hpxpy', 'pandora_lep_dcosy vs truth_dcosy', 20, -1, 1, 20, -1, 1)
# hpxpy3.GetXaxis().SetTitle("lep_dcosy_truth")
# hpxpy3.GetYaxis().SetTitle("trkstartdcosy_pandoraTrack")

c2 = TCanvas('c2', 'resolution')
hpxpy4 = TH1D('hpxpy4', 'resolution', 40, -2, 2)
hpxpy4.GetXaxis().SetTitle("ep_dcosy_truth - trkstartdcosy_pandoraTrack")

#program("newfile.root")

# if __name__ == '__main__':
#     p = Process(target=program, args=("newfile.root",))
#     p.start()
#     p.join()
program("newfile.root")
# hpxpy3.Draw("colz") #can also try option "E"
hpxpy4.Draw("colz")

# c1.Update()
c2.Update()
# c1.SaveAs("file1_lepton_vs_pandoraTrack.root") # for hpxpy2
# c1.SaveAs("pandora_lep_dcosy_vs_truth_dcosy_2.root")
c2.SaveAs("resolution.root")

hpxpy4.Draw()
# for i in List:
#     print(i[0],",", i[1])
#     file1.write(str(i[0], i[1]))
# file1.close()
# histogram Drawing options below:
# https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html

# fout = open('pandora_lep_dcosy_vs_truth_dcosy.root', 'w')
# fout.write('Hello world')
# fout.close()
# f2 = TFile('output2.root', 'recreate')
# hpxpy3.Write()
f4 = TFile('resolutionoutput.root', 'recreate')
hpxpy4.Write()


time_end = time.perf_counter()
duration = time_end-time_start
print("Time used: ", duration)