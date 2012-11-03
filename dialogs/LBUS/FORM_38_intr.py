REFMAP = {
  'LJENIS'                     : 'R_PIUTANG_PEMBIAYAAN'
  , 'LDEBITUR'                 : 'R_JENIS_PENGGUNAAN'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LDEBITUR'
    ]
    self.attrlist = [
      'Rupiah1'
      ,'Valas1'
      ,'Jumlah1'
      ,'Rupiah2'
      ,'Valas2'
      ,'Jumlah2'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form38.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LDEBITUR_reference_code'
        , 3: 'Rupiah1'
        , 4: 'Valas1'
        , 5: 'Jumlah1'
        , 6: 'Rupiah2'
        , 7: 'Valas2'
        , 8: 'Jumlah2'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form38.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [2,0]
      , [2,0]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
      , [12,1]
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
    