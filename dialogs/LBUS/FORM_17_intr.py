REFMAP = {
  'LJENIS'                      : 'R_RUPA_RUPA_AKTIVA'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLSTATUS'                  : 'R_GOLONGAN_STATUS'
}
  
class LBUS_FORM_17:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLSTATUS'
    ]
    self.attrlist = [
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form17.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLSTATUS_reference_code'
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
    