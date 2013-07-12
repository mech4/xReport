REFMAP = {
  'LJENIS'           : 'R_BENTUK_INSTRUMEN'
  ,'LJENISVALUTA'    : 'R_JENIS_MEDIA' 
}
  
class LKPBU_FORM_303:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'jumlah'
      , 'MaksLimit'
      , 'DanaFloat'
      , 'VolumeTR'
      , 'NilaiTR'
      , 'JmlhMerchant'
      , 'JmlhTerminal'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form303.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'
      , 2: 'LJENISVALUTA_reference_code'
      , 3: 'jumlah'
      , 4: 'MaksLimit'
      , 5: 'DanaFloat'
      , 6: 'VolumeTR'
      , 7: 'NilaiTR'
      , 8: 'JmlhMerchant'
      , 9: 'JmlhTerminal'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form303.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [2,0]  
      , [12,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [15,1]
      , [12,1]
      , [12,1]
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
#-------------------------------------------------------------------------------        

      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    