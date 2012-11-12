REFMAP = {
  'LPos'                        : 'R_POS2_LBBU'
}
  
class LBBU_FORM_2:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPos'
    ]
    self.attrlist = [
      'PPRupiah'
      ,'PPValas'
      ,'PPJumlah'
      ,'PLRupiah'
      ,'PLValas'
      ,'PLJumlah'
      ,'BPRupiah'
      ,'BPValas'
      ,'BPJumlah'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form2.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LPos_reference_desc'
        , 2: 'LPos_reference_code'
        , 3: 'PPRupiah'
        , 4: 'PPValas'
        , 5: 'PPJumlah'
        , 6: 'PLRupiah'
        , 7: 'PLValas'
        , 8: 'PLJumlah'
        , 9: 'BPRupiah'
        , 10: 'BPValas'
        , 11: 'BPJumlah'
        , 12: 'Jumlah'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form2.txt'
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
      return 1
    else:
      res = uapp.stdLookup(sender, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
        
      return res

  def refBeforeLookup(self, sender, linkui):
    sName = sender.Name.split('.')[0]           
    sType = sender.Name.split('.')[-1].split('_')[-1]
    sdr = self.pData_LPos
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