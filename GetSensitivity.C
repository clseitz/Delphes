
#include<iostream>
#include<fstream>

// .L GetSensitivity.C
// DrawPlots(model, uncert)
//model can be "NM" for plot with NM1, NM2, NM3
// "all" - all models NM + STC + STOC
//uncertainty in percent 15, 25, 50 

void DrawPlots(TString model = "all", Double_t uncert = 15){
  
 int W = 600;
 int H = 600;
 TString canvName = "plot_significance_vs_lumi";
 TCanvas* c = new TCanvas(canvName,canvName,10,10,W,H);

  writeExtraText = true;       // if extra text
  extraText  = "Preliminary";  // default extra text is "Preliminary"
  lumi_8TeV  = "19.1 fb^{-1}"; // default is "19.7 fb^{-1}"
  lumi_7TeV  = "4.9 fb^{-1}";  // default is "5.1 fb^{-1}"

  int iPeriod = 14;    // 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV, 14= PU=140,14TeV 
  int iPos = 11;

  Double_t lumi0 = 3000;


  //                   STC,        STOC,         NM1,        NM2,        NM3
  Double_t Bkg[5] = { 291.668101,  11.007697, 291.668101,  291.668101,   291.668101}; // bkg
  Double_t Sig[5] = {349.567000, 39.955400 , 563.800000,  518.201000 ,794.853000};
  //  Double_t Uncertainty[5] = {15, 15, 15, 15, 15};
  TF1* fun[5];
  for (Int_t i=0;i<5;i++){
    cout<<i<<endl;    
    Sig[i] = Sig[i]/lumi0;
    Bkg[i] = Bkg[i]/lumi0;
    fun[i] = new TF1("h",GetSensitivity,0.001,3000,3);
    fun[i] ->SetParameter(0,Sig[i]+Bkg[i]);
    fun[i] ->SetParameter(1,Bkg[i]);
    fun[i] ->SetParameter(2,uncert/100.0);
    fun[i] ->SetLineWidth(4);
  }

  TF1* dum = new TF1("h",GetSensitivity,0.001,3000,3);
    dum->SetParameter(0,1);
    dum ->SetParameter(1,1);
    dum ->SetParameter(2,0.1);
    dum->SetLineColor(kWhite);
  dum-> SetTitle("");
  dum ->GetXaxis()->SetTitle("Luminosity (fb^{-1})");
  dum ->GetYaxis()->SetTitle("Expected significance");
  dum ->GetYaxis()->SetTitleOffset(0.8);
  dum ->GetXaxis()->SetTitleOffset(0.8);
  dum ->GetYaxis()->SetTitleSize(0.05);
  dum ->GetXaxis()->SetTitleSize(0.05);
  dum ->GetYaxis()->SetRangeUser(0.01,12.0);
  fun[4] ->SetLineColor(6);
  fun[3] ->SetLineColor(4);
  fun[2] ->SetLineColor(2);
  fun[1] ->SetLineColor(kSpring-5);
  fun[0] ->SetLineColor(kBlack);
  
TLegend *leyenda = new TLegend(0.715517,0.677966,0.890805,0.885593,NULL,"brNDC");
   leyenda->SetBorderSize(1);
   leyenda->SetLineColor(0);
   leyenda->SetLineStyle(1);
   leyenda->SetLineWidth(1);
   leyenda->SetFillColor(0);
   leyenda->SetFillStyle(1001);
  dum -> Draw();
  if(model == "all"){
    leyenda->AddEntry(fun[0],"STC","l");
    leyenda->AddEntry(fun[1],"STOC","l");
    fun[1] ->Draw("same");
    fun[0] ->Draw("same");
  }
  leyenda->AddEntry(fun[2],"NM1","l");
  leyenda->AddEntry(fun[3],"NM2","l");
  leyenda->AddEntry(fun[4],"NM3","l");
  
  fun[4] ->Draw("same");
  fun[3] ->Draw("same");
  fun[2] ->Draw("same");

  TF1* discovery = new TF1("disc","5",0.001,3000);
  discovery->SetLineStyle(2);
  discovery->SetLineColor(kBlack);
  discovery->SetLineWidth(1);
  discovery->Draw("same");
  TF1* observation = new TF1("obs","3",0.001,3000);
  observation->SetLineStyle(2);
  observation->SetLineColor(kBlack);
  observation->SetLineWidth(1);
  observation->Draw("same");
  leyenda->Draw("same");

  TLatex *   tex = new TLatex(0.6224832,0.9230769,"14 TeV, PU = 140");
  tex->SetNDC();
  tex->SetTextAlign(12);
  tex->SetTextFont(42);
  tex->SetTextSize(0.04);
  tex->SetLineWidth(2);
  tex->Draw();
  tex->Draw("same");

  TLatex* tex1 = new TLatex(0.15,0.89,"CMS Phase II Simulation");
  tex1->SetNDC();                                                                       
  tex1->SetTextAlign(13);
  tex1->SetTextFont(61);                                                                                                   
  tex1->SetTextSize(0.045);                                                                                                
  tex1->SetLineWidth(2);                                                                                                 
  tex1->Draw();
  
  //CMS_lumi_v2( c, iPeriod, iPos );
  TString filename = model+"_uncert"+=uncert;
  c->SaveAs(filename+".pdf");
}


Double_t GetSensitivity(Double_t *x, Double_t *par){

  return RooStats::NumberCountingUtils::BinomialObsZ(par[0]*x[0],par[1]*x[0],par[2]);

}
