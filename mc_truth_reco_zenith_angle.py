import ROOT
from ROOT import TFile, TDirectory, TTree, TH1D, TCanvas, TH2C
#import matplotlib.pyplot as pyplt
#import cppyy
import numpy as np
import math as m
#import ProtoDUNETruthUtils

# /Users/muyuanhe/Desktop/Research/Lisa_1/code     copy this address when running
### Open the file
f = TFile("NNBarAtm_hA_LFG_noCCTaus_30749278_0_20200327T220101_anatree.root","READ")#get file
t = f.Get("analysistree/anatree")#get tree
n = t.GetEntries() # n = 8000

### Create canvas
# c1 = TCanvas('c1', 'neutrino vertex x/y/z in cm')
# xbin, xmin, xmax = 400, 0, 399 # cos of angle ranges from -1 to 1, with 1 being 0 degree(particle going down)
#
# h1 = TH1D("h1", "numuCC_pmtrack", xbin, xmin, xmax)
# h1.GetXaxis().SetTitle("length of track(cm)")
# h2 = TH1D("h2", "numuCC_pandoraTrack", xbin, xmin, xmax)
# h2.GetXaxis().SetTitle("length of track(cm)")
# h3 = TH1D("h3", "number_pmtrack", 50, 0, 49)
# h3.GetXaxis().SetTitle("number of tracks per event")
# h4 = TH1D("h4", "number_pandoraTrack", 50, 0, 49)
# h4.GetXaxis().SetTitle("number of tracks per event")

binN = 100
xmin2, xmax2 = 0, 99
ymin2, ymax2 = 0, 99 # y axis for pmtrack
c2 = TCanvas("c2", "2D histo numuCC pmtrack vs pandoraTrack")
h5 = TH2C("h5", "2D hist comparison", binN, xmin2, xmax2, binN, ymin2, ymax2)
h5.GetYaxis().SetTitle("length of numuCC track of pandoraTrack (cm)")
h5.GetXaxis().SetTitle("length of numuCC track of pmtrack (cm)")


nucc_length_list_pmtrack = []
nucc_length_list_pandoraTrack = []
arr1 = np.arange(n)
for i in arr1: # for each entry
    t.GetEntry(i)
    for evt in np.arange(t.mcevts_truth): # only 1 event
        #print(t.nuPDG_truth[evt], "     ", t.ccnc_truth[evt])
        templ = [] # pmtrack
        templ2 = [] # pandoraTrack
        if t.nuPDG_truth[evt] == 14 and t.ccnc_truth[evt] == 0: # vmu_cc
            #print("found one")
            for j in np.arange(t.ntracks_pmtrack):
                dx = t.trkendx_pmtrack[j] - t.trkstartx_pmtrack[j]
                dy = t.trkendy_pmtrack[j] - t.trkstarty_pmtrack[j]
                dz = t.trkendz_pmtrack[j] - t.trkstartz_pmtrack[j]
                l1 = m.sqrt(dx ** 2 + dy ** 2 + dz ** 2) # length of track
            for k in np.arange(t.ntracks_pandoraTrack):
                dx2 = t.trkendx_pandoraTrack[k] - t.trkstartx_pandoraTrack[k]
                dy2 = t.trkendy_pandoraTrack[k] - t.trkstarty_pandoraTrack[k]
                dz2 = t.trkendz_pandoraTrack[k] - t.trkstartz_pandoraTrack[k]
                l2 = m.sqrt(dx2**2 + dy2**2 + dz2**2) # length of track
                #print(l)
                templ.append(l1) # pmtrack
                templ2.append(l2) # pandoraTrack
        #print(len(templ))
        #print(len(templ2))
        if len(templ) != 0:
            #print(len(templ)) # number of tracks in 1 event
            nucc_length_list_pmtrack.append(max(templ)) # put the longest track into the list, assume this track to be muon track
            #h3.Fill(len(templ))
        if len(templ2) != 0:
            nucc_length_list_pandoraTrack.append(max(templ2))
            #h4.Fill(len(templ2))

