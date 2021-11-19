import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import peakutils
from xml.etree.ElementTree import Element, dump, ElementTree
from collections import Counter 
import boto3
import os
from PIL import Image
from datetime import datetime
import glob 
import csv

from flask_login import current_user
from apps.database.models import Ecg, User

bucket_name = 'capstone-heartbeat-s3'

def no(result_c, x):
    sum_c = 0
    count_c = 0 # 없어진 개수
    for i in range(len(result_c)-1):
        sum_c += result_c[i+1] - result_c[i] # rri를 다 더함.
    
    if len(result_c) ==1:
        sum_c = sum_c
    else:
        sum_c = sum_c//(len(result_c)-1) # rri를 개수 만큼 나눔
    if result_c[0] - sum_c*0.5 <= 0: # 맨 첫 피크에서 다 더한 것의 0.06을 곱한 것을 뺀 값이 0 혹은 음수면 지우기
        result_c=np.delete(result_c, [0]) 
        count_c += 1 # 지웠으니까 개수 증가
        
    if result_c[len(result_c)-1] +sum_c*0.5 >=len(x): # 맨 마지막이 그러면 지우기
        result_c=np.delete(result_c, [len(result_c)-1])
        count_c += 1
        
    return count_c, result_c


def box(x):
    number=[]
    result = peakutils.indexes(x, thres=0.75, min_dist=300)
    if len(result) < 15:
        result = peakutils.indexes(x, thres=0.45, min_dist=300)
    for i in range(len(result)):
        if 0.1>=x[result[i]]:
            number.append(i)
    result=np.delete(result, number)
    nono, result = no(result, x)

    sub, tot = [], []
    for i in range(len(result)-1):
        sub.append(result[i+1]-result[i])
    avg = np.average(sub)//2
    for i in range(len(result)):
        if result[i]-avg < 0:
            tot.append([0, int(result[i]+avg)])
        elif result[i]+avg > len(x):
            tot.append([int(result[i]-avg), len(x)])
        else:
            tot.append([int(result[i]-avg), int(result[i]+avg)])

    return tot, result


