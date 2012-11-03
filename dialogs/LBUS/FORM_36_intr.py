REFMAP = {
  'LJENIS'                     : 'R_JENIS_AKTIVA_PRODUKTIF'
  , 'LJENISVALUTA'             : 'R_JENIS_VALUTA'
  , 'LBENTUKPENGHAPUSANBUKUAN' : 'R_BENTUK_HAPUS_BUKU'
  , 'LDEBITUR'                 : 'R_BANK_DAN_PIHAK_KE3'
  , 'LHUBUNGANBANK'            : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'           : 'R_KOLEKTIBILITAS'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LBENTUKPENGHAPUSANBUKUAN'
      ,'LJENISVALUTA'
      ,'LDEBITUR'
      ,'LHUBUNGANBANK'
      ,'LKOLEKTIBILITAS'
    ]
    self.attrlist = [
      'NoRekening'
      ,'JumlahRekening'
      ,'TanggalHapusBuku'
      ,'Agunan'
      ,'BakiDebetHapusbuku'
      ,'BakiDebetBulan'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form36.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'NoRekening'
        , 2: 'JumlahRekening'
        , 3: 'LJENIS_reference_code'
        , 4: 'LBENTUKPENGHAPUSANBUKUAN_reference_code'
        , 5: 'LJENISVALUTA_reference_code'
        , 6: 'LDEBITUR_reference_code'
        , 7: 'LHUBUNGANBANK_reference_code'
        , 8: 'TanggalHapusBuku'
        , 9: 'LKOLEKTIBILITAS_reference_code'
        , 10: 'Agunan'
        , 11: 'BakiDebetHapusbuku'
        , 12: 'BakiDebetBulan'
        , 13: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form36.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [15,0]
      , [8,1]
      , [2,0]
      , [1,0]
      , [3,0]
      , [3,0]
      , [1,0]
      , [8,1]
      , [1,0]
      , [12,1]
      , [12,1]
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
    