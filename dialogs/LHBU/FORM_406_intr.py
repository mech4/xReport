REFMAP = {
  'LKOMPONEN'                   : 'R_KATEGORI_PB'
}
  
class LHBU_FORM_406:
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
      ,'Minggu3'
      ,'Minggu4'
      ,'sdbulan'
      ,'Keterangan'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form406.xls'
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
        , 18: 'Minggu3'
        , 19: 'Minggu4'
        , 20: 'Keterangan'
    }
    self.useheader = 3 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU
    self.txttemplate = 'lhbu/form406.txt'
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
      , [100,0]
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
    