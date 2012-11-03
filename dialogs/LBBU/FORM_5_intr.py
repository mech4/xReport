REFMAP = {
  'LINDIKEL'                    : 'R_INDIVIDU_KELOMPOK'
  ,'LHUBBANK'                    : 'R_HUB_KETERKAITAN'
  ,'LSTATUSHUB'                  : 'R_DETAIL_HUB_BANK'
  ,'LJENISDANA'                  : 'R_PENYEDIAAN_DANA'
  ,'LBENTUKJAMINAN'              : 'R_BENTUK_JAMINAN'
  ,'LPENERBIT'                   : 'R_BANK_DAN_PIHAK_KE3'
  ,'LPEMERINGKAT'                : 'R_PEMERINGKAT'
  ,'LPENATA'                     : 'R_BANK_DAN_PIHAK_KE3'
  ,'LKUALITAS'                    : 'R_KUALITAS'
}
  
class LBBU_FORM_5:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LINDIKEL'
      ,'LHUBBANK'
      ,'LSTATUSHUB'
      ,'LJENISDANA'
      ,'LBENTUKJAMINAN'
      ,'LPENERBIT'
      ,'LPEMERINGKAT'
      ,'LPENATA'
      ,'LKUALITAS'
    ]
    self.attrlist = [
      'Nama'
      ,'GrupKelompok'
      ,'JangkaAwal'
      ,'JangkaTempo'
      ,'JmlRp'
      ,'JmlVa'
      ,'Kurs'
      ,'Modal'
      ,'NilaiJaminan'
      ,'Peringkat'
      ,'TglPemeringkat'
      ,'JaminanAwal'
      ,'JaminanTempo'
      ,'Nominal'
      ,'Persen'
      ,'Keterangan'
    ]
    self.paction     = 1
    self.xlstemplate = 'lbbu/form5.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'Nama'
        , 2: 'LINDIKEL_reference_code'
        , 3: 'GrupKelompok'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'LSTATUSHUB_reference_code'
        , 6: 'LJENISDANA_reference_code'
        , 7: 'JangkaAwal'
        , 8: 'JangkaTempo'
        , 9: 'JmlRp'
        , 10: 'JmlVa'
        , 11: 'Kurs'
        , 12: 'Modal'
        , 13: 'LBENTUKJAMINAN_reference_code'
        , 14: 'NilaiJaminan'
        , 15: 'LPENERBIT_reference_code'
        , 16: 'Peringkat'
        , 17: 'LPEMERINGKAT_reference_code'
        , 18: 'TglPemeringkat'
        , 19: 'LPENATA_reference_code'
        , 20: 'JaminanAwal'
        , 21: 'JaminanTempo'
        , 22: 'Nominal'
        , 23: 'Persen'
        , 24: 'LKUALITAS_reference_code'
        , 25: 'Keterangan'
        , 26: '@Endmonth'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form5.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [25,0]
      , [1,0]
      , [30,0]
      , [1,0]
      , [4,0]
      , [2,0]
      , [8,0]
      , [8,0]
      , [30,1]
      , [30,1]
      , [30,1]
      , [30,1]
      , [2,0]
      , [30,1]
      , [3,0]
      , [12,0]
      , [2,0]
      , [8,0]
      , [3,0]
      , [8,0]
      , [8,0]
      , [30,1]
      , [10,1]
      , [3,0]
      , [100,0]
      , [8,0]
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
    