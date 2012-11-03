REFMAP = {
  'LBANK'            : 'R_SANDI_BANK'
  , 'LOPERASI'       : 'R_JENIS_OPERASIONAL'
  , 'LHUBBANK'       : 'R_HUBUNGAN_DENGAN_BANK'
  , 'LJENIS'         : 'R_JENIS_SIMPANAN_WADIAH'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
  , 'LKOLEKTIBILITAS': 'R_KOLEKTIBILITAS'
  , 'LPENJAMIN'      : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_04:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LBANK'
      ,'LOPERASI'
      ,'LHUBBANK'
      ,'LJENIS'
      ,'LJENISVALUTA'
      ,'LKOLEKTIBILITAS'
      ,'LPENJAMIN'
    ]
    self.attrlist = [
       'JatuhTempo'
      ,'PersenBagiHasil'
      ,'BagianDijamin'
      ,'Jumlah'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form04.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LBANK_reference_code'
        , 2: 'LOPERASI_reference_code'
        , 3: 'LHUBBANK_reference_code'
        , 4: 'LJENIS_reference_code'
        , 5: 'LJENISVALUTA_reference_code'
        , 7: 'JatuhTempo'
        , 8: 'LKOLEKTIBILITAS_reference_code'
        , 9: 'PersenBagiHasil'
        , 10: 'LPENJAMIN_reference_code'
        , 11: 'BagianDijamin'
        , 12: 'Jumlah'
        , 13: 'AgunanPPAP'
        , 14: 'PPAPDibentuk'
    }
    self.useheader = 2 #1: true, 0:false
    self.txttemplate = 'lbus/form04.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [3,0]
      , [1,0]
      , [1,0]
      , [2,0]
      , [3,0]
      , [6,1]
      , [6,1]
      , [1,0]
      , [4,3]
      , [3,0]
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
    