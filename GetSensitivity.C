
#include<iostream>
#include<fstream>

// .L GetSensitivity.C
// DrawPlots()

void DrawPlots(){
  TCanvas* c = new TCanvas();

  writeExtraText = true;       // if extra text
  extraText  = "Preliminary";  // default extra text is "Preliminary"
  lumi_8TeV  = "19.1 fb^{-1}"; // default is "19.7 fb^{-1}"
  lumi_7TeV  = "4.9 fb^{-1}";  // default is "5.1 fb^{-1}"

  int iPeriod = 14;    // 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV, 14= PU=140,14TeV 
  int iPos = 11;

  Double_t lumi0 = 3000;

  //  Double_t S[3] = {299.01, 299.01, 299.01}
  //Double_t B[3] = {299.01+347.3, 299.01+662.4, 299.01+644.2};//,299+853};

  Double_t S[4] = {299.017719,299.01573,299.017719,299.01771}; // bkg
  Double_t B[4] = {347.9729+299.01719,562.086+299.01573,299.017719+516.701,299.01771+794.8592}; // signal + bkg
  TF1* fun[3];
  for (Int_t i=0;i<4;i++){
    S[i] = S[i]/lumi0;
    B[i] = B[i]/lumi0;
    fun[i] = new TF1("h",GetSensitivity,0.001,3000,2);
    fun[i] ->SetParameter(0,B[i]);
    fun[i] ->SetParameter(1,S[i]);
    fun[i] ->SetLineWidth(4);
 }
  fun[3] -> SetTitle("");
  fun[3] ->GetXaxis()->SetTitle("L_{int} (fb^{-1})");
  fun[3] ->GetYaxis()->SetTitle("Expected sensitivity");
  fun[3] ->GetYaxis()->SetTitleOffset(0.85);
  fun[3] ->GetYaxis()->SetTitleSize(0.05);
  fun[3] ->GetXaxis()->SetTitleSize(0.05);
  fun[3] ->SetLineColor(1);
  fun[1] ->SetLineColor(kMagenta);
  fun[0] ->SetLineColor(8);
  
 
TLegend *leyenda = new TLegend(0.715517,0.677966,0.890805,0.885593,NULL,"brNDC");
   leyenda->SetBorderSize(1);
   leyenda->SetLineColor(0);
   leyenda->SetLineStyle(1);
   leyenda->SetLineWidth(1);
   leyenda->SetFillColor(0);
   leyenda->SetFillStyle(1001);
  leyenda->AddEntry(fun[0],"STC");
  leyenda->AddEntry(fun[1],"NM1");
  leyenda->AddEntry(fun[2],"NM2");
  leyenda->AddEntry(fun[3],"NM3");
  fun[3] ->Draw();
  fun[2] ->Draw("same");
  fun[1] ->Draw("same");
  fun[0] ->Draw("same");
  TF1* discovery = new TF1("ha","5",0.001,3000);
  discovery->SetLineStyle(2);
  discovery->Draw("same");
    TF1* observation = new TF1("ha","3",0.001,3000);
  observation->SetLineStyle(2);
  observation->Draw("same");
  leyenda->Draw("same");
  //  TLatex* label = new TLatex(-20.,50.,"Significance #frac{#delta B}{B} = 15 %");
  TLatex* label = new TLatex(-20.,50.,"14 TeV, PU = 140");
  label->SetNDC();
  label->SetTextAlign(12);
  label->SetX(0.0991379);
  label->SetY(0.93);
  label->SetTextFont(42);
  label->SetTextSize(0.04);
  label->SetTextSizePixels(22);
  label->Draw("same");

  TLatex* label2 = new TLatex(-20.,50.,"5#sigma");
  label2->SetNDC();
  label2->SetTextAlign(12);
  label2->SetX(0.862069);
  label2->SetY(0.351695);
  label2->SetTextFont(42);
  label2->SetTextSize(0.04);
  label2->SetTextSizePixels(22);
  //  label2->Draw("same");
 TLatex* label3 = new TLatex(-20.,50.,"3#sigma");
  label3->SetNDC();
  label3->SetTextAlign(12);
  label3->SetX(0.862069);
  label3->SetY(0.351695);
  label3->SetTextFont(42);
  label3->SetTextSize(0.04);
  label3->SetTextSizePixels(22);
  //label3->Draw("same");

  TLatex* tex1 = new TLatex(0.15,0.89,"CMS Phase II Simulation");
  tex1->SetNDC();                                                                       
  tex1->SetTextAlign(13);
  tex1->SetTextFont(61);                                                                                                   
  tex1->SetTextSize(0.045);                                                                                                
  tex1->SetLineWidth(2);                                                                                                 
  tex1->Draw();
  
  //CMS_lumi_v2( c, iPeriod, iPos );
  
}


Double_t GetSensitivity(Double_t *x, Double_t *par){
  ofstream temp;
  temp.open("tmp.txt");
  temp << RooStats::NumberCountingUtils::BinomialObsZ(par[0]*x[0],par[1]*x[0],0.15) << std::endl;
  temp.close();
 

  char* number;

  ifstream tmp1("tmp.txt");
  Double_t result;
  tmp1 >> result;
  return result;
 
  

}
