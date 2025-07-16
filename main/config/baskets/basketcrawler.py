

corrected_tickers = [
    "NESN.SW", "ASML.AS", "NOVO-B.CO", "MC.PA", "AZN.L", "ROG.SW", "NOVN.SW", "SHEL.L", "HSBA.L", "TTE.PA", "SAP.DE",
    "ULVR.L", "SIE.DE", "SAN.PA", "BP.L", "OR.PA", "SU.PA", "DGE.L", "AI.PA", "ALV.DE", "CFR.SW", "AIR.PA",
    "RMS.PA", "IBE.MC", "DTE.DE", "RIO.L", "ZURN.SW", "GSK.L", "DG.PA", "BNP.PA", "BATS.L", "REL.L", "MBG.DE",
    "ABBN.SW", "UBSG.SW", "GLEN.L", "SAN.MC", "SAF.PA", "EL.PA", "CS.PA", "RKT.L", "BAYN.DE", "IFX.DE", "PRX.AS",
    "ABI.BR", "ENEL.MI", "MUV2.DE", "INGA.AS", "CPG.L", "NG.L", "ADYEN.AS", "DHL.DE", "LONN.SW", "BBVA.MC", "BAS.DE",
    "RI.PA", "ISP.MI", "SIKA.SW", "LSEG.L", "ITX.MC", "KER.PA", "UCG.MI", "ALC.SW", "AAL.L", "STLAM.MI", "CRH.L",
    "PRU.L", "NDA-FI.HE", "BMW.DE", "LLOY.L", "BN.PA", "ATCO-A.ST", "BA.L", "INVE-B.ST", "RACE.MI", "FLTR.L",
    "DB1.DE", "DSV.CO", "EXPN.L", "HOLN.SW", "ENI.MI", "AMS.MC", "CAP.PA", "STMMI.MI", "WKL.AS", "AD.AS",
    "VOLV-B.ST", "DSY.PA", "EQNR.OL", "ADS.DE", "SGO.PA", "AHT.L", "RWE.DE", "BARC.L", "ENGI.PA", "VOW3.DE",
    "VWS.CO", "SREN.SW", "HEIA.AS", "LR.PA", "GIVN.SW", "EVO.ST", "SSE.L", "GMAB.CO", "EOAN.DE", "HEXA-B.ST",
    "III.L", "TSCO.L", "HLN.L", "MRK.DE", "ASSA-B.ST", "ORA.PA", "G.MI", "NOKIA.HE", "TEF.MC", "SAMPO.HE",
    "CLNX.MC", "PGHN.SW", "VOD.L", "ARGX.BR", "SAND.ST", "KNEBV.HE", "VIE.PA", "ML.PA", "DBK.DE", "IMB.L",
    "STAN.L", "RTO.L", "GLE.PA", "REP.MC", "SEB-A.ST", "ASM.AS", "PUB.PA", "PHIA.AS", "NESTE.HE", "ORSTED.CO",
    "DSFIR.AS", "SLHN.SW", "GEBN.SW", "STMN.SW", "NWG.L", "LGEN.L", "UPM.HE", "KBC.BR", "ERIC-B.ST", "EDEN.PA",
    "DTG.DE", "UMG.AS", "FER.AS", "KNIN.SW", "CABK.MC", "DNB.OL", "DANSKE.CO", "ESSITY-B.ST", "RR.L",
    "SWED-A.ST", "SHL.DE", "SCMN.SW", "CARL-B.CO", "EQT.ST", "HO.PA", "COLO-B.CO", "NIBE-B.ST", "ACA.PA",
    "MONC.MI", "KGA.IR", "SGSN.SW", "VNA.DE", "P911.DE", "AV.L", "SN.L", "SY1.DE", "AKZA.AS",
    "BAER.SW", "SOON.SW", "SHB-A.ST", "MT.AS", "EDP.LS", "MTX.DE", "BNZL.L", "INF.L", "HEN3.DE", "BEI.DE",
    "IHG.L", "HNR1.DE", "TRN.MI", "RHM.DE", "BT-A.L", "BNR.DE", "EPI-A.ST", "LISN.SW", "WPP.L", "ENR.DE",
    "AENA.MC", "CBK.DE", "SGRO.L", "UCB.BR", "FRE.DE", "HEI.DE", "SGE.L", "HLMA.L", "EBS.VI", "SRG.MI", "BRBY.L",
    "KPN.AS", "VACN.SW", "BIRG.IR", "PRY.MI", "FGR.PA", "QIA.DE", "ALFA.ST", "RYA.IR", "SPX.L", "TEP.PA",
    "NSIS-B.CO", "CA.PA", "HEIO.AS", "KGP.IR", "NXT.L", "CRDA.L", "SIGN.SW", "HM-B.ST", "SKG.IR", "PAH3.DE",
    "SRT.DE", "PKN.WA", "FME.DE", "NN.AS", "SW.PA", "SCHN.SW", "NHY.OL", "EN.PA", "ENT.L", "LOGN.SW",
    "ITRK.L", "UU.L", "EXO.AS", "CNA.L", "WTB.L", "WLN.PA", "1COV.DE", "SVT.L", "MRO.L", "BESI.AS", "ERF.PA",
    "ABF.L", "MAERSK-B.CO", "UHR.SW", "BOL.ST", "CON.DE", "FBK.MI", "IMCD.AS", "ELISA.HE", "ALO.PA", "RNO.PA",
    "SOLB.BR", "TRYG.CO", "AGN.AS", "BVI.PA", "MOWI.OL", "STERV.HE", "DHER.DE", "STJ.L", "METSO.HE", "ADM.L",
    "JMT.LS", "ANTO.L", "SMIN.L", "AUTO.L", "PSON.L", "AKRBP.OL", "PNDORA.CO", "ACS.MC", "PKO.WA",
    "SCA-B.ST", "GBLB.BR", "CPR.MI", "RED.MC", "DIM.PA", "ELE.MC", "AGS.BR", "MNDI.L", "BALN.SW", "BARN.SW",
    "ABN.AS", "ZAL.DE", "TEL.OL", "SPSN.SW", "MB.MI", "RAND.AS", "G1A.DE", "BAMI.MI", "AC.PA", "BME.L",
    "TEN.MI", "INDU-C.ST", "BANB.SW", "VIV.PA", "ASRNL.AS", "SKF-B.ST", "SAB.MC", "OMV.VI", "CCH.L",
    "TREL-B.ST", "FORTUM.HE", "LHA.DE", "SBRY.L", "WEIR.L", "PHNX.L", "MNG.L", "DCC.L", "RXL.PA",
    "ENX.PA", "UMI.BR", "KGF.L", "WRT1V.HE", "YAR.OL", "SDR.L", "ADDT-B.ST", "RMV.L", "PZU.WA", "TELIA.ST",
    "BDEV.L", "KESKOB.HE", "GALP.LS", "PUM.DE", "ORK.OL", "DNP.WA", "GET.PA", "IMI.L", "ABDN.L", "AKE.PA",
    "SKA-B.ST", "BKG.L", "NTGY.MC", "SMDS.L", "TEMN.SW", "EMSN.SW", "ADEN.SW", "NEXI.MI", "IAG.L",
    "ICG.L", "PSPN.SW", "VER.VI", "URW.AS", "WISE.L", "SXS.L", "GETI-B.ST", "LAND.L", "TECN.SW", "GFC.PA",
    "PST.MI", "AIBG.I", "EDPR.LS", "HSX.L", "AMP.MI", "TW.L", "BEAN.SW", "VAL.PA", "DPLM.L", "REC.MI",
    "BEIJ-B.ST", "BOL.PA", "NEM.DE", "LIFCO-B.ST", "BEZ.L", "HWDN.L", "HELN.SW", "RS1.L", "ATE.PA",
    "PSN.L", "PEO.WA", "TEL2-B.ST", "VALMT.HE", "MKS.L", "JD..L", "KBX.DE", "G24.DE", "ENG.MC", "SPIE.PA",
    "SSAB-B.ST", "IP.MI", "WDP.BR", "LDO.MI", "FDJ.PA", "BOSS.DE", "INW.MI", "ORNBV.HE",
    "SAAB-B.ST", "DUFN.SW", "GAW.L", "IPN.PA", "AFX.DE", "LEG.DE", "INDU-C.ST", "ANA.MC", "CTEC.L", "AM.PA",
    "SOI.PA", "SOBI.ST", "CTM.ST", "AALB.AS", "ELI.BR", "SAGA-B.ST", "FRVIA.PA", "INCH.L", "DIE.BR",
    "RILBA.CO", "SECU-B.ST", "JMAT.L", "ANDR.VI", "BKT.MC", "KOG.OL", "DEMANT.CO", "CDI.PA", "KGH.WA",
    "GALN.SW", "VOE.VI", "RBREW.CO", "BG.VI", "EVK.DE", "TOM.OL", "HIK.L", "TATE.L", "SCR.PA", "TKA.DE",
    "RF.PA", "JDEP.AS", "UTG.L", "FHZN.SW", "BLND.L", "ACKB.BR", "AIXA.DE", "AMUN.PA", "LIGHT.AS", "EVD.DE",
    "HL..L", "LPP.WA", "IGG.L", "GRF.MC", "RAA.DE", "STB.OL", "JYSK.CO", "OCDO.L", "ROR.L", "EMG.L", "SFZN.SW",
    "INVP.L", "RCO.PA", "GRG.L", "TUI1.DE", "EVT.DE", "KINV-B.ST", "ELIS.PA",
    "AAK.ST", "BC8.DE", "SOF.BR", "BKW.SW", "BWY.L", "HUH1V.HE", "HOLM-B.ST", "ALE.WA", "BAKKA.OL", "GTT.PA",
    "CLN.SW", "GXI.DE", "BBOX.L", "ITV.L", "SDF.DE", "WIE.VI", "SOP.PA", "LUND-B.ST", "ARCAD.AS", "BC.MI",
    "GJF.OL", "TLX.DE", "ELUX-B.ST", "SALM.OL", "ISS.CO", "OCI.AS", "INDV.L", "BCVN.SW", "FAG.ST", "DRX.L",
    "TE.PA", "BUCN.SW", "THULE.ST", "LOTB.BR", "FNTN.DE", "LATO-B.ST", "IG.MI", "VTY.L", "SK.PA", "BVIC.L",
    "WKL.AS", "EKTAB.ST", "MRL.MC", "HEXA-B.ST", "LXS.DE", "GN.CO", "VRLA.PA", "AED.BR", "TIT.MI", "GL9.IR",
    "DIA.MI", "A2A.MI", "ALLFG.AS", "AMBU-B.CO", "TIETO.HE", "SYDB.CO", "BPE.MI", "TKWY.AS", "OSB.L", "DLN.L",
    "REY.MI", "DKSH.SW", "UBI.PA", "COFB.BR", "ALLN.SW", "WCH.DE", "AF.PA", "BYG.L", "FPE.DE", "BB.PA",
    "VIS.MC", "LAGR-B.ST", "AZA.ST", "SECT-B.ST", "KGX.DE", "DLG.L", "SAFE.L", "PNN.L", "HER.MI", "RUI.PA",
    "SCT.L", "BALD-B.ST", "SUBC.OL", "O2D.DE", "NEX.PA", "AXFO.ST", "AZM.MI", "BAVA.CO", "VID.MC", "QQ..L",
    "SWEC-B.ST", "CMBN.SW", "TOP.CO", "CCC.L", "COV.PA", "TIGO-SDB.ST", "VOLCAR-B.ST", "NOD.OL", "AMS.SW",
    "ROCK-B.CO", "DWL.L", "SGRO.L", "TPK.L", "FRO.OL", "HAS.L", "GFTU.L", "ECV.DE", "LMP.L", "GNS.L",
    "NEL.OL", "FABG.ST", "KOJAMO.HE", "IDS.L", "WIHL.ST", "WOSG.L", "HBR.L", "NOBI.ST",
    "SESG.PA", "ANE.MC", "ENOG.L", "LXI.L", "EMBRAC-B.ST", "COL.MC", "CBG.L", "BILL.ST", "SINCH.ST",
    "ALK-B.CO", "WALL-B.ST", "HTRO.ST", "FUTR.L", "UTDI.DE", "AT1.DE", "SBB-B.ST"
]

list2 = ['KGA.IR', 'KGP.IR', 'SKG.IR', 'BDEV.L', 'SMDS.L', 'URW.AS', 'AIBG.I', 'JD..L', 'FDJ.PA', 'DUFN.SW', 'GALN.SW', 'HL..L', 'BVIC.L', 'EKTAB.ST', 'DLG.L', 'O2D.DE', 'QQ..L', 'TOP.CO', 'TIGO-SDB.ST', 'ECV.DE', 'IDS.L', 'LXI.L']
a=list(set(corrected_tickers)-set(list2))
print (a)

import yfinance as yf
import pandas as pd

valid = []
invalid = []

for ticker in a:
    try:
        info = yf.Ticker(ticker).info
        if info and 'regularMarketPrice' in info:
            valid.append(ticker)
        else:
            invalid.append(ticker)
    except Exception:
        invalid.append(ticker)

# Ergebnis anzeigen
print(f"✅ Gültige Ticker: {len(valid)}")
print(valid)
print(f"\n❌ Ungültige Ticker: {len(invalid)}")
print(invalid)
