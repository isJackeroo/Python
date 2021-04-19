import random
low="abcdefghijklmnopqrstuvwxyz"
upp="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num="0123456789"
sym="!@#$%^&*"

all=low+upp+num+sym
length=10   #修改密码长度
password="".join(random.sample(all,length))
print(password)
