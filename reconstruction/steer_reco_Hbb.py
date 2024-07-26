from Gaudi.Configuration import *

from Configurables import LcioEvent, EventDataSvc, MarlinProcessorWrapper
from k4MarlinWrapper.parseConstants import *
algList = []
evtsvc = EventDataSvc()


CONSTANTS = {
}

parseConstants(CONSTANTS)

read = LcioEvent()
read.OutputLevel = INFO
read.Files = ["input_file.slcio"]
algList.append(read)

DD4hep = MarlinProcessorWrapper("DD4hep")
DD4hep.OutputLevel = INFO
DD4hep.ProcessorType = "InitializeDD4hep"
DD4hep.Parameters = {
                     "DD4hepXMLFile": ["/opt/ilcsoft/muonc/detector-simulation/geometries/MuColl_v1/MuColl_v1.xml"],
                     "EncodingStringParameterName": ["GlobalTrackerReadoutID"]
                     }

AIDA = MarlinProcessorWrapper("AIDA")
AIDA.OutputLevel = INFO
AIDA.ProcessorType = "AIDAProcessor"
AIDA.Parameters = {
                   "Compress": ["1"],
                   "FileName": ["histograms"],
                   "FileType": ["root"]
                   }

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = INFO
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
                          "HowOften": ["1"]
                          }

