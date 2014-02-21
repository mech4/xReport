import sys, os

def GetGridData(config, params, returns):
  status = returns.CreateValues(['Err',''])
  GridData = returns.AddNewDatasetEx('gdata','fkode:string;fname:string;status:string')
  def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
      if name in files:
        result.append(os.path.join(root, name))
    return result
  rec = params.FirstRecord
  dtsid = rec.dtsid
  periodid = rec.periodid
  branchid = rec.branchid
  bCode = rec.bCode
  pCode = rec.pCode
  mlu = config.ModLibUtils
  config.BeginTransaction()
  try:
    if bCode in ('',None,0):
      bCode = '517001000'
    if len(bCode)==6:
      bCode = bCode+'000'
    if len(bCode)!=9 or not bCode.isdigit():
      raise Exception, 'Kode wilayah %s tidak sesuai format standar' % str(bCode)
    bln = int(pCode[:2])
    thn = int(pCode[2:])
    if bln<12:
      nextmo = mlu.EncodeDate(thn, bln+1, 1)
    else:
      nextmo = mlu.EncodeDate(thn+1,1,1)
    reportdate = nextmo-1
    thn, bln, tgl = mlu.DecodeDate(reportdate)
    str_repdate = '{0}-{1}-{2}'.format(str(thn).zfill(4),str(bln).zfill(2),str(tgl).zfill(2))
    s = '''
        select reportlocation dataloc from dtsreport 
        where dtsid={0}
        and period_id={1}
        and branch_id={2} 
    '''.format(dtsid,periodid,branchid)
    dataLoc = config.CreateSQL(s).RawResult.dataloc
    s = '''
        select a.* from dtsform a, dtsfile b, dtsfolder c
        where a.dtsformid=b.dtsfileid
        and b.dtsfolderid=c.dtsfolderid
        and c.dtsid={0}    
    '''.format(dtsid)
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      if res.formtype == 'N':
        pass
      else:
        instancename = str(bCode)+ '-' + str_repdate + '-MM-' + res.dtsformcode + '.xml'
        st = find_all(instancename, dataLoc)
        if len(st)>0:
          pass
        else:
          gData = GridData.AddRecord()
          gData.fkode = res.dtsformcode
          gData.fname = res.dtsformdesc
          gData.status = 'B'
      res.Next()
    res.First() 
    while not res.Eof:
      if res.formtype == 'N':
        pass
      else:
        instancename = str(bCode)+ '-' + str_repdate + '-MM-' + res.dtsformcode + '.xml'
        st = find_all(instancename, dataLoc)
        if len(st)>0:
          gData = GridData.AddRecord()
          gData.fkode = res.dtsformcode
          gData.fname = res.dtsformdesc
          gData.status = 'T'
        else:
          pass
      res.Next()
    res.First() 
    while not res.Eof:
      if res.formtype == 'N':
        gData = GridData.AddRecord()
        gData.fkode = res.dtsformcode
        gData.fname = res.dtsformdesc
        gData.status = 'N'
      else:
        pass
      res.Next() 
    config.Commit()
  except:
    config.Rollback()
    status.Err = str(sys.exc_info()[1])                                                        