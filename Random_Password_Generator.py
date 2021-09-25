'''
#简单生成全英文大小写随机密码：
import string, random
length = int(input("The Password Length You Want to Set:"))
for i in range(1):
    RandomPassword = ''.join(random.sample(string.ascii_letters,length))
    print(RandomPassword)

'''

#生成包含大小写字母、英文标点符号的自定义长度随机密码
import string, random
ascii_words = string.ascii_letters
digital_num = string.digits
english_pun = string.punctuation
all = ascii_words + digital_num + english_pun
length = int(input("The Password Length You Want to Set:"))
password = ''.join(random.sample(all,length))
print(password)
