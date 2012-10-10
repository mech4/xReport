REFMAP = {
  'LJENIS'           : 'R_PEMILIK_REKENING'
  , 'LPEMILIK'        : 'R_DATI_1DAN2'
  , 'LPERKIRAAN'   : 'R_AKUN_PEMERINTAH'
  , 'LPEMILIKDANANONDAERAH' : 'R_PEMDANA_NONDAERAH'
  , 'LPEMILIKDANA'        : 'R_DATI_1DAN2'
  , 'LJENISVALUTA' : 'R_SANDI_VALUTA'
  , 'LLAWANTRANSAKSI' : 'R_SANDI_TRANSFER'
}
  
class LKPBU_FORM_501:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LPEMILIK', , 'LPERKIRAAN', 'LPEMILIKDANANONDAERAH', 'LPEMILIKDANA', 'LJENISVALUTA', 'LLAWANTRANSAKSI']
    self.attrlist = [
      'PerkiraanLainya'
    , 'Nominal'
    , 'TglTransaksi'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form501.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'LPEMILIK_reference_code'
      , 3: 'LPERKIRAAN_reference_code'
      , 4: 'Volume'
      , 5: 'LPEMILIKDANANONDAERAH_reference_code'
      , 6: 'LPEMILIKDANA_reference_code'
      , 7: 'LLAWANTRANSAKSI_reference_code'
      , 8: 'LJENISVALUTA_reference_code'
      , 9: 'Nominal'
      , 10: 'TglTransaksi'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form501.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      , [3,0]
      , [4,0]  
      , [5,0]
      , [35,0]
      , [3,0]
      , [4,0]
      , [6,0]
      , [3,0]
      , [15,1]
      , [8,0]
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
    if sName=='LPERKIRAAN':
      Code = self.uipData.GetFieldValue('LPERKIRAAN.reference_code')
      if (Code =='10900') or (Code == '20900'):
        self.uipData.PerkiraanLainya=' '
        self.pData_PerkiraanLainya.Enabled=1
      #if (CodeTambah !='10900' or CodeKurang != '20900'):
      else:
        self.uipData.PerkiraanLainya='-'
        self.pData_PerkiraanLainya.Enabled=0
      
  def onenter(self, sender):
    Code = self.uipData.GetFieldValue('LPERKIRAAN.reference_code')
    if (Code =='10900') or (Code == '20900'):
      self.uipData.PerkiraanLainya=' '
      self.pData_PerkiraanLainya.Enabled=1
    #if (CodeTambah !='10900' or CodeKurang != '20900'):
    else:
      self.uipData.PerkiraanLainya='-'
      self.pData_PerkiraanLainya.Enabled=0

  '''    
  def masuk(self, sender):
    Code = self.uipData.GetFieldValue('LFRAUD.reference_code') 
    if Code =='99':
      self.uipData.Keterangan=' '
      self.pData_Keterangan.Enabled=1
    if Code !='99':
      self.uipData.Keterangan='-'
      self.pData_Keterangan.Enabled=0
   '''  

    