REFMAP = {
  'LPPL'           : 'R_JENIS_KARTU_APMK2'
}
  
class LKPBU_FORM_301:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LPPL']
    self.attrlist = [
      'Keterangan'
      , 'JumlahKartu'
      , 'KartuBaru'
      , 'KartuTutup'
      , 'JumlahAccount'
      , 'KartuUtama'
      , 'KartuTambahan'
      , 'KL05'
      , 'KL510'
      , 'KL1025'
      , 'KL2550'
      , 'KL50100'
      , 'KL100'
      , 'IRRMin'
      , 'IRRMax'
      , 'IRCAMin'
      , 'IRCAMax'
      , 'LateFeeMin'
      , 'LateFeeMax'
      , 'OverLimitMin'
      , 'OverLimitMax'
      , 'AnnualFeeMin'
      , 'AnnualFeeMax'
      , 'BCAMin'
      , 'BCAMax'
      , 'FPDefJumlah'
      , 'FPDefNominal'
      , 'WriteOffJumlah'
      , 'WriteOffNominal'
      , 'RecoveryJumlah'
      , 'RecoveryNominal'
      , 'HapusTagihJumlah'
      , 'HapusTagihNominal'
      , 'BRNOCurrent'
      , 'BRNOXD'
      , 'BRNO30D'
      , 'BRNO60D'
      , 'BRNO90D'
      , 'BRNO120D'
      , 'BRNO150D'
      , 'BRNO180D'
      , 'BRAOCurrent'
      , 'BRAOXD'
      , 'BRAO30D'
      , 'BRAO60D'
      , 'BRAO90D'
      , 'BRAO120D'
      , 'BRAO150D'
      , 'BRAO180D'
      , 'VolTunaiIntl'
      , 'VolTunaiLokal'
      , 'VolBelanjaIntl'
      , 'VolBelanjaLokal'
      , 'NilaiTunaiIntl'
      , 'NilaiTunaiLokal'
      , 'NilaiBelanjaIntl'
      , 'NilaiBelanjaLokal'
      , 'RevolvingRate'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form301.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LPPL_reference_code'  
      , 2: 'Keterangan'
      , 3: 'JumlahKartu'
      , 4: 'KartuBaru'
      , 5: 'KartuTutup'
      , 6: 'JumlahAccount'
      , 7: 'KartuUtama'
      , 8: 'KartuTambahan'
      , 9: 'KL05'
      , 10: 'KL510'
      , 11: 'KL1025'
      , 12: 'KL2550'
      , 13: 'KL50100'
      , 14: 'KL100'
      , 15: 'IRRMin'
      , 16: 'IRRMax'
      , 17: 'IRCAMin'
      , 18: 'IRCAMax'
      , 19: 'LateFeeMin'
      , 20: 'LateFeeMax'
      , 21: 'OverLimitMin'
      , 22: 'OverLimitMax'
      , 23: 'AnnualFeeMin'
      , 24: 'AnnualFeeMax'
      , 25: 'BCAMin'
      , 26: 'BCAMax'
      , 27: 'FPDefJumlah'
      , 28: 'FPDefNominal'
      , 29: 'WriteOffJumlah'
      , 30: 'WriteOffNominal'
      , 31: 'RecoveryJumlah'
      , 32: 'RecoveryNominal'
      , 33: 'HapusTagihJumlah'
      , 34: 'HapusTagihNominal'
      , 35: 'BRNOCurrent'
      , 36: 'BRNOXD'
      , 37: 'BRNO30D'
      , 38: 'BRNO60D'
      , 39: 'BRNO90D'
      , 40: 'BRNO120D'
      , 41: 'BRNO150D'
      , 42: 'BRNO180D'
      , 43: 'BRAOCurrent'
      , 44: 'BRAOXD'
      , 45: 'BRAO30D'
      , 46: 'BRAO60D'
      , 47: 'BRAO90D'
      , 48: 'BRAO120D'
      , 49: 'BRAO150D'
      , 50: 'BRAO180D'
      , 51: 'VolTunaiIntl'
      , 52: 'VolTunaiLokal'
      , 53: 'VolBelanjaIntl'
      , 54: 'VolBelanjaLokal'
      , 55: 'NilaiTunaiIntl'
      , 56: 'NilaiTunaiLokal'
      , 57: 'NilaiBelanjaIntl'
      , 58: 'NilaiBelanjaLokal'
      , 59: 'RevolvingRate'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form301.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [30,0]  
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [5,2]
      , [5,2]
      , [5,2]
      , [5,2]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [5,2]
      , [12,1]
      , [15,1]
      , [12,1]
      , [15,1]
      , [12,1]
      , [15,1]
      , [12,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [5,2]
    )
  #--

  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
        
      return res
      
  def onenter(self, sender):
    #self.pData_CreditCrad.Enabled=0
    Code = int(self.uipData.GetFieldValue('LJENIS.reference_code'))
    #raise Exception, Code 
    if Code >= 110 and Code < 200:
      self.uipData.CreditCrad=''
      self.pData_CreditCrad.Enabled=1
      
      
    