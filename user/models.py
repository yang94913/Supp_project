from django.db import models


# Create your models here.


class Winning_info_fff(models.Model):
    supplier_code = models.CharField(primary_key=True,max_length=30,verbose_name='供应商ID')
    contract_num = models.CharField(max_length=30, verbose_name='合同编号')
    winning_type = models.CharField(max_length=10, verbose_name='中标类型')
    winning_date = models.DateTimeField(auto_now_add=True, verbose_name='中标截止日期')
    supply_end_date = models.DateTimeField(auto_now_add=True, verbose_name='供货截止日期')
    states = ((0, '未审核'), (1, '已审核'))
    state = models.IntegerField(choices=states, default=0)

    class Meta:
        db_table = 'comm.exp_supplier_type_f'





