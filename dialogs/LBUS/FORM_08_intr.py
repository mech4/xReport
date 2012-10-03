REFMAP = {
  'LSTATUSPIUTANG'              : 'R_STATUS_PIUTANG'
  ,'LPENGGUNAAN'                 : 'R_JENIS_PENGGUNAAN'
  ,'LORIENTASI'                  : 'R_ORIENT_PENGGUNAAN'
  ,'LVALUTA'                     : 'R_JENIS_VALUTA'
  ,'LGOLDEBITUR'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPIUTANG'                 : 'R_GOLONGAN_PIUTANG'
  ,'LSEKTOREKONOMI'              : 'R_SEKTOR_EKONOMI'
  ,'LLOKASIPROYEK'               : 'R_DATI_2'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_08:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSTATUSPIUTANG'
      ,'LPENGGUNAAN'
      ,'LORIENTASI'
      ,'LVALUTA'
      ,'LGOLDEBITUR'
      ,'LHUBBANK'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPIUTANG'
      ,'LSEKTOREKONOMI'
      ,'LLOKASIPROYEK'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'BlnThnMulai'
      ,'BlnThnTempo'
      ,'PersenMargin'
      ,'BagDijamin'
      ,'HargaJual'
      ,'HargaBeli'
      ,'DebetBlnLalu'
      ,'DebetBlnLaporan'
      ,'SaldoMargin'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form08.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPIUTANG_reference_code'
        , 2: 'LSEKTOREKONOMI_reference_code'
        , 3: 'LLOKASIPROYEK_reference_code'
        , 4: 'LGOLPENJAMIN_reference_code'
        , 5: 'BagDijamin'
        , 6: 'HargaJual'
        , 7: 'HargaBeli'
        , 8: 'DebetBlnLalu'
        , 9: 'DebetBlnLaporan'
        , 10: 'SaldoMargin'
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
    