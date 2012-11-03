REFMAP = {
  'LSTATUSTENAGAKERJA'          : 'R_JENIS_PENYELESAIAN'
}
  
class LKPBU_FORM_605:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LSTATUSTENAGAKERJA']
    self.attrlist = [
      'NIP'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form807.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LSTATUSTENAGAKERJA_reference_code'
      , 2: 'NIP'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form807.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [35,0]
      '''  
      , [12,1]
      , [12,1]
      , [15,1]
      '''
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
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    