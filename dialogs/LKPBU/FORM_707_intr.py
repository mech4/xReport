REFMAP = {
      'LKOMPONEN'     : 'R_ARUS_KAS'
}
  
class LKPBU_FORM_707:
  def __init__(self, formObj, parentForm):
    self.reflist  = [ 'LKOMPONEN' ]
    self.attrlist = [
     'Hari1'
    , 'Hari2'
    , 'Hari3'
    , 'Hari4'
    , 'Hari5'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form707.xls'
    self.xlstopline  = 9
    self.xlsmap      = {
        1: '@LKOMPONEN_reference_code'  
      , 2: 'Hari1'
      , 3: 'Hari2'
      , 4: 'Hari3'
      , 5: 'Hari4'
      , 6: 'Hari5'
    }
    self.useheader = 11 #1: true, 0:false, 11: Khusus Form 707 output CSV
    self.txttemplate = 'lkpbu/form707.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [100,0]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
    )
    self.formulaField = ( '01', '02', '06', '11', '16', '21', '22', '23', '26', '31', '35', '40', '41')
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
      
  def fieldEnter(self, sender):
    uip = self.uipData
    rowcode = uip.GetFieldValue('LKOMPONEN.reference_code')
    if rowcode in self.formulaField:
      sender.ReadOnly = 1
    else:
      sender.ReadOnly = 0
      
    