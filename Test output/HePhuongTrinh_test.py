import sympy as sp
import queue
import os.path
class HPT:
	equationList = []
	domain = None
	isVaild = False

	def PassTerm(self, equationList, domain=sp.RR):
		# (term, type, domain, sentence)
		resultWork = []

		# ------------ Kiểm tra điều kiện đầu vào ------------
		if not equationList:
			print("Không có phương trình để làm!!! <Debug>")
			exit(0)

		# Kiểm tra có phải hệ phương trình mà hệ thống có thể giải được
		if len(equationList) == 1:
			sentence = "Đây không phải là hệ phương trình mà chỉ là phương trình thôi. Bạn kiểm tra xem có nhập sai chỗ nào không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild
		if len(equationList) > 3:
			sentence = "Xin lỗi bạn nhưng hệ thống của mình chỉ giải được tối đa 3 phương trình."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild

		# Chuyển PT về dạng Sympy
		for index, eq in enumerate(equationList):
			if isinstance(eq, str):
				indexEqual = eq.find("=")
				equation = sp.Equality(sp.parse_expr(eq[:indexEqual]), sp.parse_expr(eq[indexEqual + 1:]))
			else:
				equation = eq
			equationList[index] = sp.simplify(equation)

		# Kiểm tra xem mỗi phương trình có ít nhất 1 biến
		for eq in equationList:
			if eq.func != sp.Equality:
				sentence = "Có phương trình bạn nhập vào không có biến nào cả. Bạn kiểm tra lại xem."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		# Kiểm tra phương trình có phải tuyến tính không
		symbols = set()
		isLinear = True
		errorEq = None
		for eq in equationList:
			symbols.update(eq.free_symbols)
		symbols = list(symbols)

		for eq in equationList:
			try:
				poly = sp.poly(eq, symbols, domain='RR')
			except:
				isLinear = False
				errorEq = eq
				break

			if not poly.is_linear:
				isLinear = False
				errorEq = eq
				break

		if not isLinear:
			sentence = "Phương trình: \n" + sp.pretty(errorEq,use_unicode=True) + "\n" + "không phải là phương trình tuyến tính, mình chỉ có thể giải được với các phương trình tuyến tính thôi."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild

		# Kiểm tra số biến bằng số phương trình
		if len(symbols) != len(equationList):
			sentence = "Số biến và số phương trình không bằng nhau. Bạn kiểm tra lại xem có sai chỗ nào không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild

		# Kiểm tra HPT có vô nghiệm hay vô số nghiệm
		result = list(sp.linsolve(equationList, symbols))
		if not result:
			sentence = "Hệ phương trình của bạn không có nghiệm. Xin lỗi bạn nhưng mình chỉ giải được với các hệ phương trình nào có 1 nghiệm thôi."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild
		else:
			temp = result[0]
			for kq in temp:
				if len(kq.free_symbols) > 0:
					sentence = "Hệ phương trình của bạn có vô số nghiệm. Xin lỗi bạn nhưng mình chỉ giải được với các hệ phương trình nào có 1 nghiệm thôi."
					types = "Abort"
					resultWork.append((None, types, None, sentence))
					return resultWork, self.isVaild

		self.equationList = equationList
		self.domain = domain
		self.isVaild = True

		return resultWork, self.isVaild

	def GiaiHPT(self):
		if not self.isVaild:
			print("Hệ phương trình không hợp lệ. <Debug>")
			exit(0)

		# (term, type, domain, sentence)
		resultWork = []

		# ------------ Kiểm tra xong ------------
		sentence = "Biểu thức bạn nhập vào sau khi mình rút gọn lại:"
		term = ""
		for eq in self.equationList:
			term += sp.pretty(eq, use_unicode=True) + "\n"
		types = "Explain"
		resultWork.append((term, types, self.domain, sentence))

		# Khởi tạo và tìm các PT có 1 biến
		setDone = set()
		listDone = []
		for index, eq in enumerate(self.equationList):
			if len(eq.free_symbols) == 1:
				setDone.add(index)
				listDone.append(eq)

		sentence = "Đối với dạng bài này, cách dễ nhất là bạn dùng phương pháp thế.\n" \
				   "Đầu tiên bạn chọn phương trình nào có số biến ít nhất, sau đó bạn rút 1 biến theo thứ tự chữ cái trong phương trình, đem biến đó thế tiếp vào phương trình sau.\n" \
				   "Bạn nhớ thế theo thứ tự chữ cái cho dễ. Phương trình nào đã được rút thì bạn tạm thời để yên đó, còn cái nào chưa thì bạn cứ rút từ từ.\n" \
				   "Tới khi nào phương trinh bạn rút ra chỉ còn đúng 1 biến thì bạn lấy kết quả biến đó thế ngược trở lại các phương trình bạn vừa rút,\n" \
				   "theo thứ tự số lượng biến chưa có kết quả từ nhỏ nhất tới lớn nhất.\n" \
				   "Mình sẽ chỉ bạn từng bước trên:"
		types = "Explain"
		resultWork.append((None, types, self.domain, sentence))

		# Thế các phương trình
		first = True

		while len(listDone) != len(self.equationList):
			self.equationList = sorted(self.equationList, key=lambda x: len(x.free_symbols))

			for index, eq in enumerate(self.equationList):
				sentence = ""
				term = ""

				if index in setDone:
					continue
				if len(eq.free_symbols) == 1:
					setDone.add(index)
					listDone.append(eq)
					continue

				# Chọn PT
				if first:
					sentence += "Đầu tiên bạn chọn phương trình nào có số biến ít nhất, nếu bằng nhau thì bạn chọn cái nào cũng được. " \
								"Mình sẽ chọn: \n" + sp.pretty(eq, use_unicode=True) + "\n"
				else:
					sentence += "Chọn phương trình: \n" + sp.pretty(eq, use_unicode=True) + "\n"

				# Nếu không phải PT đầu tiên thì thế PT trước vào
				if index != 0:
					listPrev = []
					listStringPrev = []
					oldEq = eq

					for indexPrev in range(index - 1, -1, -1):
						listPrev.append(self.equationList[indexPrev])

					# Sort lại phương trình trước theo thứ tự Alphabet
					listPrev = sorted(listPrev, key=lambda x: str(x.lhs))

					# Nếu có biến trong PT thì mới thế
					for prevEq in listPrev:
						if prevEq.lhs in eq.free_symbols:
							self.equationList[index] = eq.subs({prevEq.lhs: prevEq.rhs})
							eq = self.equationList[index]
							listStringPrev.append(sp.pretty(prevEq, use_unicode=True))

					# Kiểm tra nếu PT hiện tại đã thế được chưa
					if not listStringPrev:
						continue

					prevEq = "\n".join(listStringPrev)
					if first:
						sentence += "Nếu trong hệ phương trình đã có một phương trình có nghiệm rùi thì bạn chỉ cần thế nghiệm đó vào phương trình này.\n" \
									"Cụ thể là thế: \n" + prevEq + "vào\n" + sp.pretty(oldEq, use_unicode=True) + "rút gọn lại bạn được\n" + sp.pretty(eq, use_unicode=True) + "\n"
					else:
						sentence += "Thế \n" + prevEq + "\nvào\n" + sp.pretty(oldEq, use_unicode=True) + "\nrút gọn lại được: \n" + sp.pretty(eq, use_unicode=True) + "\n"

				# Rút ra 1 biến theo thứ tự Alphabet
				lhs = sorted(list(eq.free_symbols), key=lambda x: str(x))[0]
				#lhs = list(eq.free_symbols)[0]
				rhs = sp.solve(eq, lhs)[0]
				self.equationList[index] = sp.Equality(lhs, rhs)

				if first:
					if len(eq.free_symbols) > 1:
						sentence += "Mình sẽ rút " + str(lhs) + " trong phương trình trên, phương trình lúc này trở thành: \n" + sp.pretty(self.equationList[index], use_unicode=True) + "\n"
					else:
						sentence += "Khi rút biến " + str(lhs) + ", phương trình sẽ có nghiệm: \n" + sp.pretty(self.equationList[index], use_unicode=True) + "\n"
					sentence += "Rồi bạn cứ tiếp tục lặp lại các bước trên, tới khi nào tìm được các nghiệm trong hệ phương trình.\n"

				else:
					if len(eq.free_symbols) > 1:
						sentence += "Rút biến " + str(lhs) + " trong phương trình trên, phương trình lúc này trở thành: \n" + sp.pretty(self.equationList[index], use_unicode=True) + "\n"
					else:
						sentence += "Phương trình sẽ có nghiệm: \n" + sp.pretty(self.equationList[index], use_unicode=True) + "\n"

				sentence += "Hệ phương trình hiện tại:"
				for eq in self.equationList:
					term += sp.pretty(eq, use_unicode=True) + "\n"

				types = "Explain"
				resultWork.append((term, types, self.domain, sentence))
				first = False

		# Sắp xếp biến theo thứ tự Alphabet
		self.equationList = sorted(self.equationList, key=lambda x: str(x.lhs))

		sentence = "Hệ phương trình sẽ có các nghiệm là:\n"
		term = ""
		for eq in self.equationList:
			term += sp.pretty(eq, use_unicode=True) + "\n"
		sentence += term
		types = "Done"
		resultWork.append((term, types, self.domain, sentence))

		return resultWork
