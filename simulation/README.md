#Exercise on the simulation and reconstruction events

#In this exercise you are going to learn how to simulate and reconstruct events without beam-induced background within the ILCSoftware framework. You are going to learn how to extract the event ntuples and use them to analyze the event. 

#The chosen signal is of mu+ mu- -> H + neutrinos -> bb + neutrinos at 1.5 TeV center of mass energy

#To simulate the signal (only 1 event of H to bb):

ddsim --steeringFile sim_steer_Hbb.py > sim.out 2>&1


#It will produce the file mumu_H_bb.slcio as output.
#To reconstruct the signal:

Marlin reco_steer_Hbb.xml > reco.out 2>&1


#It produces some outputs:
-Output_REC.slcio (collections) 
-Output_DST.slcio (collections subsample)
-hisograms.root (check histograms)

#To produce final ntuples for the analysis:


Marlin lctuple_steer.xml > ntuples.out 2>&1

#Final root file with ntuples: JetHistograms.root


#1000 events of double Higgs production are provided, and you can run a simple macro for the analysis:


#To run the macro:

 root -l
 .L invariant_mass.C
 invariant_mass()



The argument is used to chose the plot you want to see:
0: number of reconstructed jets
1: pseudorapidity of jets in the event
2: transverse momentum of jets in the event
3: phi of jets in the event
4: invariant mass of jet pair associated to Higgs with highest pT
5: invariant mass of jet pair associated to Higgs with lowest pT


#As example:  

root -l
 .L invariant_mass.C
 invariant_mass(4)

#the plot of the invariant mass of jet pair associated to Higgs with highest pT is shown


