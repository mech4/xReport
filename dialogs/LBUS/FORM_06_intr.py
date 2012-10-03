REFMAP = {
  'LSTATUSPIUTANG'              : 'R_STATUS_PIUTANG'
  ,'LJENISPENGGUNAAN'            : 'R_JENIS_PENGGUNAAN'
  ,'LORIENTPENGGUNAAN'           : 'R_ORIENT_PENGGUNAAN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLDEBITUR'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPIUTANG'                 : 'R_GOLONGAN_PIUTANG'
  ,'LSEKTOREKONOMI'              : 'R_SEKTOR_EKONOMI'
  ,'LLOKASIPROYEK'               : 'R_DATI_2'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_06:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSTATUSPIUTANG'
      ,'LJENISPENGGUNAAN'
      ,'LORIENTPENGGUNAAN'
      ,'LJENISVALUTA'
      ,'LGOLDEBITUR'
      ,'LHUBBANK'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPIUTANG'
      ,'LSEKTOREKONOMI'
      ,'LLOKASIPROYEK'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'NomorRekening'
      ,'JumlahRekening'
      ,'Mulai'
      ,'JatuhTempo'
      ,'PersenMargin'
      ,'BagDijamin'
      ,'HargaAwal'
      ,'SaldoHargaPokok'
      ,'SaldoMargin'
      ,'DebetBlnLalu'
      ,'DebetBlnLap'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form06.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPIUTANG_reference_code'
        , 2: 'LSEKTOREKONOMI_reference_code'
        , 3: 'LLOKASIPROYEK_reference_code'
        , 4: 'LGOLPENJAMIN_reference_code'
        , 5: 'BagDijamin'
        , 6: 'HargaAwal'
        , 7: 'SaldoHargaPokok'
        , 8: 'SaldoMargin'
        , 9: 'DebetBlnLalu'
        , 10: 'DebetBlnLap'
        , 11: 'AgunanPPAP'
        , 12: 'PPAPDibentuk'
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
    