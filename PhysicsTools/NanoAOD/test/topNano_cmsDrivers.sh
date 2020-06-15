PROD_TAG=v6-1-1

function runDriverMC () {
    cmsDriver.py NANO --python_filename topNano_${PROD_TAG}_$1_MC_cfg.py --fileout file:tree.root -s NANO --mc --conditions $2 --era $3 --eventcontent NANOAODSIM --datatier NANOAODSIM --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab=cms.untracked.bool(True)" --nThreads 2 -n -1 --no_exec
}

runDriverMC 2016 102X_mcRun2_asymptotic_v7      Run2_2016,run2_nanoAOD_94X2016
runDriverMC 2017 102X_mc2017_realistic_v7       Run2_2017,run2_nanoAOD_94XMiniAODv2
runDriverMC 2018 102X_upgrade2018_realistic_v20 Run2_2018,run2_nanoAOD_102Xv1

function runDriverData () {
    cmsDriver.py NANO  --python_filename topNano_${PROD_TAG}_$1_data_cfg.py --fileout file:tree.root -s NANO --data --conditions $2 --era $3 --eventcontent NANOAOD --datatier NANOAOD --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODoutput.fakeNameForCrab=cms.untracked.bool(True)" --nThreads 2 -n -1 --no_exec
}

runDriverData 2016    102X_dataRun2_v12 Run2_2016,run2_nanoAOD_94X2016
runDriverData 2017    102X_dataRun2_v12 Run2_2017,run2_nanoAOD_94XMiniAODv2
runDriverData 2018ABC 102X_dataRun2_v12 Run2_2018,run2_nanoAOD_102Xv1
runDriverData 2018D   102X_dataRun2_Prompt_v15 Run2_2018,run2_nanoAOD_102Xv1
