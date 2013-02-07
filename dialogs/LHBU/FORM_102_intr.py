REFMAP = {
  'LPENANAMDANA'                : 'R_SANDI_BANK'
  ,'LPENGELOLADANA'              : 'R_SANDI_BANK'
  ,'LCURRENCY'                   : 'R_SANDI_VALUTA'
  ,'LJENISPENANAM'               : 'R_JENIS_KEG_BANK'
  ,'LJENISPENGELOLA'             : 'R_JENIS_KEG_BANK'
  ,'LJENISPUAS'                  : 'R_PUAS'
}
  
class LHBU_FORM_102:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LPENANAMDANA', 'LPENGELOLADANA', 'LCURRENCY', 'LJENISPENANAM', 'LJENISPENGELOLA', 'LJENISPUAS']
    self.attrlist = [
      'IdOperasional'
      , 'NoReff'
      , 'TingkatImbalan'
      , 'BagHas'
      , 'Volume'
      , 'VolValDas'
      , 'TglValuta'
      , 'TglTempo'
      , 'Waktu'
      , 'JamTransaksi'
      , 'ImbalanPUAS'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form102.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'IdOperasional'
        , 2: 'NoReff'                          
        , 3: 'LPENANAMDANA_reference_code'
        , 4: 'LPENGELOLADANA_reference_code'
        , 5: 'LCURRENCY_reference_code'
        , 6: 'TingkatImbalan'
        , 7: 'BagHas'
        , 8: 'Volume'
        , 9: 'VolValDas'
        , 10: 'TglValuta'
        , 11: 'TglTempo'
        , 12: 'Waktu'
        , 13: 'JamTransaksi'
        , 14: 'LJENISPENANAM_reference_code'
        , 15: 'LJENISPENGELOLA_reference_code'
        , 16: 'LJENISPUAS_reference_code'
        , 17: 'ImbalanPUAS'
    }
    self.useheader = 3 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU
    self.txttemplate = 'lhbu/form102.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
        , [1,0]
        , [16,0]
        , [3,0]
        , [3,0]
        , [3,0]
        , [8,2]
        , [8,2]
        , [9,1]
        , [16,1]
        , [8,1]
        , [8,1]
        , [3,1]
        , [4,1]
        , [2,0]
        , [2,0]
        , [3,0]
        , [8,2]
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
    