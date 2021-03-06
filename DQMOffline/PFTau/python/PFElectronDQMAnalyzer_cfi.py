import FWCore.ParameterSet.Config as cms

pfElectronDQMAnalyzer = cms.EDAnalyzer("PFCandidateDQMAnalyzer",
    InputCollection = cms.InputTag('pfAllElectrons'),
    MatchCollection = cms.InputTag('gensource'),
    BenchmarkLabel  = cms.string('PFElectronValidation/PFElecVsGenElec'),
    deltaRMax = cms.double(0.2),
    matchCharge = cms.bool(False),
    mode = cms.int32( 1 ),
    CreateReferenceHistos = cms.bool(True),
    ptMin = cms.double( 0.0 ),
    ptMax = cms.double( 999999 ),
    etaMin = cms.double(-10),
    etaMax = cms.double(10),
    phiMin = cms.double(-3.14),
    phiMax = cms.double(3.14),
# Histogram Parameters related to pt
    VariablePtBins  = cms.vdouble(0.,1.,2.,5.,10.,20.,50.,100.,200.,400.,1000.),
    PtHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(50),
      xMin = cms.double(0.0),
      xMax = cms.double(100.0)        
    ),
    DeltaPtHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(100),
      xMin = cms.double(-50.0),
      xMax = cms.double(50.0)        
    ),
    DeltaPtOvPtHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(200),
      xMin = cms.double(-1.0),
      xMax = cms.double(1.0)        
    ),
# Histogram Parameters related to Eta                               
    EtaHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(100),
      xMin = cms.double(-5.0),
      xMax = cms.double(5.0)        
    ),
    DeltaEtaHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(50),
      xMin = cms.double(-0.5),
      xMax = cms.double(0.5)        
    ),
# Histogram Parameters related to Phi                               
    PhiHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(100),
      xMin = cms.double(-3.1416),
      xMax = cms.double(3.1416)        
    ),
    DeltaPhiHistoParameter = cms.PSet(
      switchOn = cms.bool(True),
      nBin = cms.int32(50),
      xMin = cms.double(-0.5),
      xMax = cms.double(0.5)        
    ),
# Histogram Parameters related to Charge                               
    ChargeHistoParameter = cms.PSet(
      switchOn = cms.bool(False),
      nBin = cms.int32(3),
      xMin = cms.double(-1.5),
      xMax = cms.double(1.5)        
    ),
# parameter for event skim
    SkimParameter = cms.PSet(
      switchOn = cms.bool(False),
      maximumNumberToBeStored = cms.int32(100),
      lowerCutOffOnResolution = cms.double(-1.5),
      upperCutOffOnResolution = cms.double(1.5)
    )
)
