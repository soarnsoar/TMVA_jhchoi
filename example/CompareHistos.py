import ROOT

fsig=ROOT.TFile.Open('output400/sig.root')
fbkg=ROOT.TFile.Open('output400/bkg.root')
hsig=fsig.Get("h")
hbkg=fbkg.Get("h")
#hsig.Rebin(5)
#hbkg.Rebin(5)
c=ROOT.TCanvas()
hsig.Draw()
hbkg.Draw("same")
hsig.SetLineColor(1)
hbkg.SetLineColor(2)
c.SaveAs("temp.pdf")


stotal=hsig.Integral()
btotal=hbkg.Integral()



N=100
mysum=0.
dx=0
seff_bf=1.
for i in range(1,N+1):
    x=hsig.GetBinLowEdge(i)
    s=hsig.Integral(i,N+1)
    b=hbkg.Integral(i,N+1)

    seff=s/stotal
    beff=b/btotal

    print '--x=',x,'---'
    print 'seff=',seff
    print 'beff=',beff


    dx=seff_bf-seff
    h=(1.-beff)
    seff_bf=seff

    area=dx*h
    mysum+=area



print mysum
