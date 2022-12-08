# Analysis based on LCTuple processor

The following command will convert events from the input file into a ROOT TTree.

```
Marlin steer_lctuple.xml > ntuple.log 2>&1
```

The resulting ntuple will be saved to `ntuple.root`


A simple macro can be used for analysis of the resulting TTree:

```
 root -l
 .L invariant_mass.C
 invariant_mass()
```

An integer argument can be passed to the `invariant_mass(arg)` function to choose the plot you want to see:

* `0` - number of reconstructed jets
* `1` - pseudorapidity of jets in the event
* `2` - transverse momentum of jets in the event
* `3` - phi of jets in the event
* `4` - invariant mass of jet pair associated to Higgs with highest pT
* `5` - invariant mass of jet pair associated to Higgs with lowest pT



