import sympy as sp
import ToanDaThuc
import HePhuongTrinh
import UocBoi
import queue

# 3 dạng
# Hệ phương trình (phương trình tuyến tính, 2 ẩn và 3 ẩn)
# -- stringInput = "3*x + y = 2; 2*x + 3*y - 10 + z = 0; -4*x -2*y + 7*z = 10; HPT@Giai"
# Tìm n để phép chia biểu thức là số nguyên (Dạng ước bội)
# -- stringInput = "((x**2 + 1) * (x**3 + 2))/ (x - 5); UocBoi@TimN_DeNguyen"
# Các phép toán trong đa thức (phép nhân: nằm trong tập số thực; phép chia: chỉ chia được cho mẫu bậc 1, tử bao nhiêu cũng được)
# -- stringInput = "x**2 + 4*x + 5*x + 2*x*y; x + 1 + x*y; DaThuc@NhanDaThuc"
# -- stringInput = "x**2 + 4*x + 5*x; x + 1; DaThuc@ChiaDaThuc"


# Tạm thời input nhập như vậy
def XacDinhVaNhanDang(inputString: str):
	tempList = inputString.split(";")
	term = tempList[:len(tempList)-1]
	types = tempList[-1].strip()

	return term, types


def Run(term_input:list, types_input:str):
	nameFolder = "C:/Users/Admin/DSMT/Al/"
	sentence = ""
	baiToan = None
	domain = None

	first = True
	workQueue = queue.Queue()
	workQueue.put((term_input, types_input, domain, sentence))

	while not workQueue.empty():
		currentWork = workQueue.get()
		term, types, domain, sentence = currentWork

		if first:
			tempList = types.split("@")
			types = tempList[0]
			baiToan = tempList[1]
			first = False
			Step = 1
		# Check type
		if types == "Abort":
			name = "Abort"
			f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
			f.write(sentence)
			f.close()
			print(sentence)
			break
		if types == "Done":
			name = "B" +str(Step) 
			f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
			f.truncate(0)
			f.write(sentence)
			f.close()
			print("Bước: "+ str(Step))
			print(sentence)
			continue
		if types == "Explain":
			name = "B" +str(Step)
			f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
			f.truncate(0)
			f.write(sentence)
			if term:
				f.write(str(term))
			f.close()
			print("Bước: "+ str(Step))
			Step += 1
			print(sentence)
			if term:
				print(term)
			# t = input("---------------- Nhấn phím để tiếp tục ----------------")
			continue

		if types == "UocBoi":
			# Chỉ có 1 biểu thức

			if len(term) > 1:
				sentence = "Xin lỗi bạn nhưng bài này mình chỉ có thể làm được với 1 biểu thức mà thôi."
				types = "Abort"
				workQueue.put((None, types, None, sentence))
				continue

			# Kiểm tra điều kiện input hợp lệ
			
			solver = UocBoi.UocBoi()
			results, isVaild = solver.PassTerm(term[0])
			if not isVaild:
				for work in results:
					workQueue.put(work)
				continue

			# Lấy các bước giải
			if baiToan == "TimN_DeNguyen":
				workList = solver.TimN_DeNguyen()
			else:
				workList = []
				name = "No"
				f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
				f.write("Không nhận dạng được bài toán. <Debug>")
				f.close()
				exit(0)

			# Thêm vào queue
			for work in workList:
				workQueue.put(work)

		elif types == "HPT":
			solver = HePhuongTrinh.HPT()
			# Kiểm tra điều kiện input hợp lệ
			results, isVaild = solver.PassTerm(term)
			if not isVaild:
				for work in results:
					workQueue.put(work)
				continue

			# Lấy các bước giải
			if baiToan == "Giai":
				workList = solver.GiaiHPT()
			else:
				workList = []
				name = "No"
				f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
				f.write("Không nhận dạng được bài toán. <Debug>")
				f.close()
				exit(0)

			# Thêm vào queue
			for work in workList:
				workQueue.put(work)

		elif types == "DaThuc":
			# Phải có 2 đa thức
			if len(term) != 2:
				sentence = "Xin lỗi bạn nhưng bài này mình cần có 2 đa thức để giải."
				types = "Abort"
				workQueue.put((None, types, None, sentence))
				continue

			# Kiểm tra điều kiện input hợp lệ
			solver = ToanDaThuc.DaThuc()
			results, isVaild = solver.PassTerm(term[0], term[1])
			if not isVaild:
				for work in results:
					workQueue.put(work)
				continue

			# Lấy các bước giải
			if baiToan == "NhanDaThuc":
				workList = solver.NhanDaThuc()
			elif baiToan == "ChiaDaThuc":
				workList = solver.ChiaDaThuc()
			else:
				workList = []
				name = "No"
				f = open(nameFolder+"/%s.txt"% name, "a", encoding="utf-8")
				f.write("Không nhận dạng được bài toán. <Debug>")
				f.close()
				exit(0)

			# Thêm vào queue
			for work in workList:
				workQueue.put(work)

stringInput = input()
p_term, p_types = XacDinhVaNhanDang(stringInput)
print(Run(p_term, p_types))





