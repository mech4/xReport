REFMAP = {
  'LGOLPEMSAH'     : 'R_GOL_PEMEGANG_SAHAM'

}
  
class LBUS_FORM_31:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LGOLPEMSAH'
    ]
    self.attrlist = ['Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form31.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPEMSAH_reference_code'
        , 2: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form31.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [2,0]
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
    