#include <iostream>
#include <cstdlib>


//#include "Python.h"
//#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
//#include <numpy/arrayobject.h>
//#include "TFile.h"
//#include "TTree.h"

int test(){
  cout<<"1"<<endl;
  TString WP="DeepAK8WP0p5";
  TString xmlfile="/cms_scratch/jhchoi/keras_my/scripts_ntree30000_shrinkage_0p1/TMVA_jhchoi//xml_h5_dnn/TMVAClassification_DNN.weights.xml";
  
  Float_t AddJet_pt1=0. ,AddJet_eta1=0., AddJet_pt2=0.,AddJet_eta2=0.,max_mjj=0.,mjj_of_max_dEta=0.,max_dEta=0.,dEta_of_max_mjj=0.,lnJ_pt=0.,lnJ_mass=0.;
  TMVA::Reader* myreader=new TMVA::Reader("V");
  myreader->AddVariable("Alt$(AddJetBoost_"+WP+"_nom_pt[0], -10.)",&AddJet_pt1);
  myreader->AddVariable("Alt$(AddJetBoost_"+WP+"_nom_pt[1], -10)",&AddJet_pt2);
  myreader->AddVariable("Alt$(AddJetBoost_"+WP+"_nom_eta[1] , -10)",&AddJet_eta2);
  myreader->AddVariable("Alt$(AddJetBoost_"+WP+"_nom_eta[0] , -10.)",&AddJet_eta1);
  myreader->AddVariable("max_mjj_Boost_"+WP+"_nom",&max_mjj);
  myreader->AddVariable("max_dEta_Boost_"+WP+"_nom",&max_dEta);
  myreader->AddVariable("dEta_of_max_mjj_Boost_"+WP+"_nom",&dEta_of_max_mjj);
  myreader->AddVariable("lnJ_"+WP+"_nom_pt",&lnJ_pt);
  myreader->AddVariable("lnJ_"+WP+"_nom_mass",&lnJ_mass);
  myreader->AddVariable("mjj_of_max_dEta_Boost_"+WP+"_nom",&mjj_of_max_dEta);
  //putenv("KERAS_BACKEND","tensorflow");
  setenv("KERAS_BACKEND", "tensorflow", true);

  //environ['KERAS_BACKEND'] = 'tensorflow'
  //ROOT.TMVA.PyMethodBase.PyInitialize();
  TMVA::PyMethodBase::PyInitialize();
  myreader->BookMVA("PyKeras::DNN",xmlfile);

  AddJet_pt1=30;
  AddJet_pt2=30;
  AddJet_eta2=1;
  AddJet_eta1=1;
  max_mjj=3000;
  max_dEta=3;
  dEta_of_max_mjj=3;
  lnJ_pt=200;
  lnJ_mass=1000;
  mjj_of_max_dEta=3000;

  Float_t ret=myreader->EvaluateMVA("PyKeras::DNN");
  cout <<ret <<endl;
    
  return 0;
}
