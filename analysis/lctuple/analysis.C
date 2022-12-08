#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TEfficiency.h"



void analysis(Int_t plot_ID=0)
{
    cout << "Plot IDs are the following" << endl;
    cout << "0: number of reconstructed jets" << endl;
    cout << "1: pseudorapidity of jets in the event" << endl;
    cout << "2: transverse momentum of jets in the event" << endl;
    cout << "3: phi of jets in the event" << endl;
    cout << "4: energy of jets in the event" << endl;
    cout << "5: invariant mass of jet pair associated to Higgs with highest pT" << endl;
    cout << "6: invariant mass of jet pair associated to Higgs with lowest pT" << endl;

    TH1F* m=new TH1F("m","m",40,0,250);
    TH1F* n_jets_ev=new TH1F("n_jets_ev","n_jets_ev",14,0,14);
    TH1F* m1=new TH1F("m1","m1",25,0,250);
    TH1F* m2=new TH1F("m2","m2",25,0,250);
    TH1F* eta_histo=new TH1F("eta_histo","eta_histo",30,-5,5);
    TH1F* E_histo=new TH1F("E_histo","E_histo",100,0,600);
    TH1F* pt_histo=new TH1F("pt_histo","pt_histo",60,0,300);
    TH1F* theta_histo=new TH1F("theta_histo","theta_histo",45,-0.5,4);
    TH1F* phi_histo=new TH1F("phi_histo","phi_histo",20,-2,2);
    double mh=125.;

    // Declaration of leaf types
    Int_t           nj;
    Float_t         jmox[9];   //[njet]
    Float_t         jmoy[9];   //[njet]
    Float_t         jmoz[9];   //[njet]
    Float_t         jmas[9];   //[njet]
    Float_t         jene[9];   //[njet]

    // List of branches
    TBranch        *b_njet;
    TBranch        *b_jmox;
    TBranch        *b_jmoy;
    TBranch        *b_jmoz;
    TBranch        *b_jmas;
    TBranch        *b_jene;

    TChain* fChain = new TChain("fChain");
    fChain->Add("./ntuple.root/MyLCTuple");


    fChain->SetBranchAddress("nj", &nj, &b_njet);
    fChain->SetBranchAddress("jmox", jmox, &b_jmox);
    fChain->SetBranchAddress("jmoy", jmoy, &b_jmoy);
    fChain->SetBranchAddress("jmoz", jmoz, &b_jmoz);
    fChain->SetBranchAddress("jmas", jmas, &b_jmas);
    fChain->SetBranchAddress("jene", jene, &b_jene);

    double inv_mass[1000][1000];

    double delta_min=10000000;
    double delta_tot;
    double delta_m1;
    double delta_m2;
    int jet1_num=0;
    int jet2_num=0;
    int jet3_num=0;
    int jet4_num=0;

    for(unsigned int ientry=0; ientry< fChain->GetEntries(); ++ientry) {

    fChain->GetEntry(ientry);
    n_jets_ev->Fill(nj);

    for (int k=0;k<nj; k++) {
        double jmom=sqrt(jmox[k]*jmox[k]+jmoy[k]*jmoy[k]+jmoz[k]*jmoz[k]);
        eta_histo->Fill(-TMath::Log(TMath::Tan(TMath::ACos(jmoz[k]/jmom)/2.)));
        pt_histo->Fill(jmom/TMath::CosH(-TMath::Log(TMath::Tan(TMath::ACos(jmoz[k]/jmom)/2.))));
        theta_histo->Fill(TMath::ACos(jmoz[k]/jmom));
        phi_histo->Fill(TMath::ATan(jmoy[k]/jmox[k]));
        E_histo->Fill(jene[k]);
    }
  
    if(nj>3) {//selection of events with more than four jets
        for (int i=0; i<nj-1; i++) {//Calculation of invariant mass
            for (int j=i+1; j<nj;j++) {
                double pij_mod=sqrt(((jmox[i]+jmox[j])*(jmox[i]+jmox[j]))+((jmoy[i]+jmoy[j])*(jmoy[i]+jmoy[j]))+((jmoz[i]+jmoz[j])*(jmoz[i]+jmoz[j])));
                inv_mass[i][j]=sqrt((jene[i]+jene[j])*(jene[i]+jene[j])-pij_mod*pij_mod);
        }
    }

        for (int i=0; i<nj; i++) {
            for (int j=i+1; j<nj;j++) {
                for (int k=0; k<nj; k++) {
                    for (int l=k+1; l<nj; l++) {
                        if(k==i || k==j || l==i || l==j) continue;
                        delta_m1 = mh - inv_mass[i][j];
                        delta_m2 = mh - inv_mass[k][l];
                        delta_tot = (delta_m1*delta_m1) + (delta_m2*delta_m2);
                        if (delta_tot < delta_min ) {
                            delta_min = delta_tot;
                            jet1_num = i;
                            jet2_num = j;
                            jet3_num = k;
                            jet4_num = l;
                        }
                    } //end l
                } //end k
            } //end j
        } //end i

        //ordering of H1 and H2
        double PT_H1=sqrt((jmox[jet1_num]+jmox[jet2_num])*(jmox[jet1_num]+jmox[jet2_num])+(jmoy[jet1_num]+jmoy[jet2_num])*(jmoy[jet1_num]+jmoy[jet2_num]));

        double PT_H2=sqrt((jmox[jet3_num]+jmox[jet4_num])*(jmox[jet3_num]+jmox[jet4_num])+(jmoy[jet3_num]+jmoy[jet4_num])*(jmoy[jet3_num]+jmoy[jet4_num]));

        if (PT_H1>=PT_H2){m1->Fill(inv_mass[jet1_num][jet2_num]);m2->Fill(inv_mass[jet3_num][jet4_num]);}

        if (PT_H1<PT_H2){m1->Fill(inv_mass[jet3_num][jet4_num]);m2->Fill(inv_mass[jet1_num][jet2_num]);}


    } //end nj>3

    for(int i=0; i<1000; i++) {for(int j=0;j<1000;j++){inv_mass[i][j]=0;}}
        delta_min=10000000;
        jet1_num=0;
        jet2_num=0;
        jet3_num=0;
        jet4_num=0;
    } // end of loop on fChain->GetEntries()


    if (plot_ID==0){
        TCanvas* n_jets = new TCanvas("n_jets","n_jets",900,600);
        n_jets_ev->SetTitle("Number of jets in the event");
        n_jets_ev->GetXaxis()->SetTitle("N_{jets}");
        n_jets_ev->Draw();
    }


    if (plot_ID==1){
        TCanvas* eta_canv = new TCanvas("eta_canv","eta_canv",900,600);
        eta_histo->SetTitle("Jets pseudorapidity");
        eta_histo->GetXaxis()->SetTitle("#eta");
        eta_histo->Draw();
    }

    if (plot_ID==2){
        TCanvas* pt_canv = new TCanvas("pt_canv","pt_canv",900,600);
        pt_histo->SetTitle("Jets transverse momentum");
        pt_histo->GetXaxis()->SetTitle("p_{T} [GeV]");
        pt_histo->Draw();
    }

    if (plot_ID==3){
        TCanvas* phi_canv = new TCanvas("phi_canv","phi_canv",900,600);
        phi_histo->SetTitle("Jets azimuthal angle");
        phi_histo->GetXaxis()->SetTitle("#phi [rad]");
        phi_histo->Draw();
    }

    if (plot_ID==4){
        TCanvas* E_canv = new TCanvas("E_canv","E_canv",900,600);
        E_histo->SetTitle("Jets energy");
        E_histo->GetXaxis()->SetTitle("Energy [GeV]");
        E_histo->Draw();
    }

    if (plot_ID==5){
        TCanvas* m1_canv = new TCanvas("m1_canv","m1_canv",900,600);
        m1->SetTitle("Invariant mass of jet pair with highest p_{T}");
        m1->GetXaxis()->SetTitle("M_{H_{1}} [GeV]");
        m1->Draw();
    }

    if (plot_ID==6){
        TCanvas* m2_canv = new TCanvas("m2_canv","m2_canv",900,600);
        m2->SetTitle("Invariant mass of jet pair with lowest p_{T}");
        m2->GetXaxis()->SetTitle("M_{H_{2}} [GeV]");
        m2->Draw();
    }





    TFile* f=new TFile("Plotsmass.root","RECREATE");
    if ( f->IsOpen() ) cout << "File opened successfully" << endl;
    n_jets_ev->Write();
    m->Write();
    m1->Write();
    m2->Write();
    eta_histo->Write();
    E_histo->Write();
    pt_histo->Write();
    theta_histo->Write();
    phi_histo->Write();
}
