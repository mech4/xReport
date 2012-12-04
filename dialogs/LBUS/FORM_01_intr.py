REFMAP = {
  'LPOS'           : 'R_POS_NERACA_LBU'
}
  
class LBUS_FORM_01:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LPOS']
    self.attrlist = [
      'Value1'
      , 'Value2'
      , 'Total'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form01.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LPOS_reference_code'
      , 2: 'Value1'
      , 3: 'Value2'
      , 4: 'Total'
      , 5: '@Rownum'
    } 
    self.useheader = 2 #1: true, 0:false, 2: row header only
    self.txttemplate = 'lbus/form01.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [3,0]
      , [12,1]
      , [12,1]
      , [12,1]
      , [5,1]
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
    