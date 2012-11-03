REFMAP = {
}
  
class LBBU_FORM_11:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
    ]
    self.attrlist = [
      'Aktivitas'
      ,'usd'
      ,'gbp'
      ,'sgd'
      ,'hkd'
      ,'jpy'
      ,'aud'
      ,'euro'
      ,'myr'
      ,'others'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form11.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'Aktivitas'
        , 2: '@Rownum'
        , 3: 'usd'
        , 4: 'gbp'
        , 5: 'sgd'
        , 6: 'hkd'
        , 7: 'jpy'
        , 8: 'aud'
        , 9: 'euro'
        , 10: 'myr'
        , 11: 'others'
        , 12: '@Endmonth'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form11.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [50,0]
      , [2,0]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [8,0]
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
    