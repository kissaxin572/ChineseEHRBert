import sys, os
import re
import time
import argparse

input_file_path = "data"  # 输入文件路径
output_file_path = "out"  # 输出文件路径
output_mode = "integrate"  # 输出模式
log_period = 5000  # 日志显示周期

line_counter = 0  # 有效行计数器

def main():
    global input_file_path
    global output_file_path
    global output_mode
    global log_period
    global line_counter
    
    parser = argparse.ArgumentParser()  # 创建参数解析器
    parser.add_argument("--input", type=str, default=input_file_path, required=False, help="declare input file directory (default: %(default)s)")  # 添加输入文件路径参数
    parser.add_argument("--output", type=str, default=output_file_path, required=False, help="declare output file directory (default: %(default)s)")  # 添加输出文件路径参数
    parser.add_argument("-s", "--seperate", action="store_true", help="check it to make output seperated (write into a single file \"output.txt\" by default)")  # 添加输出分离参数
    parser.add_argument("--log", type=int, default=log_period, required=False, help="period of displaying progress (default: %(default)s)")  # 添加日志显示周期参数
    args = parser.parse_args()  # 解析命令行参数
    
    if args.seperate == True:
        output_mode = "seperate"  # 根据参数判断输出模式
    
    input_file_path = args.input  # 更新输入文件路径
    output_file_path = args.output  # 更新输出文件路径
    log_period = args.log  # 更新日志显示周期
    
    time_start = time.time()  # 记录程序开始时间
    input_exist = os.path.exists(input_file_path)  # 判断输入文件路径是否存在
    if not input_exist:
        print("input directory missing:" + input_file_path + " exit.")
        return  # 输入文件路径缺失，结束程序
    output_exist = os.path.exists(output_file_path)  # 判断输出文件路径是否存在
    if not output_exist:
        os.makedirs(output_file_path)  # 输出文件路径不存在，则创建
    file_path_list = get_file_path_list(input_file_path)  # 获取输入文件路径下的文件路径列表
    file_list_handler(file_path_list)  # 处理文件列表
    time_end = time.time()  # 记录程序结束时间
    print("total valid #lines: ", line_counter)  # 输出有效行计数
    print("total time elapsed:", time_end - time_start)  # 输出程序运行时间

def get_file_path_list(data_dir):  # 获取文件路径列表的函数
    result = []  # 初始化结果列表
    for main_dir, subdir, file_name_list in os.walk(data_dir):  # 遍历文件夹树结构
        result = [os.path.join(main_dir, file_name) for file_name in file_name_list]  # 将文件名拼接成完整路径并加入结果列表
    return result  # 返回结果列表
  
def clear_file(file_path):  # 清空文件的函数
    f = open(file_path, 'w')  # 以写入模式打开文件
    f.truncate()  # 清空文件内容
    f.close()  # 关闭文件
  
def file_list_handler(file_path_list):  # 处理文件路径列表的函数
    default_output_file_path = os.path.join(output_file_path, "output.txt")  # 默认输出文件路径
    if output_mode == "integrate":  # 如果输出模式为整合模式
        clear_file(default_output_file_path)  # 清空默认输出文件
        for file_path in file_path_list:  # 遍历文件路径列表
            single_file_handler(file_path, default_output_file_path, write_mode='a')  # 处理单个文件
    elif output_mode == "seperate":  # 如果输出模式为分离模式
        for file_path in file_path_list:  # 遍历文件路径列表
            filename = os.path.split(file_path)[1]  # 获取文件名
            tmp_output_file_path = os.path.join(output_file_path, filename)  # 构建临时输出文件路径
            single_file_handler(file_path, tmp_output_file_path, write_mode='w')  # 处理单个文件
    
def single_file_handler(input_file_path, output_file_path, write_mode):  # 处理单个文件的函数
    global line_counter  # 全局有效行计数器
    f_out = open(output_file_path, write_mode)  # 打开输出文件
    for line in open(input_file_path):  # 遍历输入文件的每一行
        if is_not_empty(line):  # 如果行不为空
            f_out.write(article_processor(line).strip())  # 写入处理后的行内容
            f_out.write('\n\n')  # 写入两个换行符
            line_counter += 1  # 有效行计数器加一
            if line_counter % log_period == 0:  # 如果需要显示日志
                print("processed valid lines:" + str(line_counter))  # 输出已处理的有效行数

    f_out.close()  # 关闭输出文件
  
def is_not_empty(line):  # 判断行是否为空的函数
    return line.strip() != ""  # 移除行前后的空格，判断是否为空字符串

def test_is_not_empty():  # 测试函数，测试is_not_empty函数是否正确
    ret = [is_not_empty("123"), is_not_empty("123  "), is_not_empty("  123"), is_not_empty("1 2 3"),
           is_not_empty("123\n"), is_not_empty("123  \n"), is_not_empty("\n"), is_not_empty("   \n")]
    print(ret)  # 输出函数测试结果

article_processor = article_processor  # 定义article_processor变量，赋值给函数article_processor

def article_processor(article):  # 文章处理函数
    replaced_list = ['。', '！', '？', '!', '?', '……']  # 替换列表
    sub_dict = {str: str + '\n' for str in replaced_list}  # 替换字典，将替换字符替换为换行符
    res = article  # 初始化结果
    for rep, sub in sub_dict.items():  # 遍历替换字典
        res = res.replace(rep, sub)  # 替换字符
    return res  # 返回处理后的结果

# region Deprecated (deprecated) # 可选，deprecated的函数或代码块
# 使用正则表达式处理文章的函数
def reg_article_processor(article):
    return re.sub("[。！？!?]|……", reg_new_line, article)

def reg_new_line(matched):
    return matched.group(0) + '\n'

# endregion

if __name__ == "__main__":  # 如果作为主程序运行
    main()  # 执行主函数