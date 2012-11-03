REFMAP = {
  'LJENISAKTIVA'                : 'R_JENIS_AKTIVA_IJARAH'
  ,'LJENISVALUTAPEROLEHAN'       : 'R_VALUTA_IJARAH'
  ,'LMETODA'                     : 'R_METODA_SUSUT_IJARAH'
  ,'LJENISAKAD'                  : 'R_JENIS_AKAD_IJARAH'
  ,'LJENISVALUTAAKAD'            : 'R_VALUTA_IJARAH'
  ,'LPERIODE'                    : 'R_PERIODE_PEMBAYARAN_SEWA'
  ,'LGOLPENYEWA'                 : 'R_BANK_DAN_PIHAK_KE3'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEK'                      : 'R_KOLEKTIBILITAS'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_44:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPERIODE'
      ,'LGOLPENYEWA'
      ,'LHUBBANK'
      ,'LKOLEK'
      ,'LGOLPENJAMIN'
      ,'LJENISAKTIVA'
      ,'LJENISVALUTAPEROLEHAN'
      ,'LMETODA'
      ,'LJENISAKAD'
      ,'LJENISVALUTAAKAD'
    ]
    self.attrlist = [
      'NilaiKontrak'
      ,'Mulai'
      ,'JatuhTempo'
      ,'NilaiSewa'
      ,'BagDijamin'
      ,'Tunggakan'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
      ,'BulanTahunPerolehan'
      ,'HargaPerolehan'
      ,'Akumulasi'
      ,'NilaiBersih'
      ,'NomorAkad'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form44.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENISAKTIVA_reference_code'
        , 2: 'BulanTahunPerolehan'
        , 3: 'LJENISVALUTAPEROLEHAN_reference_code'
        , 4: 'HargaPerolehan'
        , 5: 'LMETODA_reference_code'
        , 6: 'Akumulasi'
        , 7: 'NilaiBersih'
        , 8: 'NomorAkad'
        , 9: 'LJENISAKAD_reference_code'
        , 10: 'LJENISVALUTAAKAD_reference_code'
        , 11: 'NilaiKontrak'
        , 12: 'Mulai'
        , 13: 'JatuhTempo'
        , 14: 'LPERIODE_reference_code'
        , 15: 'NilaiSewa'
        , 16: 'LGOLPENYEWA_reference_code'
        , 17: 'LHUBBANK_reference_code'
        , 18: 'LKOLEK_reference_code'
        , 19: 'LGOLPENJAMIN_reference_code'
        , 20: 'BagDijamin'
        , 21: 'Akumulasi'
        , 22: 'AgunanPPAP'
        , 23: 'PPAPDibentuk'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form44.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [2,0]
      , [6,1]
      , [1,0]
      , [12,1]
      , [2,0]
      , [12,1]
      , [12,1]
      , [15,0]
      , [1,0]
      , [1,0]
      , [12,1]
      , [6,1]
      , [6,1]
      , [1,0]
      , [12,1]
      , [3,0]
      , [1,0]
      , [1,0]
      , [3,0]
      , [12,1]
      , [4,3]
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
      
  #def OnEnter(self, sender):
        
    