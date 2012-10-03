REFMAP = {
  'LJENIS'           : 'R_JENIS_PASIVA_DI_LN'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
  , 'LPEMILIK'       : 'R_GOLONGAN_PEMILIK'
  , 'LHUBBANK'       : 'R_HUBUNGAN_DENGAN_BANK'
  , 'LJENISOPERASIONAL' : 'R_JENIS_OPERASIONAL'
  , 'LSANDIKANTOR' : 'R_SANDI_KANTOR'
}
  
class LBUS_FORM_28:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSANDIKANTOR'
      ,'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'PersentaseBonus'
      ,'Jumlah'
      ,'LPRESENTASE'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form28.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LSANDIKANTOR_reference_code'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'PersentaseBonus'
        , 5: 'Jumlah'
        , 6: 'LPRESENTASE'
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
    