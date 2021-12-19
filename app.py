from chatbot import chatbot
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import sympy as sp
import PhuongTrinh
import ToanDaThuc
import HePhuongTrinh
import UocBoi
import queue
import os

app = Flask(__name__)
# run_with_ngrok(app)
app.static_folder = 'static'

current_step = 0
global_queue_step = []
false_text = ""

@app.route("/")
def home():
    return render_template("index.html")
def find_num(text, pos):
  num = 1
  while text[pos-num].isnumeric() or text[pos-num] == "/":
    num += 1
  return num - 1
def quadratic_string(text):
  temp = text.replace(" ", "")
  if len(temp) <= 12: return temp[:temp.find("=")]
  else:
    str_x = "x^"
    pos = temp.find(str_x)
    res = ""
    if temp[pos-1].isnumeric():
      num = find_num(temp, pos)
      if pos <= num : 
        num = pos
        res = str(temp[pos-num:pos]) + str(temp[pos:pos+3])
      else: 
        res = str(temp[pos-num:pos]) + str(temp[pos:pos+3])
    else:
      res = str(temp[pos:pos+3])
    if temp[pos+4].isnumeric():
      res += str(temp[pos+3:temp.find("=")])
    return res
def change_back(str):

	final_str = str.replace("^", "**")

	final_str =list(final_str)

	#----------------#
	#loop all the list to find x
	for i in range(1,len(final_str)):
		if final_str[i] == "x":
		# check if  1x to convert to x:  1x =>x
			if ((final_str[i-1].isnumeric() ==True and final_str[i-1] =="1" and final_str[i-2].isnumeric() ==False)): # check if case 121x , 531x
				final_str[i-1] = ""
				continue
		# yx, mx
			elif final_str[i-1] =='y' or final_str[i - 1] == 'm' or (final_str[i-1].isnumeric() ==True and((final_str[i-2]).isnumeric() ==True or final_str[i-1].isnumeric()==True)):

				final_str[i] ='*' +final_str[i]
		# xy, my
		if final_str[i] == "y":
			if (final_str[i - 1].isnumeric() == True and final_str[i - 1] == "1" and final_str[i - 2].isnumeric() == False):  # check if case 121y , 531y
				final_str[i - 1] = ""
				continue
			elif final_str[i-1] =='x' or final_str[i - 1] == 'm' or final_str[i-1] =='a'or(final_str[i-1].isnumeric() ==True and((final_str[i-2]).isnumeric() ==True or final_str[i-1].isnumeric()==True)):
				final_str[i] = '*' + final_str[i]
		if final_str[i] == "m":
			if (final_str[i - 1].isnumeric() == True and final_str[i - 1] == "1" and final_str[i - 2].isnumeric() == False):  # check if case 121m , 531m
				final_str[i - 1] = ""
				continue
			elif final_str[i-1] =='x'or final_str[i - 1] == 'y' or(final_str[i-1].isnumeric() ==True and((final_str[i-2]).isnumeric() ==True or final_str[i-1].isnumeric()==True)):

				final_str[i] ='*' +final_str[i]


	for i in range(1, len(final_str)-1):
	# detect ')'
		if final_str[i] == ")":
			if final_str[i + 1].isnumeric() == True or final_str[i + 1] =='x' or final_str[i + 1] == 'y' or final_str[i + 1] == 'm':
				final_str[i+1] ="*" +final_str[i+1]
	# detect '('
		if final_str[i] == '(':
			if final_str[i-1].isnumeric() == True:
				final_str[i] ="*" +final_str[i]
			else: 
				continue
	# convert to string
	final_str = "".join(final_str)
	return final_str
def XacDinhVaNhanDang(inputString: str):
	tempList = inputString.split(";")
	term = tempList[:len(tempList)-1]
	types = tempList[-1].strip()

	return term, types

