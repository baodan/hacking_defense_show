import xlrd
from datetime import datetime
from app.models.device import Device, DevicePasswd
from app.models.datacenter import DataCenter, DCBuilding, DCRoom, Cabinet, CabinetU, NetArea
from app.models.contract import DeviceContract, ContractSecure
from tools.common_restful import com_gets, com_post, com_get, com_put, com_del
from app.database import db
from tools.encode import pc


def handle_cell(cell, column_num):
    cell_value = None
    if cell.ctype == 2:
        if column_num != 19:
            cell_value = str(int(cell.value))
    elif cell.ctype == 3:
        date_tuple = xlrd.xldate_as_tuple(cell.value, 0)
        cell_value = datetime(*date_tuple)
    else:
        cell_value = cell.value
    if column_num == 9 or column_num == 20:
        if cell.value == "是":
            cell_value = True
        elif cell.value == "否":
            cell_value = False
    return cell_value


def check_and_save(device_dict):
    device = device_dict
    print(device)
    # 获取数据库ID
    datacenter_name = device.get('datacneter_name')
    area_name = device.get('area_name')
    cabinet_sn = device.get('cabinet_sn')
    start_u = device.get('start_u')
    device_contract_order = device.get('device_contract_order')
    secure_contract_orders = device.get('secure_contract_orders')
    device['secure_contracts'] = []
    passwords = device.get('passwords')
    pop_list = ['datacenter_name', 'area_name', 'cabinet_sn', 'start_u',
                'device_contract_order', 'secure_contract_orders', 'passwords']
    if cabinet_sn:
        cabinet = Cabinet.query.filter_by(cabinet_sn=cabinet_sn).one_or_none()
        if not cabinet:
            print('找不到指定的机柜')
            raise Exception("找不到指定的机柜")
        if datacenter_name:
            datacenter = cabinet.room.building.datacenter
            if datacenter.datacenter_name != datacenter_name:
                print("+" * 100, "\n", datacenter.datacenter_name)
                print('指定机柜不在指定的数据中心内')
                raise Exception("指定机柜不在指定的数据中心内")
            else:
                device['datacenter_id'] = datacenter.id
        if start_u:
            start_u = cabinet.u_ids.filter_by(up=start_u).one_or_none()
            if not start_u:
                print('没有指定的起始U位')
                raise Exception('没有指定的起始U位')
            device['start_u_id'] = start_u.id
    else:
        if datacenter_name:
            datacenter = DataCenter.query.filter_by(datacenter_name=datacenter_name).one_or_none()
            print("*"*100, "\n", datacenter.datacenter_name)
            if not datacenter:
                print('不存在指定的数据中心')
                raise Exception("不存在指定的数据中心")
            device['datacenter_id'] = datacenter.id
        if area_name:
            net_area = NetArea.query.filter_by(area_name=area_name).one_or_none()
            if not net_area:
                print('不存在指定的网络区域')
                raise Exception("不存在指定的网络区域")
    if device_contract_order:
        print(device_contract_order)
        contract = DeviceContract.query.filter_by(contract_order=device_contract_order).one_or_none()
        if not contract:
            print("不存在设备合同：%s" % device_contract_order)
            raise Exception("不存在设备合同：%s" % device_contract_order)
        device['device_contract_id'] = contract.id

    # 将所需要维保合同对象添加到字典中
    for secure_order in secure_contract_orders:
        contract = ContractSecure.query.filter_by(contract_order=secure_order).one_or_none()
        if not contract:
            print("不存在设备合同：%s" % secure_order)
            raise Exception("不存在设备合同：%s" % secure_order)
        device['secure_contracts'].append(contract)
    # print(device)
    # 删除创建设备数据库对象不需要的字段
    res_dict = {}
    for key in device.keys():
        print('1', key)
        if key not in pop_list:
            print('2', key)
            res_dict[key] = device[key]
    print(res_dict)
    device_db = Device(**res_dict)
    db.session.add(device_db)
    # 创建密码表记录
    for password in passwords:
        password['device'] = device_db
        passwd_db = DevicePasswd(**password)
        db.session.add(passwd_db)








