#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'

"""
@brief 简介 
@details 详细信息
@author  wuhuafeng
@data    2018-03-05 
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPaginator(Paginator):
    """
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象 (是否具有下一页，是否有上一页)
    """
    def __init__(self, current_page, per_pager_num, *agrs, **kwargs):
        '''
        :param current_page:
        :param per_pager_num: 显示的页码数量
        :param agrs:
        :param kwargs:
        '''
        self.current_page = int(current_page)
        self.per_pager_num = int(per_pager_num)
        super(CustomPaginator, self).__init__(*agrs, **kwargs)


    def pager_num_range(self):
        '''
        自定义显示页码数
        第一种：总页数小于显示的页码数
        第二种：总页数大于显示页数  根据当前页做判断  a 如果当前页大于显示页一半的时候  ，往右移一下
                                                b 如果当前页小于显示页的一半的时候，显示当前的页码数量
        第三种：当前页大于总页数
        :return:
        '''
        if self.num_pages < self.per_pager_num:
            return range(1, self.num_pages+1)

        half_part = int(self.per_pager_num/2)  # 3
        if self.current_page <= half_part:
            return range(1, self.per_pager_num+1)
        else:
            if (self.current_page+half_part) > self.num_pages:
                return range(self.num_pages-self.per_pager_num+1, self.num_pages+1)
            else:
                return range(self.current_page-half_part, self.current_page+half_part)
