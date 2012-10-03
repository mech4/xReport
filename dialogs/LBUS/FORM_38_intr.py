REFMAP = {
  'LJENIS'                     : 'R_PIUTANG_PEMBIAYAAN'
  , 'LDEBITUR'                 : 'R_JENIS_PENGGUNAAN'
  , 'LHUBUNGANBANK'            : 'R_DATI_2'
  ,'LKOLEKTIBILITAS'           : 'R_KOLEKTIBILITAS'
  ,'LSEKTOREKONOMI'            : 'R_SEKTOR_EKONOMI'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LDEBITUR'
    ]
    self.attrlist = [
      'Valas1'
      ,'Jumlah1'
      ,'Rupiah2'
      ,'Valas2'
      ,'Jumlah2'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form38.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LDEBITUR_reference_code'
        , 3: 'Rupiah1'
        , 4: 'Valas1'
        , 5: 'Jumlah1'
        , 6: 'Rupiah2'
        , 7: 'Valas2'
        , 8: 'Jumlah2'
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
    