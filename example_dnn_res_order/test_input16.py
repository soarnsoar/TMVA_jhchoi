import glob
import ROOT
from array import array
import sys
import os

#_JHCHOI_TMVATEST=os.environ["_JHCHOI_TMVATEST"]
#print _JHCHOI_TMVATEST
inputname=sys.argv[1]
xmlfile=sys.argv[2]
WP='DeepAK8WP0p5'
ALGO="dMchi2Resolution"
_ALGO_="_"+ALGO+"_"

#xmlfile=_JHCHOI_TMVATEST+'../xml_h5_dnn/TMVAClassification_DNN.weights.xml'


##---Variables---##
AddJet_pt1=array('f',[0])
AddJet_eta1=array('f',[0])
AddJet_pt2=array('f',[0])
AddJet_eta2=array('f',[0])
max_mjj=array('f',[0])
mjj_of_max_dEta=array('f',[0])
max_dEta=array('f',[0])
dEta_of_max_mjj=array('f',[0])
lnjj_pt=array('f',[0])
lnjj_mass=array('f',[0])

##---Set TMVA--##

myreader=ROOT.TMVA.Reader("V")
myreader.AddVariable('Alt$(AddJetResol_'+ALGO+'_nom_pt[0], 3.)',AddJet_pt1)
myreader.AddVariable('Alt$(AddJetResol_'+ALGO+'_nom_eta[0] , 3.)',AddJet_eta1)
myreader.AddVariable('Alt$(AddJetResol_'+ALGO+'_nom_pt[1], 3.)',AddJet_pt2)
myreader.AddVariable('Alt$(AddJetResol_'+ALGO+'_nom_eta[1] , 3.)',AddJet_eta2)
myreader.AddVariable('max_mjj_Resol_'+ALGO+'_nom',max_mjj)
myreader.AddVariable('mjj_of_max_dEta_Resol_'+ALGO+'_nom',mjj_of_max_dEta)
myreader.AddVariable('max_dEta_Resol_'+ALGO+'_nom',max_dEta)
myreader.AddVariable('dEta_of_max_mjj_Resol_'+ALGO+'_nom',dEta_of_max_mjj)
myreader.AddVariable('lnjj_'+ALGO+'_nom_pt',lnjj_pt)
myreader.AddVariable('lnjj_'+ALGO+'_nom_mass',lnjj_mass)

from os import environ
environ['KERAS_BACKEND'] = 'tensorflow'
ROOT.TMVA.PyMethodBase.PyInitialize()


myreader.BookMVA("PyKeras::DNN",xmlfile)





chain_sig=ROOT.TChain('Events')
chain_sig.Add(inputname)
#for fsig in siginput_list:
#    chain_sig.Add(fsig)


h_s=ROOT.TH1D("h",'h',100,0.,1.)


print 'run sig'
N=chain_sig.GetEntries()
print N
i=0
#  'sig' : 'Lepton_pt[0] > 40 && isBoost_'+WP+'_nom && (lnjj_'+WP+'_nom_widx >=0)&&(fabs(Lepton_eta[0]) < 2.5  ) && (  Alt$(Lepton_isLoose[1]*Lepton_pt[1],-1) < 10 ) && PuppiMET_nom_pt > 40 ',


for event in chain_sig:
    i+=1
    if i%100==0 : print i,'/',N
    lepton_pt=event.Lepton_pt[0]
    #isBoost=event.isBoost_DeepAK8WP0p5_nom
    #lnjj_nom_widx=event.lnjj_DeepAK8WP0p5_nom_widx
    PuppiMET=event.PuppiMET_nom_pt

    if lepton_pt<40 : continue
    #if not isBoost:continue
    #if lnjj_nom_widx<0:continue
    if PuppiMET<40:continue
    
    AddJet_pt1[0]= event.AddJetResol_dMchi2Resolution_nom_pt[0] if len(event.AddJetResol_dMchi2Resolution_nom_pt)>1 else 3.
    AddJet_eta1[0]= event.AddJetResol_dMchi2Resolution_nom_eta[0] if len(event.AddJetResol_dMchi2Resolution_nom_eta)>1 else 3.    


    AddJet_pt2[0]=event.AddJetResol_dMchi2Resolution_nom_pt[1] if len(event.AddJetResol_dMchi2Resolution_nom_pt)>2 else 3.
    AddJet_eta2[0]=event.AddJetResol_dMchi2Resolution_nom_eta[1] if len(event.AddJetResol_dMchi2Resolution_nom_eta)>2 else 3.
    
    max_mjj[0]=event.max_mjj_Resol_dMchi2Resolution_nom
    max_dEta[0]=event.max_dEta_Resol_dMchi2Resolution_nom
    
    dEta_of_max_mjj[0]=event.dEta_of_max_mjj_Resol_dMchi2Resolution_nom
    mjj_of_max_dEta[0]=event.mjj_of_max_dEta_Resol_dMchi2Resolution_nom

    lnjj_pt[0]=event.lnjj_dMchi2Resolution_nom_pt
    lnjj_mass[0]=event.lnjj_dMchi2Resolution_nom_mass


    ret=myreader.EvaluateMVA("PyKeras::DNN")
    h_s.Fill(ret)
    #print ret

mytfile=ROOT.TFile("histos.root",'RECREATE')
mytfile.cd()
h_s.Write()

mytfile.Write()
mytfile.Close()
