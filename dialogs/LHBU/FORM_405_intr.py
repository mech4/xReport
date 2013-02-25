REFMAP = {
  'LKOMPONEN'                   : 'R_KATEGORI_RM'
}
  
class LHBU_FORM_405:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKOMPONEN'
    ]
    self.attrlist = [
      'Hari1'
      ,'Hari2'
      ,'Hari3'
      ,'Hari4'
      ,'Hari5'
      ,'Hari6'
      ,'Hari7'
      ,'Hari8'
      ,'Hari9'
      ,'Hari10'
      ,'Hari11'
      ,'Hari12'
      ,'Hari13'
      ,'Hari14'
      ,'Hari15'
      ,'Hari16'
      ,'Hari17'
      ,'Hari18'
      ,'Hari19'
      ,'Hari20'
      ,'Hari21'
      ,'Hari22'
      ,'Hari23'
      ,'Hari24'
      ,'Hari25'
      ,'Hari26'
      ,'Hari27'
      ,'Hari28'
      ,'Hari29'
      ,'Hari30'
      ,'sdbulan'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form405.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LKOMPONEN_reference_code'
        , 2: '!LKOMPONEN.reference_desc'
        , 3: 'sdbulan'
        , 4: 'Hari1'
        , 5: 'Hari2'
        , 6: 'Hari3'
        , 7: 'Hari4'
        , 8: 'Hari5'
        , 9: 'Hari6'
        , 10: 'Hari7'
        , 11: 'Hari8'
        , 12: 'Hari9'
        , 13: 'Hari10'
        , 14: 'Hari11'
        , 15: 'Hari12'
        , 16: 'Hari13'
        , 17: 'Hari14'
        , 18: 'Hari15'
        , 19: 'Hari16'
        , 20: 'Hari17'
        , 21: 'Hari18'
        , 22: 'Hari19'
        , 23: 'Hari20'
        , 24: 'Hari21'
        , 25: 'Hari22'
        , 26: 'Hari23'
        , 27: 'Hari24'
        , 28: 'Hari25'
        , 29: 'Hari26'
        , 30: 'Hari27'
        , 31: 'Hari28'
        , 32: 'Hari29'
        , 33: 'Hari30'
    }
    self.useheader = 3 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU
    self.txttemplate = 'lhbu/form405.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [4,0]
      , [100,0]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
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
    