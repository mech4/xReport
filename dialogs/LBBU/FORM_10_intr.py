REFMAP = {
  'LKUALITAS'                   : 'R_KUALITAS'
}
  
class LBBU_FORM_10:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKUALITAS'
    ]
    self.attrlist = [
      'NamaDeposan'
      ,'NPWPDeposan'
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
    self.xlstemplate = 'lbbu/form10.xls'
    self.xlstopline  = 10
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
        , 30: '@Endmonth'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form10.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [50,0]
      , [30,0]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [10,1]
      , [50,0]
      , [30,0]
      , [3,0]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [10,1]
      , [8,1]
    )
  #--

  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
        
      return res
    