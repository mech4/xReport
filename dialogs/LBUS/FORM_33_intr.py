REFMAP = {
  'LGOLPEMILIK'                 : 'R_BANK_DAN_PIHAK_KE3'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_33:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LGOLPEMILIK'
      ,'LHUBBANK'
      ,'LJENISVALUTA'
    ]
    self.attrlist = ['Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form33.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPEMILIK_reference_code'
        , 2: 'LHUBBANK_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'Jumlah'
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
    