#print(nucc_length_list)
for x, y in zip(nucc_length_list_pmtrack, nucc_length_list_pandoraTrack):
    h5.Fill(x, y)
# for length in nucc_length_list_pmtrack:
#     #h1.Fill(length)
# for length2 in nucc_length_list_pandoraTrack:
#     #h2.Fill(length2)
    # for j in np.arange(t.geant_list_size): # list of all geant particles
    #     #print("mc track id: ", t.TrackId[j])
    #     #print(t.Mother[j]) # track ID of mother particle
    #     #print(t.pdg[j]) # what particle is this
    #     #print("daughter:", t.NumberDaughters[j]) # most of them do not have daughters.
    #     #print(t.MCTruthIndex[j]) # all 0s
    #     for k in np.arange(t.ntracks_pmtrack):
    #         #print("pmtrack id: ", t.trkId_pmtrack[k])
    #         # if j == t.trkPFParticleID_pmtrack[k]:
    #         #     print("found a match")
    #         print("pm_track", trkId_pmtrack[k])
    #         print("mc_track", TrackId[k])



#L1 = np.zeros((n, 100))
# L1 = []
# arr1 = np.arange(n)
# a = 0
# for i in arr1:
#     t.GetEntry(i)

#     #print(a)
#     #print("first for", t.trkPFParticleID_pmtrack)
#     #print(t.trkhasPFParticle_pmtrack)
#     for j in np.arange(t.ntracks_pmtrack):
#         print("trkPFPID pmtrack: ", t.trkPFParticleID_pmtrack[j]) #only has -1
#         print("trkPFPID pandora: ", t.trkPFParticleID_pandoraTrack[j]) # again, all -1
#         print("pandora track: ", t.trkId_pandoraTrack[j])
#         print("trkidtruth: ", t.trkidtruth_pandoraTrack[j])
#         # t.truthUtil.GetMCParticleFromRecoTrack(thisTrack, 0, 1) #truthUtil isn't in ttree
#         #print(t.trkhasPFParticle_pmtrack[j])# only has -1
#         #print("second for", t.trkPFParticleID_pmtrack[j])
#
#     a += 1


#print("MC particle: ", t.no_primaries)   # 0
# for i in arr1:
#     t.GetEntry(i)
      #determine if it is nucc event
#     #print("MC particle 2: ", t.no_primaries)
#     #print(t.hit_trkKey)
#     # Truth
#     #print("number of mc tracks:", t.no_mctracks)
#     arr2 = np.arange(t.mcevts_truth) #2, 3, 10, 24, ... multiple types
#     #print("track ID: ", t.TrackId)
#     for j in arr2:



#         #print("track ID: ", t.TrackId[j])
#         print("pm track particle ID", t.trkPFParticleID_pmtrack)
#         #h1.Fill(t.nuvtxx_truth[j])
#         #if t.nuPDG_truth[j] == 14: # only when particles are numu
#         #print(t.hit_trkKey)
#         a = t.nu_dcosx_truth[j]
#         b = t.nu_dcosy_truth[j]
#         c = t.nu_dcosz_truth[j]
#         #print("start location truth: ", t.nuvtxx_truth[j], " ", t.nu_dcosx_truth[j])
#         #else:
#         #    continue # next iteration of the loop
#         # Below is for zenith angle
#         if b == 0  and a**2 + c**2 == 0: # Should be small amount
#             pass
#         elif b == 0 and a**2 + c**2 != 0:
#             h1.Fill(0) # cos(90)
#             #L1[i][j] = np.array([i, j, t.nuvtxx_truth[j], t.nu_dcosx_truth[j], 0])
#             #L1.append((t.trkId[j], 0))
#         else:
#             zenith_angle = np.arctan(m.sqrt(a ** 2 + c ** 2) / b)
#             # zenith_angle = np.degrees(zenith_angle)
#             cos_zenith = np.cos(zenith_angle)
#             #L1.append((t.trkId[j], zenith_angle))
#             #h1.Fill(cos_zenith)
#         #print(L1)

            #L1[i][j] = np.array([i, j, t.nuvtxx_truth[j], t.nu_dcosx_truth[j], cos_zenith])
    # t.GetEntry(i)
    # Reconstructed
    # for e in range(t.ntracks_pmtrack):
    #     print(t.trkenddcosx_pmtrack[e])