LCIOWriter_all = MarlinProcessorWrapper("LCIOWriter_all")
LCIOWriter_all.OutputLevel = INFO
LCIOWriter_all.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_all.Parameters = {
                             "DropCollectionNames": [],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": [],
                             "KeepCollectionNames": [],
                             "SplitFileSizekB": ["996147"],
                             "LCIOOutputFile": ["Output_REC.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }

LCIOWriter_light = MarlinProcessorWrapper("LCIOWriter_light")
LCIOWriter_light.OutputLevel = INFO
LCIOWriter_light.ProcessorType = "LCIOOutputProcessor"
LCIOWriter_light.Parameters = {
                               "DropCollectionNames": ["MCParticle", "MCPhysicsParticle"],
                               "DropCollectionTypes": ["SimTrackerHit", "Track", "LCRelation", "MCParticle"],
                               "FullSubsetCollections": [],
                               "KeepCollectionNames": ["SiTracks"],
                               "LCIOOutputFile": ["Output_DST.slcio"],
                               "LCIOWriteMode": ["WRITE_NEW"]
                               }

VXDBarrelDigitiser = MarlinProcessorWrapper("VXDBarrelDigitiser")
VXDBarrelDigitiser.OutputLevel = INFO
VXDBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDBarrelDigitiser.Parameters = {
                                 "CorrectTimesForPropagation": ["true"],
                                 "IsStrip": ["false"],
                                 "ResolutionT": ["0.03"],
                                 "ResolutionU": ["0.005"],
                                 "ResolutionV": ["0.005"],
                                 "SimTrackHitCollectionName": ["VertexBarrelCollection"],
                                 "SimTrkHitRelCollection": ["VXDBarrelHitsRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TimeWindowMax": ["0.15"],
                                 "TimeWindowMin": ["-0.09"],
                                 "TrackerHitCollectionName": ["VXDBarrelHits"],
                                 "UseTimeWindow": ["true"]
                                 }

VXDEndcapDigitiser = MarlinProcessorWrapper("VXDEndcapDigitiser")
VXDEndcapDigitiser.OutputLevel = INFO
VXDEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDEndcapDigitiser.Parameters = {
                                 "CorrectTimesForPropagation": ["true"],
                                 "IsStrip": ["false"],
                                 "ResolutionT": ["0.03"],
                                 "ResolutionU": ["0.005"],
                                 "ResolutionV": ["0.005"],
                                 "SimTrackHitCollectionName": ["VertexEndcapCollection"],
                                 "SimTrkHitRelCollection": ["VXDEndcapHitsRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TimeWindowMax": ["0.15"],
                                 "TimeWindowMin": ["-0.09"],
                                 "TrackerHitCollectionName": ["VXDEndcapHits"],
                                 "UseTimeWindow": ["true"]
                                 }

ITBarrelDigitiser = MarlinProcessorWrapper("ITBarrelDigitiser")
ITBarrelDigitiser.OutputLevel = INFO
ITBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
ITBarrelDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["InnerTrackerBarrelCollection"],
                                "SimTrkHitRelCollection": ["ITBarrelHitsRelations"],
                                "SubDetectorName": ["InnerTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["ITBarrelHits"],
                                "UseTimeWindow": ["true"]
                                }

ITEndcapDigitiser = MarlinProcessorWrapper("ITEndcapDigitiser")
ITEndcapDigitiser.OutputLevel = INFO
ITEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
ITEndcapDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["InnerTrackerEndcapCollection"],
                                "SimTrkHitRelCollection": ["ITEndcapHitsRelations"],
                                "SubDetectorName": ["InnerTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["ITEndcapHits"],
                                "UseTimeWindow": ["true"]
                                }

OTBarrelDigitiser = MarlinProcessorWrapper("OTBarrelDigitiser")
OTBarrelDigitiser.OutputLevel = INFO
OTBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
OTBarrelDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["OuterTrackerBarrelCollection"],
                                "SimTrkHitRelCollection": ["OTBarrelHitsRelations"],
                                "SubDetectorName": ["OuterTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["OTBarrelHits"],
                                "UseTimeWindow": ["true"]
                                }

OTEndcapDigitiser = MarlinProcessorWrapper("OTEndcapDigitiser")
OTEndcapDigitiser.OutputLevel = INFO
OTEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
OTEndcapDigitiser.Parameters = {
                                "CorrectTimesForPropagation": ["true"],
                                "IsStrip": ["false"],
                                "ResolutionT": ["0.06"],
                                "ResolutionU": ["0.007"],
                                "ResolutionV": ["0.09"],
                                "SimTrackHitCollectionName": ["OuterTrackerEndcapCollection"],
                                "SimTrkHitRelCollection": ["OTEndcapHitsRelations"],
                                "SubDetectorName": ["OuterTrackers"],
                                "TimeWindowMax": ["0.3"],
                                "TimeWindowMin": ["-0.18"],
                                "TrackerHitCollectionName": ["OTEndcapHits"],
                                "UseTimeWindow": ["true"]
                                }

ECalBarrelDigi = MarlinProcessorWrapper("ECalBarrelDigi")
ECalBarrelDigi.OutputLevel = INFO
ECalBarrelDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalBarrelCollection"],
    "outputHitCollections": ["EcalBarrelCollectionDigi"],
    "outputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalBarrelReco = MarlinProcessorWrapper("ECalBarrelReco")
ECalBarrelReco.OutputLevel = INFO
ECalBarrelReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalBarrelCollectionDigi"],
    "inputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["EcalBarrelCollectionRec"],
    "outputRelationCollections": ["EcalBarrelRelationsSimRec"]
}

ECalPlugDigi = MarlinProcessorWrapper("ECalPlugDigi")
ECalPlugDigi.OutputLevel = INFO
ECalPlugDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalPlugDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalPlugCollection"],
    "outputHitCollections": ["ECalPlugCollectionDigi"],
    "outputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalPlugReco = MarlinProcessorWrapper("ECalPlugReco")
ECalPlugReco.OutputLevel = INFO
ECalPlugReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalPlugReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["ECalPlugCollectionDigi"],
    "inputRelationCollections": ["ECalPlugRelationsSimDigi"],
    "outputHitCollections": ["ECalPlugCollectionRec"],
    "outputRelationCollections": ["ECalPlugRelationsSimRec"]
}

ECalEndcapDigi = MarlinProcessorWrapper("ECalEndcapDigi")
ECalEndcapDigi.OutputLevel = INFO
ECalEndcapDigi.ProcessorType = "RealisticCaloDigiSilicon"
ECalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalEndcapCollection"],
    "outputHitCollections": ["EcalEndcapCollectionDigi"],
    "outputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10"],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

ECalEndcapReco = MarlinProcessorWrapper("ECalEndcapReco")
ECalEndcapReco.OutputLevel = INFO
ECalEndcapReco.ProcessorType = "RealisticCaloRecoSilicon"
ECalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.00641222630095"],
    "calibration_layergroups": ["41"],
    "inputHitCollections": ["EcalEndcapCollectionDigi"],
    "inputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["EcalEndcapCollectionRec"],
    "outputRelationCollections": ["EcalEndcapRelationsSimRec"]
}

