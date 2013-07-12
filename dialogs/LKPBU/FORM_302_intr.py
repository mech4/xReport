REFMAP = {
  'LJenisData'           : 'R_JENIS_INFO'
}
  
class LKPBU_FORM_302:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJenisData']
    self.attrlist = [
      'DataATM'
      , 'DataATMDebit'
      , 'DataEMoney'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form302.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJenisData_reference_code'  
      , 2: 'DataATM'
      , 3: 'DataATMDebit'
      , 4: 'DataEMoney'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form302.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [15,1]
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
#-------------------------------------------------------------------------------      
  
  def refExit2(self, sender):
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
      
    Code = self.uipData.GetFieldValue('LJENISVALUTA.reference_code') 
    if Code =='002':
      self.pData_LBERSAMA.Enabled=0
    if Code =='001':
      self.pData_LBERSAMA.Enabled=1   

      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    