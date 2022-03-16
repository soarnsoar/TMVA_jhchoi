import os
os.system('rm *.h5')
os.system('rm *.xml')
os.system('cp ../../TMVAClassification*/*/* .')

xmlpath='TMVAClassification_DNN.weights.xml'
fxml=open(xmlpath)
fxml_new=open(xmlpath+'_new','w')

lines=fxml.readlines()

for line in lines:    
  if '>TMVAClassification/weights/TrainedModel_DNN.h5' in line:
    line=line.replace('TMVAClassification/weights/TrainedModel_DNN.h5',os.getcwd()+'/TrainedModel_DNN.h5')
  fxml_new.write(line)


os.system('mv '+xmlpath+' '+xmlpath+'_old')
os.system('mv '+xmlpath+'_new '+xmlpath)
