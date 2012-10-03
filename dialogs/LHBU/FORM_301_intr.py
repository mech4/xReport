REFMAP = {
  'LSANDIBANK'                   : 'R_SANDI_BANK'
  ,'LJENISTRANSAKSI'             : 'R_JENIS_TRANSAKSI'
  ,'LSTATUSPEMBELI'              : 'R_STATUS_PEMBELI'
  ,'LSANDIPEMBELI'               : 'R_BANK_DAN_PIHAK_KE3'
  ,'LSTATUSPENJUAL'              : 'R_STATUS_PEMBELI'
  ,'LSANDIBANKPENJUAL'           : 'R_BANK_DAN_PIHAK_KE3'
  ,'LTUJUAN'                     : 'R_SANDI_TUJUAN'
  ,'LUSAHAPEMBELI'               : 'R_JENIS_KEG_BANK'
  ,'LUSAHAPENJUAL'               : 'R_JENIS_KEG_BANK'
  ,'LNEGARAPEMBELI'              : 'R_KODE_NEGARA'
  ,'LNEGARAPENJUAL'              : 'R_KODE_NEGARA'
  ,'LJENISSURATBERHARGA'         : 'R_JNS_SURATBERHARGA'
}
  
class FORM_201:
  def __init__(self, formObj, parentForm):
    pass
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
    