def Run(term_input:list, types_input:str):
	sentence = ""
	baiToan = None
	domain = None
	first = True
	workQueue = []
	workQueue.append((term_input, types_input, domain, sentence))
	global current_step 
	current_step = 0
	global false_text

	while not len(workQueue) == 0:
		currentWork = workQueue.pop()
		term, types, domain, sentence = currentWork[0], currentWork[1], currentWork[2], currentWork[3]

		if first:
			types, baiToan = types.split("@")
			first = False
			print("Term run: ",term)
		# Check type
		if types == "Abort":
			global_queue_step.append(sentence)
			# print(sentence)
			break
		if types == "Done":
			global_queue_step.append(sentence)
			# print(sentence)
			continue
		if types == "Explain":
			# print(sentence)
			if term:
				global_queue_step.append(str(sentence)+"<br>" + str(term) )
				# print(term)
			else: 
				global_queue_step.append(sentence)
			# t = input("---------------- Nhấn phím để tiếp tục ----------------")
			continue
		if types == "Explain_Question":
			if term:
				global_queue_step.append(str(sentence)+"<br>"+ str(term) )
				# print(term)
			else: 
				global_queue_step.append(sentence)

			# print("Bạn có muốn giải thích phần trên không? (Yes/No)")
			vaildResponse = {"Yes", "yes", "y", "No", "no", "n"}
			accept = {"Yes", "yes", "y"}

			# while True:
			# # 	response = input()
				
			# 	if response in vaildResponse:
			# 		break
			# 	else:
			# 		print("Bạn phải nhập vào Yes hoặc No. Xin bạn hãy nhập lại:")
			response = "Yes"
			if response in accept:
				listEq = currentWork[4]
				types, baiToan = currentWork[5].split("@")
			else:
				continue #TAB
			if types == "DaThuc" and baiToan == "ChiaDaThuc":
					# Chỉ nhận 2 phương trình
				if len(listEq) != 2:
					false_text = "Số phương trình không đúng như dự tính."
					print("Số phương trình không đúng như dự tính. <Debug>")
					exit(0)

				solver = ToanDaThuc.DaThuc()
				solver.Reset()
				_, isVaild = solver.PassTerm(listEq)

				# Nếu không vaild thì sai chỗ nào đó
				if not isVaild:
					false_text = "Sai phần pass đa thức."
					print("Sai phần pass đa thức. <Debug>")
					exit(0)

				workList = solver.ChiaDaThuc()
				# Thêm vào queue
				for work in reversed(workList):
					workQueue.append(work)
				
			elif types == "PhuongTrinh" and baiToan == "Giai":
				# Chỉ nhận 1 phương trình
				if len(listEq) != 1:
					false_text = "Số phương trình không đúng như dự tính."
					print("Số phương trình không đúng như dự tính. <Debug>")
					exit(0)

				solver = PhuongTrinh.PT()
				solver.Reset()
				_, isVaild = solver.PassTerm(listEq[0])

				# Nếu không vaild thì sai chỗ nào đó
				if not isVaild:
					false_text = "Sai phần pass đa thức."
					print("Sai phần pass đa thức. <Debug>")
					exit(0)

				workList = solver.GiaiPT()
				# Thêm vào queue
				for work in reversed(workList):
					workQueue.append(work)
			continue

		if types == "UocBoi":
			# Chỉ có 1 biểu thức
			if len(term) > 1:
				sentence = "Xin lỗi bạn nhưng bài này mình chỉ có thể làm được với 1 biểu thức mà thôi."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue
			if len(term) == 0:
				sentence = "Mình cần 1 đa thức để giải dạng này, bạn kiểm tra lại xem có nhập sai chỗ nào không."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Kiểm tra điều kiện input hợp lệ
			solver = UocBoi.UocBoi()
			solver.Reset()
			results, isVaild = solver.PassTerm(term[0])
			if not isVaild:
				for work in reversed(results):
					workQueue.append(work)
				continue

			# Lấy các bước giải
			if baiToan == "TimN_DeNguyen":
				workList = solver.TimN_DeNguyen()
			else:
				sentence = "Xin lỗi bạn mình không làm được bài này."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Thêm vào queue
			for work in reversed(workList):
				workQueue.append(work)

		elif types == "HPT":
			if len(term) == 0:
				sentence = "Mình cần tối thiểu 2 phương trình để giải dạng này, bạn kiểm tra lại xem có nhập sai chỗ nào không."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			solver = HePhuongTrinh.HPT()
			solver.Reset()
			# Kiểm tra điều kiện input hợp lệ
			results, isVaild = solver.PassTerm(term)
			if not isVaild:
				for work in reversed(results):
					workQueue.append(work)
				continue

			# Lấy các bước giải
			if baiToan == "Giai":
				workList = solver.GiaiHPT()
			else:
				sentence = "Xin lỗi bạn mình không làm được bài này."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Thêm vào queue
			for work in reversed(workList):
				workQueue.append(work)

		elif types == "DaThuc":
			# Phải có nhiều hơn 2 đa thức
			if len(term) < 2:
				sentence = "Xin lỗi bạn nhưng bài này mình cần có tối thiểu 2 đa thức để giải."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Kiểm tra điều kiện input hợp lệ
			solver = ToanDaThuc.DaThuc()
			solver.Reset()
			print("solver list:",solver.listTerm)

			results, isVaild = solver.PassTerm(term)
			if not isVaild:
				for work in reversed(results):
					workQueue.append(work)
				continue

			# Lấy các bước giải
			if baiToan == "NhanDaThuc":
				workList = solver.NhanDaThuc()
			elif baiToan == "ChiaDaThuc":
				# Có đúng 2 đa thức
				if len(term) != 2:
					sentence = "Xin lỗi bạn nhưng bài này mình cần có đúng 2 đa thức để giải."
					types = "Abort"
					workQueue.append((None, types, None, sentence))
					continue

				workList = solver.ChiaDaThuc()
			else:
				sentence = "Xin lỗi bạn mình không làm được bài này."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Thêm vào queue
			for work in reversed(workList):
				workQueue.append(work)

		elif types == "PhuongTrinh":
			# Chỉ có 1 biểu thức
			if len(term) > 1:
				sentence = "Xin lỗi bạn nhưng bài này mình chỉ có thể làm được với 1 phương trình mà thôi."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue
			if len(term) == 0:
				sentence = "Mình cần 1 đa thức để giải dạng này, bạn kiểm tra lại xem có nhập sai chỗ nào không."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			baiToanTach = baiToan.split("_")
			baiToan = baiToanTach[0]
			bien_phu = None

			if len(baiToanTach) == 2:
				bien_phu = baiToanTach[1]

			# Kiểm tra điều kiện input hợp lệ
			solver = PhuongTrinh.PT()
			solver.Reset()
			results, isVaild = solver.PassTerm(term[0], bien_phu)
			if not isVaild:
				for work in reversed(results):
					workQueue.append(work)
				continue

			# Lấy các bước giải
			if baiToan == "Giai" or baiToan == "BienLuan":
				workList = solver.GiaiPT()
			else:
				sentence = "Xin lỗi bạn mình không làm được bài này."
				types = "Abort"
				workQueue.append((None, types, None, sentence))
				continue

			# Thêm vào queue
			for work in reversed(workList):
				workQueue.append(work)

		else:
			sentence = "Xin lỗi bạn nhưng mình không thể hiểu bạn muốn làm gì, bạn kiểm tra lại xem."
			types = "Abort"
			workQueue.append((None, types, None, sentence))
			continue


