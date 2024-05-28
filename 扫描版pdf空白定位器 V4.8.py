#coding=utf-8
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pdfplumber
import cv2
import fitz
import numpy as np
import math
import os


class windows: # tkUI的类
    def __init__(self, root):
        self.root = root
        self.root.title('扫描版pdf空白定位器 V4.8')
        self.create_cascade()
        self.container0 = tk.Frame(self.root)
        self.container0.grid(column=0, row=0 ,sticky="w")
        self.container1 = tk.Frame(self.root)
        self.container1.grid(column=0, row=1 ,sticky="w")
        self.container2 = tk.Frame(self.root)
        self.container2.grid(column=0, row=2, sticky="w")
        self.container3 = tk.Frame(self.root)
        self.container3.grid(column=0, row=3, sticky="w")
        self.create_Frame0()
        self.create_Frame1()
        self.create_Frame2()
        self.create_Frame3()

    def create_cascade(self):
        menu = tk.Menu(self.root)  # 参数是父级控件
        cascade = tk.Menu(menu, tearoff=False)  # 二级菜单 # tearoff=False 表示这个菜单不可以被拖出来
        menu.add_cascade(label='清除表格', command=delete)
        self.root['menu'] = menu  # 窗口root的menu是menu0

    def create_Frame0(self):
        global var0 ,var1
        self.button = tk.Button(self.container0, text='pdf_path0', bg='white', command=select_files0)
        self.button.grid(column=0, row=0)
        self.button = tk.Button(self.container0, text='pdf_path1', bg='white', command=select_files1)
        self.button.grid(column=0, row=1)
        var0 = tk.StringVar()
        self.label = tk.Label(self.container0, textvariable=var0, bg='gray', width=50)
        self.label.grid(column=1, row=0)
        var1 = tk.StringVar()
        self.label = tk.Label(self.container0, textvariable=var1, bg='gray', width=50)
        self.label.grid(column=1, row=1)

    def create_Frame1(self):
        self.button = tk.Button(self.container1, text='开始执行', bg='white', command=panduan_pages)
        self.button.grid(column=0, row=0)
        self.p1 = ttk.Progressbar(self.container1, length=100, cursor='spider', mode="determinate", orient=tk.HORIZONTAL)
        self.p1.grid(column=1, row=0 ,ipadx = 120) # 进度条拉伸
        self.button = tk.Button(self.container1, text='在图片中显示结果', bg='white',command=lambda: xianshi(dict_output))
        self.button.grid(column=0, row=1, columnspan=2)

    def create_Frame2(self):
        # ===========设置treeview============
        self.scrollBary = tk.Scrollbar(self.container2)
        column_n = []
        column_m = ['页码', '空白个数']
        for i, j in enumerate(column_m):
            column_n.append(str(i))
        self.tree = ttk.Treeview(self.container2, columns = column_n, show='headings', selectmode='browse', height=20, yscrollcommand=self.scrollBary.set)
        self.tree.grid(column=0, row=0)
        for i in column_n:
            self.tree.column(i, anchor='center')
        for i, j in enumerate(column_m):
            self.tree.heading(str(i), text=j)
        # ===========设置滚动条===============
        self.scrollBary.grid(column=1, row=0, sticky='ns') #靠右，充满Y轴
        self.scrollBary.config(command=self.tree.yview)

    def create_Frame3(self):
        global var2, var3
        # ===========绑定单击显示事件===========
        self.tree.bind('<ButtonRelease-1>', treeviewClick)
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        var2.set('单击行显示具体内容')
        var3.set('单击行显示具体内容')
        self.label = tk.Label(self.container3, textvariable=var2, relief="groove")
        self.label.grid(column=0, row=0, padx=40)
        self.label = tk.Label(self.container3, textvariable=var3, relief="groove")
        self.label.grid(column=1, row=0, padx=40)


def treeviewClick(event): # 单击显示事件
    for item in app.tree.selection():
        item_text = app.tree.item(item,"values")
        var2.set(item_text[0])
        var3.set(item_text[1])