# L2 = []
# L3 = []
# for i in arr1:
#     t.GetEntry(i)
#     for k in np.arange(t.ntracks_pandoraTrack):
#         x1 = t.trkendx_pandoraTrack[k] - t.trkstartx_pandoraTrack[k]
#         y1 = t.trkendy_pandoraTrack[k] - t.trkstarty_pandoraTrack[k]
#         z1 = t.trkendz_pandoraTrack[k] - t.trkstartz_pandoraTrack[k]
#         print("trkidtruth_pmtrack: ",t.trkidtruth_pmtrack[k])
#         #print("trkId_pandoraTrack: ", t.trkId_pandoraTrack[k])
#         #print("trkKey_pandoraTrack: ", t.trkKey_pandoraTrack[k])
#         if y1 == 0 and x1**2 + z1**2 == 0:
#             pass
#         elif y1 == 0 and x1**2 + z1**2 != 0:
#             h2.Fill(0) # cos(pi/2) = 0
#             #L2.append()
#             #L2.extend((i, k, t.nuvtxx_truth[k], t.nu_dcosx_truth[k], 0))
#         else:
#             zenith_angle1 = np.arctan(m.sqrt(x1**2 + z1**2)/y1)
#             cos_zenith1 = np.cos(zenith_angle1)
#             #print("cos_zenith1", cos_zenith1)
#             #print("h2 is filled: ", cos_zenith1)
#             h2.Fill(cos_zenith1)
#             #L2.extend((i, k, t.nuvtxx_truth[k], t.nu_dcosx_truth[k], cos_zenith1))
    #t.GetEntry(i)
    # for l in np.arange(t.ntracks_pmtrack):
    #     x2 = t.trkenddcosx_pmtrack[l] - t.trkstartdcosx_pmtrack[l]
    #     y2 = t.trkenddcosy_pmtrack[l] - t.trkstartdcosy_pmtrack[l]
    #     z2 = t.trkenddcosz_pmtrack[l] - t.trkstartdcosz_pmtrack[l]
    #     #print("trkId_pmtrack: ", t.trkId_pmtrack[l])
    #     if y2 == 0 and x2 ** 2 + z2 ** 2 == 0:
    #         pass
    #     elif y2 == 0 and x2 ** 2 + z2 ** 2 != 0:
    #         h3.Fill(0)
    #         #L3.extend((i, l, t.nuvtxx_truth[l], t.nu_dcosx_truth[l], 0))
    #     else:
    #         zenith_angle2 = np.arctan(m.sqrt(x2 ** 2 + z2 ** 2) / y2)
    #         cos_zenith2 = np.cos(zenith_angle2)
    #         #print("h3 is filled: ", cos_zenith2)
    #         h3.Fill(cos_zenith2)
    #         #L3.extend((i, l, t.nuvtxx_truth[l], t.nu_dcosx_truth[l], cos_zenith2))


# h1.Draw()
# h1.SetLineColor(ROOT.kRed)
# h2.Draw("same")
# h2.SetLineColor(ROOT.kBlue)
# h3.Draw()
# h3.SetLineColor(ROOT.kRed)
# h4.Draw("same")
# h4.SetLineColor(ROOT.kBlue)
h5.Draw("colz")


# c1.Update()
# c1.SaveAs("number_of_tracks.root")
c2.Update()
c2.SaveAs("2D_numuCC_pmtrack_pandoraTrack.root")
