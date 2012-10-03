REFMAP = {
  'LJENIS'           : 'R_JENIS_MESIN'
  ,'LJENISVALUTA'    : 'R_STATUS_PEMANFAATANMESIN'
}
  
class LKPBU_FORM_302:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'Keterangan'
      , 'jumlah'
      , 'JmlhMerchant'
      , 'VolumeTR'
      , 'NilaiTR'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form302.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'Keterangan'
      , 3: 'LJENISVALUTA_reference_code'
      , 4: 'jumlah'
      , 5: 'JmlhMerchant'
      , 6: 'VolumeTR'
      , 7: 'NilaiTR'
    }
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
    