def true_path0(dl, new_pdf, old_pdf):
    def continue_execution():
        global pdf_path0
        root.destroy()
        for i in dl[::-1]:
            del new_pdf[i]
        new_path = old_pdf.replace(old_pdf[old_pdf.rfind('/') + 1:], '临时.pdf')
        new_pdf.save(new_path)
        new_pdf.close()
        pdf_path0 = new_path
    root = tk.Tk()
    root.title('提醒：请单击确认再执行程序')
    label = tk.Label(root, text="请确认需要删除的页" + str([i + 1 for i in dl]))
    label.pack()
    button = tk.Button(root, text="确认", command=continue_execution)
    button.pack()
    root.mainloop()

def select_files0():
    selected_files_path = filedialog.askopenfilename()
    var0.set(selected_files_path)
    delete_file = []
    pdf = fitz.open(selected_files_path)
    for i in range(pdf.page_count):
        page = pdf[i]
        if page.rect.height > page.rect.width:
            delete_file.append(i)
    true_path0(delete_file, pdf, selected_files_path)

def select_files1(): # askopenfilenames函数选择文件，可以选择单个或多个文件
    global pdf_path1
    selected_files_path = filedialog.askopenfilename()
    var1.set(selected_files_path)
    pdf_path1 = selected_files_path

def different_pages(len0,len1):
    root = tk.Tk()
    root.title('提醒：页码不一致')
    label = tk.Label(root, text=pdf_path0 + '页码总数：' + str(len0))
    label.pack()
    label = tk.Label(root, text=pdf_path1 + '页码总数：' + str(len1))
    label.pack()
    root.mainloop()

def panduan_pages():
    global pdf_len0
    pdf_len0 = len(pdfplumber.open(pdf_path0).pages)
    pdf_len1 = len(pdfplumber.open(pdf_path1).pages)
    if pdf_len0 == pdf_len1:
        zuobiao()
    if pdf_len0 != pdf_len1:
        different_pages(pdf_len0,pdf_len1)


def delete(): # 单击删除目录事件
    app.p1["value"] = 0
    app.root.update()
    for i in app.tree.get_children():
        app.tree.delete(i)

def progressbar(): # 进度条事件
    for i in range(0, int(num / pdf_len0 * 100)):
        app.p1["value"] = i + 1
    app.root.update()

def start(): # tkUI主体事件
    global app
    root = tk.Tk()
    root.resizable(False, True) # 窗口x轴锁定，y轴可拉伸
    app = windows(root)
    root.mainloop()


