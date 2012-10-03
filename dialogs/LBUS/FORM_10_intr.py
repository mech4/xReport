REFMAP = {
  'LSTATUSPEMBIAYAAN'           : 'R_STATUS_PEMBIAYAAN'
  ,'LSIFAT'                      : 'R_SIFAT_PEMBIAYAAN'
  ,'LJENIS'                      : 'R_JENIS_PEMBIAYAAN'
  ,'LJENISPENGGUNAAN'            : 'R_JENIS_PENGGUNAAN'
  ,'LORIENTPENGGUNAAN'           : 'R_ORIENT_PENGGUNAAN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLDEBITUR'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPEMBIAYAAN'              : 'R_GOLONGAN_PEMBIAYAAN'
  ,'LSEKTOREKONOMI'              : 'R_SEKTOR_EKONOMI'
  ,'LLOKASIPROYEK'               : 'R_DATI_2'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_10:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSTATUSPEMBIAYAAN'
      ,'LSIFAT'
      ,'LJENIS'
      ,'LJENISPENGGUNAAN'
      ,'LORIENTPENGGUNAAN'
      ,'LJENISVALUTA'
      ,'LGOLDEBITUR'
      ,'LHUBBANK'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPEMBIAYAAN'
      ,'LSEKTOREKONOMI'
      ,'LLOKASIPROYEK'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'BlnThnMulai'
      ,'BlnThnTempo'
      ,'Nisbah'
      ,'PersenBagiHasil'
      ,'BagDijamin'
      ,'Plafond'
      ,'KelonggaranTarik'
      ,'DebetBlnLalu'
      ,'DebetBlnLap'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form10.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'Nisbah'
        , 2: 'PersenBagiHasil'
        , 3: 'LGOLPEMBIAYAAN_reference_code'
        , 4: 'LSEKTOREKONOMI_reference_code'
        , 5: 'LLOKASIPROYEK_reference_code'
        , 6: 'LGOLPENJAMIN_reference_code'
        , 7: 'BagDijamin'
        , 8: 'Plafond'
        , 9: 'KelonggaranTarik'
        , 10: 'DebetBlnLalu'
        , 11: 'DebetBlnLap'
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
    