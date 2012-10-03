REFMAP = {
  'LPENANAMDANA'                : 'R_SANDI_BANK'
  ,'LPENGELOLADANA'              : 'R_SANDI_BANK'
  ,'LCURRENCY'                   : 'R_SANDI_VALUTA'
  ,'LJENISPENANAM'               : 'R_JENIS_KEG_BANK'
  ,'LJENISPENGELOLA'             : 'R_JENIS_KEG_BANK'
}
  
class LHBU_FORM_102:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LPENANAMDANA', 'LPENGELOLADANA', 'LCURRENCY', 'LJENISPENANAM', 'LJENISPENGELOLA']
    self.attrlist = [
      'IdOperasional'
      , 'NoReff'
      , 'TingkatImbalan'
      , 'BagHas'
      , 'Volume'
      , 'VolValDas'
      , 'TglValuta'
      , 'TglTempo'
      , 'Waktu'
      , 'JamTransaksi'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form102.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'IdOperasional'
        , 2: 'NoReff'
        , 3: 'LPENANAMDANA_reference_code'
        , 4: 'LPENGELOLADANA_reference_code'
        , 5: 'LCURRENCY_reference_code'
        , 6: 'TingkatImbalan'
        , 7: 'BagHas'
        , 8: 'Volume'
        , 9: 'VolValDas'
        , 10: 'TglValuta'
        , 11: 'TglTempo'
        , 12: 'Waktu'
        , 13: 'JamTransaksi'
        , 14: 'LJENISPENANAM_reference_code'
        , 15: 'LJENISPENGELOLA_reference_code'
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
    