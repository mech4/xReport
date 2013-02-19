REFMAP = {
  'LPLN'                      : 'R_SANDI_PLN'
  ,'LNEGARA'                    : 'R_KODE_NEGARA'
  ,'LSEKTOR'                     : 'R_SEKTOR_RIIL'
  ,'LVALUTA'                     : 'R_SANDI_VALUTA'
}
  
class LHBU_FORM_407:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPLN'
      ,'LNEGARA'
      ,'LSEKTOR'
      ,'LVALUTA'
    ]
    self.attrlist = [
      'JangkaWaktu'
      ,'Modal'
      ,'NominalPLN'
      ,'TglModal'
      ,'TglMulai'
      ,'TglPosisi'
      ,'TglTempo'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form407.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'TglPosisi'
        , 2: 'LVALUTA_reference_code'
        , 3: 'LPLN_reference_code'
        , 4: 'NominalPLN'
        , 5: 'JangkaWaktu'
        , 6: 'TglTempo'
        , 7: 'TglMulai'
        , 8: 'TglModal'
        , 9: 'Modal'
        ,10: 'LSEKTOR_reference_code'
        ,11: 'LNEGARA_reference_code'
    }
    self.useheader = 3 #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU
    self.txttemplate = 'lhbu/form407.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [8,1]
      , [3,0]
      , [2,0]
      , [15,1]
      , [3,0]
      , [8,1]
      , [8,1]
      , [8,1]
      , [15,1]
      , [6,0]
      , [2,0]
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
    