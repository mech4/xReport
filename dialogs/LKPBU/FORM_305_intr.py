REFMAP = {
  'LJenisKartu'           : 'R_JENIS_KARTU2'
  , 'LJenisTransaksi'   : 'R_TRX_KARTU2'
}
  
class LKPBU_FORM_305:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJenisKartu', 'LJenisTransaksi']
    self.attrlist = [
      'JmlPeserta'
      , 'VolTransaksi'
      , 'NominalTransaksi'
      , 'NominalSettlement'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form305.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJenisKartu_reference_code'  
      , 2: 'JmlPeserta'
      , 3: 'LJenisTransaksi_reference_code'
      , 4: 'VolTransaksi'
      , 5: 'NominalTransaksi'
      , 6: 'NominalSettlement'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form305.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [12,1]
      , [2,0]
      , [12,1]
      , [15,1]
      , [15,1]
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
      

    