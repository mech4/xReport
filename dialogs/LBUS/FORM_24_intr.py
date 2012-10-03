REFMAP = {
  'LJENIS'                      : 'R_KEWAJIBAN_LAINNYA'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPENAGIH'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_24:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPENAGIH'
      ,'LHUBBANK'
    ]
    self.attrlist = [
      'Hari'
      ,'Persen'
      ,'Jumlah'
      ,'Bulan'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form24.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLPENAGIH_reference_code'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'Bulan'
        , 6: 'Hari'
        , 7: 'Persen'
        , 8: 'Jumlah'
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
    