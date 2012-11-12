import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def FormOnSetDataEx(uideflist, params):
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  form_loaditem.setData(uideflist, params)
  if uideflist.uipData.Dataset.RecordCount==0:
    config = uideflist.config
    mlu = config.ModLibUtils
    pid = params.FirstRecord.period_id
    pCode = config.CreateSQL("select period_code from period where period_id=%s" % pid).RawResult.period_code
    #week = int(pCode[:1])
    #bln = int(pCode[5:7])
    #thn = int(pCode[1:5])
    ds = uideflist.uipData.Dataset
    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_KOMPONEN_RP' order by a.reference_code" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rec = ds.AddRecord()
      rec.SetFieldByName('LKOMPONEN.reference_desc', res.reference_desc)    
      rec.SetFieldByName('LKOMPONEN.reference_code', res.reference_code)    
      rec.SetFieldByName('LKOMPONEN.refdata_id', res.refdata_id)    
      res.Next()
    #--
    
