REFMAP = {
  'LJANGKA'                     : 'R_JANGKA_LBBU'
}
  
class LBBU_FORM_8:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJANGKA'
    ]
    self.attrlist = [
      'PosisiDIM'
      ,'ImbalanDIM'
      ,'BagHas'
      ,'DistribusiDIM'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form8.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'PosisiDIM'
        , 2: 'LJANGKA_reference_code'
        , 3: 'ImbalanDIM'
        , 4: 'BagHas'
        , 5: 'DistribusiDIM'
        , 6: '@Endmonth'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form8.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [30,1]
      , [2,0]
      , [10,1]
      , [10,1]
      , [10,1]
      , [8,0]
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
    