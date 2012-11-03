REFMAP = {
  'LCARA'                       : 'R_RESTRUKTURISASI'
  ,'LAKADSBLM'                   : 'R_AKAD_LBBU'
  ,'LAKADSTLH'                   : 'R_AKAD_LBBU'
  ,'LVALSBLM'                    : 'R_JENIS_VALUTA'
  ,'LKUASBLM'                    : 'R_KUALITAS'
  ,'LVALSTLH'                    : 'R_JENIS_VALUTA'
  ,'LKUASTLH'                    : 'R_KUALITAS'
}
  
class LBBU_FORM_9:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LCARA'
      ,'LAKADSBLM'
      ,'LVALSBLM'
      ,'LKUASBLM'
      ,'LAKADSTLH'
      ,'LVALSTLH'
      ,'LKUASTLH'
    ]
    self.attrlist = [
      'Nama'
      ,'NPWP'
      ,'Alamat'
      ,'Frekuensi'
      ,'PlafonSblm'
      ,'SaldoSBLM'
      ,'NisbahSBLM'
      ,'BagHasSBLM'
      ,'TunggakanSBLM'
      ,'AwalSBLM'
      ,'TempoSBLM'
      ,'TglAgunanSBLM'
      ,'NilaiAgunanSBLM'
      ,'PlafonSTLH'
      ,'SaldoSTLH'
      ,'NisbahSTLH'
      ,'BagHasSTLH'
      ,'AwalSTLH'
      ,'TempoSTLH'
      ,'TglAgunanSTLH'
      ,'NilaiAgunanSTLH'
      ,'Kerugian'
    ]
    self.paction     = None
    self.xlstemplate = 'lbbu/form9.xls'
    self.xlstopline  = 9
    self.xlsmap      = {
          1: 'Nama'
        , 2: 'NPWP'
        , 3: 'Alamat'
        , 4: 'LCARA_reference_code'
        , 5: 'Frekuensi'
        , 6: 'LAKADSBLM_reference_code'
        , 7: 'PlafonSblm'
        , 8: 'SaldoSBLM'
        , 9: 'LVALSBLM_reference_code'
        , 10: 'NisbahSBLM'
        , 11: 'BagHasSBLM'
        , 12: 'TunggakanSBLM'
        , 13: 'AwalSBLM'
        , 14: 'TempoSBLM'
        , 15: 'LKUASBLM_reference_code'
        , 16: 'TglAgunanSBLM'
        , 17: 'NilaiAgunanSBLM'
        , 18: 'LAKADSTLH_reference_code'
        , 19: 'PlafonSTLH'
        , 20: 'SaldoSTLH'
        , 21: 'LVALSTLH_reference_code'
        , 22: 'NisbahSTLH'
        , 23: 'BagHasSTLH'
        , 24: 'AwalSTLH'
        , 25: 'TempoSTLH'
        , 26: 'LKUASTLH_reference_code'
        , 27: 'TglAgunanSTLH'
        , 28: 'NilaiAgunanSTLH'
        , 29: 'Kerugian'
        , 30: '@Endmonth'
    }
    self.useheader = 4 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    self.txttemplate = 'lbbu/form9.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    #       jenis 4 untuk tgl dgn separator '/' dan spasi 
    self.txtmap      = ( [0,0]
      , [85,0]
      , [15,0]
      , [200,0]
      , [3,0]
      , [3,1]
      , [2,0]
      , [30,1]
      , [30,1]
      , [3,0]
      , [10,1]
      , [10,1]
      , [30,1]
      , [8,0]
      , [8,0]
      , [1,0]
      , [8,0]
      , [30,1]
      , [2,0]
      , [30,1]
      , [30,1]
      , [3,0]
      , [10,1]
      , [10,1]
      , [8,0]
      , [8,0]
      , [1,0]
      , [8,0]
      , [30,1]
      , [30,1]
      , [8,1]
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
    