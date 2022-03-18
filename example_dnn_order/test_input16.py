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
lnJ_pt=array('f',[0])
lnJ_mass=array('f',[0])

##---Set TMVA--##

myreader=ROOT.TMVA.Reader("V")
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_pt[0], -10.)',AddJet_pt1)
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_eta[0] , -10.)',AddJet_eta1)
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_pt[1], -10)',AddJet_pt2)
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_eta[1] , -10)',AddJet_eta2)

myreader.AddVariable('max_mjj_Boost_'+WP+'_nom',max_mjj)
myreader.AddVariable('mjj_of_max_dEta_Boost_'+WP+'_nom',mjj_of_max_dEta)

myreader.AddVariable('max_dEta_Boost_'+WP+'_nom',max_dEta)
myreader.AddVariable('dEta_of_max_mjj_Boost_'+WP+'_nom',dEta_of_max_mjj)

myreader.AddVariable('lnJ_'+WP+'_nom_pt',lnJ_pt)
myreader.AddVariable('lnJ_'+WP+'_nom_mass',lnJ_mass)


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
#  'sig' : 'Lepton_pt[0] > 40 && isBoost_'+WP+'_nom && (lnJ_'+WP+'_nom_widx >=0)&&(fabs(Lepton_eta[0]) < 2.5  ) && (  Alt$(Lepton_isLoose[1]*Lepton_pt[1],-1) < 10 ) && PuppiMET_nom_pt > 40 ',


for event in chain_sig:
    i+=1
    if i%100==0 : print i,'/',N
    lepton_pt=event.Lepton_pt[0]
    isBoost=event.isBoost_DeepAK8WP0p5_nom
    lnJ_nom_widx=event.lnJ_DeepAK8WP0p5_nom_widx
    PuppiMET=event.PuppiMET_nom_pt

    if lepton_pt<40 : continue
    if not isBoost:continue
    if lnJ_nom_widx<0:continue
    if PuppiMET<40:continue
    
    AddJet_pt1[0]= event.AddJetBoost_DeepAK8WP0p5_nom_pt[0] if len(event.AddJetBoost_DeepAK8WP0p5_nom_pt)>1 else -10.
    AddJet_eta1[0]= event.AddJetBoost_DeepAK8WP0p5_nom_eta[0] if len(event.AddJetBoost_DeepAK8WP0p5_nom_eta)>1 else -10.    


    AddJet_pt2[0]=event.AddJetBoost_DeepAK8WP0p5_nom_pt[1] if len(event.AddJetBoost_DeepAK8WP0p5_nom_pt)>2 else -10.
    AddJet_eta2[0]=event.AddJetBoost_DeepAK8WP0p5_nom_eta[1] if len(event.AddJetBoost_DeepAK8WP0p5_nom_eta)>2 else -10.
    
    max_mjj[0]=event.max_mjj_Boost_DeepAK8WP0p5_nom
    max_dEta[0]=event.max_dEta_Boost_DeepAK8WP0p5_nom
    
    dEta_of_max_mjj[0]=event.dEta_of_max_mjj_Boost_DeepAK8WP0p5_nom
    mjj_of_max_dEta[0]=event.mjj_of_max_dEta_Boost_DeepAK8WP0p5_nom

    lnJ_pt[0]=event.lnJ_DeepAK8WP0p5_nom_pt
    lnJ_mass[0]=event.lnJ_DeepAK8WP0p5_nom_mass


    ret=myreader.EvaluateMVA("PyKeras::DNN")
    h_s.Fill(ret)
    #print ret

mytfile=ROOT.TFile("histos.root",'RECREATE')
mytfile.cd()
h_s.Write()

mytfile.Write()
mytfile.Close()
