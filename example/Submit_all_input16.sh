address='root://cms-xrdr.private.lo:2094'
#INPUTDIR=/cms_scratch/jhchoi/keras_my/input_tree
INPUTDIR="${address}"'//xrd/store/user/jhchoi/Latino/HWWNano/Summer16_102X_nAODv7_Full2016v7_HWW/MCl1loose2016v7__MCCorr2016v7__HMSemilepSKIMv7_1__HMFull_V13_jhchoi_nom/'


RUNPY=/cms_scratch/jhchoi/keras_my/scripts_ntree30000_shrinkage_0p1/TMVA_jhchoi/example/test_input16.py


ARR_F=(
nanoLatino_GluGluHToWWToLNuQQ_M4000__part0.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part1.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part2.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part3.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part4.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part5.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part6.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part7.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part8.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part9.root
nanoLatino_GluGluHToWWToLNuQQ_M4000__part10.root

nanoLatino_VBFHToWWToLNuQQ_M4000__part0.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part1.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part2.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part3.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part4.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part5.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part6.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part7.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part8.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part9.root
nanoLatino_VBFHToWWToLNuQQ_M4000__part10.root

)
ARR_F=()
cd /xrootd//store/user/jhchoi/Latino/HWWNano/Summer16_102X_nAODv7_Full2016v7_HWW/MCl1loose2016v7__MCCorr2016v7__HMSemilepSKIMv7_1__HMFull_V13_jhchoi_nom/
ARR_F+=( $(ls nanoLatino_GluGluHToWWToLNuQQ_M*__part*.root) )
ARR_F+=( $(ls nanoLatino_VBFHToWWToLNuQQ_M*__part*.root) )
cd -

#   parser.add_option("-c","--command",   dest="command", help="command to run")
#   parser.add_option("-d","--workdir",   dest="workdir", help="workarea")
#   parser.add_option("-n","--jobname",   dest="jobname", help="jobname")
#   parser.add_option("-m","--ncpu",   dest="ncpu", help="number of multicores",default=1)
#   parser.add_option("-s","--submit",   dest="submit",action="store_true", help="submit",default=False)
#   parser.add_option("-r","--memory",   dest="memory", help="memory")

for F in ${ARR_F[@]};do
    #echo $F
    python python_tool/ExportShellCondorSetup.py -c "python ${RUNPY} ${INPUTDIR}/${F}" -d "WORKDIR/${F}" -n "testinput" -m 1 -s 

done