def draw(x, peak_num, a, r, second, third, end, name_n, num_id, dates):

    peak_set = find_peak(x, r, second, third, end,a, num_id)
    if peak_set == 0:
        return 0, 0
    else:
        plt.plot(x, 'k')
        plt.xticks(np.arange(r-len(x)//2+1, r+len(x)//2, step=(r-a)//2))
        plt.axvline(x = second, color='lightgray', linewidth=1)
        plt.axvline(r, color='lightgray', linewidth=1.5)
        plt.axvline(x = third, color='lightgray', linewidth=1)
        if peak_set[0]:
            plt.axhline(y = x[peak_set[0]], color='r', linewidth=1, label='P')

        if peak_set[1]:
            plt.axhline(y = x[peak_set[1]], color='b', linewidth=1, label='Q')

        if peak_set[3]:
            plt.axhline(y = x[peak_set[3]], color='g', linewidth=1, label='S')

        if peak_set[4]:
            plt.axhline(y = x[peak_set[4]], color='c', linewidth=1, label='T')

        plt.legend(loc='upper right')
        plt.title(dates[num_id] + ' ' + str(peak_num) +' Peak')
        peak_num+=1
        return peak_num, peak_set
        

def find_peak(x, r, second, third, end, a, num_id, dates):
    p, q, s, t= [], [], [], []
    q_idx = 0
    for i in range(r-1, second, -1):
        if x[i] - x[i-1] < 0:
            if x[i] + 0.2 > x[r] or x[i] > 0:
                continue
            else:
                q.append(i)
    if len(q) >= 2:
        if x[q[0]] > x[q[1]]:
            q_idx = q[1]
        
            
    if q_idx == 0:
        for i in range(r-1, a, -1):
            if x[i] - x[i-1] == 0:
                if x[i] > 0:
                    continue
                else:
                    q.append(i)    
            if q:
                q_idx = q[0] 
                break             
                

    for i in range(q_idx-1, second, -1):
        if x[i] - x[i-1] > 0:
            p.append(i)
            
    p_idx = []
    if p:
        pp_idx = []
        p_idx = x[x == np.max(x[p])]

        p_idx = p_idx.index.values
        for i in range(len(p_idx)):
            if p_idx[i] < q_idx:
                pp_idx.append(p_idx[i])
        if pp_idx:
            p_idx = pp_idx[-1]               
           
            
                    
    for i in range(r, third+1):
        if x[i] - x[i+1] < 0:
            if x[i] + 0.2 > x[r]:
                continue
            else:
                s.append(i)  
        if s:
            s_idx = s[0]
            break

    if not s:
        s_idx = r
     
    
    for i in range(s_idx, end):
        if x[i] - x[i+1] > 0:
            t.append(i)  
            

    t_idx = x[x == np.max(x[t])]
    t_idx = t_idx[:1].index.values            
    if s_idx == r:
        s_idx = []

    if t_idx:
        t_idx = t_idx[0]
    peak_set = [p_idx, q_idx, r, s_idx, t_idx, dates[num_id]]

    return peak_set


def average(raw, box_size):
    bbox = np.ones(box_size)/box_size
    raw_smooth = np.convolve(bbox, raw, mode='same')
    return raw_smooth


def median(raw, box_size):
    raw_smooth = ndimage.median_filter(raw, box_size)
    return raw_smooth


def onoffset(x, start,end,  p_peak, q_peak, nn, nname, dates):
    o=0
    pon_idx, poff_idx = 0, 0
    inflexion_point_1 = 0
    df = x.values.tolist()
    df = pd.DataFrame(df, columns = ['value'])
    pvc = False
    a=average(df['value'],10)
    df=pd.DataFrame(a)
    df.columns = ['value']
    df.index = x.index
    if not p_peak or not q_peak:
        o=0
    else:
        try:
            np.diff(a[start-start+20:q_peak-start-10]).argmin()
            inflexion_point_1 = np.diff(a[start-start+20:q_peak-start-10]).argmin()
            pvc = False
        except ValueError:
            pvc = True
            pass
        if inflexion_point_1 != 0:
            
            if inflexion_point_1<75:
                try:
                    np.diff(a[75:q_peak-start-10]).argmin()
                    inflexion_point_1 = np.diff(a[75:q_peak-start-10]).argmin()
                    inflexion_point_2 = np.diff(a[75+inflexion_point_1:q_peak-start-10]).argmax()
                    inf3=abs(inflexion_point_2+inflexion_point_1-50-inflexion_point_1+75)//2
                    if inflexion_point_1>inflexion_point_2:
                        poff_idx = inflexion_point_1+start+inf3+75
                        pon_idx = inflexion_point_1-50+inflexion_point_2+start-inf3+75
                    elif inflexion_point_1<inflexion_point_2:
                        poff_idx = inflexion_point_1+start-inf3+75
                        pon_idx = inflexion_point_1-50+inflexion_point_2+start+inf3+75
                    pvc = False
                except ValueError:
                    pvc = True
                    pass


            else:
                inflexion_point_2 = np.diff(a[inflexion_point_1-50:inflexion_point_1]).argmax()
                inf3=abs(inflexion_point_2+inflexion_point_1-50-inflexion_point_1+20)//2
                if inflexion_point_1>inflexion_point_2:
                    poff_idx = inflexion_point_1+start+inf3+20
                    pon_idx = inflexion_point_1-50+inflexion_point_2+start-inf3
                elif inflexion_point_1<inflexion_point_2:
                    poff_idx = inflexion_point_1+start-inf3+20
                    pon_idx = inflexion_point_1-50+inflexion_point_2+start+inf3
        else:
            pvc=True
    if not p_peak:
        pvc = True
    return pon_idx, poff_idx, pvc


def PC(tmp, result, x, a, b, p_peak, q_peak, nn, nname, n, plot_num, dates):
    r_peak = result
    inter = []
    pc = False
    pac = False
    pvc = False
    plot_idx = 'no'
    plot_set = [_ for _ in range(len(result-1))]
    for i in range(1, len(r_peak)):
        inter.append(r_peak[i] - r_peak[i-1])
    rri_avg = np.average(inter)
    pv_all_cnt = []
    count_pc = 0
    for i in range(len(inter)):
        if (inter[i]-rri_avg < 0) and (abs(inter[i]-rri_avg) >= rri_avg*n): # 0.1
            count_pc += 1
            pv_all_cnt.append(i)
    
    if pv_all_cnt:
        for j in range(len(pv_all_cnt)):
            if plot_num == pv_all_cnt[j]:
                plot_idx = 'yes'

    if count_pc != 0:
        pc = True
        pon_idx, poff_idx, pvc = onoffset(x, a, b, p_peak, q_peak, nn, nname, dates)
        if pvc == False:
            pac = True
    else:
        pon_idx, poff_idx, pvc = onoffset(x, a, b, p_peak, q_peak, nn, nname, dates)
        pc = False
        pvc = False 
       
        
    r_list=np.array(tmp[result])
    r_avg=r_list.mean()
    for j in range(len(r_list)):
        if abs(r_avg-r_list[j]) >= 0.5:
            if pc == True:
                pvc = True
                
    if pc == True:  
        if not p_peak:
            pvc  = True 
    return pc, pac, pvc, pon_idx, poff_idx, plot_idx

def width(all_peak):
    Q, T = [], []
    pvc_qrs = []
    pvc = False
    for i in range(len(all_peak)):
        if not all_peak[i][1] or not all_peak[i][3]:
            continue
        else:
            Q.append(all_peak[i][1])
            T.append(all_peak[i][3])
    diff = np.subtract(T,Q)
    qrs_avg = np.average(diff)
    for i in range(len(diff)):
        if diff[i] - qrs_avg >= qrs_avg * 0.66:
            pvc_qrs.append(i)
    if pvc_qrs:
        pvc = True
    return pvc, pvc_qrs


def main2(data2, dates, n):
    all_peak_all = []
    name_n = 1
    tmp = data2[0]
    total, result = box(tmp)
    num, peak_num=0, 1
    plot_num = 0
    plot_all = []
    pac_plot = []
    pvc_plot = []
    all_peak = []
    for a, b in total:
        x = []
        x = tmp[a:b]
        r = result[num]
        second = (r+a)//2
        third = (r+len(x)//4)
        end = x.last_valid_index()
        peak_set = find_peak(x, r, second, third, end,a, 0, dates)
        if peak_set == 0 and peak_num == 0:
            if peak_num == 0:
                peak_num = 1
        else:
            pc, pac, pvc, pon_idx, poff_idx, plot_set = PC(tmp, result, x, a, b, peak_set[0], peak_set[1], 0, peak_set[-1], n, plot_num, dates)
            peak_set = peak_set + [pon_idx, poff_idx, pc, pac, pvc, plot_set]
            all_peak_all.append(peak_set)
            all_peak.append(peak_set)
            if peak_num == 0:
                peak_num = 1
            if plot_set == 'yes':
                plot_all.append([a, b])
            if pac == True:
                pac_plot.append([a, b])
            if pvc == True:
                pvc_plot.append((a, b))

        num+=1
        plot_num +=1
        peak_num += 1
        
    pvc_sub, pvc_qrs = width(all_peak)
    if pvc_qrs and (pvc and pvc_sub):
        if pc == True: 
            for j in range(len(pvc_qrs)):
                pvc_plot.append((total[pvc_qrs[j]][0], total[pvc_qrs[j]][1]))
    
    plt.plot(tmp, 'k')
    if plot_all:
        for j in range(len(plot_all)):
            plt.plot(tmp[plot_all[j][0]:plot_all[j][1]], color = 'r')
    if pvc_plot:
        if len(set(pvc_plot)) >=3:
            for j in range(len(pvc_plot)):
                plt.plot(tmp[pvc_plot[j][0]:pvc_plot[j][1]], color = 'b')
        
    name_n += 1
    plt.plot(tmp, 'k')
    image_now = datetime.now()
    image_number = image_now.isoformat()[2:4]+ image_now.isoformat()[5:7] + image_now.isoformat()[8:10] + image_now.isoformat()[11:13] + image_now.isoformat()[14:16] + image_now.isoformat()[17:19]
    my_path = os.path.abspath('/Users/Pc/vsc/Backend-Flask/static/tmp_images')
    #my_path = os.path.abspath('/home/ubuntu/Backend-Flask/static/tmp_images')
    my_file = 'graph' + str(image_number)+'.png'
    s3 = boto3.client('s3')

    plt.savefig(os.path.join(my_path, my_file), dpi=80)
    #s3.upload_file('C:/Users/Pc/vsc/Backend-Flask/static/tmp_images/graph'+ str(image_number) +'.png', bucket_name, my_file)
    #os.remove('C:/Users/Pc/vsc/Backend-Flask/static/tmp_images/graph'+ str(image_number) +'.png')

    s3.upload_file('/Users/Pc/vsc/Backend-Flask/static/tmp_images/graph'+ str(image_number) +'.png', bucket_name, my_file)
    os.remove('/Users/Pc/vsc/Backend-Flask/static/tmp_images/graph'+ str(image_number) +'.png')

    image_url = 'https://capstone-heartbeat-s3.s3.ap-northeast-2.amazonaws.com/graph'+ str(image_number) +'.png'
    pvc_cnt = 0
    all_peak_all = pd.DataFrame(all_peak_all, columns = ['P', 'Q', 'R', 'S', 'T', 'id', 'ponset', 'poffset', 'pc', 'pac', 'pvc', 'plot_idx'])
    for i in range(len(all_peak_all)):
        if all_peak_all['pc'][i] == True:
            pc = True
        if all_peak_all['pac'][i] == True:
            pac = True
        if all_peak_all['pvc'][i] == True:
            pvc_cnt += 1
    if pvc_cnt >=3:
        pvc = True
        pac = False
    plt.close()
    return pc, pac, pvc, image_url


def calculatePc(data2, dates):
    pc, pac, pvc, image_url = main2(data2, dates, 0.7)

    return pc, pac, pvc, image_url