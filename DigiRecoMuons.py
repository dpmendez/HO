def unpackHcalIndex(idx):
    det  = (idx>>28)&15
    depth= (idx>>26)&3
    depth+=1
    lay  = (idx>>21)&31
    #lay+=1
    z    = (idx>>20)&1
    eta  = (idx>>10)&1023
    phi  = (idx&1023)

    z = -1 if z==0 else 1

    # if (det==2) and (eta==16):
    #     lay += 8

    return (det,z,eta,phi,depth,lay)

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')
parser.add_option('-o', dest='outputFile', default='Muons5k_Half_1_Hist.root',
                  help='output filename')
parser.add_option('--ieta', dest='ieta', default=1, type='int',
                  help='target ieta')
parser.add_option('--iphi', dest='iphi', default=1, type='int',
                  help='target iphi')
parser.add_option('--testNumbering', dest='testNumbers', default=False,
                  action='store_true', help='use SimHit test number unpacker')
(opts, args) = parser.parse_args()

print 'opts:',opts,'\nargs:',args

from DataFormats.FWLite import Events, Handle
from ROOT import *
from array import array
from math import sqrt


files = []
if len(args) > 0:
    files = args
print 'len(files)',len(files),'first:',files[0]
events = Events (files)

simHitHandle = Handle('vector<PCaloHit>')
horecoHandle = Handle('edm::SortedCollection<HORecHit,edm::StrictWeakOrdering<HORecHit> >')
simDigiHandle = Handle('edm::SortedCollection<HODataFrame,edm::StrictWeakOrdering<HODataFrame> >')

simHitLabel = ('g4SimHits','HcalHits')
horecoLabel = ('horeco')
simDigiLabel = ('simHcalUnsuppressedDigis')

EvtN = 0

outFile = TFile(opts.outputFile, 'recreate')


#Histograms

HOSimHitSum = TH1F("HOSimHitSum", 'Sum HO Sim Hits ; SimHit Energy (GeV)', 20, 0., 0.02)


HOEtaEnergy = TH2F("HOSimHit EtaEnergy", 'SimHits 100GeV/c Muons; SimHit Eta ; Total SimHit Energy (GeV) ; Counts', 31, -15.5,15.5, 20, 0., 0.02)
HOTransEnergy = TH2F("HOSimHit TransEnergy", 'SimHits 100GeV/c Muons; SimHit Eta ; Total SimHit TransEnergy (GeV) ; Counts', 31, -15.5,15.5, 20, 0., 0.02)

HORecoEtaEnergy = TH2F("HOReco EtaEnergy", 'SimHits 100GeV/c Muons; SimHit Eta ; Total RecoHit Energy (GeV) ; Counts', 31, -15.5,15.5, 20, -1.0 , 5.0)
HORecoTransEnergy = TH2F("HOReco TransEnergy", 'SimHits 100GeV/c Muons; SimHit Eta ; Total RecoHit TransEnergy (GeV) ; Counts', 31, -15.5,15.5, 20, -1.0 , 5.0)


HOSimDigi = TH2F("HO SimDigi", 'SimHits 100GeV/c Muons; Time Slice ; SimDigi Charge (fC) ; Counts', 12, -1.0 , 11.0 , 100 , 0.0, 100.0)
HOSimDigiEta = TH2F("HO SimDigi Eta", 'SimHits 100GeV/c Muons; Eta ; SimDigi Charge (fC) ; Counts', 31, -15.5 , 15.5 , 100 , 0.0, 100.0)
HOSimDigiEta2 = TH2F("HO SimDigi Eta", 'SimHits 100GeV/c Muons; Eta ; SimDigi Charge (fC) ; Counts',31, -15.5 , 15.5 , 100 , 0.0, 100.0)

