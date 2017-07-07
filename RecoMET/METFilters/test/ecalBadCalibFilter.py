import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag (process.GlobalTag, 'auto:run2_mc')
process.GlobalTag = GlobalTag (process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6')

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    outputCommands = cms.untracked.vstring('drop *', 'keep *_ecalBadCalibFilter*_*_*' )
)
process.endpath= cms.EndPath(process.out)


## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/MINIAODSIM/NoPU_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/02758D78-52C0-E611-B027-0025905B8576.root'
      #'root://cms-xrd-global.cern.ch//store/data/Run2016D/ZeroBias/MINIAOD/03Feb2017-v1/100000/0057FDCB-28EC-E611-BB28-02163E019BAA.root'
    )
)

## Add PAT jet collection based on the above-defined ak4PFJetsCHS
process.p = cms.Path()

process.load("RecoMET.METFilters.ecalBadCalibFilter_cfi")
process.ecalBadCalibFilter.taggingMode = True
process.ecalBadCalibFilter.debug = True
#process.ecalBadCalibFilterEMin25 = process.ecalBadCalibFilter.clone( 
#    EBminet        = cms.double(25.),
#    EEminet        = cms.double(25.)
#    )
#process.ecalBadCalibFilterEMin75 = process.ecalBadCalibFilter.clone( 
#    EBminet        = cms.double(75.),
#    EEminet        = cms.double(75.)
#    )
process.p += process.ecalBadCalibFilter
#process.p += process.ecalBadCalibFilterEMin25
#process.p += process.ecalBadCalibFilterEMin75

## Adapt primary vertex collection
process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True), # while the timing of this is not reliable in unscheduled mode, it still helps understanding what was actually run
        allowUnscheduled = cms.untracked.bool(True)
)
