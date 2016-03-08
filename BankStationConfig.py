class BankStation_config:
    def __init__(self):
        self.filePath = "C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek/Stony_V3.0/"
        self.dssFileName = self.filePath + "HydraulicModel/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss"
        self.timestageFileName = self.filePath + "StonyCreek_timestage3.csv"
        self.bankFileName = self.filePath + "StonyCreek_banks2.csv"
        self.maxstageFileName = self.filePath + "StonyCreek_maxstage2.csv"
        self.outFileName = self.filePath + "OOB_StonyCreek.csv"