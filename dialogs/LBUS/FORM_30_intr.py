REFMAP = {
  'LGOLKREDITUR'     : 'R_GOLONGAN_KREDITUR'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'

}
  
class LBUS_FORM_29:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LGOLKREDITUR'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'JangkaWaktuAkhir'
      ,'JangkaWaktuMulai'
      ,'Presentase'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form30.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLKREDITUR_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'JangkaWaktuMulai'
        , 4: 'JangkaWaktuAkhir'
        , 5: 'Presentase'
        , 6: 'Jumlah'
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
    