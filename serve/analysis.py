from pyecharts.charts import Bar
from pyecharts.options import InitOpts, AxisOpts
from db.get_increment import get_change, get_time
from pyecharts import options as opts


# InitOpts(width="500px", height="1000px", page_title="虚拟主播小时粉丝变化表")
# res = get_time(flags='d')
# get_one = get_change(res[0], res[1], reverse=False)
# all_info = get_one.run()
# uid_list = get_one.get_ranked_uid()
# name_list = get_one.get_ranked_name()
# change_list = get_one.get_ranked_change()


def draw_chart(x_data, y_data, title, page_title, series_name, floder_name, res):

    bar = Bar(InitOpts(width="1500px", height="4600px", page_title=page_title, animation_opts=opts.AnimationOpts(animation_easing='exponentialInOut')))
    bar.add_xaxis(xaxis_data=x_data)
    bar.add_yaxis(yaxis_data=y_data, series_name=series_name, category_gap="30%")
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title + '粉丝数变化', subtitle=res[0] + '到' + res[1]),
                        xaxis_opts=AxisOpts(boundary_gap=['5%', '10%']), toolbox_opts=opts.ToolboxOpts())
    # bar.set_global_opts(xaxis_opts=AxisOpts(boundary_gap=['5%', '10%']), toolbox_opts=opts.ToolboxOpts())
    bar.reversal_axis()
    bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    bar.render("chart/{0}/{1}.html".format(floder_name, title))


def analysis_create_days():
    res = get_time(flags='d')
    get_one = get_change(res[0], res[1], reverse=False)
    all_info = get_one.run()
    uid_list = get_one.get_ranked_uid()
    name_list = get_one.get_ranked_name()
    change_list = get_one.get_ranked_change()
    draw_chart(name_list, change_list, res[0][0:13], '虚拟主播粉丝数日变化', '变化量', 'days', res)


def analysis_create_hours():
    res = get_time(flags='h')
    get_one = get_change(res[0], res[1], reverse=False)
    all_info = get_one.run()
    uid_list = get_one.get_ranked_uid()
    name_list = get_one.get_ranked_name()
    change_list = get_one.get_ranked_change()
    draw_chart(name_list, change_list, res[0][0:13], '虚拟主播粉丝小时变化', '变化量', 'hours', res)

