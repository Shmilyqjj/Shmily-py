"""
 *天猫双十一大促营销活动，某用户获得了两张满m元减优惠券，用户已经挑选了n件商品备选，价格分别为 x0, … , x(n-1)。
 * 假设满减优惠券无法叠加使用，需要分开下两单，一单可以有多件商品，且商品只能在上述n个备选商品内选择。
 *请问用户最少需要花费多少钱才能把这两张优惠券都花出去。输出结果保留1位小数。如果不存在合适方案则输出-1.0。
 *
 * 输入:
 * 每组测试数据第一行为1个数字m,  ( 1<= m <=100000， m为整数 )。
 * 第二行有n个数字，表示n个备选商品的价格xi，且（ 1<=xi<=100000， xi为整数）。
 * 举例来说上图的输入如下：
 * 300
 * 200 50 50 251 251
 * 输出:
 * 输出用户为了把两张优惠券都用掉，最少花费的金额。输出结果保留1位小数。
 * 输入范例:
 * 300
 * 200 50 50 251 251
 * 输出范例:
 * 602.0
"""
m = int(input())
n = input()
money = n.split(' ')
length = len(money)
for i in range(length):
    money[i] = int(money[i])
money = sorted(money)
total_money = 0
for i in range(length):
    total_money = total_money + money[i]
if total_money < m*2:
    print(-0.1)
else:
    count = 0
    for i in range(length,0):
        if (m*2 - money[i])>0:
            count = count + money[i]
        else:
            for j in range(length):
                if money[i] + count >= m*2:
                    print(count)
                else:
                    print(count+money[i])

