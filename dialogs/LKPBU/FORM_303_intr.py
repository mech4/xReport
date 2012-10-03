REFMAP = {
  'LJENIS'           : 'R_BENTUK_INSTRUMEN'
  ,'LJENISVALUTA'    : 'R_JENIS_MEDIA' 
}
  
class LKPBU_FORM_303:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'jumlah'
      , 'MaksLimit'
      , 'DanaFloat'
      , 'VolumeTR'
      , 'NilaiTR'
      , 'JmlhMerchant'
      , 'JmlhTerminal'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form303.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'
      , 2: 'LJENISVALUTA_reference_code'
      , 3: 'jumlah'
      , 4: 'MaksLimit'
      , 5: 'DanaFloat'
      , 6: 'VolumeTR'
      , 7: 'NilaiTR'
      , 8: 'JmlhMerchant'
      , 9: 'JmlhTerminal'
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
#-------------------------------------------------------------------------------        

      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    