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
        , 2: 'sdbulan'
        , 3: 'Hari1'
        , 4: 'Hari2'
        , 5: 'Hari3'
        , 6: 'Hari4'
        , 7: 'Hari5'
        , 8: 'Hari6'
        , 9: 'Hari7'
        , 10: 'Hari8'
        , 11: 'Hari9'
        , 12: 'Hari10'
        , 13: 'Hari11'
        , 14: 'Hari12'
        , 15: 'Hari13'
        , 16: 'Hari14'
        , 17: 'Minggu3'
        , 18: 'Minggu4'
        , 19: 'Keterangan'
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
    