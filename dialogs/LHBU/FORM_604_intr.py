REFMAP = {
  'LJANGKA'                     : 'R_JANGKA_WAKTU'
}
  
class LHBU_FORM_604:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJANGKA'
    ]
    self.attrlist = [
      'Realisasi'
      ,'Nisbah'
      ,'Distribusi'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form604.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJANGKA_reference_code'
        , 2: 'Realisasi'
        , 3: 'Nisbah'
        , 4: 'Distribusi'
    }
    self.useheader = 3 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU
    self.txttemplate = 'lhbu/form604.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
       , [2,0]
       , [8,2]
       , [8,2]
       , [8,2]
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
    