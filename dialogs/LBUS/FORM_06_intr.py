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
          1: 'NomorRekening'
        , 2: 'JumlahRekening'
        , 3: 'LSTATUSPIUTANG_reference_code'
        , 4: 'LJENISPENGGUNAAN_reference_code'
        , 5: 'LORIENTPENGGUNAAN_reference_code'
        , 6: 'LJENISVALUTA_reference_code'
        , 7: 'LGOLDEBITUR_reference_code'
        , 8: 'LHUBBANK_reference_code'
        , 9: 'Mulai'
        , 10: 'JatuhTempo'
        , 11: 'LKOLEKTIBILITAS_reference_code'
        , 12: 'PersenMargin'
        , 13: 'LGOLPIUTANG_reference_code'
        , 14: 'LSEKTOREKONOMI_reference_code'
        , 15: 'LLOKASIPROYEK_reference_code'
        , 16: 'LGOLPENJAMIN_reference_code'
        , 17: 'BagDijamin'
        , 18: 'HargaAwal'
        , 19: 'SaldoHargaPokok'
        , 20: 'SaldoMargin'
        , 21: 'DebetBlnLalu'
        , 22: 'DebetBlnLap'
        , 23: 'AgunanPPAP'
        , 24: 'PPAPDibentuk'
    }
    self.useheader = 2 #1: true, 0:false
    self.txttemplate = 'lbus/form06.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [15,0]
      , [8,1]
      , [2,0]
      , [2,0]
      , [1,0]
      , [3,0]
      , [3,0]
      , [1,0]
      , [6,1]
      , [6,1]
      , [1,0]
      , [4,3]
      , [2,0]
      , [4,0]
      , [4,0]
      , [3,0]
      , [4,3]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
  )
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
    