#! /usr/bin/env python

from CRABAPI.RawCommand import crabCommand
import CRABClient.UserUtilities as crab

import json
import copy
import os
import argparse
import sys

# DAS client
from Utilities.General.cmssw_das_client import get_data as myDASclient

CMSSW_ROOT = os.path.join(os.environ['CMSSW_BASE'], 'src')
NANO_ROOT = os.path.join(os.environ['CMSSW_BASE'], 'src', 'PhysicsTools', 'NanoAOD')
PROD_TAG = "v6-1-1"

def retry(nattempts, exception=None):
    """
    Decorator allowing to retry an action several times before giving up.
    @params:
        nattempts  - Required: maximal number of attempts (Int)
        exception  - Optional: if given, only catch this exception, otherwise catch 'em all (Exception)
    """

    def tryIt(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < nattempts - 1:
                try:
                    return func(*args, **kwargs)
                except (exception if exception is not None else Exception):
                    attempts += 1
            return func(*args, **kwargs)
        return wrapper
    return tryIt

@retry(5)
def get_parent_DAS(dataset):
    """Retrieve parent dataset from DAS"""
    data = myDASclient("parent dataset=" + dataset)
    if data['status'] != 'ok':
        raise Exception("Failed retrieving parent dataset from DAS.\n{}".format(data))
    assert(len(data['data']) == 1)
    assert(len(data['data'][0]['parent']) == 1)
    return data['data'][0]['parent'][0]['name']


def get_options():
    """
    Parse and return the arguments provided by the user.
    """
    parser = argparse.ArgumentParser(description='Generate crab config files for multiple datasets.')

    parser.add_argument('-e', '--era', required=False, choices=['2016', '2017', '2018', '2018ABC', '2018D'], help='Choose specific era. If not specified, run on all eras')
    parser.add_argument('-d', '--datasets', nargs='*', help='Json file(s) with dataset list')
    parser.add_argument('-s', '--site', required=True, help='Site to which to write the output')
    parser.add_argument('-o', '--output', default='./', help='Folder in which to write the config files')

    return parser.parse_args()


def create_default_config(is_mc):
    config = crab.config()

    config.General.workArea = 'tasks'
    config.General.transferOutputs = True
    config.General.transferLogs = True
    config.JobType.allowUndistributedCMSSW = True # for slc7

    config.JobType.pluginName = 'Analysis'
    config.JobType.maxMemoryMB = 5000
    config.JobType.numCores = 2

    config.Data.inputDBS = 'global'
    config.Data.publication = True

    if is_mc:
        config.Data.splitting = 'EventAwareLumiBased'
        config.Data.unitsPerJob = 300000
    else:
        config.Data.splitting = 'LumiBased'
        config.Data.unitsPerJob = 650

    return config


def findPSet(pset):
    c = pset
    if not os.path.isfile(c):
        # Try to find the psetName file
        filename = os.path.basename(c)
        path = NANO_ROOT
        c = None
        for root, dirs, files in os.walk(path):
            if filename in files:
                c = os.path.join(root, filename)
                break
        if c is None:
            raise IOError('Configuration file %r not found' % filename)
    return os.path.abspath(c)


def writeCrabConfig(pset, dataset, is_mc, metadata, era, crab_config, site, output):
    c = copy.deepcopy(crab_config)

    c.JobType.psetName = pset

    name = metadata.pop('name')

    c.General.requestName = "TopNanoAOD{}_{}__{}".format(PROD_TAG, name, era)

    c.Data.outputDatasetTag = "TopNanoAOD{}_{}".format(PROD_TAG, era)
    c.Data.inputDataset = dataset
    c.Data.outLFNDirBase = '/store/user/{user}/topNanoAOD/{tag}/{era}/'.format(user=os.getenv('USER'), tag=PROD_TAG, era=era)
    c.Site.storageSite = site

    # customize if asked
    for attr,val in metadata.items():
        setattr(getattr(c, attr.split(".")[0]), attr.split(".")[1], val)

    print("Creating new task {}".format(c.General.requestName))

    # Create output file
    crab_config_file = os.path.join(output, 'crab_' + c.General.requestName + '.py')
    with open(crab_config_file, 'w') as f:
        f.write(str(c))

    print('Configuration file saved as %r' % (crab_config_file))



if __name__ == "__main__":

    options = get_options()
    
    if not os.path.isdir(options.output):
        os.makedirs(options.output)

    # Load datasets
    datasets = {}
    for dataset in options.datasets:
        with open(dataset) as f:
            datasets.update(json.load(f))

    crab_config_mc = create_default_config(True)
    crab_config_data = create_default_config(False)

    for era, era_datasets in datasets.items():
        if options.era and era != options.era:
            continue

        for dataset, metadata in era_datasets.items():
            print("Working on {}".format(dataset))
            if dataset.endswith("NANOAODSIM") or dataset.endswith("NANOAOD"):
                print("Will convert from nano to mini!")
                dataset = get_parent_DAS(dataset)
                print(" --> Found {}".format(dataset))
            elif (not (dataset.endswith("MINIAODSIM") or dataset.endswith("MINIAOD"))) and not dataset.endswith("USER"):
                print("Dataset {} cannot be used - must be either nano or mini!".format(dataset))

            is_mc = dataset.endswith("SIM")
            if is_mc:
                print("Dataset is MC")
                pset = findPSet("topNano_{}_{}_MC_cfg.py".format(PROD_TAG, era))
                crab_config = crab_config_mc
            else:
                print("Dataset is data")
                crab_config = crab_config_data
                pset = findPSet("topNano_{}_{}_data_cfg.py".format(PROD_TAG, era))

            year = "".join(i for i in era if i.isdigit()) # just keep the year from now on
            writeCrabConfig(pset, dataset, is_mc, metadata, year, crab_config, options.site, options.output)
            print("")
