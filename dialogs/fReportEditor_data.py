import com.ihsan.foundation.pobjecthelper as phelper
import com.ihsan.labs.excel as excel
import sys

def PreparingSchedule(config, parameter, returns):
    # config: ISysConfig object
    # parameter: TPClassUIDataPacket
    # returnpacket: TPClassUIDataPacket (undefined structure)
    rec = parameter.FirstRecord

    status = returns.CreateValues(
        ['Is_Err', 0],
        ['Err_Message', '']
    )
    try:
        helper = phelper.PObjectHelper(config)
        account = helper.GetObject(
            'MurabahahAccount',
            rec.mlnop
        )

        sFileName = account.PreparingSchedule()

        sw = returns.AddStreamWrapper()
        sw.LoadFromFile(sFileName)
    except:
        status.Is_Err = 1
        status.Err_Message = str(sys.exc_info()[1])

    return 1

def InstallmentSave(config, parameter, returns):
    # config: ISysConfig object
    # parameter: TPClassUIDataPacket
    # returnpacket: TPClassUIDataPacket (undefined structure)
    rec = parameter.FirstRecord

    status = returns.CreateValues(
        ['Is_Err', 0],
        ['Err_Message', '']
    )
    try:
        helper = phelper.PObjectHelper(config)
        account = helper.GetObject(
            'MurabahahAccount',
            rec.mlnop
        )

        #rpdb2.start_embedded_debugger('solusi')
        if parameter.StreamWrapperCount > 0:
            sw = parameter.GetStreamWrapper(0)
        else:
            raise Exception, 'PERINGATAN!. Download stream not found'

        corporate = helper.CreateObject('Corporate')
        hfilename = '%s/schedule_murabahah.xls' % corporate.GetUserHomeDir()
        sw.SaveToFile(hfilename)

        owb = excel.Workbook(hfilename)
        try:
            account.ProcessSchedule(owb)
        finally:
            owb.CloseBook()

    except:
        status.Is_Err = 1
        status.Err_Message = str(sys.exc_info()[1])

    return 1

