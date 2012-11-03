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
      'NomorRekening'
      ,'JumlahRekening'
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
          1: 'NomorRekening'
        , 2: 'JumlahRekening'
        , 3: 'LSTATUSPEMBIAYAAN_reference_code'
        , 4: 'LSIFAT_reference_code'
        , 5: 'LJENIS_reference_code'
        , 6: 'LJENISPENGGUNAAN_reference_code'
        , 7: 'LORIENTPENGGUNAAN_reference_code'
        , 8: 'LJENISVALUTA_reference_code'
        , 9: 'LGOLDEBITUR_reference_code'
        , 10: 'LHUBBANK_reference_code'
        , 11: 'BlnThnMulai'
        , 12: 'BlnThnTempo'
        , 13: 'LKOLEKTIBILITAS_reference_code'
        , 14: 'Nisbah'
        , 15: 'PersenBagiHasil'
        , 16: 'LGOLPEMBIAYAAN_reference_code'
        , 17: 'LSEKTOREKONOMI_reference_code'
        , 18: 'LLOKASIPROYEK_reference_code'
        , 19: 'LGOLPENJAMIN_reference_code'
        , 20: 'BagDijamin'
        , 21: 'Plafond'
        , 22: 'KelonggaranTarik'
        , 23: 'DebetBlnLalu'
        , 24: 'DebetBlnLap'
        , 25: 'AgunanPPAP'
        , 26: 'PPAPDibentuk'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form10.txt'
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
      , [1,0]
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
    