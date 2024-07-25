import glob
import pyLCIO
from pyLCIO import EVENT, UTIL

import ROOT
ROOT.gROOT.SetBatch()

DATA_PATH = "/ospool/uc-shared/project/muoncollider/tutorial2024/photonGun_E_250_1000"
PDF = "photons.pdf"

ECAL_BARREL = "EcalBarrelCollectionDigi"
ECAL_ENDCAP = "EcalEndcapCollectionDigi"

COLS = [
    ECAL_BARREL,
    ECAL_ENDCAP,
]

def main():
    nlayers = 50
    ytitle = "N(digi hits per event)"
    barrel_occ = ROOT.TH1F("barrel_occ", f"Barrel Occupancy;Barrel Layer;{ytitle}", nlayers, -0.5, nlayers-0.5)
    endcap_occ = ROOT.TH1F("endcap_occ", f"Endcap Occupancy;Endcap Layer;{ytitle}", nlayers, -0.5, nlayers-0.5)
    fill_histograms(barrel_occ, endcap_occ)
    plot_histograms(barrel_occ, endcap_occ)


def fill_histograms(barrel_occ, endcap_occ):
    n_events = 0
    for event in get_events():
        n_events += 1
        barrel_hits = get_collection(event, ECAL_BARREL)
        endcap_hits = get_collection(event, ECAL_ENDCAP)
        if not barrel_hits and not endcap_hits:
            continue
        decoder = get_decoder(barrel_hits if barrel_hits else endcap_hits)
        for hit in barrel_hits:
            decoder.setValue((hit.getCellID0() & 0xFFFFFFFF) | (hit.getCellID1() << 32))
            barrel_occ.Fill(decoder["layer"].value())
        for hit in endcap_hits:
            decoder.setValue((hit.getCellID0() & 0xFFFFFFFF) | (hit.getCellID1() << 32))
            endcap_occ.Fill(decoder["layer"].value())
    barrel_occ.Scale(1.0 / n_events)
    endcap_occ.Scale(1.0 / n_events)


def plot_histograms(barrel_occ, endcap_occ):
    rootlogon()
    for hist in [barrel_occ, endcap_occ]:
        name = hist.GetName()
        canv = ROOT.TCanvas(f"canv_{name}", "canv_{name}", 800, 800)
        canv.Draw()
        stylize(hist)
        hist.SetMinimum(0)
        hist.Draw("histesame")
        suffix = "(" if hist == barrel_occ else ")"
        canv.Print(PDF + suffix, "pdf")


def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []


def get_decoder(collection):
    encoding = collection.getParameters().getStringVal(EVENT.LCIO.CellIDEncoding)
    decoder = UTIL.BitField64(encoding)
    return decoder


def get_events():

    print("Opening slcio files ...")
    filenames = get_files()

    for i_filename, filename in enumerate(filenames):
        print(f"Analyzing {filename} ({i_filename})")
        reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
        reader.setReadCollectionNames(COLS)
        reader.open(filename)

        for event in reader:
            yield event

        reader.close()


def get_files(num=-1):
    files = sorted(glob.glob(DATA_PATH + "/*.slcio"))
    if num != -1:
        files = files[:num]
    print(f"Found {len(files)} files")
    return files


def rootlogon():
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPaintTextFormat(".2f")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetFillColor(10)
    # ROOT.gStyle.SetPalette(ROOT.kCherry)
    # ROOT.TColor.InvertPalette()
    ROOT.gStyle.SetPadTopMargin(0.06)
    ROOT.gStyle.SetPadRightMargin(0.19)
    ROOT.gStyle.SetPadBottomMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.15)


def stylize(hist):
    size = 0.04
    hist.SetLineWidth(2)
    hist.GetXaxis().SetTitleSize(size)
    hist.GetXaxis().SetLabelSize(size)
    hist.GetYaxis().SetTitleSize(size)
    hist.GetYaxis().SetLabelSize(size)
    hist.GetZaxis().SetTitleSize(size)
    hist.GetZaxis().SetLabelSize(size)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetYaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetLabelOffset(0.003)
    hist.GetXaxis().SetNdivisions(505)

if __name__ == "__main__":
    main()
