"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几步：

在视图函数中：
    def mobile_list(request):

        # 1、根据自己的情况去筛选自己的数据
        queryset = Mobile_Num.objects.filter(**data_dict).all().order_by('-level')

        # 2、实例化分页对象
        pagination = Pagination(request, queryset)

        context = {
            'search_data': search_data,

            'queryset': pagination.page_queryset,   # 分完页的数据
            'page_string': pagination.html()        # 生成页码
        }

        return render(request, 'mobile_list.html', context)

在 HTML 页面中：
    <ul class="pagination center">
	    {{ page_string }}
	</ul>
"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_param='page', page_size=10, plus=5):
        """
        :param request:  请求的对象
        :param queryset:  符合条件的数据（根据这个数据给他进行分页处理）
        :param page_param:  在URL中传递的获取分页的参数， 例如：/mobile/list/?page=1
        :param page_size:  每页显示多少条数据
        :param plus:   显示当前页的  前或后几页
        """

        import copy

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.plus = plus
        self.page_param = page_param

        start = (page - 1) * page_size
        end = page * page_size

        self.page_queryset = queryset[start: end]

        # 计算总页码数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count

    def html(self):
        page_str_list = []
        if self.total_page_count < 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) >= self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        self.query_dict.setlist(self.page_param, [1])
        # 首页
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            page_str_list.append('<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_param, [1])
            page_str_list.append('<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode()))

        # 页码显示
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                page_str_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i))
            else:
                self.query_dict.setlist(self.page_param, [i])
                page_str_list.append('<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i))

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            page_str_list.append('<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            page_str_list.append('<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode()))

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_page_string = """
            <li>
                <form action="" method="get" style="float: left; margin-left: 10px">
                    <div class="input-group" style="width: 150px">
                        <input type="text" class="form-control" placeholder="页码" name="page">
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="submit">跳转</button>
                        </span>
                    </div><!-- /input-group -->
                </form>
            </li>
        """
        page_str_list.append(search_page_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string
