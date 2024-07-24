#!/bin/bash
echo $HOSTNAME
echo $APPTAINER_NAME
echo $PWD
echo

echo "Sourcing setup scripts"
source /setup.sh
which ddsim
which Marlin
which k4run
echo

echo "Copying data from /ospool/uc-shared/project/"
export STASHCP=/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/23/current/el8-x86_64/usr/bin/stashcp
$STASHCP -d osdf:///ospool/uc-shared/project/futurecolliders/data/fmeloni/DataMuC_MuColl10_v0A/v2/reco/photonGun_E_250_1000/photonGun_E_250_1000_reco_0.slcio ./photonGun_E_250_1000_reco_0.slcio
ls -ltrh
anajob -m 10 photonGun_E_250_1000_reco_0.slcio
rm -f photonGun_E_250_1000_reco_0.slcio
echo

echo "Job complete"
