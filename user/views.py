import json
from datetime import datetime
import random
import math
import time

import os
from django.shortcuts import render, redirect
import cx_Oracle
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# 获取数据库的数据
from Supp_project import settings

tnsname = cx_Oracle.makedsn('192.168.40.141', '1521', 'his')
ora = cx_Oracle.connect('system', '1', tnsname)
cursor = ora.cursor()


def get_data(sql):
    conn = cx_Oracle.connect('system/1@192.168.40.141/his')
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()  # 搜取所有结果
    # cur.close()
    # conn.close()
    return results


# 登录
@csrf_exempt
def sign_in(request):
    if request.method == 'GET':
        name = request.GET.get('username')
        password = request.GET.get('password')
    sql = " select * from exp_supplier_catalog where INPUT_CODE='" + name + "'and PASSWORD = '" + password + "'"
    m_data = get_data(sql)
    if m_data:
        supplier_code = m_data[0][23]
        print('supplier_code----------',supplier_code)
        return JsonResponse({"code": 0, "message": "登录成功", "data": {'supplier_code': supplier_code}})
    else:
        return JsonResponse({"code": -1, "message": "登录失败"})


# 中标
@csrf_exempt
def zb_info(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    sql = "select * from comm.exp_supplier_type where SUPPLIER_CODE= '" + supplier_code + "'"
    m_data = get_data(sql)
    # print('1111111',sql)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict['supplier_code'] = i[0]
        json_dict['contract_num'] = i[1]
        json_dict['winning_type'] = i[2]
        json_dict['winning_date'] = timeFormat(i[3])
        json_dict['supply_end_date'] = timeFormat(i[4])
        json_dict['state'] = stateStr(i[5])
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 基本信息form 改过
@csrf_exempt
def jbxx_info(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    sql = " select * from exp_supplier_catalog where SUPPLIER_CODE='" + supplier_code + "'"
    m_data = get_data(sql)
    json_dict = {}
    for i in m_data:
        json_dict["memo"] = i[3]  # 备注
        json_dict["input_code"] = i[4]  # 拼音码
        json_dict["supplier_addres"] = i[7]  # 地址
        json_dict["supplier_postalcode"] = i[8]  # 邮编
        json_dict["artificial_person"] = i[9]  # 法人
        json_dict["supplier_code"] = i[23]
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_dict})


