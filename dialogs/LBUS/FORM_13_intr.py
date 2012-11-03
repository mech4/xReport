REFMAP = {
  'LBENTUKPENYISIHAN'           : 'R_BENTUK_PENYISIHAN'
  ,'LJENISVALUTA'                : 'R_VALUTA_IJARAH'
}
  
class LBUS_FORM_13:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LBENTUKPENYISIHAN'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'CadUmumPPAP'
      ,'CadKhususPPAP'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form13.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LBENTUKPENYISIHAN_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'CadUmumPPAP'
        , 4: 'CadKhususPPAP'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form13.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [2,0]
      , [1,0]
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
    