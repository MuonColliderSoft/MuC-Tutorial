# Exercise on the simulation of events in GEANT4 using ILCSoft

In this exercise you are going to learn how to simulate and reconstruct events without beam-induced background within the ILCSoftware framework. You are going to learn how to extract the event ntuples and use them to analyze the event. 

The chosen signal is of `mu+ mu- -> H + neutrinos -> bb + neutrinos` at sqrt(s) = 1.5 TeV center of mass energy.  
To simulate the signal (only 1 event of H -> bb):

```
ddsim --steeringFile sim_steer_Hbb.py > sim.log 2>&1
```

It will produce the file mumu_H_bb.slcio as output.
