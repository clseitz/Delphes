#!/usr/bin/python

import sys
from ROOT import *

gROOT.LoadMacro("tdrstyle.C")
setTDRStyle()

gROOT.LoadMacro("CMS_lumi_v2.C")
dirName='September18'
f = TFile(dirName+"/"+dirName+"_plots_allsig.root", "recreate")

global h_stc,h_stoc,h_nm1,h_nm2,h_nm3,h_stcBkd,h_nm1Bkd,h_nm2Bk,h_nm3Bkd

def get(file,what,Lfac,lineCol,lineWid,lineSty,fillCol,reb=0):
	
	h = file.Get(what)
	h.SetLineColor(lineCol)
	h.SetLineWidth(lineWid)
	h.SetLineStyle(lineSty)
	h.SetFillColor(fillCol)
	h.Scale(Lfac)
	if reb!=0: h.Rebin(reb)
	return h.Clone()

def plot(ana,histos,h_legend,minY,maxY,minX,maxX,whatX,whatY,c1=0,all=1):
	global stack,leg,dum
	print ana
	#prepare the layou
	if c1==0:
		c1=TCanvas('c1','',800,600)
	c1.SetLogy() 
        c1.SetBottomMargin(0.1306294);
	dum = h_ttbar.Clone()
	dum.Reset()
	dum.SetMinimum(minY)
	dum.SetMaximum(maxY)
	dum.GetXaxis().SetRangeUser(minX,maxX)
	dum.GetXaxis().SetTitleSize(0.06)
	dum.GetYaxis().SetTitleSize(0.06)
	dum.GetXaxis().SetLabelSize(0.05)
	dum.GetYaxis().SetLabelSize(0.05)
        dum.GetXaxis().SetTitleOffset(0.95)
        #dum.GetYaxis().SetTitleOffset(0.85)

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
        #tex.Draw()
        CMS_lumi_v2( c1, 14, 11 )
        tex1 = TLatex(0.15,0.89,"CMS Phase II Simulation")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(61)
        tex1.SetTextSize(0.045)
        tex1.SetLineWidth(2)
        #tex1.Draw()
	# a legend

	leg = TLegend(0.63,0.525,0.87,0.875) #for 33 TeV (0.65,0.65,0.9,0.9)
        leg.SetBorderSize(1)
        leg.SetTextFont(62)
        leg.SetTextSize(0.03321678)
        leg.SetLineColor(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)


	leg.AddEntry(h_stc,'STC','l')
	leg.AddEntry(h_stoc,'STOC','l')
	leg.AddEntry(h_nm1,'NM1','l')
	leg.AddEntry(h_nm2,'NM2','l')
	leg.AddEntry(h_nm3,'NM3','l')
	#leg.AddEntry(h_stc_stoponly,'stc only stop','l')
	#leg.AddEntry(h_nm1_stoponly,'natural model 1 only stop','l')
	#leg.AddEntry(h_nm2_stoponly,'natural model 2 only stop','l')
	#leg.AddEntry(h_nm3_stoponly,'natural model 3 only stop','l')
	#if pu== 'NoPU': leg.SetHeader('no pileup')
	#if pu== '50PU': leg.SetHeader('pileup: 50')
	#if pu=='140PU': leg.SetHeader('pileup: 140')
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
	h_stoc.Draw('samehist')
	h_nm1.Draw('samehist')
	h_nm2.Draw('samehist')
	h_nm3.Draw('samehist')

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
W = 800
H = 600
H_ref = 600
W_ref = 800
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref
c1 = TCanvas('c1','c1',10,10,W,H);
c1.SetFillColor(0);
c1.SetBorderMode(0);
c1.SetFrameFillStyle(0);
c1.SetFrameBorderMode(0);
c1.SetLeftMargin( L/W );
c1.SetRightMargin( R/W );
c1.SetTopMargin( T/H );
c1.SetBottomMargin( B/H );
c1.SetTickx(0);
c1.SetTicky(0);
#c1=TCanvas('c1','',800,600)

#--------------------------------------------------------------------------------------------------------------------------------------------------------

########## preselection
quantity=['HT','0JetpT','1JetpT','2JetpT','3JetpT','nJet','nBJet','nMu','nEl','nLep','LeppT','Central','RawMET','dPhi','mT','mT2W']

label=['H_{T} (GeV)','0JetpT','1JetpT','2JetpT','3JetpT',
	  'Number of jets','Number of b-jets','nMu','nEl',
	  'Number of leptons','Leading lepton p_{T} (GeV)',
	  'Centrality','E_{T}^{miss} (GeV)',
	  'min ( #Delta #phi(j_{1},E_{T}^{miss}),#Delta #phi(j_{1},E_{T}^{miss}))','M_{T} (GeV)','M^{W}_{T2} (GeV)']

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
#n-1 plots
quantity_N1 =["HT_N1_stc","nJet_N1_stc","nBJet_N1_stc","Central_N1_stc","RawMET_N1_stc",
              "dPhi_N1_stc","mT_N1_stc","mT2W_N1_stc"]

lable_N1 =["H_{T} (GeV)","Number of jets","Number of b-jets","Centrality","E_{T}^{Miss} (GeV)",
           "min( #Delta #phi(j_{1},E_{T}^{miss}),#Delta #phi(j_{2},E_{T}^{miss}))",
           "M_{T} (GeV)","M^{W}_{T2} (GeV)"]
xmax_N1 =[5000,20,10,1,2000,3.2,1000,500]
bin_N1 =['150 GeV','1','1','0.02','40 GeV','0.08','20 GeV','10 GeV']

l=0

