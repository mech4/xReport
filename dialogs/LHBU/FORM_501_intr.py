REFMAP = {
  'LSANDIBANK'                     : 'R_SANDI_BANK'
  , 'LMATAUANG'                      : 'R_SANDI_VALUTA'
  
}
  
class LHBU_FORM_501:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSANDIBANK'
      ,'LMATAUANG'
    ]
    self.attrlist = [
      'JenisKegiatanUsaha'
      ,'TanggaLaporan'
      ,'JumlahRecordIsi'
      ,'Overnight'
      ,'satuMinggu'
      ,'satuBulan'
      ,'tigaBulan'
      ,'enamBulan'
      ,'duabelasBulan'
      ,'JamKuotasi'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form501.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LSANDIBANK_reference_code'
        , 2: 'JenisKegiatanUsaha'
        , 3: 'TanggaLaporan'
        , 4: 'JumlahRecordIsi'
        , 5: 'LMATAUANG_reference_code'
        , 6: 'Overnight'
        , 7: 'satuMinggu'
        , 8: 'satuBulan'
        , 9: 'tigaBulan'
        , 10: 'enamBulan'
        , 11: 'duabelasBulan'
        , 12: 'JamKuotasi'
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
    