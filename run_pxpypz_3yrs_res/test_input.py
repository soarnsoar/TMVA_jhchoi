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
AddJet_phi1=array('f',[0])
AddJet_pt2=array('f',[0])
AddJet_eta2=array('f',[0])
AddJet_phi2=array('f',[0])
max_mjj=array('f',[0])
mjj_of_max_dEta=array('f',[0])
max_dEta=array('f',[0])
dEta_of_max_mjj=array('f',[0])
lnjj_pt=array('f',[0])
lnjj_eta=array('f',[0])
lnjj_phi=array('f',[0])
lnjj_mass=array('f',[0])

##---Set TMVA--##

myreader=ROOT.TMVA.Reader("V")
myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_pt[0],-10.)',AddJet_pt1)
myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_eta[0],-10.)',AddJet_eta1)
myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_phi[0],-10.)',AddJet_phi1)

myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_pt[1],-10.)',AddJet_pt2)
myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_eta[1],-10.)',AddJet_eta2)
myreader.AddVariable('Alt$(AddJetResol_dMchi2Resolution_nom_phi[1],-10.)',AddJet_phi2)


myreader.AddVariable('max_mjj_Resol_dMchi2Resolution_nom',max_mjj)
myreader.AddVariable('mjj_of_max_dEta_Resol_dMchi2Resolution_nom',mjj_of_max_dEta)
myreader.AddVariable('max_dEta_Resol_dMchi2Resolution_nom',max_dEta)
myreader.AddVariable('dEta_of_max_mjj_Resol_dMchi2Resolution_nom',dEta_of_max_mjj)
myreader.AddVariable('lnjj_dMchi2Resolution_nom_pt',lnjj_pt)
myreader.AddVariable('TMath::ASinH(Whad_dMchi2Resolution_nom_pt*TMath::SinH(Whad_dMchi2Resolution_nom_eta)+Wlep_nom_pt*TMath::SinH(Wlep_nom_eta)/lnjj_dMchi2Resolution_nom_pt)',lnjj_eta)
myreader.AddVariable('TMath::ATan2(Whad_dMchi2Resolution_nom_pt*TMath::Sin(Whad_dMchi2Resolution_nom_phi)+Wlep_nom_pt*TMath::Sin(Wlep_nom_phi),Whad_dMchi2Resolution_nom_pt*TMath::Cos(Whad_dMchi2Resolution_nom_phi)+Wlep_nom_pt*TMath::Cos(Wlep_nom_phi))',lnjj_phi)
myreader.AddVariable('lnjj_dMchi2Resolution_nom_mass',lnjj_mass)

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
    isResol=event.isResol_dMchi2Resolution_nom
    minptWOverM=event.lnjj_dMchi2Resolution_nom_minPtWOverM
    Wlep_Mt=event.Wlep_nom_Mt
    lnjj_Mt=event.lnjj_dMchi2Resolution_nom_Mt
    isboost=event.isBoost_DeepAK8WP0p5_nom
    '''
  'sig' : 'Lepton_pt[0] > 40 &&(isResol'+_ALGO_+'nom) &&(lnjj'+_ALGO_+'nom_minPtWOverM>0.35) &&(Wlep_nom_Mt > 50)&&(lnjj'+_ALGO_+'nom_Mt > 60)&&(fabs(Lepton_eta[0]) < 2.5  ) && \
(  Alt$(Lepton_isLoose[1]*Lepton_pt[1],-1) < 10 ) && PuppiMET_nom_pt > 30 ',

    '''
    if isboost:continue
    if lepton_pt<40 : continue
    #if not isBoost:continue
    #if lnjj_nom_widx<0:continue
    if PuppiMET<30:continue
    if not isResol:continue
    if minptWOverM < 0.35:continue
    if Wlep_Mt < 50 :continue
    if lnjj_Mt < 60 : continue
    AddJet_pt1[0]= event.AddJetResol_dMchi2Resolution_nom_pt[0] if len(event.AddJetResol_dMchi2Resolution_nom_pt)>1 else -10.
    AddJet_eta1[0]= event.AddJetResol_dMchi2Resolution_nom_eta[0] if len(event.AddJetResol_dMchi2Resolution_nom_eta)>1 else -10.    
    AddJet_phi1[0]= event.AddJetResol_dMchi2Resolution_nom_phi[0] if len(event.AddJetResol_dMchi2Resolution_nom_phi)>1 else -10.    


    AddJet_pt2[0]=event.AddJetResol_dMchi2Resolution_nom_pt[1] if len(event.AddJetResol_dMchi2Resolution_nom_pt)>2 else -10.
    AddJet_eta2[0]=event.AddJetResol_dMchi2Resolution_nom_eta[1] if len(event.AddJetResol_dMchi2Resolution_nom_eta)>2 else -10.
    AddJet_phi2[0]=event.AddJetResol_dMchi2Resolution_nom_phi[1] if len(event.AddJetResol_dMchi2Resolution_nom_phi)>2 else -10.
    
    max_mjj[0]=event.max_mjj_Resol_dMchi2Resolution_nom
    max_dEta[0]=event.max_dEta_Resol_dMchi2Resolution_nom
    
    dEta_of_max_mjj[0]=event.dEta_of_max_mjj_Resol_dMchi2Resolution_nom
    mjj_of_max_dEta[0]=event.mjj_of_max_dEta_Resol_dMchi2Resolution_nom

    lnjj_pt[0]=event.lnjj_dMchi2Resolution_nom_pt
    lnjj_eta[0]=ROOT.TMath.ASinH(event.Whad_dMchi2Resolution_nom_pt*ROOT.TMath.SinH(event.Whad_dMchi2Resolution_nom_eta)+event.Wlep_nom_pt*ROOT.TMath.SinH(event.Wlep_nom_eta)/event.lnjj_dMchi2Resolution_nom_pt)
    lnjj_phi[0]=ROOT.TMath.ATan2(event.Whad_dMchi2Resolution_nom_pt*ROOT.TMath.Sin(event.Whad_dMchi2Resolution_nom_phi)+event.Wlep_nom_pt*ROOT.TMath.Sin(event.Wlep_nom_phi),event.Whad_dMchi2Resolution_nom_pt*ROOT.TMath.Cos(event.Whad_dMchi2Resolution_nom_phi)+event.Wlep_nom_pt*ROOT.TMath.Cos(event.Wlep_nom_phi))
    lnjj_mass[0]=event.lnjj_dMchi2Resolution_nom_mass


    ret=myreader.EvaluateMVA("PyKeras::DNN")
    h_s.Fill(ret)
    #print ret

mytfile=ROOT.TFile("histos.root",'RECREATE')
mytfile.cd()
h_s.Write()

mytfile.Write()
mytfile.Close()