def zuobiao():
    global list1,list2,list3,list4,list5,list6,list7,list8,list9,table,page_num,dict_output,list_pct,num,table_x,table_y
    dict_output = {}
    dict1 = {}
    dict0 = {}
    list9 = []
    pdf = pdfplumber.open(pdf_path0)
    dict_output = {pdf_path1: dict1 ,pdf_path0: dict0}
    num = 0
    for page_num in range(len(pdf.pages)):
        try:
            num += 1
            list1, list2, list3, list4, list5, list6, list7, list8 = [[] for i in range(8)]
            list_pct = []
            # 获取第一页
            page = pdf.pages[page_num]
            # 获取页面的宽度和高度（以像素为单位）
            width = page.width
            height = page.height
            # =========================list1字符串坐标=====================
            for j, i in enumerate(page.chars):
                list1.extend([[i['x0'], height - i['y1'], i['x1'], height - i['y0'], i['text']]])
            # =========================list2括号坐标=====================
            char = page.chars  # 所有字符串
            for i, j in enumerate(char):
                if j['text'] == '（':
                    for m, n in enumerate(char[(i + 1):]):
                        if n['text'] == '）':
                            m = m + i
                            str_text = ''.join([data['text'] for data in char[(i - 10):i]])
                            result0 = all(data['text'] == ' ' for data in char[(i + 1):(m + 1)])
                            result1 = any(data in str_text for data in ['装置', '符合', '前端', '恢复'])
                            if result0 == True:
                                if result1 == False:
                                    list2.append([j['x0'] + 2, height - j['y1'], char[m + 1]['x1'] - 2,
                                                  height - char[m + 1]['y0']])
                                    pass
                            break
            for i, j in enumerate(char):
                if j['text'] == '(':
                    for m, n in enumerate(char[(i + 1):]):
                        if n['text'] == ')':
                            m = m + i
                            str_text = ''.join([data['text'] for data in char[(i - 10):i]])
                            result0 = all(data['text'] == ' ' for data in char[(i + 1):(m + 1)])
                            result1 = any(data in str_text for data in ['装置', '符合', '前端', '恢复'])
                            if result0 == True:
                                if result1 == False:
                                    list2.append([j['x0'] - 1, height - j['y1'], char[m + 1]['x1'] + 1,
                                                  height - char[m + 1]['y0']])
                                    pass
                            break
            # =========================list4底线坐标=====================
            for i in page.curves:  # 所有曲线实际是从左下到右上的斜线
                if abs(i['y1'] - i['y0']) >= 1.50:
                    list4.append([i['x0'] + 1, height - i['y1'] + 1, i['x1'] - 1, height - i['y0'] - 1])
                else:  # 修改曲线的类为直线
                    i['object_type'] = 'rect'
                    page.rects.append(i)
            # =========================list3底线坐标=====================
            list_num = []
            for j, r in enumerate(page.rects):  # 去除白色线,去除框只留线
                if r['non_stroking_color'] == (1, 1, 1):
                    list_num.append(j)
                if r['width'] > 1.5 and r['height'] > 1.5:
                    list_num.append(j)
            for index in list_num[::-1]:
                page.rects.pop(index)
            for i_r in page.rects:
                list3.append([i_r['x0'], height - i_r['y1'], i_r['x1'], height - i_r['y0']])
            # =========================表格的坐标=====================
            # 获取页面的所有表格
            tables = page.find_tables()  # 注意.find_tables()放在这里是有原因的
            for table in tables:
                table_x = table.cells[0]
                table_y = table.cells[-1]
            for table in tables:
                table_all()
                table_line()
                table_empty()
                table_brackets()
                white_empty()
                white_brackets()
                list5.extend(list6)
                list5.extend(list7)
            dict1[page_num] = list_pct
            dict0[page_num] = list5
            # list_pct.append((50,50,100,100))
            if len(list_pct) > 0:
                app.tree.insert('', 'end', values=['Page_' + str(page_num + 1), len(list_pct)])
            progressbar()
        except:
            app.tree.insert('', 'end', values=['Page_' + str(page_num + 1), '出错，请人工核对'])
            continue
    app.tree.insert('', 'end', values=['======', '======'])
    pdf_document.close()  # 关闭PDF文件
    pdf.close()


def table_all():
    for i in table.cells:
        list8.extend([[int(list(i)[1]), int(list(i)[3]), int(list(i)[0]), int(list(i)[2])]])

def table_line(): # list5.append(满足条件的线的坐标)
    first_table = table.cells[0]
    for i in list3:  # 上部分横线
        if i[0] > first_table[0] and i[2] < first_table[2] and i[1] > first_table[1] and i[3] < first_table[3]:
            if abs(i[3] - i[1]) <= 1.5:  # 排除竖线y轴间距小于
                if abs(i[2] - i[0]) >= 16.0:  # 排除横线x轴间距大于
                    list5.extend([[int(i[1]) - 10, int(i[3]), int(i[0]), int(i[2])]])

