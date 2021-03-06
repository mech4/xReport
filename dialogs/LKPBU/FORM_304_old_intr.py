REFMAP = {
  'LJENIS'           : 'R_JENIS_KARTU_APMK'
  , 'LFRAUD'   : 'R_JENIS_FRAUD'
}
  
class LKPBU_FORM_304:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LFRAUD']
    self.attrlist = [
      'KeteranganJK'
      , 'Keterangan'
      , 'JmlhKasus1'
      , 'JmlhKasus2'
      , 'NominalKerugian'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form304.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'KeteranganJK'
      , 3: 'LFRAUD_reference_code'
      , 4: 'Keterangan'
      , 5: 'JmlhKasus1'
      , 6: 'JmlhKasus2'
      , 7: 'NominalKerugian'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form304.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [35,0]  
      , [2,0]
      , [35,0]
      , [12,1]
      , [12,1]
      , [15,1]
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
    if sName=='LJENIS':
      Code = self.uipData.GetFieldValue('LJENIS.reference_code') 
      if Code =='199':
        self.uipData.KeteranganJK=' '
        self.pData_KeteranganJK.Enabled=1
      if Code !='199':
        self.uipData.KeteranganJK='-'
        self.pData_KeteranganJK.Enabled=0
    if sName=='LFRAUD':
      Code = self.uipData.GetFieldValue('LFRAUD.reference_code') 
      if Code =='99':
        self.uipData.Keterangan=' '
        self.pData_Keterangan.Enabled=1
      if Code !='99':
        self.uipData.Keterangan='-'
        self.pData_Keterangan.Enabled=0
      
  def onenter(self, sender):
    Code = self.uipData.GetFieldValue('LJENIS.reference_code') 
    if Code =='199':
      self.uipData.KeteranganJK=' '
      self.pData_KeteranganJK.Enabled=1
    if Code !='199':
      self.uipData.KeteranganJK='-'
      self.pData_KeteranganJK.Enabled=0
      
  def masuk(self, sender):
    Code = self.uipData.GetFieldValue('LFRAUD.reference_code') 
    if Code =='99':
      self.uipData.Keterangan=' '
      self.pData_Keterangan.Enabled=1
    if Code !='99':
      self.uipData.Keterangan='-'
      self.pData_Keterangan.Enabled=0
      

    