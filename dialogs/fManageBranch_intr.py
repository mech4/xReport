class fManageBranch:
  def __init__(self, formObj, parentForm):
    pass
  #--
  def Show(self):
    self.app = self.FormObject.ClientApplication
    ph = self.app.CreateValues(['branch_id', self.uipBranch.branch_id])
    res = self.FormObject.CallServerMethod('GetLinkedBranch', ph)
    status = res.FirstRecord
    if status.Err not in (None,'',0):
       self.app.ShowMessage('PERINGATAN : ' + status.Err)
       return 0
       
    grid = self.uipMember
    grid.ClearData()
    ds = res.packet.cabang
    for i in range(ds.RecordCount):
      grid.Append()
      rec = ds.GetRecord(i)
      grid.kode = rec.kode
      grid.nama = rec.nama                  
    #grid.Post()
    grid.First()    
    self.FormContainer.Show()
    
  def Add2Group(self, sender):
    self.app = self.FormObject.ClientApplication
    asbranch = self.uiLookup.GetFieldValue('LCabang.Kode_Cabang') 
    if asbranch in (None,'',0):
       self.app.ShowMessage('PERINGATAN : Cabang belum dipilih.')
       return 0
       
    #ph = self.app.CreateValues(['kode_cabang', asbranch])
    #res = self.FormObject.CallServerMethod('BranchCheck', ph)
    #status = res.FirstRecord
    #if status.Err not in (None,'',0):
    #   self.app.ShowMessage('PERINGATAN : ' + status.Err)
    #   return 0
       
    #if status.Ada>0 :
    #   self.app.ShowMessage('PERINGATAN : Cabang lokal telah terdaftar pada %s' % status.nama)
    #   return 0
       
    asbase = self.uipBranch.branch_id 
    ph = self.app.CreateValues(['branch_id', asbase], ['kode_cabang', asbranch])
    res = self.FormObject.CallServerMethod('AddLinkedBranch', ph)
    status = res.FirstRecord
    if status.Err not in (None,'',0):
       self.app.ShowMessage('PERINGATAN : ', status.Err)
       return 0
    self.Show()
    
  def DelFromGroup(self):
    self.app = self.FormObject.ClientApplication
    if self.app.ConfirmDialog('Yakin akan menghapus data dari group ?') :
       kode = self.uipMember.kode
       asbase = self.uipBranch.branch_id
       ph = self.app.CreateValues(['branch_id',asbase],['kode_cabang',kode])
       res = self.FormObject.CallServerMethod('Hapus', ph)
       status = res.FirstRecord
       if status.Err not in (None,'',0):
          self.app.ShowMessage('PERINGATAN : ' + status.Err)
          return 0
       self.app.ShowMessage('Data berhasil dihapus.')
       self.Show()          
    