REFMAP = {
  'LKUALITAS'                   : 'R_KUALITAS'
}
  
class LBBU_FORM_10:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKUALITAS'
    ]
    self.attrlist = [
      'NPWPDeposan'
      ,'Giro'
      ,'Girov'
      ,'Tabungan'
      ,'Tabunganv'
      ,'Deposito'
      ,'Depositov'
      ,'TotalDeposan'
      ,'PersenDeposan'
      ,'NamaDebitur'
      ,'NPWPDebitur'
      ,'Murabahah'
      ,'Murabahahv'
      ,'Margin'
      ,'Marginv'
      ,'Salam'
      ,'Salamv'
      ,'Istishna'
      ,'Istishnav'
      ,'Mudharabah'
      ,'Mudharabahv'
      ,'Musyarakah'
      ,'Musyarakahv'
      ,'Lain'
      ,'Lainv'
      ,'TotalDebitur'
      ,'PersenDebitur'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form10.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'NamaDeposan'
        , 2: 'NPWPDeposan'
        , 3: 'Giro'
        , 4: 'Girov'
        , 5: 'Tabungan'
        , 6: 'Tabunganv'
        , 7: 'Deposito'
        , 8: 'Depositov'
        , 9: 'TotalDeposan'
        , 10: 'PersenDeposan'
        , 11: 'NamaDebitur'
        , 12: 'NPWPDebitur'
        , 13: 'LKUALITAS_reference_code'
        , 14: 'Murabahah'
        , 15: 'Murabahahv'
        , 16: 'Margin'
        , 17: 'Marginv'
        , 18: 'Salam'
        , 19: 'Salamv'
        , 20: 'Istishna'
        , 21: 'Istishnav'
        , 22: 'Mudharabah'
        , 23: 'Mudharabahv'
        , 24: 'Musyarakah'
        , 25: 'Musyarakahv'
        , 26: 'Lain'
        , 27: 'Lainv'
        , 28: 'TotalDebitur'
        , 29: 'PersenDebitur'
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
    