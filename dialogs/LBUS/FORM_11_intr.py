REFMAP = {
  'LJENIS'                      : 'R_JENIS_TAGIHAN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLDEBITUR'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LSEKTOREKONOMI'              : 'R_SEKTOR_EKONOMI'
  ,'LLOKASIPROYEK'               : 'R_DATI_2'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_11:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLDEBITUR'
      ,'LHUBBANK'
      ,'LKOLEKTIBILITAS'
      ,'LSEKTOREKONOMI'
      ,'LLOKASIPROYEK'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'BlnThnMulai'
      ,'BlnThnTempo'
      ,'Margin'
      ,'BagDijamin'
      ,'DebetBlnLalu'
      ,'DebetBlnLap'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form11.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LSEKTOREKONOMI_reference_code'
        , 2: 'LLOKASIPROYEK_reference_code'
        , 3: 'LGOLPENJAMIN_reference_code'
        , 4: 'BagDijamin'
        , 5: 'DebetBlnLalu'
        , 6: 'DebetBlnLap'
        , 7: 'AgunanPPAP'
        , 8: 'PPAPDibentuk'
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
    