HCalBarrelDigi = MarlinProcessorWrapper("HCalBarrelDigi")
HCalBarrelDigi.OutputLevel = INFO
HCalBarrelDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004925"],
    "inputHitCollections": ["HCalBarrelCollection"],
    "outputHitCollections": ["HcalBarrelCollectionDigi"],
    "outputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalBarrelReco = MarlinProcessorWrapper("HCalBarrelReco")
HCalBarrelReco.OutputLevel = INFO
HCalBarrelReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0287783798145"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalBarrelCollectionDigi"],
    "inputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["HcalBarrelCollectionRec"],
    "outputRelationCollections": ["HcalBarrelRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalEndcapDigi = MarlinProcessorWrapper("HCalEndcapDigi")
HCalEndcapDigi.OutputLevel = INFO
HCalEndcapDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalEndcapCollection"],
    "outputHitCollections": ["HcalEndcapCollectionDigi"],
    "outputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalEndcapReco = MarlinProcessorWrapper("HCalEndcapReco")
HCalEndcapReco.OutputLevel = INFO
HCalEndcapReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalEndcapCollectionDigi"],
    "inputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["HcalEndcapCollectionRec"],
    "outputRelationCollections": ["HcalEndcapRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

HCalRingDigi = MarlinProcessorWrapper("HCalRingDigi")
HCalRingDigi.OutputLevel = INFO
HCalRingDigi.ProcessorType = "RealisticCaloDigiScinPpd"
HCalRingDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalRingCollection"],
    "outputHitCollections": ["HCalRingCollectionDigi"],
    "outputRelationCollections": ["HCalRingRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    #"timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    #"timingResolution": ["0"],
    #"timingWindowMax": ["10"],
    #"timingWindowMin": ["-0.5"]
}

HCalRingReco = MarlinProcessorWrapper("HCalRingReco")
HCalRingReco.OutputLevel = INFO
HCalRingReco.ProcessorType = "RealisticCaloRecoScinPpd"
HCalRingReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0285819096797"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HCalRingCollectionDigi"],
    "inputRelationCollections": ["HCalRingRelationsSimDigi"],
    "outputHitCollections": ["HCalRingCollectionRec"],
    "outputRelationCollections": ["HCalRingRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MuonDigitiser = MarlinProcessorWrapper("MuonDigitiser")
MuonDigitiser.OutputLevel = INFO
MuonDigitiser.ProcessorType = "DDSimpleMuonDigi"
MuonDigitiser.Parameters = {
                            "CalibrMUON": ["70.1"],
                            "MUONCollections": ["YokeBarrelCollection", "YokeEndcapCollection"],
                            "MUONOutputCollection": ["MuonHits"],
                            "MaxHitEnergyMUON": ["2.0"],
                            "MuonThreshold": ["1e-06"],
                            "RelationOutputCollection": ["MuonHitsRelations"]
                            }

FilterDL_VXDB = MarlinProcessorWrapper("FilterDL_VXDB")
FilterDL_VXDB.OutputLevel = INFO
FilterDL_VXDB.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDB.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.0", "35.0", "2", "3", "1.7", "18.0", "4", "5", "1.5", "10.0", "6", "7", "1.4", "6.5"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDBarrelHits"],
                            "OutputCollection": ["VXDBarrelHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

FilterDL_VXDE = MarlinProcessorWrapper("FilterDL_VXDE")
FilterDL_VXDE.OutputLevel = INFO
FilterDL_VXDE.ProcessorType = "FilterDoubleLayerHits"
FilterDL_VXDE.Parameters = {
                            "DoubleLayerCuts": ["0", "1", "2.2", "8.0", "2", "3", "1.4", "2.8", "4", "5", "0.86", "0.7", "6", "7", "0.7", "0.3"],
                            "FillHistograms": ["false"],
                            "InputCollection": ["VXDEndcapHits"],
                            "OutputCollection": ["VXDEndcapHits_DLFiltered"],
                            "SubDetectorName": ["Vertex"]
                            }

OverlayFull = MarlinProcessorWrapper("OverlayFull")
OverlayFull.OutputLevel = INFO
OverlayFull.ProcessorType = "OverlayTimingRandomMix"
OverlayFull.Parameters = {
    "PathToMuPlus": ["/path/to/muminus/"],
    "PathToMuMinus": ["/path/to/muplus/"],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MergeMCParticles": ["false"],
    "NumberBackground": ["192"] #Magic number assumes 20 phi clones of each MC particle
}

OverlayIP = MarlinProcessorWrapper("OverlayIP")
OverlayIP.OutputLevel = INFO
OverlayIP.ProcessorType = "OverlayTimingGeneric"
OverlayIP.Parameters = {
    "AllowReusingBackgroundFiles": ["true"],
    "BackgroundFileNames": ["/path/to/pairs.slcio"],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.5", "15.",
        "VertexEndcapCollection", "-0.5", "15.",
        "InnerTrackerBarrelCollection", "-0.5", "15.",
        "InnerTrackerEndcapCollection", "-0.5", "15.",
        "OuterTrackerBarrelCollection", "-0.5", "15.",
        "OuterTrackerEndcapCollection", "-0.5", "15.",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalPlugCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "HCalRingCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "Delta_t": ["10000"],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MCPhysicsParticleCollectionName": ["MCPhysicsParticles_IP"],
    "MergeMCParticles": ["true"],
    "NBunchtrain": ["1"],
    "NumberBackground": ["1"],
    "PhysicsBX": ["1"],
    "Poisson_random_NOverlay": ["false"],
    "RandomBx": ["false"],
    "StartBackgroundFileIndex": ["0"],
    "TPCDriftvelocity": ["0.05"]
}

CKFTracking = MarlinProcessorWrapper("CKFTracking")
CKFTracking.OutputLevel = INFO
CKFTracking.ProcessorType = "ACTSSeededCKFTrackingProc"
CKFTracking.Parameters = {
    "CKF_Chi2CutOff": ["10"],
    "CKF_NumMeasurementsCutOff": ["1"],
    "MatFile": ["/opt/ilcsoft/muonc/ACTSTracking/v1.0.0/data/material-maps.json"],
    "PropagateBackward": ["False"],
    "RunCKF": ["True"],
    "SeedFinding_CollisionRegion": ["3.5"],
    "SeedFinding_DeltaRMax": ["60"],
    "SeedFinding_DeltaRMin": ["2"],
    "SeedFinding_DeltaRMaxBottom": ["50"],
    "SeedFinding_DeltaRMaxTop": ["50"],
    "SeedFinding_DeltaRMinBottom": ["5"],
    "SeedFinding_DeltaRMinTop": ["2"],
    "SeedFinding_ImpactMax": ["3"],
    "SeedFinding_MinPt": ["500"],
    "SeedFinding_RMax": ["150"],
    "SeedFinding_ZMax": ["500"],
    "SeedFinding_RadLengthPerSeed": ["0.1"],
    "SeedFinding_zBottomBinLen": ["1"],
    "SeedFinding_zTopBinLen": ["1"],
    "SeedFinding_phiBottomBinLen": ["1"],
    "SeedFinding_phiTopBinLen": ["1"],
    "SeedFinding_SigmaScattering": ["3"],
    "SeedingLayers": [
        "13", "2", "13", "6", "13", "10", "13", "14", 
        "14", "2", "14", "6", "14", "10", "14", "14", 
        "15", "2", "15", "6", "15", "10", "15", "14",
        ],
    "TGeoFile": ["/opt/ilcsoft/muonc/ACTSTracking/v1.0.0/data/MuColl_v1.root"],
    "TrackCollectionName": ["AllTracks"],
    "TrackerHitCollectionNames": ["VBTrackerHits", "IBTrackerHits", "OBTrackerHits", "VETrackerHits", "IETrackerHits", "OETrackerHits"],
    "CaloFace_Radius": ["1500"],
    "CaloFace_Z": ["2307"]
}

TrackDeduplication = MarlinProcessorWrapper("TrackDeduplication")
TrackDeduplication.OutputLevel = INFO
TrackDeduplication.ProcessorType = "ACTSDuplicateRemoval"
TrackDeduplication.Parameters = {
                                 "InputTrackCollectionName": ["AllTracks"],
                                 "OutputTrackCollectionName": ["SiTracks"]
                                 }


DDMarlinPandora = MarlinProcessorWrapper("DDMarlinPandora")
DDMarlinPandora.OutputLevel = INFO
DDMarlinPandora.ProcessorType = "DDPandoraPFANewProcessor"
DDMarlinPandora.Parameters = {
                              "ClusterCollectionName": ["PandoraClusters"],
                              "CreateGaps": ["false"],
                              "CurvatureToMomentumFactor": ["0.00015"],
                              "D0TrackCut": ["200"],
                              "D0UnmatchedVertexTrackCut": ["5"],
                              "DigitalMuonHits": ["0"],
                              "ECalBarrelNormalVector": ["0", "0", "1"],
                              "ECalCaloHitCollections": ["EcalBarrelCollectionRec", "EcalEndcapCollectionRec", "EcalPlugCollectionRec"],
                              "ECalMipThreshold": ["0.5"],
                              "ECalScMipThreshold": ["0"],
                              "ECalScToEMGeVCalibration": ["1"],
                              "ECalScToHadGeVCalibrationBarrel": ["1"],
                              "ECalScToHadGeVCalibrationEndCap": ["1"],
                              "ECalScToMipCalibration": ["1"],
                              "ECalSiMipThreshold": ["0"],
                              "ECalSiToEMGeVCalibration": ["1"],
                              "ECalSiToHadGeVCalibrationBarrel": ["1"],
                              "ECalSiToHadGeVCalibrationEndCap": ["1"],
                              "ECalSiToMipCalibration": ["1"],
                              "ECalToEMGeVCalibration": ["1.02373335516"],
                              "ECalToHadGeVCalibrationBarrel": ["1.24223718397"],
                              "ECalToHadGeVCalibrationEndCap": ["1.24223718397"],
                              "ECalToMipCalibration": ["181.818"],
                              "EMConstantTerm": ["0.01"],
                              "EMStochasticTerm": ["0.17"],
                              "FinalEnergyDensityBin": ["110."],
                              "HCalBarrelNormalVector": ["0", "0", "1"],
                              "HCalCaloHitCollections": ["HcalBarrelCollectionRec", "HcalEndcapCollectionRec", "HcalRingCollectionRec"],
                              "HCalMipThreshold": ["0.3"],
                              "HCalToEMGeVCalibration": ["1.02373335516"],
                              "HCalToHadGeVCalibration": ["1.01799349172"],
                              "HCalToMipCalibration": ["40.8163"],
                              "HadConstantTerm": ["0.03"],
                              "HadStochasticTerm": ["0.6"],
                              "InputEnergyCorrectionPoints": [],
                              "KinkVertexCollections": ["KinkVertices"],
                              "LayersFromEdgeMaxRearDistance": ["250"],
                              "MCParticleCollections": ["MCParticle"],
                              "MaxBarrelTrackerInnerRDistance": ["200"],
                              "MaxClusterEnergyToApplySoftComp": ["2000."],
                              "MaxHCalHitHadronicEnergy": ["1000000"],
                              "MaxTrackHits": ["5000"],
                              "MaxTrackSigmaPOverP": ["0.15"],
                              "MinBarrelTrackerHitFractionOfExpected": ["0"],
                              "MinCleanCorrectedHitEnergy": ["0.1"],
                              "MinCleanHitEnergy": ["0.5"],
                              "MinCleanHitEnergyFraction": ["0.01"],
                              "MinFtdHitsForBarrelTrackerHitFraction": ["0"],
                              "MinFtdTrackHits": ["0"],
                              "MinMomentumForTrackHitChecks": ["0"],
                              "MinTpcHitFractionOfExpected": ["0"],
                              "MinTrackECalDistanceFromIp": ["0"],
                              "MinTrackHits": ["0"],
                              "MuonBarrelBField": ["-1.34"],
                              "MuonCaloHitCollections": ["MuonHits"],
                              "MuonEndCapBField": ["0.01"],
                              "MuonHitEnergy": ["0.5"],
                              "MuonToMipCalibration": ["19607.8"],
                              "NEventsToSkip": ["0"],
                              "NOuterSamplingLayers": ["3"],
                              "OutputEnergyCorrectionPoints": [],
                              "PFOCollectionName": ["PandoraPFOs"],
                              "PandoraSettingsXmlFile": ["PandoraSettings/PandoraSettingsDefault.xml"],
                              "ProngVertexCollections": ["ProngVertices"],
                              "ReachesECalBarrelTrackerOuterDistance": ["-100"],
                              "ReachesECalBarrelTrackerZMaxDistance": ["-50"],
                              "ReachesECalFtdZMaxDistance": ["1"],
                              "ReachesECalMinFtdLayer": ["0"],
                              "ReachesECalNBarrelTrackerHits": ["0"],
                              "ReachesECalNFtdHits": ["0"],
                              "RelCaloHitCollections": ["CaloHitsRelations", "MuonHitsRelations"],
                              "RelTrackCollections": ["SiTracks_Relations"],
                              "ShouldFormTrackRelationships": ["1"],
                              "SoftwareCompensationEnergyDensityBins": ["0", "2.", "5.", "7.5", "9.5", "13.", "16.", "20.", "23.5", "28.", "33.", "40.", "50.", "75.", "100."],
                              "SoftwareCompensationWeights": ["1.61741", "-0.00444385", "2.29683e-05", "-0.0731236", "-0.00157099", "-7.09546e-07", "0.868443", "1.0561", "-0.0238574"],
                              "SplitVertexCollections": ["SplitVertices"],
                              "StartVertexAlgorithmName": ["PandoraPFANew"],
                              "StartVertexCollectionName": ["PandoraStartVertices"],
                              "StripSplittingOn": ["0"],
                              "TrackCollections": ["SiTracks"],
                              "TrackCreatorName": ["DDTrackCreatorCLIC"],
                              "TrackStateTolerance": ["0"],
                              "TrackSystemName": ["DDKalTest"],
                              "UnmatchedVertexTrackMaxEnergy": ["5"],
                              "UseEcalScLayers": ["0"],
                              "UseNonVertexTracks": ["1"],
                              "UseOldTrackStateCalculation": ["0"],
                              "UseUnmatchedNonVertexTracks": ["0"],
                              "UseUnmatchedVertexTracks": ["1"],
                              "V0VertexCollections": ["V0Vertices"],
                              "YokeBarrelNormalVector": ["0", "0", "1"],
                              "Z0TrackCut": ["200"],
                              "Z0UnmatchedVertexTrackCut": ["5"],
                              "ZCutForNonVertexTracks": ["250"]
                              }

PFOSelection = MarlinProcessorWrapper("PFOSelection")
PFOSelection.OutputLevel = INFO
PFOSelection.ProcessorType = "CLICPfoSelector"
PFOSelection.Parameters = {
                           "ChargedPfoLooseTimingCut": ["3"],
                           "ChargedPfoNegativeLooseTimingCut": ["-1"],
                           "ChargedPfoNegativeTightTimingCut": ["-0.5"],
                           "ChargedPfoPtCut": ["0"],
                           "ChargedPfoPtCutForLooseTiming": ["4"],
                           "ChargedPfoTightTimingCut": ["1.5"],
                           "CheckKaonCorrection": ["0"],
                           "CheckProtonCorrection": ["0"],
                           "ClusterLessPfoTrackTimeCut": ["10"],
                           "CorrectHitTimesForTimeOfFlight": ["0"],
                           "DisplayRejectedPfos": ["1"],
                           "DisplaySelectedPfos": ["1"],
                           "FarForwardCosTheta": ["0.975"],
                           "ForwardCosThetaForHighEnergyNeutralHadrons": ["0.95"],
                           "ForwardHighEnergyNeutralHadronsEnergy": ["10"],
                           "HCalBarrelLooseTimingCut": ["20"],
                           "HCalBarrelTightTimingCut": ["10"],
                           "HCalEndCapTimingFactor": ["1"],
                           "InputPfoCollection": ["PandoraPFOs"],
                           "KeepKShorts": ["1"],
                           "MaxMomentumForClusterLessPfos": ["2"],
                           "MinECalHitsForTiming": ["5"],
                           "MinHCalEndCapHitsForTiming": ["5"],
                           "MinMomentumForClusterLessPfos": ["0.5"],
                           "MinPtForClusterLessPfos": ["0.5"],
                           "MinimumEnergyForNeutronTiming": ["1"],
                           "Monitoring": ["0"],
                           "MonitoringPfoEnergyToDisplay": ["1"],
                           "NeutralFarForwardLooseTimingCut": ["2"],
                           "NeutralFarForwardTightTimingCut": ["1"],
                           "NeutralHadronBarrelPtCutForLooseTiming": ["3.5"],
                           "NeutralHadronLooseTimingCut": ["2.5"],
                           "NeutralHadronPtCut": ["0"],
                           "NeutralHadronPtCutForLooseTiming": ["8"],
                           "NeutralHadronTightTimingCut": ["1.5"],
                           "PhotonFarForwardLooseTimingCut": ["2"],
                           "PhotonFarForwardTightTimingCut": ["1"],
                           "PhotonLooseTimingCut": ["2"],
                           "PhotonPtCut": ["0"],
                           "PhotonPtCutForLooseTiming": ["4"],
                           "PhotonTightTimingCut": ["1"],
                           "PtCutForTightTiming": ["0.75"],
                           "SelectedPfoCollection": ["SelectedPandoraPFOs"],
                           "UseClusterLessPfos": ["1"],
                           "UseNeutronTiming": ["0"]
                           }

FastJetProcessor = MarlinProcessorWrapper("FastJetProcessor")
FastJetProcessor.OutputLevel = INFO
FastJetProcessor.ProcessorType = "FastJetProcessor"
FastJetProcessor.Parameters = {
    "algorithm": ["antikt_algorithm", "0.4"],
    "clusteringMode": ["Inclusive", "5"],
    "jetOut": ["JetOut"],
    "recParticleIn": ["SelectedPandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

algList.append(AIDA)
algList.append(EventNumber)
algList.append(DD4hep)
# algList.append(OverlayFull)   # Full BX BIB overlay
# algList.append(OverlayIP)     # Incoherent pairs full BX BIB overlay
algList.append(VXDBarrelDigitiser)
algList.append(VXDEndcapDigitiser)
algList.append(ITBarrelDigitiser)
algList.append(ITEndcapDigitiser)
algList.append(OTBarrelDigitiser)
algList.append(OTEndcapDigitiser)
# algList.append(FilterDL_VXDB)  # Config.OverlayNotFalse
# algList.append(FilterDL_VXDE)  # Config.OverlayNotFalse
algList.append(ECalBarrelDigi)
algList.append(ECalBarrelReco)
algList.append(ECalPlugDigi)
algList.append(ECalPlugReco)
algList.append(ECalEndcapDigi)
algList.append(ECalEndcapReco)
algList.append(HCalBarrelDigi)
algList.append(HCalBarrelReco)
algList.append(HCalEndcapDigi)
algList.append(HCalEndcapReco)
algList.append(HCalRingDigi)
algList.append(HCalRingReco)
algList.append(MuonDigitiser)
algList.append(CKFTracking)
algList.append(TrackDeduplication)
algList.append(DDMarlinPandora)
algList.append(PFOSelection)
algList.append(FastJetProcessor)
algList.append(LCIOWriter_all)
algList.append(LCIOWriter_light)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax   = 10,
                ExtSvc = [evtsvc],
                OutputLevel=INFO
              )
