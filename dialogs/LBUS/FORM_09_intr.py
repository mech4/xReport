REFMAP = {
  'LSTATUSPIUTANG'              : 'R_STATUS_PIUTANG'
  ,'LSIFAT'                      : 'R_SIFAT_PIUTANG'
  ,'LJENIS'                      : 'R_JENIS_PIUTANG'
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
  
class LBUS_FORM_09:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSTATUSPIUTANG'
      ,'LSIFAT'
      ,'LJENIS'
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
      'JumlahRekening'
      ,'BlnThnMulai'
      ,'BlnThnTempo'
      ,'PersenFee'
      ,'BagDijamin'
      ,'Plafond'
      ,'Kelonggaran'
      ,'DebetBlnLalu'
      ,'DebetBlnLap'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form09.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPIUTANG_reference_code'
        , 2: 'LSEKTOREKONOMI_reference_code'
        , 3: 'LLOKASIPROYEK_reference_code'
        , 4: 'LGOLPENJAMIN_reference_code'
        , 5: 'BagDijamin'
        , 6: 'Plafond'
        , 7: 'Kelonggaran'
        , 8: 'DebetBlnLalu'
        , 9: 'DebetBlnLap'
        , 10: 'AgunanPPAP'
        , 11: 'PPAPDibentuk'
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
    