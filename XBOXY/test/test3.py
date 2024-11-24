import re

text = "[Microsoft_Hit][MC][XGP][Banned][1]pstewart03@hotmail.com:Devany08 |Name:xk_0g7Qh_1110 [BanTime:27d 19h 1m 59s] SW:1 BW:1"

# 正则表达式
pattern = r"([\w\.\-]+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}):([^\s,]+)"

# 查找所有符合的邮箱和密码
matches = re.findall(pattern, text)

# 输出结果
for email, password in matches:
    print(f"Email: {email}, Password: {password}")
