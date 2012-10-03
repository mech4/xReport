REFMAP = {
  'LJENIS'           : 'R_JENIS_KARTU_APMK'
  ,'LJNSDENDA'       : 'R_SANDI_BIAYA_DENDA' 
}
  
class LKPBU_FORM_301:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJNSDENDA']
    self.attrlist = [
      'Keterangan'
      , 'ChargeCard'
      , 'CreditCrad'
      , 'KUtama'
      , 'KTambahan'
      , 'KUtama2'
      , 'KTambahan2'
      , 'VTTunai'
      , 'VTBelanja'
      , 'VTIntrabank'
      , 'VTAntarbank'
      , 'SBTunai'
      , 'SBBelanja'
      , 'NTTunai'
      , 'NTBelanja'
      , 'NTTransferIntrabank'
      , 'NTTransferAntarbank'
      , 'Keterangan2'
      , 'Volume'
      , 'OutstandingCredit'
      , 'SelainKartuKredit'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form301.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'Keterangan'
      , 3: 'ChargeCard'
      , 4: 'CreditCrad'
      , 5: 'KUtama'
      , 6: 'KTambahan'
      , 7: 'KUtama2'
      , 8: 'KTambahan2'
      , 9: 'VTTunai'
      , 10: 'VTBelanja'
      , 11: 'VTIntrabank'
      , 12: 'VTAntarbank'
      , 13: 'SBTunai'
      , 14: 'SBBelanja'
      , 15: 'NTTunai'
      , 16: 'NTBelanja'
      , 17: 'NTTransferIntrabank'
      , 18: 'NTTransferAntarbank'
      , 19: 'LJNSDENDA_reference_code'
      , 20: 'Keterangan2'
      , 21: 'Volume'
      , 22: 'OutstandingCredit'
      , 23: 'SelainKartuKredit'
    }
  #--

  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
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
      
      
    