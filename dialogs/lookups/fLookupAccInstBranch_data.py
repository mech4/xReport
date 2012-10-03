import os
import sys
import com.ihsan.lib.remotequery as remotequery

def runQuery(config, params, returns):
  rqsql = remotequery.RQSQL(config)
  rqsql.handleOperation(params, returns)
#--

def initQuery(config, params, returns):
  rqsql = remotequery.RQSQL(config)
  mlu = config.ModLibUtils
  rqsql.SELECTFROMClause = "SELECT\r\n\
    br.kode_cabang, br.nama_cabang \
    FROM GLAccount g,\r\n\
    AccountInstance ai,\r\n\
    %s br\r\n" % (config.MapDBTableName('enterprise.Cabang'))
  fr = params.FirstRecord
  if fr.prefix == "":
    noprefix = 1
  else:
    noprefix = 0
  sPrefix = mlu.QuotedStr(fr.prefix + "%")
  rqsql.WHEREClause = "g.accountinstance_id = ai.accountinstance_id\r\n\
    AND br.kode_cabang = ai.branch_code\r\n\
    AND (ai.account_code=%(account_code)s)(1 = %(noprefix)%d OR br.kode_cabang LIKE %(prefix)s)" \
    % {'account_code': mlu.QuotedStr(fr.account_code), 'noprefix': noprefix, 'prefix': sPrefix}
  rqsql.GROUPBYClause = "GROUP BY br.kode_cabang, br.nama_cabang"
  rqsql.setAltOrderFieldNames("kode_cabang;nama_cabang")
  rqsql.keyFieldName = "kode_cabang"
  rqsql.setBaseOrderFieldNames("kode_cabang")
  rqsql.initOperation(returns)
#--
  