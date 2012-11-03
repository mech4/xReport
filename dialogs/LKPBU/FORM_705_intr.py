REFMAP = {
  'LINSTRUMEN'                  : 'R_KOMPONEN_NONDERIVATIF'
  ,'LPOSOPTION'                  : 'R_KOMPONEN_D_OPTION'
  ,'LVAROPTION'                  : 'R_VAR_DASAR'
  ,'LPOSFORWARD'                 : 'R_KOMPONEN_D_FORWARD'
  ,'LVARFORWARD'                 : 'R_VAR_DASAR'
  ,'LVARSWAP'                    : 'R_VAR_DASAR'
  ,'LKARAKTERISTIK'              : 'R_KARAKTERISTIK_PRODUK'
  ,'LVALDAS'                     : 'R_SANDI_VALUTA'
}
  
class LKPBU_FORM_705:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LINSTRUMEN'
      ,'LPOSOPTION'
      ,'LVAROPTION'
      ,'LPOSFORWARD'
      ,'LVARFORWARD'
      ,'LVARSWAP'
      ,'LKARAKTERISTIK'
      ,'LVALDAS'
    ]
    self.attrlist = [
      'NamaProduk'
      ,'JmlNasabah'
      ,'StrikePrice'
      ,'Nominal'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form705.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'NamaProduk'
        , 2: 'JmlNasabah'
        , 3: 'LINSTRUMEN_reference_code'
        , 4: 'LPOSOPTION_reference_code'
        , 5: 'LVAROPTION_reference_code'
        , 6: 'LPOSFORWARD_reference_code'
        , 7: 'LVARFORWARD_reference_code'
        , 8: 'LVARSWAP_reference_code'
        , 9: 'LKARAKTERISTIK_reference_code'
        , 10: 'LVALDAS_reference_code'
        , 11: 'StrikePrice'
        , 12: 'Nominal'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form705.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[50,0]
      ,[12,1]
      ,[2,0]
      ,[2,0]
      ,[2,0]
      ,[2,0]
      ,[2,0]
      ,[2,0]
      ,[1,0]
      ,[3,0]
      ,[7,3]
      ,[15,1]
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
    