@app.route("/get")
def get_bot_response():
    # Text người nhập
	global current_step
	global global_queue_step
	userText = str(request.args.get('msg'))
	temp = userText.replace(" ", "")

	# all_step 	= {"all","All","aLl","alL","ALl","AlL","ALL"}
	B_step 		= {"b","B"}
	Kq_step 	= {"kq","KQ","kQ","Kq"}
	accept 		= {"N", "n", "ne","nex","next","Ne","Nex","Next","NE","NEX","NEXT","nExt","neXt","nexT","nEXt","nEXT","NExt","NeXt","NexT","NEXt","NEXT"}
	if len(userText) == 1 or userText == "." or userText in accept:
		if len(global_queue_step) == 0:
			return str("Bạn hãy nhập phương trình rồi hãy nhấn . để xem các bước giải nhé.")
		elif current_step == len(global_queue_step):
			current_step = 0
			return str("Đây đã là bước cuối rồi mong bạn hãy nhập phương trình khác hoặc chọn bất kỳ bước trước bằng *B + số bước*...")
		else:
			temp = current_step
			current_step +=1
			Num_string = "Bước "+str(current_step)+": <br>"
			return str(Num_string+global_queue_step[current_step-1])
	if userText in Kq_step:
		if len(global_queue_step) == 0:
			return str("Bạn hãy nhập phương trình rồi hãy nhấn . để xem các bước giải nhé.")
		else:
			return str(global_queue_step[len(global_queue_step)-1])
	if userText.find('HPT') != -1 or userText.find('UocBoi') != -1 or userText.find('DaThuc') != -1 or userText.find('PhuongTrinh') != -1:
		current_step = 0
		global_queue_step = []
		p_term, p_types = XacDinhVaNhanDang(change_back(userText))
		print("change_back(userText) ",change_back(userText))
		print("p_term: ",p_term)
		Run(p_term, p_types)

		return str("Đã xác nhận và tính toán xong phương trình."+"<br>Gồm có: "+str(len(global_queue_step))+" bước..."+" Bạn có 2 lựa chọn:<br>1. Hãy nhập . hoặc Next để bắt đầu xem các bước giải.<br>2. Hãy nhập KQ để xem kết quả của phương trình.")#<br> 2. All để xem tất cả các bước.
	if len(userText) <= 4 and userText in B_step:
		if userText.find("B") != -1:
			pos =  userText.split('B')
		else: 
			pos =  userText.split('b')
		current_step = int(pos[1])
		return str(global_queue_step[int(pos[1])-1])
	
	
	# Tìm xem có x^2 trong text nhập
	if(temp.find('x^2') != -1):
        # Nếu đúng thì str(chatbot.get_response(userText)) sẽ lấy câu trả lời từ txt train + text người nhập
		if len(userText) >= 9:
			return (str(chatbot.get_response(temp))+" "+quadratic_string(userText)+"=0")
		else:
			return (str(chatbot.get_response(temp))+" "+userText)
	else:
        # Nếu ko thì str(chatbot.get_response(userText)) sẽ lấy câu trả lời từ txt train thôi
		return str(chatbot.get_response(userText))





if __name__ == "__main__":
    app.run() 
#.\env\Scripts\activate  
#python app.py
