REFMAP = {
  'LStatusPiutang'            : 'R_STATUS_PIUTANG'
  ,'LJenisValuta'            : 'R_JENIS_VALUTA'
  ,'GolDebitur'            : 'R_SANDI_PIHAK_KETIGA'
  ,'LHubBank'            : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKolektibilitas'            : 'R_KOLEKTIBILITAS'
  ,'LGolPiutang'            : 'R_GOLONGAN_PIUTANG'
  ,'LSektorEkonomi'            : 'R_SEKTOR_EKONOMI'
  ,'LLokasiProyek'            : 'R_DATI_2'
  ,'LGolPenjamin'            : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_07:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LStatusPiutang'
      ,'LJenisValuta'
      ,'GolDebitur'
      ,'LHubBank'
      ,'LKolektibilitas'
      ,'LGolPiutang'
      ,'LSektorEkonomi'
      ,'LLokasiProyek'
      ,'LGolPenjamin'
    ]
    self.attrlist = [
      'NomorRekening'
      ,'JumlahRekening'
      ,'BulanTahunMulai'
      ,'JatuhTempo'
      ,'BagianDijamin'
      ,'HargaAwal'
      ,'DebetBlnLalu'
      ,'DebetBlnLaporan'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form07.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGolPenjamin_reference_code'
        , 2: 'BagianDijamin'
        , 3: 'HargaAwal'
        , 4: 'DebetBlnLalu'
        , 5: 'DebetBlnLaporan'
        , 6: 'AgunanPPAP'
        , 7: 'PPAPDibentuk'
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
    