def table_empty(): # list7.append(满足条件的空白的坐标)
    del table.cells[0]
    list_beizhu = []
    list_empty = []
    # =========================取得备注和所有空白坐标=====================
    for i in table.cells:
        list_temp0 = []
        for j in list1:
            if j[0] > list(i)[0] and j[2] < list(i)[2] and j[1] > list(i)[1] and j[3] < list(i)[3]:
                list_temp0.append(j[4])
        if ''.join(list_temp0).replace(' ', '').replace(r'\n', '') == '备注':
            for k in table.cells:
                if list(i)[0] - 0.5 < list(k)[0] < list(i)[0] + 0.5 and list(i)[2] - 0.5 < list(k)[2] < list(i)[2] + 0.5:
                    list_beizhu.append(list(k))
        if len(list_temp0) == 0:
            list_empty.append(list(i))
    # =========================空白减去'备注'和斜线后的坐标=====================
    for i in list_empty:
        if not i in list_beizhu:
            list_temp1 = []
            for j in list4:
                if j[0] > i[0] and j[2] < i[2] and j[1] > i[1] and j[3] < i[3]:
                    list_temp1.append(j)
            if len(list_temp1) == 0:
                list7.extend([[int(list(i)[1]), int(list(i)[3]), int(list(i)[0]), int(list(i)[2])]])



def table_brackets():  # list6.append(满足条件的括号的坐标)
    for i in list2:  # 括号
        list6.extend([[int(i[1]), int(i[3]), int(i[0]), int(i[2])]])


def zhuanhuan(path,pnum):
    global pdf_document,image_cv2_path0,image_cv2_path1
    pdf_document = fitz.open(path)
    page = pdf_document[pnum]  # 获取当前页
    image = page.get_pixmap()  # 将当前页转换为图像
    image_data = image.samples  # 获取图像数据
    image_np = np.frombuffer(image_data, dtype=np.uint8).reshape(image.height, image.width, 3)  # 将图像数据转换为NumPy数组
    if path == pdf_path0:
        image_cv2_path0 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  # 将图像数据转换为OpenCV格式
    if path == pdf_path1:
        image_cv2_path1 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    # cv2.imwrite(r"saved_image.jpg", image_cv2)
    # 在这里可以使用OpenCV对图像进行处理，如显示、保存等操作

def jiaozheng_roi(cts,list_roi,roi_x,roi_y,coord):
    for contour in cts:
        for point in contour:
            x, y = point[0]
            if roi_x - 5 < x < roi_x + 5:
                if roi_y - 5 < y < roi_y + 5:
                    distance = math.hypot(abs(coord[0] - x), abs(coord[1] - y))
                    list_roi.append((distance, (x, y)))
    return list_roi

