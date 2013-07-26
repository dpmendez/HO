# Auto generated configuration file
# using: 
# Revision: 1.15 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/Generator/python/SinglePi0E10_cfi.py -s GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,RECO --conditions auto:mc --eventcontent AODSIM -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.15 $'),
    annotation = cms.untracked.string('Configuration/Generator/python/SinglePi0E10_cfi.py nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('M5k_Eta1_Phi1_100.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition
process.AODSIMoutput.outputCommands.extend([
	'keep HBHEUpgradeDigiCollection_*_*_*',
	'keep HFUpgradeDigiCollection_*_*_*',
	'keep *_simHcalDigis_*_*',
	'keep *_simHcalUnsuppressedDigis_*_*',
	'keep *_hfUpgradeReco_*_*',
	'keep *_hbheUpgradeReco_*_*',
	'keep *_horeco_*_*',
	'keep *_g4SimHits_HcalHits_*',
	])

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')



process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        PartID = cms.vint32(13),
	# only in the center of tower ieta = 1, iphi = 1
        #MaxEta = cms.double(0.0435),
        #MinEta = cms.double(0.0435),
        #MaxPhi = cms.double(0.0435),
        #MinPhi = cms.double(0.0435),
	# all over the HO area
        MaxEta = cms.double(0.087),
        MinEta = cms.double(0.),
        MaxPhi = cms.double(0.087),
        MinPhi = cms.double(0.0),
        MinE = cms.double(100.),
        MaxE = cms.double(100.)
    ),
    Verbosity = cms.untracked.int32(0),
    psethack = cms.string('single muon E 100'),
    AddAntiParticle = cms.bool(False),
    firstRun = cms.untracked.uint32(1)
)

# add SiPMs to HO
process.mix.digitizers.hcal.ho.pixels = cms.int32(2500)
process.mix.digitizers.hcal.ho.siPMCode = 1
process.mix.digitizers.hcal.ho.photoelectronsToAnalog = cms.vdouble([4.0]*16)

#turn off HO ZS
process.hcalRawData.HO = cms.untracked.InputTag("simHcalUnsuppressedDigis", "", "")

#hard code conditions
#process.es_hardcode.toGet.extend(['ChannelQuality','RespCorrs','TimeCorrs'])

#ascii file conditions
process.hcales_ascii = hcales_ascii = cms.ESSource(
	    "HcalTextCalibrations",
	    input = cms.VPSet(
		cms.PSet(
			object = cms.string('ChannelQuality'),
			file = cms.FileInPath('usercode/HOSiPMAnalysis/data/chan_qual_0.txt')
			),
		cms.PSet(
			object = cms.string('Pedestals'),
			file = cms.FileInPath('usercode/HOSiPMAnalysis/data/db_pedestals.txt')
			),
	)
)

process.hcalasciiprefer = cms.ESPrefer("HcalTextCalibrations", "hcales_ascii")

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.reconstruction_step,process.endjob_step,process.AODSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

