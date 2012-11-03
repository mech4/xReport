REFMAP = {
  'LJENIS'           : 'R_JENIS_PASIVA_DI_LN'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
  , 'LJENISOPERASIONAL' : 'R_JENIS_OPERASIONAL'
}
  
class LBUS_FORM_27:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENISOPERASIONAL'
      ,'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
       'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form27.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJENISOPERASIONAL_reference_code'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form27.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [1,0]
      , [2,0]
      , [3,0]
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
    