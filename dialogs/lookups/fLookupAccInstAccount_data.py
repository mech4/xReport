import os
import sys
import com.ihsan.lib.remotequery as remotequery
import com.ihsan.lib.

def runQuery(config, params, returns):
  rqsql = remotequery.RQSQL(config)
  rqsql.handleOperation(params, returns)
#--

def initQuery(config, params, returns):
  mlu = config.ModLibUtils
  rqsql = remotequery.RQSQL(config)
  rqsql.SELECTFROMClause = "SELECT\r\n\
    acc.account_code, acc.account_name \
    acc.account_type FROM GLAccount g,\r\n\
    AccountInstance ai,\r\n\
    Account acc\r\n"
  fr = params.FirstRecord
  if fr.prefix == "":
    noprefix = 1
  else:
    noprefix = 0
  sPrefix = mlu.QuotedStr(fr.prefix + "%")
  rqsql.WHEREClause = "g.accountinstance_id = ai.accountinstance_id\r\n\
    AND acc.account_code = ai.account_code\r\n\
    AND 1 = %(noprefix)%d OR acc.account_code LIKE %(prefix)s " % {'noprefix': noprefix, 'prefix': sPrefix}
  rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
  rqsql.setAltOrderFieldNames("account_code;account_name;account_type")
  rqsql.keyFieldName = "account_code"
  rqsql.setBaseOrderFieldNames("account_code")
  rqsql.initOperation(returns)
#--
  