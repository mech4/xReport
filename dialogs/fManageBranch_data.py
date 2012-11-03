
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  key = params.FirstRecord.key
  uideflist.SetData('uipBranch',key)
  
def GetLinkedBranch(config, params, returns):
  branch_id = params.FirstRecord.branch_id
  status = returns.CreateValues(['Err',''])
  cabData = returns.AddNewDatasetEx(
     'cabang',
     ';'.join([
     'kode:string',
     'nama:string'
     ])
  )
  config.BeginTransaction()
  try:
    s = "select a.kode_cabang, ent.nama_cabang from branchmember a, %s ent \
         where a.kode_cabang=ent.kode_cabang and a.branch_id='%s' \
         " % (config.MapDBTableName('enterprise.Cabang'), branch_id)
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rec = cabData.AddRecord()
      rec.kode = res.kode_cabang
      rec.nama = res.nama_cabang
      res.Next()
    config.Commit()
  except:
    config.Rollback()
    status.Err = str(sys.exc_info()[1])
    
def AddLinkedBranch(config, params, returns):
  kode_cabang = params.FirstRecord.kode_cabang
  branch_id = params.FirstRecord.branch_id
  status = returns.CreateValues(['Err',''])
  config.BeginTransaction()
  try:
    s = "insert into branchmember (branch_id,kode_cabang) values('%s','%s')" % (branch_id,kode_cabang)
    config.ExecSQL(s)
    config.Commit()
  except:
    config.Rollback()
    status.Err = str(sys.exc_info()[1])

def Hapus(config, params, returns):
  kode_cabang = params.FirstRecord.kode_cabang
  branch_id = params.FirstRecord.branch_id
  status = returns.CreateValues(['Err',''])
  config.BeginTransaction()
  try:
    s = "delete from branchmember where branch_id='%s' and kode_cabang='%s'" % (branch_id,kode_cabang)
    config.ExecSQL(s)
    config.Commit()
  except:
    config.Rollback()
    status.Err = str(sys.exc_info()[1])
  