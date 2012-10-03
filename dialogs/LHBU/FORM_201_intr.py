REFMAP = {
  'LVALDAS'                     : 'R_SANDI_VALUTA'
  ,'LVALWAN'                     : 'R_SANDI_VALUTA'
  ,'LSTATUSPEMBELI'              : 'R_STATUS_PEMBELI'
  ,'LSANDIPEMBELI'               : 'R_BANK_DAN_PIHAK_KE3'
  ,'LSTATUSPENJUAL'              : 'R_STATUS_PEMBELI'
  ,'LSANDIPENJUAL'               : 'R_BANK_DAN_PIHAK_KE3'
  ,'LTUJUAN'                     : 'R_SANDI_TUJUAN'
  ,'LUSAHAPEMBELI'               : 'R_JENIS_KEG_BANK'
  ,'LUSAHAPENJUAL'               : 'R_JENIS_KEG_BANK'
  ,'LNEGARAPEMBELI'              : 'R_KODE_NEGARA'
  ,'LNEGARAPENJUAL'              : 'R_KODE_NEGARA'
}
  
class LHBU_FORM_201:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LVALDAS'
      ,'LVALWAN'
      ,'LSTATUSPEMBELI'
      ,'LSANDIPEMBELI'
      ,'LSTATUSPENJUAL'
      ,'LSANDIPENJUAL'
      ,'LTUJUAN'
      ,'LUSAHAPEMBELI'
      ,'LUSAHAPENJUAL'
      ,'LNEGARAPEMBELI'
      ,'LNEGARAPENJUAL'
    ]
    self.attrlist = [
      'IdOperasional'
      ,'NoReff'
      ,'Kurs'
      ,'VolumeValDas'
      ,'NamaPembeli'
      ,'PembeliNonBank'
      ,'NamaPenjual'
      ,'PenjualNonBank'
      ,'TglValuta'
      ,'TglTempo'
      ,'JangkaWaktu'
      ,'JamTransaksi'
      ,'JumlahTransaksi'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form201.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'IdOperasional'
        , 2: 'NoReff'
        , 3: 'LVALDAS_reference_code'
        , 4: 'LVALWAN_reference_code'
        , 5: 'Kurs'
        , 6: 'VolumeValDas'
        , 7: 'LSTATUSPEMBELI_reference_code'
        , 8: 'LSANDIPEMBELI_reference_code'
        , 9: 'NamaPembeli'
        , 10: 'PembeliNonBank'
        , 11: 'LSTATUSPENJUAL_reference_code'
        , 12: 'LSANDIPENJUAL_reference_code'
        , 13: 'NamaPenjual'
        , 14: 'PenjualNonBank'
        , 15: 'TglValuta'
        , 16: 'TglTempo'
        , 17: 'JangkaWaktu'
        , 18: 'JamTransaksi'
        , 19: 'LTUJUAN_reference_code'
        , 20: 'LUSAHAPEMBELI_reference_code'
        , 21: 'LUSAHAPENJUAL_reference_code'
        , 22: 'JumlahTransaksi'
        , 23: 'LNEGARAPEMBELI_reference_code'
        , 24: 'LNEGARAPENJUAL_reference_code'
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
    