def import_from_xls():
    filename = "doc\devices.xlsx"
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    device_headers = ['sn', 'mac', 'device_name', 'device_type', 'device_model', 'device_origin',
                      'manager_mode', 'device_charger', 'app', 'is_case', 'case_id',
                      'device_create_time', 'device_destory_time', 'vendor', 'datacenter_name',
                      'area_name', 'device_contract_order', 'cabinet_sn', 'start_u', 'u_high',
                      'is_active', 'remark', 'secure_contract_orders']
    password_headers = ['username', 'password']
    tmp_device_dict = {}
    tmp_password_dict = {}
    device_list = []
    for row_num in range(1, table.nrows):
        columns = table.row(row_num)
        if columns[0].value:
            device_info = []
            password_info = []
            for column_num in range(len(columns)):
                cell_value = handle_cell(columns[column_num], column_num)
                if column_num <= 21:
                    device_info.append(cell_value)
                elif column_num == 22:
                    secure = [cell_value]
                    device_info.append(secure)
                else:
                    password_info.append(pc.encrypt(cell_value))
            tmp_device_dict = dict(zip(device_headers, device_info))
            tmp_password_dict = dict(zip(password_headers, password_info))
            tmp_device_dict['passwords'] = [tmp_password_dict]
            device_list.append(tmp_device_dict)
        else:
            password_info = []
            for column_num in range(21, len(columns)):
                cell_value = handle_cell(columns[column_num], column_num)
                if column_num == 21:
                    tmp_device_dict['secure_contract_orders'].append(cell_value)
                else:
                    password_info.append(cell_value)
                tmp_password_dict = dict(zip(password_headers, password_info))
                tmp_device_dict['passwords'] = [tmp_password_dict]
    for device in device_list:
        check_and_save(device)
        # try:
        #     check_and_save(device)
        #     db.session.commit()
        # except Exception as e:
        #     print("设备信息有误%s" % device['sn'])


        # 使用字典创建数据库对象
    #     device_db = Device(**device_dict)
    #     password_dict['device'] = device_db
    #     pass_db = DevicePasswd(**password_dict)
    #     db.session.add_all([device_db, pass_db])
    # db.session.commit()


def import_from_xls_old(filename):
    # 没有做U位

    filename = "doc\devices.xlsx"
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    device_headers = ['sn', 'device_name', 'device_type', 'device_model', 'device_origin',
                      'manager_mode', 'device_charger', 'app', 'is_case', 'case_id',
                      'device_create_time', 'device_destory_time', 'vendor', 'datacenter_id',
                      'net_area_id', 'device_contract_id', 'start_u_id', 'u_high',
                      'is_active', 'remark', 'secure_contracts']
    password_headers = ['username', 'password']
    for row_num in range(1, table.nrows):
        columns = table.row(row_num)
        device_info = []
        password_info = []
        for column_num in range(len(columns)):
            cell_value = None
            cell = columns[column_num]
            if cell.ctype == 2:
                if column_num != 18:
                    cell_value = str(int(cell.value))
            elif cell.ctype == 3:
                date_tuple = xlrd.xldate_as_tuple(cell.value, 0)
                cell_value = datetime(*date_tuple)
            else:
                cell_value = cell.value
            if column_num == 8 or column_num == 20:
                if cell.value == "是":
                    cell_value = True
                elif cell.value == "否":
                    cell_value = False
            if column_num <= 21:
                device_info.append(cell_value)
            else:
                password_info.append(cell_value)
        device_dict = dict(zip(device_headers, device_info))
        password_dict = dict(zip(password_headers, password_info))
        print(device_dict)
        print(password_dict)

        # 使用字典创建数据库对象
    #     device_db = Device(**device_dict)
    #     password_dict['device'] = device_db
    #     pass_db = DevicePasswd(**password_dict)
    #     db.session.add_all([device_db, pass_db])
    # db.session.commit()


