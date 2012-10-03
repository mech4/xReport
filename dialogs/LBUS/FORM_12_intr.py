REFMAP = {
  'LEMITEN'                     : 'R_SANDI_PIHAK_KETIGA'
  ,'LJENISPERUSAHAAN'            : 'R_JENIS_PERUSAHAAN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LTUJUAN'                     : 'R_TUJUAN_PENYERTAAN'
}
  
class LBUS_FORM_12:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LEMITEN'
      ,'LJENISPERUSAHAAN'
      ,'LJENISVALUTA'
      ,'LKOLEKTIBILITAS'
      ,'LTUJUAN'
    ]
    self.attrlist = [
      'BagPenyertaan'
      ,'Jumlah'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form12.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LEMITEN_reference_code'
        , 2: 'LJENISPERUSAHAAN_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'LKOLEKTIBILITAS_reference_code'
        , 5: 'LTUJUAN_reference_code'
        , 6: 'WaktuPenyertaan'
        , 7: 'BagPenyertaan'
        , 8: 'Jumlah'
        , 9: 'AgunanPPAP'
        , 10: 'PPAPDibentuk'
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
    