#-*- encoding: utf-8 -*-
import sys, string

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

primary = [0.618,0.786,1.27,1.618]
secondary = [0.236,0.382,0.50,1.0,2.0,2.24,2.618,3.14,4.236]
Fibonacci = [0.236,0.382,0.50,0.618,0.786,1.0,1.272,1.618,2.0,2.24,2.618,3.14,4.236]
# 注意：Fibonacii 数列长度对后面计算有影响，因此增加比率数据应修改后面内容BackTrace_Ratio

def isNum(value):
    try:
        float(value)+1.0
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception, e:
        return False
    else:
        return True

# 参数为用户输入，0.618+A+B+C，分离出ABC
def get_fibonacci_paras(content):
    paras = content.split('+')
    return paras

# 检查用户输入参数是否有效
def check_paras_valid(paras):
    para_num = len(paras)
    
    if (para_num<3 or para_num>4):
        return '参数数量错误。接受2或三个参数，如0.618+A+B或0.618+A+B+C'
    else:
        return 1
    for para in paras:
        if not isNum(para):
            return 'Bad Para 【参数必须为数字】'
       
# 获得 AB 腿的绝对长度
def Leg_AB(A,B):
	if A>B:
		return A-B
	else:
		return B-A

# 获得 AB 腿回退的可能值数列
def BackTrace(A,B):
	back_leg = []
	Position_C = []
	FibPos = []
	leg_ab = Leg_AB(A,B) # 获得AB腿长度
	for r in Fibonacci:
		back_leg.append(leg_ab * r)  # 按照斐波那契比率计算回退距离
	
    # 根据看涨还是看跌模式计算C的点位
	if A>B:
		for leg in back_leg:
			Position_C.append(round(B+leg,2))
	else:
		for leg in back_leg:
			Position_C.append(round(B-leg,2))

	for pc in Position_C:
		if pc>0:
			list_index = Position_C.index(pc)
			aPair = [Fibonacci[list_index], pc]
			FibPos.append(aPair)

	return FibPos


# 已知ABC三点，获得C相对AB的回退比率
def BackTrace_Ratio(A,B,C):
	leg_bc = Leg_AB(B,C)  # 获得AB腿长度
	backleg_ab = BackTrace(A,B)  # 获得AB腿回退的长度
	backleg_ab.append(leg_bc)
	backleg_ab.sort()  # 排序

	count = 0
	for leg in backleg_ab:
		if leg==leg_bc:
			if count==0:
				return Fibonacci[0]  # 最小
			elif count==13:  # Fibonacci比率数列中有13个值
				return Fibonacci[12]  # 最大
			elif abs(backleg_ab[count-1] - leg_bc)-abs(backleg_ab[count+1] - leg_bc)>0:
				return Fibonacci[count-1]  # 接近前一值
			else:
				return Fibonacci[count]  # 接近后一值
		count = count + 1

	return 'Error: 错误的回退值！'

# 根据AB=CD及扩展模式获得CD腿
def Trade_Model_ABeqCD(A,B,C):
	leg_ab = Leg_AB(A,B)
	leg_cd = []
	Position_D = []
	FibPos = []
	for r in Fibonacci:
		leg_cd.append(leg_ab * r)
	if A>B:
		for leg in leg_cd:
			Position_D.append(round(C-leg,2))
	else:
		for leg in leg_cd:
			Position_D.append(round(C+leg,2))

	for pd in Position_D:
		if pd>0:
			list_index = Position_D.index(pd)
			aPair = [Fibonacci[list_index], pd]
			FibPos.append(aPair)

	return FibPos



def fibonacci_predicted(content):
    paras = get_fibonacci_paras(content)
    para_num = len(paras)
    isValid = check_paras_valid(paras)
    if isValid==1:
        if para_num == 3:
            A = float(paras[1])
            B = float(paras[2])
            PC = BackTrace(A,B)
            return PC
        if para_num == 4:
            A = float(paras[1])
            B = float(paras[2])
            C = float(paras[3])
            PD = Trade_Model_ABeqCD(A,B,C)
            return PD
        
        return '参数错误！'
    else:
        return isValid
        