# 基本信息table
@csrf_exempt
def test_api(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    sql = "select * from comm.exp_supplier_cert where SUPPLIER_CODE='" + supplier_code + "'"
    m_data = get_data(sql)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict["id"] = i[0]
        json_dict["serial_no"] = i[1]
        json_dict["supplier_code"] = i[2]
        json_dict["cert_name"] = i[3]
        json_dict["cert_code"] = i[4]
        json_dict["regist_cert_auth"] = i[8]
        json_dict["cert_expire_date"] = timeFormat(i[9])
        json_dict["cert_status"] = certStateStr(i[10])
        json_dict["cert_picture_path"] = i[11]
        # print('dssd', i[10])
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 基本信息_demo_edit
@csrf_exempt
def jbxx_edit(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'cert_expire_date':
                # print('json_list', type(request.POST.getlist(key)[0]))
                if request.POST.getlist(key)[0]:
                    json_list[key] = request.POST.getlist(key)[0].strip()
                    # print('json_list', type(json_list[key]))
                    # print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    # print('json_list', json_list)
    sql = "update comm.exp_supplier_cert set cert_name = '" \
          + json_list['cert_name'] + "', cert_code = '" + json_list['cert_code'] + "',cert_status = '" \
          + json_list['cert_status'] + "',regist_cert_auth = '" + json_list['regist_cert_auth'] \
          + "',cert_picture_path = '" + json_list['cert_picture_path'] \
          + "',cert_expire_date = to_date('"+ json_list['cert_expire_date'] +"', 'yyyy-mm-dd') where id = :id"

    # print('sql', sql)
    cursor.prepare(sql)
    cursor.execute(None, {'id': json_list['id']})
    ora.commit()
    cursor.execute('select * from comm.exp_supplier_cert')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
    # cursor.close()
    # ora.close()

    return JsonResponse({"result": 0, "msg": "执行成功"})


# 基本信息 新增
@csrf_exempt
def jbxx_add(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'cert_expire_date':
                # print('json_list', type(request.POST.getlist(key)[0]))
                if request.POST.getlist(key)[0]:
                    json_list[key] = datetime.strptime(request.POST.getlist(key)[0].strip(), '%Y-%m-%d')
                    # print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    # print('json_list', json_list)
    cursor.execute('insert into comm.exp_supplier_cert values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)', ('', 1, json_list['supplier_code'], json_list['cert_name'], json_list['cert_code'], json_list['supplier_grade'], '','', json_list['regist_cert_auth'], json_list['cert_expire_date'], json_list['cert_status'],json_list['cert_picture_path'], ''))
    # print('sql-----------', cursor.execute)
    ora.commit()

    cursor.execute('select * from comm.exp_supplier_cert')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
        # print(res)

    # cursor.close()
    # ora.close()
    return JsonResponse({"result": 0, "msg": "执行成功"})


# 委托信息form 查询--------------
@csrf_exempt
def jbxx_see(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    sql = "select * from comm.exp_client_information where SUPPLIER_CODE='" + supplier_code + "'"
    m_data = get_data(sql)
    if(m_data):
        json_dict = {}
        for i in m_data:
            json_dict["client"] = i[1]
            json_dict["id_card"] = i[2]
            json_dict["phone"] = i[3]
            json_dict["address"] = i[4]
            json_dict["mailbox"] = i[5]
    else:
        json_dict = {}
        for i in m_data:
            json_dict["client"] = ''
            json_dict["id_card"] = ''
            json_dict["phone"] = ''
            json_dict["address"] = ''
            json_dict["mailbox"] = ''
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_dict})


# 委托信息form 增加--------------
@csrf_exempt
def jbxx_add(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            json_list[key] = request.POST.getlist(key)[0]
    print('json_list', json_list)
    supplier_code = json_list['supplier_code']
    delSql = "delete from comm.exp_client_information where SUPPLIER_CODE='" + supplier_code + "'"
    cursor.execute(delSql)
    ora.commit()

    cursor.execute('insert into comm.exp_client_information values(:1,:2,:3,:4,:5,:6)', (json_list['supplier_code'], json_list['client'], json_list['id_card'], json_list['phone'], json_list['address'], json_list['mailbox']))
    # print('sql-----------', cursor.execute)
    ora.commit()

    cursor.execute('select * from comm.exp_client_information')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
        # print(res)

    # cursor.close()
    # ora.close()
    return JsonResponse({"result": 0, "msg": "执行成功"})


# 委托信息_entrust_edit
@csrf_exempt
def wtxx_edit(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'effective_end_date':
                if request.POST.getlist(key)[0]:
                    json_list[key] = request.POST.getlist(key)[0].strip()
                    # print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    # print('json_list', json_list)
    sql = "update comm.exp_supplier_information set " \
          "certificates = '"+ json_list['certificates'] \
          + "', id_card = '" + json_list['id_card']\
          + "',regist_cert_auth = '" + json_list['regist_cert_auth'] \
          + "',cert_picture_path = '" + json_list['cert_picture_path'] \
          + "',effective_end_date = to_date('" + json_list['effective_end_date'] +"', 'yyyy-mm-dd') where id = :id"
    print('sql', sql)
    cursor.prepare(sql)
    cursor.execute(None, {'id': json_list['id']})
    ora.commit()
    cursor.execute('select * from comm.exp_supplier_cert')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
    return JsonResponse({"result": 0, "msg": "执行成功"})


# 委托信息table
@csrf_exempt
def wtxx_info(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    sql = "select * from comm.exp_supplier_information where SUPPLIER_CODE='" + supplier_code + "'"
    m_data = get_data(sql)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict["id"] = i[0]
        json_dict["certificates"] = i[3]
        json_dict["id_card"] = i[4]
        json_dict["effective_end_date"] = timeFormat(i[5])
        json_dict["regist_cert_auth"] = i[11]
        json_dict["cert_picture_path"] = i[12]
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 委托信息 新增
@csrf_exempt
def wtxx_add(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'effective_end_date':
                if request.POST.getlist(key)[0]:
                    json_list[key] = datetime.strptime(request.POST.getlist(key)[0].strip(), '%Y-%m-%d')
                    print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    # print('json_list', json_list)
    cursor.execute('insert into comm.exp_supplier_information values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)', ('', json_list['supplier_code'], json_list['legal_person'], json_list['certificates'], json_list['id_card'], json_list['effective_end_date'], '', '', '', '', '',json_list['regist_cert_auth'], ''))
    ora.commit()

    cursor.execute('select * from comm.exp_supplier_information')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
        # print(res)

    # cursor.close()
    # ora.close()
    return JsonResponse({"result": 0, "msg": "执行成功"})


# 采购医列表
@csrf_exempt
def cglb_info(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
        buy_id = request.GET.get('buy_id') or ''

    if buy_id != '':
        # sql = "select distinct buy_id, exp_code, buyer from buy_exp_plan where buy_id='" + buy_id + "'"
        sql = "select distinct buy_id, buyer from buy_exp_plan s,exp_supplier_catalog t where s.stock_supplier = t.supplier_id and t.supplier_class = '供应商' and s.buy_id='" + buy_id + "' and t.supplier_code  = '" + supplier_code + "'"
    else:
        sql = "select distinct buy_id, buyer from buy_exp_plan order by buy_id desc"
    m_data = get_data(sql)
    # print('sql', sql)
    # print('aaa', m_data)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict["buy_id"] = i[0]
        # json_dict["exp_code"] = i[1]
        json_dict["buyer"] = i[1]
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 采购医材明细
@csrf_exempt
def cgmx_info(request):
    if request.method == 'GET':
        buy_id = request.GET.get('buy_id')
    sql = "select * from buy_exp_plan where buy_id='" + buy_id + "'"
    m_data = get_data(sql)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict["buy_id"] = i[0]
        json_dict["buy_no"] = i[1]
        json_dict["exp_code"] = i[2]
        json_dict["exp_name"] = i[3]
        json_dict["exp_spec"] = i[4]
        json_dict["units"] = i[5]
        json_dict["exp_from"] = i[6]
        # json_dict["TOXI_PROPERTY"] = i[7]
        # json_dict["DOSE_PER_UNIT"] = i[8]
        # json_dict["EXP_INDICATOR"] = i[9]
        # json_dict["DOSE_UNITS"] = i[10]
        # json_dict["INPUT_CODE"] = i[11]
        json_dict["want_number"] = i[12]
        # json_dict["STORER"] = i[13]
        # json_dict["STOCK_NUMBER"] = i[14]
        json_dict["stock_supplier"] = i[15]
        # json_dict["BUYER"] = i[16]
        # json_dict["CHECK_NUMBER"] = i[17]
        # json_dict["CHECK_SUPPLIER"] = i[18]
        # json_dict["CHECKER"] = i[19]
        # json_dict["FLAG"] = i[20]
        json_dict["pack_spec"] = i[21]
        json_dict["pack_unit"] = i[22]
        json_dict["firm_id"] = i[23]
        json_dict["purchase_price"] = i[24]
        # json_dict["STORAGE"] = i[25]
        # json_dict["STOCKQUANTITY_REF"] = i[26]
        # json_dict["EXPORTQUANTITY_REF"] = i[27]
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 送货信息table
@csrf_exempt
def shxx_info(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
        deliverer = request.GET.get('deliverer') or ''
        plan_code = request.GET.get('plan_code') or ''
        delivery_time = request.GET.get('delivery_time') or ''
        warehouse_name = request.GET.get('warehouse_name') or ''
    sql = "select * from comm.exp_purchase_list where " "SUPPLIER_CODE='" + supplier_code \
          + "'and deliverer like'" + deliverer \
          + "%'and plan_code like'" + plan_code \
          + "%'and delivery_time like'" + delivery_time \
          + "%'and warehouse_name like'" + warehouse_name + "%'"
    # print('sql', sql)
    m_data = get_data(sql)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict["plan_code"] = i[0]
        json_dict["delivery_time"] = timeFormat(i[1])
        json_dict["deliverer"] = i[2]
        json_dict["supplier_code"] = i[3]
        json_dict["warehouse_name"] = i[4]
        json_dict["state"] = stateStrr(i[5])
        json_dict["memo"] = i[6]
        json_dict["phone"] = i[7]
        json_dict["buy_id"] = i[8]
        # json_dict["detailed"] = i[9]
        # print('------------------dssd', type(i[1]))
        json_list.append(json_dict)
    return JsonResponse({"result": 0, "msg": "执行成功", "data": json_list})


# 送货信息 编辑
@csrf_exempt
def menu_edit_info(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'delivery_time':
                if request.POST.getlist(key)[0]:
                    json_list[key] = request.POST.getlist(key)[0].strip()
                    # print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    print('json_list', type(json_list['plan_code']))
    print('json_list', json_list['plan_code'])
    plan_code = json_list['plan_code']
    delSql = "delete from comm.exp_purchase_medical_details where plan_code=" + plan_code;
    cursor.execute(delSql)
    ora.commit()

    detailed = json.loads(json_list['detail'])
    print('detailed==============', detailed)
    datailedTuple = []
    for key in detailed:
        tupleKey = (json_list['plan_code'], key['item_no'], key['exp_code'], key['exp_name'], key['spec'], key['unit'], '', key['production_manu'], '', key['purchase_quantity'])
        datailedTuple.append(tupleKey)
    print('detailed==============', datailedTuple)
    cursor.prepare('insert into comm.exp_purchase_medical_details values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)')
    cursor.executemany(None, datailedTuple)
    ora.commit()

    cursor.execute('select * from comm.exp_purchase_medical_details')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break

    sql = "update comm.exp_purchase_list set " \
          "plan_code = '" + json_list['plan_code'] \
          + "', memo = '" + json_list['memo'] \
          + "', deliverer = '" + json_list['deliverer']\
          + "',warehouse_name = '" + json_list['warehouse_name'] \
          + "', phone = '" + json_list['phone'] \
          + "', state = '" + json_list['state'] \
          + "', detailed = '" + json_list['detail'] \
          + "',delivery_time = to_date('" + json_list['delivery_time'] +"', 'yyyy-mm-dd') where plan_code = :plan_code"
    cursor.prepare(sql)
    cursor.execute(None, {'plan_code': json_list['plan_code']})
    ora.commit()
    cursor.execute('select * from comm.exp_purchase_list')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
    # cursor.close()
    # ora.close()
    return JsonResponse({"result": 0, "msg": "执行成功"})


# 送货信息 新增
@csrf_exempt
def menu_add_info(request):
    if request.method == 'POST':
        json_list = {}
        for key in request.POST:
            if key == 'delivery_time':
                if request.POST.getlist(key)[0]:
                    json_list[key] = datetime.strptime(request.POST.getlist(key)[0].strip(), '%Y-%m-%d')
                    print('valuelist', json_list[key])
                else:
                    json_list[key] = ''
            else:
                json_list[key] = request.POST.getlist(key)[0]
    # print('json_list88888888', json_list)
    detailed = json.loads(json_list['detailed'])
    plan_code = generateTimeReqestNumber()
    datailedTuple = []
    for key in detailed:
        tupleKey = (plan_code, key['ITEM_NO'], key['EXP_CODE'], key['EXP_NAME'], key['SPEC'], key['UNIT'], '', key['PRODUCTION_MANU'], '', key['PURCHASE_QUANTITY'])
        datailedTuple.append(tupleKey)
    print('detailed==============', datailedTuple)
    cursor.prepare('insert into comm.exp_purchase_medical_details values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)')
    cursor.executemany(None, datailedTuple)
    ora.commit()

    cursor.execute('select * from comm.exp_purchase_medical_details')
    # while 1:
    #     res = cursor.fetchone()
    #     if res == None:
    #         break
    #     print(res)

    cursor.execute('insert into comm.exp_purchase_list values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)', (plan_code, json_list['delivery_time'], json_list['deliverer'], json_list['supplier_code'], json_list['warehouse_name'], '1', json_list['memo'], json_list['phone'], json_list['buy_id'], json_list['detailed']))
    ora.commit()

    cursor.execute('select * from comm.exp_purchase_list')
    while 1:
        res = cursor.fetchone()
        if res == None:
            break
        # print(res)

    # cursor.close()
    # ora.close()
    return JsonResponse({"result": 0, "msg": "新增成功"})


# 送货信息table:menu_see
@csrf_exempt
def get_menu_see(request):
    if request.method == 'GET':
        plan_code = request.GET.get('plan_code')
    # print('plan_code', plan_code)
    sql = "select * from comm.exp_purchase_medical_details where plan_code=" + plan_code;
    # print('sql', sql)
    m_data = get_data(sql)
    # print('m_data', m_data)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict['item_no'] = i[1]
        json_dict['exp_code'] = i[2]
        json_dict['exp_name'] = i[3]
        json_dict['spec'] = i[4]
        json_dict['unit'] = i[5]
        json_dict['effective_date'] = i[6]
        json_dict['production_manu'] = i[7]
        json_dict['bath_number'] = i[8]
        json_dict['purchase_quantity'] = i[9]
        json_list.append(json_dict)
    print('json_list', json_list)
    return JsonResponse({"result": 0, "message": "执行成功", "data":json_list})


# 删除 基本
@csrf_exempt
def jbxx_del(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # print('dddd', id)
    cursor.execute("delete from comm.exp_supplier_cert where id=" + id)
    ora.commit()

    cursor.execute("select * from comm.exp_supplier_cert where id=" + id)
    while 1:
        res = cursor.fetchone()
        if res == None:
            return JsonResponse({"result": 1, "msg": "删除成功"})
        else:
            return JsonResponse({"result": 0, "msg": "删除失败"})
            break
        # print(res)
    # cursor.close()
    # ora.close()


# 删除 委托
@csrf_exempt
def wtxx_del(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # print('dddd', id)
    cursor.execute("delete from comm.exp_supplier_information where id=" + id)
    ora.commit()

    cursor.execute("select * from comm.exp_supplier_information where id=" + id)
    while 1:
        res = cursor.fetchone()
        if res == None:
            return JsonResponse({"result": 1, "msg": "删除成功"})
        else:
            return JsonResponse({"result": 0, "msg": "删除失败"})
            break
        # print(res)
    # cursor.close()
    # ora.close()


# 删除 送货
@csrf_exempt
def shxx_del(request):
    if request.method == 'GET':
        plan_code = request.GET.get('plan_code')
        # print('dddd', plan_code)
    cursor.execute("delete from comm.exp_purchase_list where plan_code=" + plan_code)
    ora.commit()

    cursor.execute("select * from comm.exp_purchase_list where plan_code=" + plan_code)
    while 1:
        res = cursor.fetchone()
        if res == None:
            return JsonResponse({"result": 1, "msg": "删除成功"})
        else:
            return JsonResponse({"result": 0, "msg": "删除失败"})
            break
        # print(res)
    # cursor.close()
    # ora.close()


# 上传
@csrf_exempt
def upload_img(request):
    # 开始上传
    uploadFile = request.FILES.get('imgfile')
    name = str(uploadFile).replace('.', '_')
    saveFileName = newFileName(uploadFile.content_type, name)
    saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

    # 将上传文件的数据分段写入到目标文件（存放到当前服务端）中
    with open(saveFilePath, 'wb') as f:
        for part in uploadFile.chunks():
            f.write(part)
            f.flush()

    return JsonResponse({"result": 0, "msg": "上传成功", 'imgUrl': 'upload/' + saveFileName})


# 中标耗材
@csrf_exempt
def winning_bid_consumables(request):
    if request.method == 'GET':
        supplier_code = request.GET.get('supplier_code')
    # print('plan_code', plan_code)
    sql = "select * from comm.exp_ascend_firm_exp where supplier_code='" + supplier_code + "'";
    print('sql', sql)
    m_data = get_data(sql)
    # print('m_data', m_data)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict['title'] = i[1]
        json_dict['id'] = 2
        json_dict['firm_id'] = i[0]
        json_dict['exp_code'] = i[1]
        json_dict['contract_number'] = i[2]
        json_dict['expire_date'] = timeFormat(i[3])
        json_dict['supplier_code'] = i[4]
        json_list.append(json_dict)
    print('json_list', json_list)
    return JsonResponse({"result": 0, "message": "执行成功", "data": json_list})


# 中标耗材明细
@csrf_exempt
def winning_bid_consumables_detailed(request):
    if request.method == 'GET':
        # supplier_code = request.GET.get('supplier_code')
        exp_code = request.GET.get('exp_code')
    # print('plan_code', plan_code)
    # sql = "select * from comm.exp_ascend_firm_exp where supplier_code='" + supplier_code + "'";
    sql = "select * from comm.exp_dict where exp_code='" + exp_code + "'"
    print('sql', sql)
    m_data = get_data(sql)
    # print('m_data', m_data)
    json_list = []
    for i in m_data:
        json_dict = {}
        json_dict['exp_code'] = i[0]
        json_dict['exp_name'] = i[1]
        json_dict['exp_spec'] = i[2]
        json_dict['units'] = i[3]
        json_dict['exp_form'] = i[4]
        json_dict['toxi_property'] = i[5]
        json_dict['dose_per_unit'] = i[6]
        json_dict['dose_units'] = i[7]
        json_dict['input_code'] = i[8]
        json_dict['exp_indicator'] = i[9]
        json_dict['storage_code'] = i[10]
        json_dict['single_group_indicator'] = i[11]
        json_dict['exp_spec_1'] = i[12]
        json_dict['exp_type'] = i[13]
        json_dict['class_equip'] = i[14]
        json_dict['exp_seq'] = i[15]
        json_list.append(json_dict)
    print('json_list', json_list)
    return JsonResponse({"result": 0, "message": "执行成功", "data": json_list})


# 函数
def pad2(n):
    if n < 10:
        return '0' + str(n)
    else:
        return str(n)


def generateTimeReqestNumber():
    now_time = datetime.now()
    year = now_time.strftime('%Y')
    month = now_time.strftime('%m')
    date = now_time.strftime('%d')
    hours = now_time.strftime('%H')
    minutrs = datetime.now().strftime('%M')
    rand = int(math.floor(random.random() * 900) + 100)
    return year + pad2(int(month)) + pad2(int(date)) + pad2(int(hours)) + pad2(int(minutrs)) + str(rand)


def timeFormat(time):
    if time:
        return datetime.strftime(time, '%Y-%m-%d')
    else:
        return ''


def newFileName(contentType, name):
    fileName = name + '_'+str(int(time.time()))#构造文件名以及文件路径
    extName = '.jpg'
    if contentType == 'image/png':
        extName = '.png'
    elif contentType == 'image/jpeg':
        extName = '.jpg'
    return fileName + extName


# 中标state
def stateStr(state):
    if state == '0':
        return '未审核'
    else:
        return '已审核'


# 基本信息tate
def certStateStr(cert_status):
    if cert_status == '1':
        return '是'
    else:
        return '否'


# 送貨state
def stateStrr(state):
    if state == '1':
        return '已提交'
    elif state == '2':
        return '已审核'
    elif state == '3':
        return '已入库'


# 页面
def login(req):
    return render(req, "login.html")


def index(req):
    return render(req, "index.html")


def welcome(req):
    return render(req, "welcome.html")


def winning_bid_info(request):
    return render(request, 'winning_bid_info.html')


def admin_info(request):
    return render(request, "admin_info.html")


def winning_detail(req):
    return render(req, "winning_detail.html")


def demo_add(request):
    return render(request, "demo_add.html")


def demo_edit(request):
    return render(request, "demo_edit.html")


def entrust_add(request):
    return render(request, "entrust_add.html")


def entrust_edit(request):
    return render(request, "entrust_edit.html")


def menu1(request):
    # sql = "select distinct buy_id,buyer from buy_exp_plan"
    # sqla = "select buy_id,buy_no,exp_code,exp_name,exp_spec,units,exp_form,want_number,pack_spec,pack_unit,firm_id,purchase_price,stock_supplier from  buy_exp_plan"
    # m_data = get_data(sql)
    # w_data = get_data(sqla)
    # print('-------', m_data)
    # print('=======', w_data)
    return render(request, 'menu1.html')


def menu2(request):
    return render(request, 'menu2.html')


def menu_add(request):
    sql = "select distinct buy_id,buyer from buy_exp_plan"
    m_data = get_data(sql)
    return render(request, "menu_add.html", {'menu1': m_data})


def menu_see(request):
    return render(request, "menu_see.html")


def menu_edit(request):
    return render(request, "menu_edit.html")


def supplier_management(request):
    return render(request, "supplier_management.html")


def qualification_management(request):
    return render(request, "qualification_management.html")


def qua_mana_edit(request):
    return render(request, "qua_mana_edit.html")


def winning_detail_child(request):
    return render(request, "winning_detail_child.html")


def winning_detail_child_add(request):
    return render(request, "winning_detail_child_add.html")


def winning_detail_child_edit(request):
    return render(request, "winning_detail_child_edit.html")


# 中标耗材明细
def winning_bid_consum_deta(request):
    return render(request, "winning_bid_consum_deta.html")

