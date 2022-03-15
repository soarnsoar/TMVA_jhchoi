import glob
import ROOT
from array import array

WP='DeepAK8WP0p5'
xmlfile='/cms_scratch/jhchoi/keras_my/scripts_ntree30000_shrinkage_0p1/TMVA_jhchoi//xml/TMVAClassification_BDT.weights.xml'


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
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_pt[1], -10)',AddJet_pt2)
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_eta[1] , -10)',AddJet_eta2)
myreader.AddVariable('Alt$(AddJetBoost_'+WP+'_nom_eta[0] , -10.)',AddJet_eta1)
myreader.AddVariable('max_mjj_Boost_'+WP+'_nom',max_mjj)
myreader.AddVariable('max_dEta_Boost_'+WP+'_nom',max_dEta)
myreader.AddVariable('dEta_of_max_mjj_Boost_'+WP+'_nom',dEta_of_max_mjj)
myreader.AddVariable('lnJ_'+WP+'_nom_pt',lnJ_pt)
myreader.AddVariable('lnJ_'+WP+'_nom_mass',lnJ_mass)
myreader.AddVariable('mjj_of_max_dEta_Boost_'+WP+'_nom',mjj_of_max_dEta)

myreader.BookMVA("BDT::BDT",xmlfile)




bkginput_list=glob.glob('../../../input_tree/nanoLatino_GluGluHToWWToLNuQQ_M400__part*.root')
siginput_list=glob.glob('../../../input_tree/nanoLatino_VBFHToWWToLNuQQ_M400__part*.root')


chain_sig=ROOT.TChain('Events')
chain_bkg=ROOT.TChain('Events')
for fsig in siginput_list:
    chain_sig.Add(fsig)
for fbkg in bkginput_list:
    chain_bkg.Add(fbkg)

#TH1D (const char *name, const char *title, Int_t nbinsx, const Double_t *xbins)
#TH1D (const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup)

h_s=ROOT.TH1D("hs",'hs',100,-1.,1.)
h_b=ROOT.TH1D("hb",'hb',100,-1.,1.)

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


    ret=myreader.EvaluateMVA("BDT::BDT")
    h_s.Fill(ret)
    #print ret
print 'run bkg'
N=chain_bkg.GetEntries()
print N
i=0
for event in chain_bkg:
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


    ret=myreader.EvaluateMVA("BDT::BDT")
    h_b.Fill(ret)
    #print ret

mytfile=ROOT.TFile("histos.root",'RECREATE')
mytfile.cd()
h_s.Write()
h_b.Write()
mytfile.Write()
mytfile.Close()