file_TTbar = TFile.Open(base+pu+'_TTbar_his.root')
file_BosonJets = TFile.Open(base+pu+'_BosonJets_his.root')
file_TopJets = TFile.Open(base+pu+'_TopJets_his.root')
file_DiBoson = TFile.Open(base+pu+'_DiBoson_his.root')
file_STC = TFile.Open(base+pu+'_STCfirst_his.root')
file_STOC = TFile.Open(base+pu+'_STOC_his.root')
file_NM1 = TFile.Open(base+pu+'_NM1_his.root')
file_NM2 = TFile.Open(base+pu+'_NM2_his.root')
file_NM3 = TFile.Open(base+pu+'_NM3_his.root')
file_dummy = TFile.Open(base+pu+'_NM3_his.root')



for what in quantity:
	for k in range (0,26):
		reb = 2
		if what == 'nLep' or what == 'nJet' or what == 'nBJet' or what == 'nEl' or what == 'nMu' or what =='mT2W':
			reb = 0
		print what+'_'+str(k)
		h_ttbar = get(file_TTbar, what+'_'+str(k),Lfac,1,1,1,kAzure-4,reb)
		h_bjets = get(file_BosonJets, what+'_'+str(k),Lfac,1,1,1,kViolet+5,reb)
		h_tjets = get(file_TopJets, what+'_'+str(k),Lfac,1,1,1,kCyan-6,reb)
		h_dibos = get(file_DiBoson, what+'_'+str(k),Lfac,1,1,1,kPink+3,reb)
		h_stc  = get(file_STC, what+'_'+str(k),Lfac,kBlack,2,1,0,reb)
		h_stoc  = get(file_STOC, what+'_'+str(k),Lfac,kSpring-5,2,1,0,reb)
		h_nm1  = get(file_NM1, what+'_'+str(k),Lfac,2,2,1,0,reb)
		h_nm2  = get(file_NM2, what+'_'+str(k),Lfac,4,2,1,0,reb)
		h_nm3  = get(file_NM3, what+'_'+str(k),Lfac,6,2,1,0,reb)

		# fill the bgrd stack - smallest first
		h_ent={}
		h_leg={} # entries in legend
		# bgrds
                h_ent[h_ttbar]=h_ttbar.Integral(0,5000)
                h_leg[h_ttbar]='t#bar{t}'
                #                                                                                                        
                h_ent[h_bjets]=h_bjets.Integral(0,5000)
                h_leg[h_bjets]='V + jets'
                #                                                                                                        
                h_ent[h_tjets]=h_tjets.Integral(0,5000)
                h_leg[h_tjets]='Single top'
                h_ent[h_dibos]=h_dibos.Integral(0,5000)
                h_leg[h_dibos]='VV'

		max = h_ttbar.GetMaximum()+h_bjets.GetMaximum()+h_tjets.GetMaximum()+h_dibos.GetMaximum()+h_ttbar.GetMaximum()
                max = max + 0.1*max
		import operator
		sorted_h = sorted(h_ent.iteritems(), key=operator.itemgetter(1))
		
		#plot(cutsShort[k]+'_'+str(k),sorted_h,h_leg,0.1,max,0,ymax[l],'selection: '+cuts[k]+'               '+what,'evts / bin',c1,1)
		plot(cutsShort[k]+'_'+str(k),sorted_h,h_leg,0.1,max,0,ymax[l],label[l],'evts / bin',c1,1)
	l=l+1

l=0

for what in quantity_N1:
	print what
	reb=2
	if what == 'nJet_N1_stc' or what == 'nBJet_N1_stc' or what == 'mT2W_N1_stc':
		reb = 0
	if what == 'HT_N1_stc' :
                reb = 15
	h_ttbar = get(file_TTbar, what,Lfac,1,1,1,kAzure-4,reb)
        h_bjets = get(file_BosonJets, what,Lfac,1,1,1,kViolet+5,reb)
        h_tjets = get(file_TopJets, what,Lfac,1,1,1,kCyan-6,reb)
        h_dibos = get(file_DiBoson, what,Lfac,1,1,1,kPink+3,reb)
        h_stc  = get(file_STC, what,Lfac,kBlack,2,1,0,reb)
        h_stoc  = get(file_STOC, what,Lfac,kSpring-5,2,1,0,reb)
        h_nm1  = get(file_NM1, what,Lfac,2,2,1,0,reb)
        h_nm2  = get(file_NM2, what,Lfac,4,2,1,0,reb)
        h_nm3  = get(file_NM3, what,Lfac,6,2,1,0,reb)

	# fill the bgrd stack - smallest first
	h_ent={}
	h_leg={} # entries in legend
	# bgrds
	h_ent[h_ttbar]=h_ttbar.Integral(0,5000)
	h_leg[h_ttbar]='t#bar{t}'
	#
	h_ent[h_bjets]=h_bjets.Integral(0,5000)
	h_leg[h_bjets]='V + jets'
	#
	h_ent[h_tjets]=h_tjets.Integral(0,5000)
	h_leg[h_tjets]='Single top'
	h_ent[h_dibos]=h_dibos.Integral(0,5000)
	h_leg[h_dibos]='VV'
	max = h_ttbar.GetMaximum()+h_bjets.GetMaximum()+h_tjets.GetMaximum()+h_dibos.GetMaximum()+h_ttbar.GetMaximum()
	import operator
	sorted_h = sorted(h_ent.iteritems(), key=operator.itemgetter(1))
	plot(what,sorted_h,h_leg,0.1,max,0,xmax_N1[l],lable_N1[l],'Events / '+bin_N1[l],c1,1)
	l=l+1
	
	#--------------------------------------------------------------------------------------------------------------------------------------------------------
