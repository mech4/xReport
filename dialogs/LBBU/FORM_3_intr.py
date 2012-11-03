REFMAP = {
  'LJenis'                      : 'R_JENIS_DANA'
}
  
class LBBU_FORM_3:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJenis'
    ]
    self.attrlist = [
      'PPKPKNRp'
      ,'PPKPKNVa'
      ,'PPDKRp'
      ,'PPDKVa'
      ,'PPDLRp'
      ,'PPDLVa'
      ,'PPSubJml'
      ,'PPSubJmlVa'
      ,'PDT1Rp'
      ,'PDT1Va'
      ,'PDT2Rp'
      ,'PDT2Va'
      ,'PDSubJmlRp'
      ,'PDSubJmlVa'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form3.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJenis_reference_desc'
        , 2: 'LJenis_reference_code'
        , 3: 'PPKPKNRp'
        , 4: 'PPKPKNVa'
        , 5: 'PPDKRp'
        , 6: 'PPDKVa'
        , 7: 'PPDLRp'
        , 8: 'PPDLVa'
        , 9: 'PPSubJml'
        , 10: 'PPSubJmlVa'
        , 11: 'PDT1Rp'
        , 12: 'PDT1Va'
        , 13: 'PDT2Rp'
        , 14: 'PDT2Va'
        , 15: 'PDSubJmlRp'
        , 16: 'PDSubJmlVa'
        , 17: 'Jumlah'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form3.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [80,0]
      , [5,0]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
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
    