import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def FormOnSetDataEx(uideflist, params):
  config = uideflist.config 
  def GetValue(code, period, branches, isrp):
    if code=="()":
      return None
    code = eval(code)
    wClause = '('
    for i in range(len(code)):
      if i>0: 
        wClause+= " or "
      wClause+= "account_code like '%s" % (code[i])
      wClause+= "%'"
    wClause+= ') and branch_code in (%s)' % branches
    if isrp==1:
      wClause+= " and currency_code = 'IDR'"
    else:
      wClause+= " and currency_code <> 'IDR'"
    s = '''
       select sum(balancecumulative) "value" from table(%s(to_date('%s', 'dd-mm-yyyy')))
       where %s
    ''' % (config.MapDBTableName('core.getdailybalanceat'), period, wClause)
    #raise Exception, s
    value = config.CreateSQL(s).RawResult.value
    #raise Exception, value
    return value
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  form_loaditem.setData(uideflist, params)
  if uideflist.uipData.Dataset.RecordCount==0:
    coaMapX = {
      '100':'''('101000000010','101000000020','101000000030','101000000040','101000000050','101000000060',)''',
      '120':'''('102010000001','102010000002','102010000003','102020000001','102030000001','102040000009',)''',
      '130':'''('103010100010','103010200010','103020100010','103020200010','103030100010','103030200010',
              '103030300039','103050110010','103050110020','103050110039','103050120010','103050120020',
              '103050120039','103050130010','103050130020','103050130039','103050210010','103050210020',
              '103050210039','103050220010','103050220020','103050220039','103050230010','103050230020',
              '103050230039','103060100010','103060400010','103060500039',)''',
      '135':'''()''',
      '140':'''('105010200010','105010400010','105010400020','105010500010','105010500020','105010600010',
              '105010600020','105010800010','105010800020','105010800030','105020100010','105020100020',
              '105020600003','105020600004',)''',
      '145':'''()''',
      '148':'''('107030000039',)''',
      '150':'''('108010110001','108010110011','108010120001','108010120011','108010130001','108010130011',
              '108010210001','108010210011','108010220001','108010220011','108010230001','108010230011',
              '108010300001','108010300011',)''',
      '151':'''('108020110001','108020110011','108020120001','108020120011','108020130001','108020130011',
              '108020210001','108020210011','108020220001','108020220011','108020230001','108020230011',
              '108020300001','108020300011','108020300026',)''',
      '152':'''('114000000000', )''',
      '153':'''('108030110001','108030110011','108030120001','108030120011','108030130001','108030130011',
              '108030210001','108030210011','108030220001','108030220011','108030230001','108030230011',
              '108030300001','108030300011',)''',
      '154':'''('108040110001','108040110011','108040120001','108040120011','108040130001','108040130011',
              '108040210001','108040210011','108040220001','108040220011','108040230001','108040230011',
              '108040300001','108040300011',)''',
      '159':'''('108050110001','108050110011','108050120001','108050120011','108050130001','108050130011',
              '108050210001','108050210011','108050220001','108050220011','108050230001','108050230011',
              '108050300001','108050300011',)''',
      '160':'''('109010000000', '109010100000', '109010110000', '109010110001', '109010110011', '109010120000', 
                '109010120001', '109010120011', '109010130000', '109010130001', '109010130001', '109010130001', 
                '109010130001', '109010130001', '109010130011', '109010130011', '109010130011', '109010130011', 
                '109010130011', '109010200000', '109010210000', '109010210001', '109010210011', '109010220000', 
                '109010220001', '109010220011', '109010230000', '109010230001', '109010230011', '109010240000', 
                '109010300000', '109010310000', '109010310001', '109010310011', '109010320000', '109010320001', 
                '109010320011', '109010330000', '109010330001', '109010330011', '109010340000', )''',
      '161':'''('109020000000', '109020100000', '109020110000', '109020110001', '109020110011', 
                '109020120000', '109020120001', '109020120011', '109020130000', '109020130001', 
                '109020130011', '109020200000', '109020210000', '109020210001', '109020210011', 
                '109020220000', '109020220001', '109020220011', '109020230000', '109020230001', 
                '109020230001', '109020230001', '109020230011', '109020230011', '109020230011', 
                '109020300000', '109020310000', '109020310001', '109020310011', '109020320000', 
                '109020320001', '109020320011', '109020330000', '109020330001', '109020330011', 
                '109020340000',)''',
      '169':'''('109030000000', '109030100000', '109030110000', '109030110001', '109030110011', 
                '109030120000', '109030120001', '109030120011', '109030130000', '109030130001', 
                '109030130011', '109030200000', '109030210000', '109030210001', '109030210011', 
                '109030220000', '109030220001', '109030220011', '109030230000', '109030230001', 
                '109030230011', '109030300000', )''',
      '170':'''('109010110001','109010110011','109010120001','109010120011','109010130001','109010130011',
              '109010210001','109010210011','109010220001','109010220011','109010230001','109010230011',
              '109010310001','109010310011','109010320001','109010320011','109010330001','109010330011',)''',
      '171':'''('109020110001','109020110011','109020120001','109020120011','109020130001','109020130011',
              '109020210001','109020210011','109020220001','109020220011','109020230001','109020230011',
              '109020310001','109020310011','109020320001','109020320011','109020330001','109020330011',)''',
      '179':'''('109030110001','109030110011','109030120001','109030120011','109030130001','109030130011',
              '109030210001','109030210011','109030220001','109030220011','109030230001','109030230011',)''',
      '180':'''('110010100001','110010200001','110010300001','110010300002',)''',
      '185':'''('110020100001','110020200001','110020200002','110020300001','110020300002',)''',
      '186':'''('110030100001','110030100002','110030200001','110030200002',)''',
      '190':'''('104000000000', '106000000000', '107000000000', '107010000000', '107020000000', '107030000000', 
                '107030000039', '107030000039', )''',
      '200':'''('111030000039',)''',
      '205':'''('112020000000',)''',
      '207':'''('112020110001','112020110002','112020110003','112020110039','112020120001','112020120002',
              '112020120003','112020120039','112020210001','112020220001','112020310001','112020320001',
              '112020410001','112020420001','112020510001','112020510002','112020520001','112020520002',
              '112020530001','112020530002','112020540001','112020540002','112020610001','112020610002',
              '112020620001','112020620002','112020630001','112020630002','112020710001','112020720001',)''',
      '210':'''('113010100001','113010200001','113010300001','113010400001',)''',
      '211':'''('113020100001','113020200001','113020300001','113020400001',)''',
      '212':'''()''',
      '213':'''()''',
      '214':'''('115020100001','115020100002','115020100003','115020200009',)''',
      '215':'''('116010110001','116010120001','116010130001','116010210001','116010220001','116010230001',
              '116010230002','116010240001','116010250039',)''',
      '216':'''('116020110001','116020120001','116020210001','116020220001','116020230001','116020230002',
              '116020240001',)''',
      '217':'''('117010000001','117010000002','117010000003','117010000004','117010000005','117010000006',
              '117010000007','117020000001','117020000002','117020000003','117020000004','117020000005',
              '117020000006','117020000007','117030000001','117030000002','117030000003','117030000004',
              '117030000005','117030000006','117030000007',)''',
      '218':'''('118010400001','118020400001',)''',
      '219':'''('119000000001',)''',
      '223':'''('120010110001','120010120010','120010210010','120010220010','120010230010','120010500001',
              '120010500002','120010500003','120010500004','120020110010','120020110020',)''',
      '224':'''()''',
      '225':'''('121040000001',)''',
      '226':'''('122090000039',)''',
      '228':'''('123000000001',)''',
      '230':'''('113000000000', '113010000000', '113010100000', '113010100001', '113010200000', '113010200001', 
              '113010300000', '113010300001', '113010400000', '113010400001', '113020000000', '113020100000', 
              '113020100001', '113020200000', '113020200001', '113020300000', '113020300001', '113020400000', 
              '113020400001', '124010000001','124010000002','124020000001','124020000002','124030000001','124040000001',
              '124050000001','124060110001','124060110002','124060110003','124060110004','124060110006',
              '124060110015','124060120001','124060130001','124060130002','124060130003','124060130004',
              '124060130005','124060130006','124060130039','124070000001','124080100001','124080100002',
              '124080100003','124080100004','124080100005','124080100039','124080200001','124080200002',
              '124080200003','124080200004','124080200039','124080300001','124080300002','124080300003',
              '124080300004','124080300005','124080300006','124080300007','124080300008','124080300009',
              '124080300010','124080300039','124090000001','124090000002','124110100001','124110100002',
              '124110200001','124110200002','124110200003','124110200004','124110200005','124110200006',
              '124110200007','124110200015','124110200020','124110200021','124110200022','124110200023',
              '124110200024','124110200025','124110200026','124110200027','124110200028','124110200029',
              '124110200030','124110200031','124110200032','124110200033','124110200034','124110200035',
              '124110200036','124110200039','124110300001','124110300002','124110300003','124110300004',
              '124110300005','124110300006','124110300007','124110300008','124110300009','124110400001',
              '124110400002','124110400003','124110400004','124110400005','124110400006','124110400007',
              '124110400008','124110400009','124110400010','124110400011','124110400012','124110400013',
              '124110400014','124110400015','124110400039','124110500001','124110500002','124110500003',
              '124110500004','124110500039','124110600001','124110600002','124110600003','124110600004',
              '124110700001','124110700002','124110700003','124110700004','124110700039',)''',
      '290':'''()''',
      '301':'''('201010000001','201010000002',)''',
      '302':'''('201020000001',)''',
      '309':'''()''',
      '320':'''('202010000001',)''',
      '321':'''('202020000001',)''',
      '322':'''('202030100001','202030100002','202030100003','202030100004','202030100005','202030100006',
              '202030200001','202030200002','202030200003','202030200004','202030200005','202030200006',)''',
      '329':'''()''',
      '340':'''('203010000001','203020100001','203020100002','203020200001','203020200002','203030000001',
              '203040000001','203050000039',)''',
      '350':'''('204010000001','204010000002','204020000001','204020000002','204030000001','204030000002',
              '204030000003','204030000004','204030000005','204030000006','204030000007','204060000001',
              '204060000002','204060000039',)''',
      '351':'''()''',
      '353':'''()''',
      '355':'''('206010100010','206010200010','206010300010','206010400039','206020100001','206020100002',
              '206020200001','206020200002','206020400010','206020400039',)''',
      '360':'''('208010600039',)''',
      '365':'''('205000000000', '207000000000', '207010000000', '207020000000', '207020000001',
                '207030000000', )''',
      '368':'''('208020000000', '208020100000', '208020200000', '208030000000', '208030100000', 
                '208030200000', )''',
      '370':'''('209010000001','209010000002','209010000003','209010000039','209020000001','209030000002',
              '209040000002','209050000002','209070000039',)''',
      '393':'''('210010110001','210010120001','210010210001','210010220001','210010230001','210010700001',
              '210010700002','210010700003','210010700039',)''',
      '394':'''()''',
      '396':'''('212010000001','212010000002','212010000003','212010000004','212010000005','212010000006',
              '212010000007','212010000008','212010000009','212010000013','212010000039',)''',
      '400':'''('212020000001','212020000002','212020000003','212020000004','212020000005','212030000001',
              '212030000002','212030000003','212030000004','212030000005','212030000006','212030000007',
              '212040000001','212060000001','212070220001','212070220002','212070220003','212070220039',
              '212080000001','212130000001','212190100001','212190100002','212190100003','212190100004',
              '212190200001','212190200003','212190200004','212190200005','212190200039','212190300001',
              '212190300002','212190300003','212190300004','212190300005','212190300006','212190300007',
              '212190300008','212190300009','212190300039','212190400001','212190400002','212190510001',
              '212190520001','212190600001','212190600002','212190600003','212190700001','212190700002',
              '212190700003','212190700004','212190700005','212190700006','212190700007','212190700008',
              '212190700009','212190700010','212190700011','212190700012','212190700013','212190700014',
              '212190700015','212190700016','212190700017','212190700018','212190700019','212190700020',
              '212190700021','212190700022','212190700023','212190700024','212190700025','212190700026',
              '212190700027','212190700028','212190700029','212190700030','212190700031','212190700032',
              '212190700033','212190700034','212190700035','212190700036','212190700037','212190700038',
              '212190700039','212190700040','212190700049',)''',
      '401':'''()''',
      '402':'''()''',
      '403':'''()''',
      '404':'''()''',
      '405':'''()''',
      '406':'''()''',
      '410':'''()''',
      '421':'''('315010000001',)''',
      '422':'''('315020000001',)''',
      '423':'''('315030000001',)''',
      '431':'''('316010000001',)''',
      '432':'''('316020000001',)''',
      '433':'''('316030000001',)''',
      '434':'''('316040000001',)''',
      '436':'''('316050000001',)''',
      '437':'''('316050000002',)''',
      '438':'''()''',
      '439':'''()''',
      '441':'''()''',
      '442':'''()''',
      '445':'''('318000000001','318000000002',)''',
      '451':'''('319010000001',)''',
      '452':'''('319020000001',)''',
      '461':'''('320010100001',)''',
      '462':'''('320010200001',)''',
      '465':'''('320020100001',)''',
      '466':'''('320020200001',)''',
      '490':'''()''',
      '494':'''()''',
      '495':'''()''',
      '500':'''()''',
      '505':'''()''',
      '510':'''()''',
      '514':'''()''',
      '515':'''('910020100000', )''',
      '520':'''('910020200000', )''',
      '521':'''()''',
      '524':'''()''',
      '525':'''('910030100000', )''',
      '529':'''('910030200000', )''',
      '531':'''('505230600039','505230700001','505230700002','505230700003','505230700004','505230700005',
              '505230700006','505230700007','505230700008','505230700009','505230700010','505230700011',)''',
      '532':'''('505230700012','505230700013','505230700014','505230700015','505230700016','505230700017',
              '505230700018','505230700019','505230700020','505230700021','505230700022','505230700023',)''',
      '533':'''('505230700024','505230700025','505230700026','505230700027','505230700028','505230700029',
              '505230700030','505230700031','505230700032','505230700033','505230700034','505230700035',)''',
      '534':'''('505230700036','505230700037','505230700038','505230700039','505230700040','505230700041',
              '505230700042','505230700043','505230700044','407010000001','407010000002','407010000003',)''',
      '535':'''()''',
      '536':'''('920010111000', '920010111001', '920010111002', '920010111003', '920010111039', )''',
      '537':'''('920010112000', '920010112001', '920010112001', )''',
      '538':'''()''',
      '539':'''('920010113000', '920010113001', '920010113001', )''',
      '540':'''('920010210001', '920010210002', '920010210003', '920010210039', '920010210004', )''',
      '541':'''('407020000001',)''',
      '542':'''()''',
      '551':'''('407040000001','508010000001',)''',
      '552':'''()''',
      '543':'''('407040000002','508020000001','508030100002',)''',
      '544':'''('407040000003','407040000004',)''',
      '545':'''('407040000005','407040000006',)''',
      '549':'''('407040000007','407040000039',)''',
      '553':'''('508030100001',)''',
      '554':'''('508030100039','508030200001',)''',
      '559':'''('508030200002','508030200003',)''',
      '561':'''()''',
      '562':'''()''',
      '569':'''()''',
      '571':'''()''',
      '575':'''()''',
      '576':'''()''',
      '579':'''()''',
      '580':'''()''',
      '585':'''()''',
      '591':'''('930010000001',)''',
      '592':'''('930020130001', '930020130001', )''',
      '594':'''('930020150001', '930020150002', '930020140001', '930020140001', '930020140001', '930020140001', 
                '930020140001', '930020140001', '930020140002', '930020140002', '930020140002', '930020140002', 
                '930020120001', '930020110001', '930020110001', )''',
      '595':'''('930020230001', '930020210001', )''',
      '597':'''('930020250001', '930020250002', '930020240001', '930020240002', '930020220001', '930020210001', )''',
      '598':'''()''',
      '599':'''('940010100001', '940010200001',)''',
      '601':'''()''',
      '609':'''()''',
      '611':'''('508030200006','508030200007','508030200039','513010000001',)''',
      '619':'''('513020100001',)''',
      '621':'''()''',
      '625':'''('950010110001', '950010110002', '950010110003', '950010110004', '950010120001', )''',
      '627':'''()''',
      '629':'''('960000000001', )''',
      '632':'''()''',
      '633':'''()''',
      '635':'''('513020200001',)''',
    }
    coaMap = {
      "100" : '''('101000000010', '101000000020', '101000000030', '101000000040', '101000000050', '101000000060',)''',
      "120" : '''('102010000001', '102010000002', '102010000003', '102020000001', '102030000001', '102040000009',)''',
      "130" : '''('103010100010', '103010200010', '103020100010', '103020200010', '103030100010', '103030200010', 
                  '103030300039', '103060400010', '105010800010', '103060100010',)''',
      "140" : '''('105010800020', '105010800030', '105020100010', '105020100020', '105020600003', '105020600004', 
                  '103060500039', '105010200010', '105010400010', '105010400020', '105010500010', '105010500020', 
                  '105010600010', '105010600020', '103050110010', '103050110020', '103050110039', '103050120010', 
                  '103050120020', '103050120039', '103050130010', '103050130020', '103050130039', '103050210010', 
                  '103050210020', '103050210039', '103050220010', '103050220020', '103050220039', '103050230010', 
                  '103050230020', '103050230039',)''',
      "150" : '''('108010110001', '108010110011', '108010120001', '108010120011', '108010130001', '108010130011', 
                  '108010210001', '108010210011', '108010220001', '108010220011', '108010230001', '108010230011', 
                  '108010300001', '108010300002', '108010300004', '108010300005', '108010300019', '108010300020', 
                  '108010300021', '108010300022', '108010300024', '108010300025', '108010300026', '108010300029', 
                  '108010300030',)''',
      "151" : '''('108020110001', '108020110011', '108020120001', '108020120011', '108020130001', '108020130011', 
                  '108020210001', '108020210011', '108020220001', '108020220011', '108020230001', '108020230011', 
                  '108020300001', '108020300002', '108020300003', '108020300004', '108020300005', '108020300006', 
                  '108020300021', '108020300022', '108020300023', '108020300024', '108020300025', '108020300026',)''',
      "152" : '''()''',
      "153" : '''('108030110001', '108030110011', '108030120001', '108030120011', '108030130001', '108030130011', 
                  '108030210001', '108030210011', '108030220001', '108030220011', '108030230001', '108030230011', 
                  '108030300001', '108030300002', '108030300003', '108030300004', '108030300005', '108030300006', 
                  '108030300021', '108030300022', '108030300023', '108030300024', '108030300025', '108030300026',)''',
      "154" : '''('108040110001', '108040110011', '108040120001', '108040120011', '108040130001', '108040130011', 
                  '108040210001', '108040210011', '108040220001', '108040220011', '108040230001', '108040230011', 
                  '108040300001', '108040300002', '108040300003', '108040300004', '108040300005', '108040300021', 
                  '108040300022', '108040300023', '108040300024', '108040300025', '108040300026',)''',
      "159" : '''('108050110001', '108050110011', '108050120001', '108050120011', '108050130001', '108050130011', 
                  '108050210001', '108050210011', '108050220001', '108050220011', '108050230001', '108050230011', 
                  '108050300001', '108050300002', '108050300003', '108050300004', '108050300005', '108050300006', 
                  '108050300021', '108050300022', '108050300023', '108050300024', '108050300025', '108050300026',)''',
      "160" : '''('109010110001', '109010110011', '109010120001', '109010120011', '109010130001', '109010130011', 
                  '109010210001', '109010210011', '109010220001', '109010220011', '109010230001', '109010230011', 
                  '109010310001', '109010310011', '109010320001', '109010320011', '109010330001', '109010330011',)''',
      "161" : '''('109020110001', '109020110011', '109020120001', '109020120011', '109020130001', '109020130011', 
                  '109020210001', '109020210011', '109020220001', '109020220011', '109020230001', '109020230011', 
                  '109020310001', '109020310011', '109020320001', '109020320011', '109020330001', '109020330011',)''',
      "169" : '''('109030110001', '109030110011', '109030120001', '109030120011', '109030130001', '109030130011', 
                  '109030210001', '109030210011', '109030220001', '109030220011', '109030230001', '109030230011',)''',
      "170" : '''('122090000039',)''',
      "180" : '''('110010100001', '110010200001', '110010300001', '110010300002',)''',
      "185" : '''('110020100001', '110020200001', '110020200002', '110020300001', '110020300002',)''',
      "190" : '''('107030000039',)''',
      "200" : '''('111030000039',)''',
      "205" : '''('112010110001', '112010110002', '112010110003', '112010110039', '112010210001', '112010310001', 
                  '112010410001', '112010510001', '112010520001', '112010530001', '112010540001', '112010610001', 
                  '112010620001', '112010630001', '112010710001', '112020110001', '112020110002', '112020110003', 
                  '112020110039', '112020210001', '112020310001', '112020410001', '112020510001', '112020520001', 
                  '112020530001', '112020540001', '112020610001', '112020710001', '110030100001', '110030100002', 
                  '121040000001', '112020620001', '112020630001',)''',
      "207" : '''('112020630002', '112020620002', '110030200001', '110030200002', '112020720001', '112020610002', 
                  '112020540002', '112020530002', '112020520002', '112020510002', '112020420001', '112020320001', 
                  '112020220001', '112020120001', '112020120002', '112020120003', '112020120039', '112010720001', 
                  '112010630002', '112010620002', '112010610002', '112010540002', '112010530002', '112010520002', 
                  '112010510002', '112010420001', '112010320001', '112010220001', '112010120001', '112010120002', 
                  '112010120003', '112010120039',)''',
      "210" : '''()''',
      "211" : '''('115020100001', '115020100002', '115020100003', '115020200009',)''',
      "213" : '''('116010110001', '116010120001', '116010130001',)''',
      "214" : '''('116020110001', '116020120001',)''',
      "215" : '''('116010210001', '116010220001', '116010230001', '116010230002', '116010240001', '116010250039',)''',
      "216" : '''('116020210001', '116020220001', '116020230001', '116020230002', '116020240001',)''',
      "223" : '''('120010110001', '120010120010', '120010210010', '120010220010', '120010230010', '120010500001', 
                  '120010500002', '120010500003', '120010500004',)''',
      "224" : '''('120020110010', '120020110020',)''',
      "230" : '''('123000000001', '124010000001', '124010000002', '124020000001', '124020000002', '124030000001', 
                  '124040000001', '124050000001', '124060110001', '124060110002', '124060110003', '124060110004', 
                  '124060110006', '124060110015', '124060120001', '124060130001', '124060130002', '124060130003', 
                  '124060130004', '124060130006', '124060130039', '124070000001', '124080100001', '124080100002', 
                  '124080100003', '124080100004', '124080100005', '124080100039', '124080200001', '124080200002', 
                  '124080200003', '124080200004', '124080200039', '124080300001', '124080300002', '124080300003', 
                  '124080300004', '124080300005', '124080300006', '124080300007', '124080300008', '124080300009', 
                  '124080300010', '124080300039', '124090000001', '124090000002', '124110100001', '124110100002', 
                  '124110200001', '124110200002', '124110200003', '124110200004', '124110200005', '124110200006', 
                  '124110200007', '124110200015', '124110200020', '124110200021', '124110200022', '124110200023', 
                  '124110200024', '124110200025', '124110200026', '124110200027', '124110200028', '124110200029', 
                  '124110200030', '124110200031', '124110200032', '124110200033', '124110200034', '124110200035', 
                  '124110200036', '124110200039', '124110300001', '124110300002', '124110300003', '124110300004', 
                  '124110300005', '124110300006', '124110300007', '124110300008', '124110300009', '124110400001', 
                  '124110400002', '124110400003', '124110400004', '124110400005', '124110400006', '124110400007', 
                  '124110400008', '124110400009', '124110400010', '124110400011', '124110400012', '124110400013', 
                  '124110400014', '124110400015', '124110400039', '124110500001', '124110500002', '124110500003', 
                  '124110500004', '124110500039', '124110600001', '124110600002', '124110600003', '124110600004', 
                  '124110700001', '124110700002', '124110700003', '124110700004', '124110700039', '117010000001', 
                  '117010000002', '117010000003', '117010000004', '117010000005', '117010000006', '117010000007', 
                  '117020000001', '117020000002', '117020000003', '117020000004', '117020000005', '117020000006', 
                  '117020000007', '118010400001', '118020400001', '119000000001', '113010100001', '113010200001', 
                  '113010300001', '113010400001', '113020100001', '113020200001', '113020300001', '113020400001',)''',
      "290" : '''('103060130005', '320010200001',)''',
      "301" : '''('201010000001', '201010000002',)''',
      "302" : '''('201020000001',)''',
      "309" : '''()''',
      "321" : '''('202020000001',)''',
      "322" : '''('202030100001', '202030100002', '202030100003', '202030100004', '202030100005', '202030100006', 
                  '202030200001', '202030200002', '202030200003', '202030200004', '202030200005', '202030200006',)''',
      "329" : '''('202010000001',)''',
      "340" : '''('203010000001', '203020100001', '203020100002', '203020200001', '203020200002', '203030000001', 
                  '203040000001', '203050000039',)''',
      "350" : '''('204010000001', '204010000002', '204020000001', '204020000002', '204030000001', '204030000002', 
                  '204030000003', '204030000004', '204030000005', '204030000006', '204030000007', '204060000001', 
                  
                  '204060000002', '204060000039', '206010100010',)''',
      "355" : '''('206010200010', '206010300010', '206010400039', '206020100001', '206020100002', '206020200001', 
                  '206020200002', '206020400010', '206020400039',)''',
      "360" : '''('208010600039',)''',
      "365" : '''('207020000001', '212190700028', '212190700029', '212190700030', '212190700031', '212190700032', 
                  '212190700033', '212190700034', '212190700035', '212190700036', '212190700037', '212190700038', 
                  '212190700039', '212190700040', '212190700049', '212080000001', '212030000001', '212030000002', 
                  '212030000003', '212030000004', '212030000005', '212030000006', '212030000007', '212010000001', 
                  '212010000002', '212010000003', '212010000004', '212010000005', '212010000006', '212010000007', 
                  '212010000008', '212010000009', '212010000013', '212010000039', '212190200001', '212190200002', 
                  '212190200004', '212190200005', '212190200006', '212190200007', '212190200008', '212190200009', 
                  '212190200039',)''',
      "368" : '''()''',
      "370" : '''('209010000001', '209010000002', '209010000003', '209010000039', '209020000001', '209030000002', 
                  '209040000002', '209050000002', '209070000039',)''',
      "393" : '''('210010110001', '210010120001', '210010210001', '210010220001', '210010230001', '210010700001', 
                  '210010700002', '210010700003', '210010700039',)''',
      "394" : '''()''',
      "400" : '''('212190300001', '212190300002', '212190300003', '212190300004', '212190300005', '212190300006', 
                  '212190300007', '212190300008', '212190300009', '212190300039', '212190400001', '212190400002', 
                  '212190510001', '212190520001', '212190600001', '212190600002', '212190600003', '212190700001', 
                  '212190700002', '212190700003', '212190700004', '212190700005', '212190700006', '212190700007', 
                  '212190700008', '212190700009', '212190700010', '212190700011', '212190700012', '212190700013', 
                  '212190700014', '212190700015', '212190700016', '212190700017', '212190700018', '212190700019', 
                  '212190700020', '212190700021', '212190700022', '212190700023', '212190700024', '212190700025', 
                  '212190700026', '212020000001', '212020000002', '212020000003', '212020000004', '212020000005', 
                  '212040000001', '212060000001', '212070220001', '212070220002', '212070220003', '212070220039', 
                  '212130000001', '212190100001', '212190100002', '212190100003', '212190100004',)''',
      "410" : '''()''',
      "421" : '''('315010000001',)''',
      "422" : '''('315020000001', '315030000001',)''',
      "431" : '''('316010000001',)''',
      "432" : '''('316020000001',)''',
      "433" : '''('316030000001',)''',
      "434" : '''('316040000001',)''',
      "436" : '''('316050000001',)''',
      "437" : '''('316050000002',)''',
      "445" : '''('318000000001', '318000000002',)''',
      "451" : '''('319010000001',)''',
      "452" : '''('319020000001',)''',
      "461" : '''('320010100001',)''',
      "462" : '''('320010100001',)''',
      "465" : '''('320020100001',)''',
      "466" : '''('320020100001',)''',
      "490" : '''('320010200001', '103060130005',)''',

      "536" : '''('920010111001', '920010111002', '920010111003', '920010111039',)''',
      "537" : '''('920010112001',)''',
      "531" : '''('920010113001',)''',
      "540" : '''('920010211001', '920010211002', '920010211003', '920010211004', '920010211039',)''',
      "591" : '''('930010000001',)''',
      "597" : '''('930020110001', '930020120001', '930020130001', '930020140001', '930020140002', 
                  '930020150001', '930020150002', '930020210001', '930020220001', '930020230001', 
                  '930020240001', '930020240002', '930020250001', '930020250002',)''',
      "599" : '''('940010100001', '940010200001',)''',
      "609" : '''('950010110001', '950010110002', '950010110003', '950010110004',)''',
      "627" : '''('950010120001',)''',
      "629" : '''('960000000001',)''',
    }
    mlu = config.ModLibUtils
    s = '''
      select kode_cabang from branchmember where branch_id=%s
    ''' % (str(params.FirstRecord.branch_id))
    branchmembers = config.CreateSQL(s).RawResult
    listcabang = ''
    while not branchmembers.Eof:
      if listcabang != '':
        listcabang+=', '
      listcabang+=mlu.QuotedStr(branchmembers.kode_cabang)
      branchmembers.Next()
    pid = params.FirstRecord.period_id
    pCode = config.CreateSQL("select period_code from period where period_id=%s" % pid).RawResult.period_code
    tgl = 1
    bln = int(pCode[:2])
    thn = int(pCode[2:6])
    if bln<12:
      repdate = mlu.EncodeDate(thn, bln+1, tgl)
    else:
      repdate = mlu.EncodeDate(thn+1, 1, tgl)
    repdate = repdate-1
    (thn, bln, tgl) = mlu.DecodeDate(repdate)  
    period = "%s-%s-%s" % (str(tgl),str(bln),str(thn))
    ds = uideflist.uipData.Dataset
    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_POS_NERACA_LBU' order by a.refdata_id" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    #raise Exception, config.CreateSQL('select max(reference_code) vals from (%s)' % s).RawResult.vals
    r290 = 0
    r490 = 0
    v290 = 0
    v490 = 0
    while not res.Eof:
      if res.reference_code in coaMap.keys(): 
        value = GetValue(coaMap[res.reference_code], period, listcabang, 1)
      else:
        value = None
      if value not in (None,'',0):
        #if value<0: value=value*-1
        rp = int(value/100000)
        if int(str(rp)[-1])>4:
          if rp<0:
            rp = (rp/10)
          else:
            rp = (rp/10)+1
        else:
          if rp<0:
            rp = (rp/10)+1
          else:
            rp = rp/10
      else:
        rp = 0
      if res.reference_code in coaMap.keys(): 
        value = GetValue(coaMap[res.reference_code], period, listcabang, 0)
      else:
        value = None
      if value not in (None,'',0):
        #if value<0: value=value*-1
        valas = int(value/1000000)
        if int(str(valas)[-1])>4:
          if valas<0:
            valas = valas/10
          else:
            valas = (valas/10)+1
        else:
          if valas<0:
            valas = (valas/10)+1
          else:
            valas = valas/10
      else:
        valas = 0
      if res.reference_code=='290':
        rp = r290
        valas = v290
      if res.reference_code=='490':
        rp = r490
        valas = v490
      #if rp==0 and valas==0 and res.reference_code not in ('290','490'):
      #  pass
      #else:
      rec = ds.AddRecord()
      rec.SetFieldByName('LPOS.reference_desc', res.reference_desc)    
      rec.SetFieldByName('LPOS.reference_code', res.reference_code)    
      rec.SetFieldByName('LPOS.refdata_id', res.refdata_id)
      if res.reference_code not in (None,'', ' '):
        kode = int(res.reference_code)
      else:
        kode = 0
      if kode>0 and kode<290:
        r290 += rp
        v290 += valas
      if kode>290 and kode<490 and kode not in (462,466):
        r490 +=rp 
        v490 += valas
      if kode==461 and rp<0:
        rp = 0
      if kode==462 and rp>0:
        rp = 0
      if kode==465 and rp<0:
        rp = 0
      if kode==466 and rp>0:
        rp = 0
      total = rp+valas
      if kode==445:
        sATr = rp
        sATv = valas
      if rp<0: rp=rp*-1
      if valas<0: valas=valas*-1
      if total<0: total=total*-1
      rec.SetFieldByName('Value1', str(rp))    
      rec.SetFieldByName('Value2', str(valas))    
      rec.SetFieldByName('Total', str(total))    
      res.Next()
    if (sATr<0) or (sATv<0):
      for i in range(ds.RecordCount):
        cek = ds.GetRecord(i)
        if cek.GetFieldByName('LPOS.reference_code')=='230':
          recnum230 = i
        if cek.GetFieldByName('LPOS.reference_code')=='445':
          recnum445 = i
        if cek.GetFieldByName('LPOS.reference_code')=='290':
          recnum290 = i
        if cek.GetFieldByName('LPOS.reference_code')=='490':
          recnum490 = i
    if sATr<0:
      upd = ds.GetRecord(recnum230)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATr*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATr*-1)))
      upd = ds.GetRecord(recnum290)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATr*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATr*-1)))
      upd = ds.GetRecord(recnum445)
      upd.SetFieldByName('Value1', '0')
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATr)))
      upd = ds.GetRecord(recnum490)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATr*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATr*-1)))
    if sATv<0:
      upd = ds.GetRecord(recnum230)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATv*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATv*-1)))
      upd = ds.GetRecord(recnum290)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATv*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATv*-1)))
      upd = ds.GetRecord(recnum445)
      upd.SetFieldByName('Value1', '0')
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATv)))
      upd = ds.GetRecord(recnum490)
      upd.SetFieldByName('Value1', str(int(upd.GetFieldByName('Value1'))+(sATv*-1)))
      upd.SetFieldByName('Total', str(int(upd.GetFieldByName('Total'))+(sATv*-1)))

















    #--
    
