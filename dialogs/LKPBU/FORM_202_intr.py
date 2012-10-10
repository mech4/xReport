REFMAP = {
  'LJENIS'           : 'R_PENJUAL_SKBDN'
  ,'LJENISVALUTA'    : 'R_SANDI_VALUTA' 
}
  
class LKPBU_FORM_202:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'jumlah'
      , 'Volume'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form202.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'jumlah'
      , 3: 'LJENISVALUTA_reference_code'
      , 4: 'Volume'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form202.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [1,0]
      , [5,1]  
      , [3,0]
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
      
  def onenter(self, sender):
    Code = self.uipData.GetFieldValue('LJENISSURATBERHARGA.reference_code') 
    if Code =='99':
      self.uipData.Keterangan=' '
      self.pData_Keterangan.Enabled=1
    if Code !='99':
      self.uipData.Keterangan='-'
      self.pData_Keterangan.Enabled=0
      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_code')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    