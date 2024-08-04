import glob
import math
import pyLCIO

import ROOT

ROOT.gROOT.SetBatch()

DATA_PATH = "/ospool/uc-shared/project/muoncollider/tutorial2024/nuGun_pT_0_50"
PDF = "bib.pdf"

ECAL_BARREL = "ECalBarrelCollection"
ECAL_ENDCAP = "ECalEndcapCollection"
HCAL_BARREL = "HCalBarrelCollection"
HCAL_ENDCAP = "HCalEndcapCollection"

COLS = [
    ECAL_BARREL,
    ECAL_ENDCAP,
    HCAL_BARREL,
    HCAL_ENDCAP,
]


def main():
    nlayers = 50
    hist = ROOT.TH2F(
        "rz", ";Z [mm];R [mm];Sim. Energy [GeV]", 100, -5000, 5000, 100, 0, 5000
    )
    fill_histogram(hist)
    plot_histogram(hist)


def fill_histogram(hist):
    n_events = 0
    for event in get_events():
        n_events += 1
        for col in COLS:
            hits = get_collection(event, col)
            for hit in hits:
                r, z = get_rz(hit)
                hist.Fill(z, r, hit.getEnergy())

    hist.Scale(1.0 / n_events)


def get_rz(hit):
    position = hit.getPosition()
    x, y, z = position[0], position[1], position[2]
    r = math.sqrt(x**2 + y**2)
    return r, z


def plot_histogram(hist):
    rootlogon()
    name = hist.GetName()
    canv = ROOT.TCanvas(f"canv_{name}", "canv_{name}", 800, 800)
    canv.Draw()
    stylize(hist)
    hist.SetMinimum(0)
    hist.Draw("colzsame")
    canv.Print(PDF + "(", "pdf")
    canv.SetLogz()
    canv.Print(PDF + ")", "pdf")


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
    i_event = 0

    for i_filename, filename in enumerate(filenames):
        print(f"Analyzing {filename} ({i_filename})")
        reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
        reader.setReadCollectionNames(COLS)
        reader.open(filename)

        for event in reader:
            print(f"Processing event {i_event}")
            i_event += 1
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
    hist.GetYaxis().SetTitleOffset(1.7)
    hist.GetZaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetLabelOffset(0.003)
    hist.GetXaxis().SetNdivisions(505)


if __name__ == "__main__":
    main()
