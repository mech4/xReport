REFMAP = {
  'LPOS'                        : 'R_POS_NERACA'
}
  
class LBBU_FORM_4B:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPOS'
    ]
    self.attrlist = [
      'Saldo'
      ,'Eks1'
      ,'Eks3'
      ,'Eks6'
      ,'Eks12'
      ,'Eks15'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form4B.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LPOS_reference_desc'
        , 2: 'LPOS_reference_code'
        , 3: '@Endmonth'
        , 4: 'Saldo'
        , 5: 'Eks1'
        , 6: 'Eks3'
        , 7: 'Eks6'
        , 8: 'Eks12'
        , 9: 'Eks15'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form4b.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [100,0]
      , [5,0]
      , [8,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
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
      
  def refBeforeLookup(self, sender, linkui):
    sName = sender.Name.split('.')[0]           
    sType = sender.Name.split('.')[-1].split('_')[-1]
    sdr = self.pData_LPOS
    self.uipData.ClearLink(sName)
    uapp = self.FormObject.ClientApplication.UserAppObject
    if sType == 'desc':
      res = uapp.stdLookup(sdr, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
    else:
      res = uapp.stdLookup(sdr, "reference@lookupRefByCode", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
    return 0
    