for event in events:
    ## if EvtN > 9:
    ##     break
    EvtN += 1
    if EvtN%500 == 1:
        print 'record:',EvtN,'Run:',event.object().id().run(),\
              'event:',event.object().id().event()

    event.getByLabel(simHitLabel, simHitHandle)
    simHits = simHitHandle.product()

    sumSim = 0.
    sum11 = 0.
    sumHB = 0.
    sumHBTarget = 0.
    sumHE = 0.
    EtaSum={};
    TransEnergy={};
    ieta_max = -100.
    iphi_max = -100.
    energy_max = -100.

    for hit in simHits:
        if opts.testNumbers:
            (det, z, ieta, iphi, depth, layer) = unpackHcalIndex(hit.id())
        else:
            hid = HcalDetId(hit.id())
            det = hid.subdet()
            ieta = hid.ieta()
            iphi = hid.iphi()
  
	if (det == 3):
            sumSim += hit.energy()
	    try:
		EtaSum[ieta] += hit.energy()
	        TransEnergy[ieta] += hit.energy()*sin(2*atan(exp(-ieta*0.087+0.0435)))
	    except KeyError:
		    EtaSum[ieta] = hit.energy()
                    TransEnergy[ieta] = hit.energy()*sin(2*atan(exp(-ieta*0.087+0.0435)))
	    if (ieta == opts.ieta) and (iphi == opts.iphi):
                sum11 += hit.energy()
	    if (energy_max < hit.energy()):
	        energy_max = hit.energy()
		ieta_max = ieta
		iphi_max = iphi
	
	elif (det == 1):
            sumHB += hit.energy()
            if (ieta == opts.ieta) and (iphi == opts.iphi):
                sumHBTarget += hit.energy()
        elif (det == 2):
            sumHE += hit.energy()
            if (ieta == opts.ieta) and (iphi == opts.iphi):
                sumHBTarget += hit.energy()

    for ieta in EtaSum:
        HOEtaEnergy.Fill(ieta,EtaSum[ieta])
    for ieta in TransEnergy:
	HOTransEnergy.Fill(ieta,TransEnergy[ieta])

    HOSimHitSum.Fill(sumSim)

    event.getByLabel(horecoLabel, horecoHandle)
    horeco = horecoHandle.product()

    for hohit in horeco:
        if (hohit.id().ieta() == ieta_max) and (hohit.id().iphi() == iphi_max):
            HORecoEtaEnergy.Fill(hohit.id().ieta(), hohit.energy())
    for hohit in horeco:
         if (hohit.id().ieta() == ieta_max) and (hohit.id().iphi() == iphi_max):
            HORecoTransEnergy.Fill(hohit.id().ieta(), (hohit.energy())*(sin(2*atan(exp((-hohit.energy())*0.087+0.0435)))))
 
    event.getByLabel(simDigiLabel, simDigiHandle)
    simDigis = simDigiHandle.product()

    for simDigi in simDigis:
        if (simDigi.id().ieta() == ieta_max) and (simDigi.id().iphi()== iphi_max) and (simDigi.id().subdet() == 3):
            for i in range(0, simDigi.size()):
                HOSimDigi.Fill(i, simDigi[i].nominal_fC())
            HOSimDigiEta2.Fill(simDigi.id().ieta(),simDigi[5].nominal_fC() + simDigi[6].nominal_fC())  
        HOSimDigiEta.Fill(simDigi.id().ieta(), simDigi[5].nominal_fC() + simDigi[6].nominal_fC())


print 'total records processed:',EvtN

c0 = TCanvas("c0", "SimHits", 1000, 1000)
HOSimHitSum.Fit("landau");
gStyle.SetOptFit(1);
HOSimHitSum.Draw();

c1 = TCanvas("c1", "SimHits Histograms", 1000, 1000)
c1.Divide(2,2)

c1.cd(1)
HOEtaEnergy.Draw("LEGO");
c1.cd(2)
HOTransEnergy.Draw("LEGO");

"""c1.cd(1)
HOEtaEnergy.Draw();
c1.cd(2)
HOTransEnergy.Draw();
c1.cd(3)
HOSimHitSum.Fit("landau");
gStyle.SetOptFit(1);
HOSimHitSum.Draw(); """

c1.cd(3)
HOEtaEnergy.ProfileX().Draw();
c1.cd(4)
HOTransEnergy.ProfileX().Draw();

c2 = TCanvas("c2", "RecoHits Histograms")
c2.Divide(2,2)

c2.cd(1)
HORecoEtaEnergy.Draw("LEGO");
c2.cd(2)
HORecoTransEnergy.Draw("LEGO");

"""c2.cd(3)
HOSimHitSum.Fit("landau");
gStyle.SetOptFit(1);
HOSimHitSum.Draw(); """

c2.cd(3)
HORecoEtaEnergy.ProfileX().Draw();
c2.cd(4)
HORecoTransEnergy.ProfileX().Draw();


c3 = TCanvas("c3", "HOSimHits")
c3.Divide(2,2)

c3.cd(1)
HOEtaEnergy.Draw();
c3.cd(2)
HOTransEnergy.Draw();
c3.cd(3)
HOEtaEnergy.ProfileX().Draw();
c3.cd(4)
HOTransEnergy.ProfileX().Draw(); 

c4 = TCanvas("c3", "HORecoHits")
c4.Divide(2,2)

c4.cd(1)
HORecoEtaEnergy.Draw();
c4.cd(2)
HORecoTransEnergy.Draw();
c4.cd(3)
HORecoEtaEnergy.ProfileX().Draw();
c4.cd(4)
HORecoTransEnergy.ProfileX().Draw(); 

c5 = TCanvas("c4", "SimDigi")
c5.Divide(1,2)

c5.cd(1)
HOSimDigi.Draw("colz");
c5.cd(2)
HOSimDigiEta.Draw("colz");

c6 = TCanvas("c6","SimDigis Maximums");
HOSimDigiEta2.Draw("colz");

gPad.Update()
gPad.WaitPrimitive()


outFile.Write()
outFile.Close()
