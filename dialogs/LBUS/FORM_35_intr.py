REFMAP = {
  'LJENIS'                      : 'R_JENIS_GARANSI'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPEMOHON'                 : 'R_BANK_DAN_PIHAK_KE3'
  ,'LHUBBANK'                           : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
  ,'LTUJUAN'                     : 'R_TUJUAN_GARANSI'
}
  
class LBUS_FORM_35:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPEMOHON'
      ,'LHUBBANK'
      ,'LGOLPENJAMIN'
      ,'LTUJUAN'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'BagianDijamin'
      ,'Jumlah'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form35.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LKOLEKTIBILITAS_reference_code'
        , 4: 'Mulai'
        , 5: 'JatuhTempo'
        , 6: 'LGOLPEMOHON_reference_code'
        , 7: 'LHUBBANK_reference_code'
        , 8: 'LGOLPENJAMIN_reference_code'
        , 9: 'BagianDijamin'
        , 10: 'LTUJUAN_reference_code'
        , 11: 'Jumlah'
        , 12: 'AgunanPPAP'
        , 13: 'PPAPDibentuk'
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
    