REFMAP = {
  'LJENIS'                      : 'R_SURT_BRHARGA_YANG_DIMIL'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPENERBIT'                : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANKPENERBIT'            : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LTUJUANPEMILIKAN'            : 'R_TUJUAN_PEMILIKAN'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_05:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPENERBIT'
      ,'LHUBBANKPENERBIT'
      ,'LTUJUANPEMILIKAN'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'BagHas'
      ,'BagianDijamin'
      ,'Nominal'
      ,'Jumlah'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form05.xls'
    self.xlstopline  = 2
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLPENERBIT_reference_code'
        , 4: 'LHUBBANKPENERBIT_reference_code'
        , 5: 'LTUJUANPEMILIKAN_reference_code'
        , 6: 'Mulai'
        , 7: 'JatuhTempo'
        , 8: 'LKOLEKTIBILITAS_reference_code'
        , 9: 'BagHas'
        , 10: 'LGOLPENJAMIN_reference_code'
        , 11: 'BagianDijamin'
        , 12: 'Nominal'
        , 13: 'Jumlah'
        , 14: 'AgunanPPAP'
        , 15: 'PPAPDibentuk'
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
    