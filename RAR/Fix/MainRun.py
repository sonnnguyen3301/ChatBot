import PhuongTrinh
import ToanDaThuc
import HePhuongTrinh
import UocBoi
import NhanDang

# 8 dạng
# Hệ phương trình (phương trình tuyến tính, 2 ẩn và 3 ẩn)
# -- stringInput = "3*x + y = 2; 2*x + 3*y - 10 + z = 0; -4*x -2*y + 7*z = 10; HPT@Giai"
# Tìm n để phép chia biểu thức là số nguyên (Dạng ước bội)
# -- stringInput = "((x**2 + 1) * (x**3 + 2))/ (x - 5); UocBoi@TimN_DeNguyen"
# Các phép toán trong đa thức (phép nhân: nằm trong tập số thực; phép chia: chỉ chia được cho mẫu bậc 1, tử bao nhiêu cũng được)
# -- stringInput = "x**2 + 4*x + 5*x + 2*x*y; x + 1 + x*y; 4*x+5*y-5; DaThuc@NhanDaThuc"
# -- stringInput = "x**2 + 4*x + 5*x; x + 1; DaThuc@ChiaDaThuc"
# Phương trình
# -- stringInput = "x**2 + 4*y = 2; PhuongTrinh@Giai"
# -- stringInput = "2*x**2 - (3 - 5*x) = 4*(x + 3); PhuongTrinh@Giai"
# -- stringInput = "(2*x**2 + 3)**2  + 4*x**2 + 12= 4; PhuongTrinh@Giai"
# -- stringInput = "(2*x**2 + 7)**2  + 4*x**2 + 12= 4; PhuongTrinh@Giai"
# -- stringInput = "(2*x + 7)**2  + 4*x + 12= 4; PhuongTrinh@Giai"
# -- stringInput = "x**4 + 4*x**2 = 12; PhuongTrinh@Giai"
# -- stringInput = "m*x + 12*m + x*m**2= 4; PhuongTrinh@BienLuan_m"
# -- stringInput = "x**2 + 12*x + m = 4; PhuongTrinh@BienLuan_m"

# Input chính thức
# Tìm n để phép chia biểu thức là số nguyên (Dạng ước bội)
# -- stringInput = "Tìm n để đa thức sau có nghiệm nguyên "((x**2 + 1) * (x**3 + 2))/ (x - 5)""


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

	while not len(workQueue) == 0:
		currentWork = workQueue.pop()
		term, types, domain, sentence = currentWork[0], currentWork[1], currentWork[2], currentWork[3]

		if first:
			types, baiToan = types.split("@")
			first = False

		# Check type
		if types == "Abort":
			print(sentence)
			break
		if types == "Done":
			print(sentence)
			continue
		if types == "Explain":
			print(sentence)
			if term:
				print(term)
			input("---------------- Nhấn phím để tiếp tục ----------------")
			continue
		if types == "Explain_Question":
			print(sentence)
			if term:
				print(term)

			print("Bạn có muốn giải thích phần trên không? (Yes/No)")
			vaildResponse = {"Yes", "yes", "y", "No", "no", "n"}
			accept = {"Yes", "yes", "y"}

			while True:
				response = input()

				if response in vaildResponse:
					break
				else:
					print("Bạn phải nhập vào Yes hoặc No. Xin bạn hãy nhập lại:")

			if response in accept:
				listEq = currentWork[4]
				types, baiToan = currentWork[5].split("@")
			else:
				continue

			if types == "DaThuc" and baiToan == "ChiaDaThuc":
				# Chỉ nhận 2 phương trình
				if len(listEq) != 2:
					print("Số phương trình không đúng như dự tính. <Debug>")
					exit(0)

				solver = ToanDaThuc.DaThuc()
				solver.Reset()
				_, isVaild = solver.PassTerm(listEq)

				# Nếu không vaild thì sai chỗ nào đó
				if not isVaild:
					print("Sai phần pass đa thức. <Debug>")
					exit(0)

				workList = solver.ChiaDaThuc()
				# Thêm vào queue
				for work in reversed(workList):
					workQueue.append(work)

			elif types == "PhuongTrinh" and baiToan == "Giai":
				# Chỉ nhận 1 phương trình
				if len(listEq) != 1:
					print("Số phương trình không đúng như dự tính. <Debug>")
					exit(0)

				solver = PhuongTrinh.PT()
				solver.Reset()
				_, isVaild = solver.PassTerm(listEq[0])

				# Nếu không vaild thì sai chỗ nào đó
				if not isVaild:
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

stringInput = input()
#deBai = NhanDang.ChuyenDeThanhDangToan(stringInput)
p_term, p_types = XacDinhVaNhanDang(stringInput)
Run(p_term, p_types)





