'''
    Tính độ tương đồng cosine
'''
# -*- coding: utf-8 -*-
import math
import re
import numpy
import search_index


def format_data(search_index_results):
    """
    :param results: list các tài liệu được tìm thấy
    :return: list các từ không trùng [[0],[0,1]]
    """
    kq_tfi = []
    data_out = [] # mảng lưu  tài liệu kể cả q
    kq = []  # mảng lưu các từ đã tách của tất cả các tài liệu
    data_out.append(search_index_results[0][0])
    for i in range(len(search_index_results)):
        for j in range(len(search_index_results[i])):
            if j % 2 == 0:
                i_search_index_results = search_index.word_separation(search_index_results[i][j])  # tách từ thành list
                i_search_index_results = search_index.clearn_stop_word(i_search_index_results)  # xóa stop words
                i_search_index_results = re.findall('\w+', i_search_index_results)  #tách từ thành danh sách
                kq += i_search_index_results #chuyển list thành chuỗi
                kq_tfi.append(i_search_index_results)
            else:
                data_out.append(search_index_results[i][j])
    kq_set = set(kq)  # mảng lưu từ sau khi loại bỏ từ trùng
    return (kq_set, data_out, kq_tfi)


# tfi
def calculated_tfi(kq_set, kq_tfi):
    tfi = []
    for word in kq_set:
        tfi.append(word)
        kq_index = []
        for k in kq_tfi:
            sl = k.count(word)
            kq_index.append(sl)
        tfi.append(kq_index)
    return tfi  # cấu trúc tfi bao gồm [từ,[số lượng từ trong tài liệu kể cả câu truy vấn]]


# dfi
def calculated_dfi(tfi):
    dfi = []
    for i in range(0, len(tfi)):
        if (i % 2 != 0):
            sum = 0
            for counts in range(1, len(tfi[i])):
                if tfi[i][counts] > 0:
                    sum += 1
            dfi.append(sum)
    return dfi


# idfi  = log(n/dfi)
def calculated_idfi(dfi, data_out):
    idfi = []
    for i in range(0, len(dfi)):
        kq = ((len(data_out) - 1) * 1.0) / dfi[i]
        kq1 = math.log10(kq)
        if (kq1 == 0.0):
            kq1 = 0.6
        idfi.append(round(kq1, 4))
    return idfi


# wi = tfi x idfi
def calculated_wi(idfi, tfi):
    wi = []
    tmp = []
    for i in range(1, len(tfi), 2):
        tmp.append(tfi[i])
    tmp_wi = numpy.array(tmp)
    for j in range(len(idfi)):
        wi_kq = tmp_wi[j] * idfi[j]
        wi.append(wi_kq)
    wi = numpy.array(wi)
    items = []  # chứa các mảng có các giá trị của wi theo cột(từng tài liệu)
    shape = wi.shape
    x_shape = shape[0]  # 10
    y_shape = shape[1]  # 4
    for k in range(y_shape):
        item = []  # chứa giá trị của tung tài liệu
        for i_wi in range(x_shape):
            tmp_kq = wi[i_wi][k]
            item.append(tmp_kq)  # giá trị theo tài liệu
        items.append(item)
    return items


# similarity
def similarity(wi, search_index_results):
    ''' Tính độ tương đồng của câu'''
    if len(wi) <= 0:
        print("Array WI NO data!")
        return 0
    else:
        arr = []
        arr_qd = []
        cosin = []
        for i in wi:
            a = 0.0
            for j in i:
                a += math.pow(j, 2)
            arr.append(round(math.sqrt(a), 4))  # tinh q2 va d2
        for k in range(1, len(wi)):  # tinh q * d
            sum_qd = 0.0
            for h in range(len(wi[0])):
                sum_qd += wi[0][h] * wi[k][h]
            arr_qd.append(sum_qd)

        for m in range(len(arr_qd)):  # tinh goc cosin = q*d / (q2 * d2)
            tmp = []
            rs = arr_qd[m] / (arr[0] * arr[m + 1])
            tmp.append(search_index_results[m + 1])
            tmp.append(round(rs, 4))
            cosin.append(tmp)
        # format arr cosin : [['câu hỏi', giá trị cosin], ['câu hỏi', giá trị cosin]]
        return cosin


def choose_document(cosin):
    rs = sorted(cosin, key=lambda cosin: cosin[1], reverse=True)
    i = 0
    choose = []
    while i <= math.ceil(len(rs) / 2):
        choose.append(rs[i])
        i += 1
    return choose


def print_document(choose_doc):
    for i in range(len(choose_doc)):
        for j in range(len(choose_doc[i])):
            if j == 1:
                print('====================================\n')
                print(choose_doc[i][j])
            else:
                print('====================================\n')
                print(choose_doc[i][j][1])


def output():
    results = search_index.search_index_main01()
    if results == 0:
        print("Không có kết quả phù hợp với câu hỏi!")
    elif len(results) <= 2:
        for j in range(len(results)):
            if j == 0:
                print('Tiền xử lý câu truy vấn: ', results[j][0])
            else:
                print('===================================\n')
                print(results[j][1])
    else:
        kq_set, data_out, kq_tfi = format_data(results)
        tfi = calculated_tfi(kq_set, kq_tfi)
        dfi = calculated_dfi(tfi)
        idfi = calculated_idfi(dfi, data_out)
        wi = calculated_wi(idfi, tfi)
        cosin = similarity(wi, results)
        choose_doc = choose_document(cosin)
        print('Các Document được chọn là: ')
        print_document(choose_doc)


# GUI
def format_output(query):
    results = search_index.search_index_main(query)
    if results == 0:
        print("Không có kết quả phù hợp với câu hỏi!")
        return 0
    elif len(results) <= 2:
        for j in range(len(results)):
            if j == 0:
                print('Tiền xử lý câu truy vấn: ', results[j])
            else:
                print(results[j])
    else:
        print('Số lượng document sau khi tìm kiếm là: %d' % (len(results) - 1))
        print(results)
        kq_set, data_out, kq_for_tfi = format_data(results)
        tfi = calculated_tfi(kq_set, kq_for_tfi)
        dfi = calculated_dfi(tfi)
        idfi = calculated_idfi(dfi, data_out)
        wi = calculated_wi(idfi, tfi)
        cosin = similarity(wi, results)
        choose_doc = choose_document(cosin)
        print('Các Document được chọn là: ')
        print_document(choose_doc)
        return choose_doc


if __name__ == '__main__':
    output()
