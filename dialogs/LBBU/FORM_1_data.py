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
    week = int(pCode[:1])
    tgl = mlu.DecodeDate(config.Now())
    bln = int(pCode[5:7])
    thn = int(pCode[1:5])
    ds = uideflist.uipData.Dataset
    if week==1:
      rg = (1,8)
    elif week==2:
      rg = (8,16)
    elif week==3:
      rg = (16,24)
    else:
      if bln<12:
        bln_berikutnya = bln+1
        thn_berikutnya = thn
      else:
        bln_berikutnya = 1
        thn_berikutnya = thn+1
      tglakhir = mlu.DecodeDate(mlu.EncodeDate(thn_berikutnya,bln_berikutnya,1)-1)[2]
      rg = (24, tglakhir)
    for i in range(rg[0],rg[1]):  
      rec = ds.AddRecord()
      rec.Tanggal = str(i).zfill(2)+str(bln).zfill(2)+str(thn)
    #comment for auto on output
    #rec = ds.AddRecord()
    #rec.Tanggal = 'Jml'
    #rec = ds.AddRecord()
    #rec.Tanggal = 'Rata2'
    
