REFMAP = {
  'LSANDIBANK'                     : 'R_SANDI_BANK'
  , 'LMATAUANG'                      : 'R_SANDI_VALUTA'
  , 'LJENISBUNGAKREDIT'            : 'R_JENIS_SUKU_BUNGA_KREDIT' 
}
  
class LHBU_FORM_602:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSANDIBANK'
      ,'LJENISBUNGAKREDIT'
      ,'LMATAUANG'
    ]
    self.attrlist = [
      'JenisKegiatanUsaha'
      ,'TanggaLaporan'
      ,'JumlahRecordIsi'
      ,'Flat'
      ,'Efektif'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form602.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LSANDIBANK_reference_code'
        , 2: 'JenisKegiatanUsaha'
        , 3: 'TanggaLaporan'
        , 4: 'JumlahRecordIsi'
        , 5: 'LJENISBUNGAKREDIT_reference_code'
        , 6: 'LMATAUANG_reference_code'
        , 7: 'Flat'
        , 8: 'Efektif'
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
    