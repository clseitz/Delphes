#!/usr/bin/python

import sys
from ROOT import TH1D,THStack,TFile,TCanvas,TLegend,kRed,kOrange,kBlue,kCyan,kGreen,kMagenta,TLine,TLatex,kYellow
#from ROOT import TH1D,THStack,TFile,TCanvas,TLegend,kRed,kOrange,kBlue,kCyan

dirName='September5_30GeV20GeVveto'
f = TFile(dirName+"/"+dirName+"_plots_stoc.root", "recreate")

global h_stc,h_nm1,h_nm2,h_nm3,h_stcBkd,h_nm1Bkd,h_nm2Bkd,h_nm3Bkd

def get(file,what,Lfac,lineCol,lineWid,lineSty,fillCol,reb=0):
	
	h = file.Get(what)
	h.SetLineColor(lineCol)
	h.SetLineWidth(lineWid)
	h.SetLineStyle(lineSty)
	h.SetFillColor(fillCol)
	h.Scale(Lfac)
	if reb==1: h.Rebin()
	return h.Clone()

def plot(ana,histos,h_legend,minY,maxY,minX,maxX,whatX,whatY,c1=0,all=1):
	global stack,leg,dum
	print ana
	#prepare the layou
	if c1==0:
		c1=TCanvas('c1','',800,600)
	c1.SetLogy() 
	dum = h_ttbar.Clone()
	dum.Reset()
	dum.SetMinimum(minY)
	dum.SetMaximum(maxY)
	dum.GetXaxis().SetRangeUser(minX,maxX)
	dum.SetXTitle(whatX)
	dum.SetYTitle(whatY)
	dum.SetTitle('')
	dum.SetStats(0)
	dum.Draw()

        tex = TLatex(0.90,0.93,"14 TeV, 3000 fb^{-1}, PU = 140")
        tex.SetNDC()
        tex.SetTextAlign(31)
        tex.SetTextFont(42)
        tex.SetTextSize(0.048)
        tex.SetLineWidth(2)
        tex.Draw()
        tex1 = TLatex(0.15,0.89,"CMS Phase II Simulation")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(61)
        tex1.SetTextSize(0.045)
        tex1.SetLineWidth(2)
        tex1.Draw()
	# a legend

	leg = TLegend(0.63,0.525,0.87,0.875) #for 33 TeV (0.65,0.65,0.9,0.9)
        leg.SetBorderSize(1)
        leg.SetTextSize(0.025)
        leg.SetLineColor(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
	##if whatX=='MT2W': leg = TLegend(0.55,0.5,0.87,0.9)
	leg.SetFillColor(0)
	leg.SetLineColor(0)


	leg.AddEntry(h_stc,'STOC','l')
	#leg.AddEntry(h_nm1,'NM1','l')
	#leg.AddEntry(h_nm2,'NM2','l')
	#leg.AddEntry(h_nm3,'NM3','l')
	#leg.AddEntry(h_stc_stoponly,'stc only stop','l')
	#leg.AddEntry(h_nm1_stoponly,'natural model 1 only stop','l')
	#leg.AddEntry(h_nm2_stoponly,'natural model 2 only stop','l')
	#leg.AddEntry(h_nm3_stoponly,'natural model 3 only stop','l')
	if pu== 'NoPU': leg.SetHeader('no pileup')
	if pu== '50PU': leg.SetHeader('pileup: 50')
	if pu=='140PU': leg.SetHeader('pileup: 140')
	if all:
		# bgrd stack
		stack = THStack('stack','')
		N=len(histos)
		for i in range(N):
			h=histos[i][0]
			stack.Add(h)
		for i in range(N-1,-1,-1):
			h=histos[i][0]
			t=h_legend[h]
			leg.AddEntry(h,t,'f')
		# draw bgrds + signals
		stack.Draw('samehist')

	h_stc.Draw('samehist')
	#h_nm1.Draw('samehist')
	#h_nm2.Draw('samehist')
	#h_nm3.Draw('samehist')

	#h_stc_stoponly.Draw('samehist')
	#h_nm1_stoponly.Draw('samehist')
	#h_nm2_stoponly.Draw('samehist')
	#h_nm3_stoponly.Draw('samehist')

	leg.Draw()
	c1.RedrawAxis()
	c1.SetName(tev+'_'+pu+'_'+what+'_'+ana)
	#c1.SaveAs(dirName+'/'+tev+'_'+pu+'_'+what+'_'+ana+'.pdf')
	f.cd()
	c1.Write()



ana='SingleS_P+DelphMET'
tev='14TeV'	
# scale factor - histos are for 300/fb
Lfac=1.0
#base of filename
base=dirName+'/'+ana+'_'
#
###
## pileup scenario
#pu  ='NoPU' 
#pu  ='50PU' 
pu ='140PU'

c1=TCanvas('c1','',800,600)

#--------------------------------------------------------------------------------------------------------------------------------------------------------

########## preselection
quantity=['HT','0JetpT','1JetpT','2JetpT','3JetpT','nJet','nBJet','nMu','nEl','nLep','LeppT','Central','RawMET','dPhi','mT','mT2W']

label=['H_{T} [GeV]','0JetpT','1JetpT','2JetpT','3JetpT',
	  'Number of jets','Number of b-jets','nMu','nEl',
	  'Number of leptons','Leading lepton p_{T} [GeV]',
	  'Centrality','E_{T}^{miss} [GeV]',
	  'min ( #Delta #phi(j_{1},E_{T}^{miss}),  #Delta #phi(j_{1},E_{T}^{miss}))','M_{T} [GeV]','M^{W}_{T2} [GeV]']

ymax=[4000,2000,2000,2000,2000,20,20,10,10,10,1000,1,1500,3.2,700,500]

cuts=["nocut","1 lepton not cleaned","add. lep veto (not cleaned)", "iso track veto (clean)",
      "nJets >= 3", "nJets >= 4", "nJets >= 5",
      "bjets == 1/2", "MET>300", "dphi > 0.8", "HT > 400", "central > 0.6",
      "MT>140","MT>260","MT2W>200","MT2W>220",
      "stc 4 <= Njet <= 6","stc Njet >= 6","stc ","stc MET400","nm stops",
      "nm gluinos MET400, HT1000","nm gluinos MET400, HT1400", "nm gluinos MET400, HT1700",
      "nm gluinos MET600, HT1000","nm gluinos MET600, HT1400", "nm gluinos MET600, HT1700",
      "nm gluinos MET800, HT1000", "nm gluinos MET800, HT1400", "nm gluinos MET800, HT1700"]

cutsShort=["noCut","1lep_noclean","addlepveto_noclean", "trackveto_clean",
	   "nJetsgeq3", "nJetsgeq4", "nJetsgeq5",
	   "nBJeteq12", "MET300", "dPhi0p8","HT400", "Central0p6",
	   "MT140", "MT260","MT2W200", "MT2W220",
	   "stc4njet6","stcnjetgeq6","stc","stcMET400","nm_stops",
	   "nm_gluinos_MET400_HT1000","nm_gluinos_MET400_HT1400", "nm_gluinos_MET400_HT1700",
	   "nm_gluinos_MET600_HT1000","nm_gluinos_MET600_HT1400", "nm_gluinos_MET600_HT1700",
	   "nm_gluinos_MET800_HT1000", "nm_gluinos_MET800_HT1400", "nm_gluinos_MET800_HT1700"]



l=0

file_TTbar = TFile.Open(base+pu+'_TTbar_his.root')
file_BosonJets = TFile.Open(base+pu+'_BosonJets_his.root')
file_TopJets = TFile.Open(base+pu+'_TopJets_his.root')
file_DiBoson = TFile.Open(base+pu+'_DiBoson_his.root')
file_STC = TFile.Open(base+pu+'_STOC_his.root')
file_NM1 = TFile.Open(base+pu+'_NM1_his.root')
file_NM2 = TFile.Open(base+pu+'_NM2_his.root')
file_NM3 = TFile.Open(base+pu+'_NM3_his.root')

#file_STC_stoponly = TFile.Open(base+pu+'_STCfirst_his_stoponly.root')
#file_NM1_stoponly = TFile.Open(base+pu+'_NM1_his_stoponly.root')
#file_NM2_stoponly = TFile.Open(base+pu+'_NM2_his_stoponly.root')
#file_NM3_stoponly = TFile.Open(base+pu+'_NM3_his_stoponly.root')
reb = 1
for what in quantity:
	for k in range (0,26):
		if what == 'nLep' or what == 'nJet' or what == 'nBJet' or what == 'nEl' or what == 'nMu':
			reb = 0
		print what+'_'+str(k)
		h_ttbar = get(file_TTbar, what+'_'+str(k),Lfac,1,1,1,kBlue,reb)
		h_bjets = get(file_BosonJets, what+'_'+str(k),Lfac,1,1,1,kOrange,reb)
		h_tjets = get(file_TopJets, what+'_'+str(k),Lfac,1,1,1,kCyan,reb)
		h_dibos = get(file_DiBoson, what+'_'+str(k),Lfac,1,1,1,kRed,reb)
		h_stc  = get(file_STC, what+'_'+str(k),Lfac,kMagenta-2,2,1,0,reb)
		h_nm1  = get(file_NM1, what+'_'+str(k),Lfac,6,2,1,0,reb)
		h_nm2  = get(file_NM2, what+'_'+str(k),Lfac,1,2,1,0,reb)
		h_nm3  = get(file_NM3, what+'_'+str(k),Lfac,8,2,1,0,reb)

		#h_stc_stoponly  = get(file_STC_stoponly, what+'_'+str(k),Lfac,9,2,2,0,0)
		#h_nm1_stoponly  = get(file_NM1_stoponly, what+'_'+str(k),Lfac,6,2,2,0,0)
		#h_nm2_stoponly  = get(file_NM2_stoponly, what+'_'+str(k),Lfac,1,2,2,0,0)
		#h_nm3_stoponly  = get(file_NM3_stoponly, what+'_'+str(k),Lfac,8,2,2,0,0)
		
		
		# fill the bgrd stack - smallest first
		h_ent={}
		h_leg={} # entries in legend
		# bgrds
		h_ent[h_ttbar]=h_ttbar.Integral(0,5000)
		h_leg[h_ttbar]='t#bar{t} + jets'
		#
		h_ent[h_bjets]=h_bjets.Integral(0,5000)
		h_leg[h_bjets]='W,Z + jets'
		#
		h_ent[h_tjets]=h_tjets.Integral(0,5000)
		h_leg[h_tjets]='single top + jets'
		h_ent[h_dibos]=h_dibos.Integral(0,5000)
		h_leg[h_dibos]='Diboson'
		max = h_ttbar.GetMaximum()+h_bjets.GetMaximum()+h_tjets.GetMaximum()+h_dibos.GetMaximum()+h_ttbar.GetMaximum()
		import operator
		sorted_h = sorted(h_ent.iteritems(), key=operator.itemgetter(1))
		
		#plot(cutsShort[k]+'_'+str(k),sorted_h,h_leg,0.1,max,0,ymax[l],'selection: '+cuts[k]+'               '+what,'evts / bin',c1,1)
		plot(cutsShort[k]+'_'+str(k),sorted_h,h_leg,0.1,max,0,ymax[l],label[l],'evts / bin',c1,1)
	l=l+1
#--------------------------------------------------------------------------------------------------------------------------------------------------------
