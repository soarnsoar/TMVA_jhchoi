import ROOT
from array import array

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


WP='DeepAK8WP0p5'


xmlfile='../xml/TMVAClassification_BDT.weights.xml'

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





##by order
myreader.BookMVA("BDT::BDT",xmlfile)
##now mva tool is ready.(loaded)

AddJet_pt1[0]=30.
AddJet_eta1[0]=2.
AddJet_pt2[0]=0.
AddJet_eta1[0]=-10
max_mjj[0]=500.
mjj_of_max_dEta[0]=200
max_dEta[0]=2
dEta_of_max_mjj[0]=2
lnJ_pt[0]=100
lnJ_mass[0]=300

ret=myreader.EvaluateMVA("BDT::BDT")



print ret

