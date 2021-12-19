def find_num(text, pos):
  num = 1
  while text[pos-num].isnumeric():
    num += 1
  return num - 1
def quadratic_string(text):
  temp = text.replace(" ", "")
#  if len(temp) <= 12:
#    temp = temp.replace("^", "**")
#    return temp[:temp.find("=")]
#  else:
  str_x = "x"
  pos = temp.find(str_x)
  res = ""
  if temp[pos - 1].isnumeric():
    num = find_num(temp, pos)
    if pos <= num:

      num = pos
      res = temp[pos - num:pos] + temp[pos:pos + 3]
    else:
      res = temp[pos - num:pos] + temp[pos:pos + 3]
  else:
    res = temp[pos:pos + 3]
  if temp[pos + 4].isnumeric():
    res += temp[pos + 3:temp.find("=")]
  return res
# Hệ phương trình (phương trình tuyến tính, 2 ẩn và 3 ẩn)
# -- stringInput = "3*x + y = 2; 2*x + 3*y - 10 + z = 0; -4*x -2*y + 7*z = 10; HPT@Giai"
# Tìm n để phép chia biểu thức là số nguyên (Dạng ước bội)
# -- stringInput = "((x**2 + 1) * (x**3 + 2))/ (x - 5); UocBoi@TimN_DeNguyen"
# Các phép toán trong đa thức (phép nhân: nằm trong tập số thực; phép chia: chỉ chia được cho mẫu bậc 1, tử bao nhiêu cũng được)
# -- stringInput = "x**2 + 4*x + 5*x + 2*x*y; x + 1 + x*y; DaThuc@NhanDaThuc"
# -- stringInput = "x**2 + 4*x + 5*x; x + 1; DaThuc@ChiaDaThuc"

# str ='3x + y = 2; 2x + 3y - 10 + z = 0; -4x -2y + 7z = 10; HPT@Giai'
str = '((x^2 + 1) * (x^3 + 2))/ (x - 5); UocBoi@TimN_DeNguyen'
# str = 'x^2 + 4x + 5x + 2xy; x + 1 + xy; DaThuc@NhanDaThuc'

# print(quadratic_string(str))
# Convert x^ to x** || x or 1x to *x
# final_str =quadratic_string(str)
# replace x^ by x**
str = str.replace("^", "**")
# Convert string to list to modify the value
final_str =list(str)
#loop all the list to find x
for i in range(1,len(final_str)):
  if final_str[i] == "x" :

    # check if  1x to convert to x:  1x =>x

    if (final_str[i-1].isnumeric() ==True and final_str[i-1] =="1" and final_str[i-2].isnumeric() ==False ): # check if case 121x , 531x
      final_str[i-1] = ""

    # change x to z if it like 2312x => 2312z

    elif (final_str[i-1].isnumeric() ==True and (final_str[i-2].isnumeric() ==True or final_str[i-1].isnumeric() ==True )):
      final_str[i] = '_'
  if final_str[i] == "y":
    if (final_str[i - 1].isnumeric() == True and final_str[i - 1] == "1" and final_str[
      i - 2].isnumeric() == False):  # check if case 121x , 531x
      final_str[i - 1] = ""

    # change x to z if it like 2312x => 2312z

    elif (final_str[i - 1].isnumeric() == True and (
            final_str[i - 2].isnumeric() == True or final_str[i - 1].isnumeric() == True)):
      final_str[i] = '&'
  # check if  1x to convert to x:  1x =>x



# convert to string
final_str = "".join(final_str)
print(final_str)
#replace z to *x
final_str =final_str.replace("_","*x")
final_str =final_str.replace("&","*y")

print((final_str))


