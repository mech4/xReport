REFMAP = {
  'LJENIS'                     : 'R_GOL_PEMILIK_KUSTODIAN'
  , 'LJENISVALUTA'             : 'R_JENIS_VALUTA'
  , 'LBENTUKPENGHAPUSANBUKUAN' : 'R_GOLPENERBIT_KUSTODIAN'
  ,'LKOLEKTIBILITAS'           : 'R_JENIS_KUSTODIAN'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LBENTUKPENGHAPUSANBUKUAN'
      ,'LKOLEKTIBILITAS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'BulanJthTempo'
      ,'BulanPenerbit'
      ,'NilaiNominal'
      ,'Tahun1'
      ,'Tahun2'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form39.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LBENTUKPENGHAPUSANBUKUAN_reference_code'
        , 3: 'LKOLEKTIBILITAS_reference_code'
        , 4: 'LJENISVALUTA_reference_code'
        , 5: 'BulanPenerbit'
        , 6: 'BulanJthTempo'
        , 7: 'NilaiNominal'
        , 8: 'Tahun1'
        , 9: 'Tahun2'
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
      
  #def OnEnter(self, sender):
        
    