# -----------------##################---------------------
def XacDinhVaNhanDang(inputString: str):
	tempList = inputString.split(";")
	term = tempList[:len(tempList)-1]
	types = tempList[-1].strip()

	return term, types
# -----------------##################---------------------
stringInput = input()
p_term, p_types = XacDinhVaNhanDang(stringInput)
sentence = ""
baiToan = None
domain = None
nameFolder = "C:/Users/Admin/DSMT/Al/"
first = True
workQueue = queue.Queue()
workQueue.put((p_term, p_types, domain, sentence))

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
			f.write(term)
		f.close()
		print("Bước: "+ str(Step))
		Step += 1
		print(sentence)
		if term:
			print(term)
		# t = input("---------------- Nhấn phím để tiếp tục ----------------")
		continue
	if types == "HPT":
			solver = HPT()
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
				print("Không nhận dạng được bài toán. <Debug>")
				exit(0)

			# Thêm vào queue
			for work in workList:
				workQueue.put(work)
# -- stringInput = "3*x + y = 2; 2*x + 3*y - 10 + z = 0; -4*x -2*y + 7*z = 10; HPT@Giai"
name = "B1"
file = open(nameFolder+"/%s.txt"% name, "r", encoding="utf-8")
 
# all_of_it = file.read()
Lines = file.readlines()
str_full_downline= ""
for line in Lines:
	str_full_downline = str_full_downline +  line + "<br>"
file.close()
print("READ ALL B1: ",str_full_downline)
print("Lines",Lines)

# Python code to
# demonstrate readlines()

# L = ["Geeks\n", "for\n", "Geeks\n"]

# # writing to file
# file1 = open('myfile.txt', 'w')
# file1.writelines(L)
# file1.close()

# # Using readlines()
# file1 = open('myfile.txt', 'r')
# Lines = file1.readlines()

# count = 0
# # Strips the newline character
# for line in Lines:
# 	count += 1
# 	print("Line{}: {}".format(count, line.strip()))

