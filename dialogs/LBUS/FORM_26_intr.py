REFMAP = {
  'LJENIS'           : 'R_JENIS_SIMPANAN_WADIAH'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
  , 'LPEMILIK'       : 'R_GOLONGAN_PEMILIK'
}
  
class LBUS_FORM_26:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LPEMILIK'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'PersentaseBonus'
      ,'Jumlah'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form26.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LPEMILIK_reference_code'
        , 4: 'Mulai'
        , 5: 'JatuhTempo'
        , 6: 'PersentaseBonus'
        , 7: 'Jumlah'
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
    