def jiaozheng():
    global image_cv2_path1
    new_top_left_tuple = (table_x[0], table_x[1])
    new_top_right_tuple = (table_y[2], table_x[1])
    new_bottom_left_tuple = (table_x[0], table_y[3])
    new_bottom_right_tuple = (table_y[2], table_y[3])
    # ==================================================
    img2 = cv2.cvtColor(image_cv2_path1, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(img2 , 250, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2,2), np.uint8) # 腐蚀线框变粗
    binary_erode = cv2.erode(binary,kernel,iterations=1)
    edgs = cv2.Canny(binary, 50, 150)
    edgs_erode = cv2.Canny(binary_erode , 50, 150)
    contours, _ = cv2.findContours(edgs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_erode, _ = cv2.findContours(edgs_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # ==================================================
    top_left = (0, 0)
    top_right = (binary.shape[1], 0)
    buttom_left = (0, binary.shape[0])
    bottom_right = (binary.shape[1], binary.shape[0])
    # ==================================================
    list_tl, list_tr, list_bl, list_br = [[] for i in range(4)]
    for contour in contours_erode:
        x1, y1, w, h = cv2.boundingRect(contour)
        if h > 15:
            # cv2.rectangle(image_cv2_path1, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 1)
            for point in contour:
                x, y = point[0]
                if table_x[1] - 20 < y < table_y[3] + 20:
                    if table_x[0] - 20 < x < table_y[2] + 20:
                        top_left_distance = math.hypot(x - top_left[0], y - top_left[1])
                        list_tl.append((top_left_distance, (x, y)))
                        top_right_distance = math.hypot(top_right[0] - x, y - top_right[1])
                        list_tr.append((top_right_distance, (x, y)))
                        # bottom_left_distance = math.hypot(x - buttom_left[0], buttom_left[1] - y)
                        # list_bl.append((bottom_left_distance, (x, y)))
                        bottom_right_distance = math.hypot(bottom_right[0] - x, bottom_right[1] - y)
                        list_br.append((bottom_right_distance, (x, y)))
    top_left_tuple = min(list_tl, key=lambda x: x[0])
    top_right_tuple = min(list_tr, key=lambda x: x[0])
    #bottom_left_tuple = min(list_bl, key=lambda x: x[0])
    bottom_right_tuple = min(list_br, key=lambda x: x[0])
    # ==================================================
    list_tl = jiaozheng_roi(contours, list_tl, top_left_tuple[1][0], top_left_tuple[1][1], top_left)
    #top_left_tuple = min(list_tl, key=lambda x: x[0])
    list_tr = jiaozheng_roi(contours, list_tr, top_right_tuple[1][0], top_right_tuple[1][1], top_right)
    #top_right_tuple = min(list_tr, key=lambda x: x[0])
    #list_bl = jiaozheng_roi(contours, list_bl, bottom_left_tuple[1][0], bottom_left_tuple[1][1], buttom_left)
    #bottom_left_tuple = min(list_bl, key=lambda x: x[0])
    list_br = jiaozheng_roi(contours, list_br, bottom_right_tuple[1][0], bottom_right_tuple[1][1], bottom_right)
    #bottom_right_tuple = min(list_br, key=lambda x: x[0])
    # ==================================================
    pos1 = np.array(top_left_tuple[1], dtype=np.float32)
    pos2 = np.array(top_right_tuple[1], dtype=np.float32)
    pos4 = np.array(bottom_right_tuple[1], dtype=np.float32)
    M = (pos1 + pos4) / 2
    vec_P3M = M - pos2
    pos3 = M + vec_P3M
    # ==================================================
    pts_src = np.array([top_left_tuple[1], top_right_tuple[1], pos3, bottom_right_tuple[1]],dtype=np.float32)
    points_dst = np.array([new_top_left_tuple, new_top_right_tuple, new_bottom_left_tuple, new_bottom_right_tuple],dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(pts_src, points_dst)
    image_cv2_path1 = cv2.warpPerspective(image_cv2_path1, matrix, (image_cv2_path1.shape[1], image_cv2_path1.shape[0]))
    #score = np.max(cv2.matchTemplate(image_cv2_path0, image_cv2_path1, cv2.TM_CCOEFF_NORMED))
    #if score < 0.25:
        #app.tree.insert('', 'end', values=['Page_' + str(page_num + 1), '本页相似度低，建议人工复核'])
    list9.append((page_num,image_cv2_path1,table_x,table_y))


def click_event(event, x, y, flags, param):  # 检测鼠标点击事件
    global index
    if event == cv2.EVENT_LBUTTONDOWN:
        if 0 < x < 80 and 0 < y < 25:  # 如果点击上一页按钮区域
            index = (index - 1) % len_index
            xianshi(dict_output)
        if 100 < x < 180 and 0 < y < 25:  # 如果点击下一页按钮区域
            index = (index + 1) % len_index
            xianshi(dict_output)
        if 300 < x < 380 and 0 < y < 25:  # 如果点击pdf_path0按钮区域
            for i, j0 in dict_output.items():
                if i == pdf_path0:
                    j0 = {k:j0[k] for k in j0 if k in j1} # 根据j1的key，取j0的key和value
                    list_index = list(j0.items())[index]
                    zhuanhuan(i, list_index[0])
                    for k in list_index[1]:
                        cv2.rectangle(image_cv2_path0, (k[2], k[0]), (k[3], k[1]), (0, 0, 255), 1)
                        cv2.putText(image_cv2_path0, str(k[4]), (k[2], k[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 0)
                    cv2.namedWindow('pdf_path0_result', cv2.WINDOW_NORMAL)
                    cv2.imshow('pdf_path0_result', image_cv2_path0)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()


index = 0
def xianshi(dict):
    global len_index ,image_cv2_path1 ,j1
    for i, j1 in dict.items():
        if i == pdf_path1:
            j1 = {key : value for key, value in j1.items() if len(value) > 0}  # 去除空元素
            list_index = list(j1.items())[index]  # 按照index选取字典
            len_index = len(j1.items())  # 字典长度
            zhuanhuan(i, list_index[0])
            for l in list9:
                if l[0] == list_index[0]:  # 最佳ssim和坐标区域的页码一致
                    image_cv2_path1 = l[1]
                    cv2.rectangle(image_cv2_path1, (int(l[2][0]),int(l[2][1])), (int(l[3][2]),int(l[3][3])), (0, 0, 255), 1)
            for k in list_index[1]:
                top_left = (k[2], k[0])  # 左上角的坐标 (x, y)
                bottom_right = (k[3], k[1])  # 右下角的坐标 (x, y)
                color = (0, 0, 255)  # BGR颜色，这里是红色
                thickness = 1  # 线宽
                cv2.rectangle(image_cv2_path1, top_left, bottom_right, color, thickness)
            # 添加上一页按钮
            cv2.rectangle(image_cv2_path1, (0, 0), (80, 25), (255, 255, 255), -1)
            cv2.putText(image_cv2_path1, "<<<<<<<", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            # 添加下一页按钮
            cv2.rectangle(image_cv2_path1, (100, 0), (180, 25), (255, 255, 255), -1)
            cv2.putText(image_cv2_path1, ">>>>>>>", (100, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            # 添加页数显示
            cv2.putText(image_cv2_path1, 'Page_' + str(list_index[0] + 1), (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            # 添加pdf_path0按钮
            cv2.rectangle(image_cv2_path1, (300, 0), (380, 25), (255, 255, 255), -1)
            cv2.putText(image_cv2_path1, "pdf_path0", (300, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            # 显示
            cv2.namedWindow('pdf_path1_result', cv2.WINDOW_NORMAL)
            cv2.imshow('pdf_path1_result', image_cv2_path1)
            # 设置鼠标点击事件回调
            cv2.setMouseCallback('pdf_path1_result', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def white_empty():
    zhuanhuan(pdf_path0, page_num)
    zhuanhuan(pdf_path1, page_num)
    jiaozheng()
    gray = cv2.cvtColor(image_cv2_path1, cv2.COLOR_BGR2GRAY) # 转换为灰度图像
    # =========================去除像素0=====================
    for i in list5:
        list_result = []
        for j in range(0, 4):
            roi = gray[i[0] - j:i[1] - j, i[2]:i[3]]  # 缩小范围
            _, binary = cv2.threshold(roi, 250, 255, cv2.THRESH_BINARY)  # 二值化处理
            black_pixels0 = np.sum(binary == 0)  # 计算黑色像素的总数
            list_result.append(black_pixels0)
        black_pixels0 = min(list_result)
        i.append(black_pixels0)
        if black_pixels0 <= 5:
            list_pct.append(i)
    for i in list7:
        a = int((i[1] - i[0]) / 2)
        b = int((i[3] - i[2]) / 2)
        m0 = min(a, b, 9) - 3
        list_result = []
        for j in range(0, m0 + 1):
            roi = gray[i[0] + m0:i[1] - m0, i[2] + m0:i[3] - m0]  # 缩小范围
            _, binary = cv2.threshold(roi, 250, 255, cv2.THRESH_BINARY)  # 二值化处理
            black_pixels1 = np.sum(binary == 0)  # 计算黑色像素的总数
            list_result.append(black_pixels1)
        black_pixels1 = min(list_result)
        i.append(black_pixels1)
        #list_pct.append(i)
        #print(i, page_num, "黑色像素数量:", black_pixels1)
        if black_pixels1 <= 5:
            list_pct.append(i)
            #cv2.namedWindow('pdf_path0_result_emtpty', cv2.WINDOW_NORMAL)
            #cv2.imshow('pdf_path0_result_emtpty', roi)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()








def demo0(gray ,i ,gray_path):
    if gray_path == 0:
        roi = gray[i[0]:i[1], i[2]:i[3]]
    if gray_path == 1:
        roi = gray[i[0]:i[1], i[2]:i[3]]
    _, binary = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
    black_pixels = np.sum(binary == 0)
    total_pixels = binary.shape[0] * binary.shape[1]
    black_percentage = (black_pixels / total_pixels) * 100
    data = black_percentage
    return data

def demo1(gray ,i ,gray_path ,j0,j1,rj):
    if gray_path == 0:
        roi = gray[i[0]-rj+j1:i[1]+rj+j1, i[2]+j0:i[3]+j0]
        _, binary = cv2.threshold(roi, 250, 255, cv2.THRESH_BINARY)
    if gray_path == 1:
        roi = gray[i[0]-rj+j1:i[1]+rj+j1, i[2]+j0:i[3]+j0]
        _, binary = cv2.threshold(roi, 220, 255, cv2.THRESH_BINARY)
    return binary

def tiaozheng(i):
    list_fanwei = []
    for r in range(0, 7):
        for j in list8:
            if i[0] - r > j[0] and i[1] + r < j[1] and i[2] > j[2] and i[3] < j[3]:  # y轴扩大范围
                list_fanwei.append(r)
    if list_fanwei == []:
        max_fanwei = 4 # 最下面的页码
    else:
        max_fanwei = max(list_fanwei)
        if max_fanwei > 0:
            max_fanwei = max_fanwei - 1
    return max_fanwei




def white_brackets():
    # 灰度图
    gray0 = cv2.cvtColor(image_cv2_path0, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(image_cv2_path1, cv2.COLOR_BGR2GRAY)
    # =========================去除像素差小于2的括号=====================
    for i in list6:
        value = round(abs(demo0(gray0, i ,0) - demo0(gray1, i ,1)), 2)
        i.append(value)
        if value <= 20.0:
            list_result = []
            tiaozheng(i)
            range_j = tiaozheng(i)
            for j0 in range(-3,4):
                for j1 in range(-3,4):
                    binary0 = demo1(gray0, i, 0 ,0 ,0  ,range_j)
                    binary1 = demo1(gray1, i, 1 ,j0 ,j1 ,range_j)
                    part_score = np.max(cv2.matchTemplate(binary0, binary1, cv2.TM_CCOEFF_NORMED))
                    list_result.append((part_score,binary0,binary1,j0,j1))
            tuple_result=max(list_result,key = lambda x:x[0])
            overlap = cv2.bitwise_or(tuple_result[1],tuple_result[2])
            black_overlap = np.sum(overlap == 0)
            black1 = np.sum(tuple_result[2] == 0)
            if black1 == 0:
                list_pct.append(i)
            else:
                black_percent = black_overlap / black1  # 除以0时候无穷大会出错
                if black_percent >= 0.66:
                    list_pct.append(i)
                    i[4] = black_percent
                    #xianshi2(tuple_result[1], tuple_result[2], str(tuple_result[0]) + str((tuple_result[3], tuple_result[4])))


def xianshi2(b0, b1, value):
    b0 = cv2.resize(b0, (b0.shape[1] * 20, b0.shape[0] * 20), interpolation=cv2.INTER_LINEAR)
    b1 = cv2.resize(b1, (b1.shape[1] * 20, b1.shape[0] * 20), interpolation=cv2.INTER_LINEAR)
    combined_image = cv2.vconcat([b0, b1])
    cv2.putText(combined_image, value, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.imshow('pdf_path1_result_part', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start()

