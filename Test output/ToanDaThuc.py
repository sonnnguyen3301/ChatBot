import sympy as sp

class DaThuc:
	lhs, rhs = None, None
	domain = None
	is_vaild = False

	def PassTerm(self, p_lhs, p_rhs, domain=sp.RR):
		resultWork = []

		# ------------ Kiểm tra điều kiện đầu vào ------------
		if not p_lhs or not p_rhs:
			print("Không có đa thức để làm!!! <Debug>")
			exit(0)

		# Kiểm tra lhs và rhs có phải là đa thức không
		is_Poly = True
		poly_lhs = None

		if isinstance(p_lhs, str):
			try:
				poly_lhs = sp.parse_expr(p_lhs, evaluate=False)
				if not poly_lhs.is_polynomial():
					is_Poly = False
			except:
				is_Poly = False
		else:
			poly_lhs = p_lhs

			if not poly_lhs.is_polynomial():
				is_Poly = False

		if not is_Poly:
			sentence = "Phương trình " + p_lhs + " không phải là đa thức, bạn kiểm tra lại xem biểu thức có nhập đúng không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.is_vaild

		is_Poly = True
		poly_rhs = None
		if isinstance(p_rhs, str):
			try:
				poly_rhs = sp.parse_expr(p_rhs, evaluate=False)
				if not poly_rhs.is_polynomial():
					is_Poly = False
			except:
				is_Poly = False
		else:
			poly_rhs = p_rhs

			if not poly_rhs.is_polynomial():
				is_Poly = False

		if not is_Poly:
			sentence = "Phương trình " + p_rhs + " không phải là đa thức, bạn kiểm tra lại xem biểu thức có nhập đúng không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.is_vaild

		self.lhs = poly_lhs
		self.rhs = poly_rhs
		self.domain = domain
		self.is_vaild = True

		return resultWork, self.is_vaild

	def NhanDaThuc(self):
		# Phải ở dạng đa thức tối giản
		lhs = sp.expand(sp.simplify(self.lhs))
		rhs = sp.expand(sp.simplify(self.rhs))
		workList = []  # (term, type, domain, sentence)

		# Đoạn đầu
		sentence = "Giống như phép nhân thông thường, để nhân 2 đa thức bạn thì với mỗi phần trong đa thức bên trái, bạn nhân lần lượt mỗi phần trong đa thức bên phải, bao gồm cả phần có chữ và phần số (còn gọi là nhân phân phối).\n" \
				   "Sau khi nhân xong hết, bạn chỉ việc cộng các thành phần có cùng chữ phía sau lại, những phần nào không có chữ thì bạn cộng hết lại.\n" \
				   "Mình sẽ chỉ bạn cách làm từng bước cho phép nhân sau:"
		types = "Explain"
		term = lhs * rhs
		workList.append((term, types, self.domain, sentence))

		# Bước giải
		listTerm = []
		result = 0
		first = True

		# Nhân phân phối
		for arg in lhs.args:
			if first:
				sentence = "Đầu tiên các bạn nhân " + str(arg) + " với từng phần trong " + str(rhs) + " lại. Số nhân với số, chữ nhân với chữ,\n" \
							"nếu có nhiều hơn 2 chữ giống nhau nhân lại thì chỉ cần bạn ghi lại 1 chữ đó và ghi thêm 1 con số nhỏ tương đương với số lần xuất hiện của chữ đó trên đầu bên phải.\n" \
							"VD. x*x*x*x*x có thể viết thành " + str(sp.Pow(sp.Symbol('x'), sp.Integer(5))) + " và cũng có thể viết thành " + str(sp.Mul(sp.Pow(sp.Symbol('x'), sp.Integer(2)), sp.Pow(sp.Symbol('x'), sp.Integer(3)), evaluate=False)) + "\n" \
							"Sau khi nhân xong, bạn được:"
				types = "Explain"
				term = sp.expand(arg * rhs)
				listTerm.append(term)
				workList.append((term, types, self.domain, sentence))
				first = False
			else:
				sentence = "Nhân " + str(arg) + " cho " + str(rhs) + " được:"
				types = "Explain"
				term = sp.expand(arg * rhs)
				listTerm.append(term)
				workList.append((term, types, self.domain, sentence))

		# Cộng các term lại
		sentence = "Sau khi nhân các thành phần xong, bạn chỉ cần cộng các đa thức sau lại theo chữ phía sau. Chữ nào giống cộng lại, số nào không có chữ thì bạn cộng chung lại.\n" \
				   "Các đa thức sau khi đã nhân xong:"
		term = "\n".join([str(temp) for temp in listTerm])
		workList.append((term, types, self.domain, sentence))

		tempResult = sp.Integer(0)
		for tempTerm in listTerm:
			tempResult += tempTerm

		for arg in tempResult.args:
			if len(arg.free_symbols) == 0:
				sentence = "Cộng tất cả các phần không có chữ số lại, bạn được: " + str(arg) + ". Kết quả hiện tại:"
			else:
				sentence = "Cộng tất cả các phần có chữ " + str(sp.LM(arg)) + " lại, bạn được: " + str(arg) + ". Kết quả hiện tại:"

			result += arg
			term = result
			workList.append((term, types, self.domain, sentence))

		sentence = "Cuối cùng, phép nhân: " + str(lhs * rhs) + " = " + str(result)
		types = "Done"
		workList.append((None, types, None, sentence))

		return workList

	def ChiaDaThuc(self):
		if not self.is_vaild:
			print("Đa thức này không hợp lệ. <Debug>")
			exit(0)

		# Phải ở dạng đa thức tối giản
		lhs = sp.expand(sp.simplify(self.lhs))
		rhs = sp.expand(sp.simplify(self.rhs))
		workList = []  # (term, type, domain, sentence)

		# Đoạn đầu
		sentence = "Giống như phép chia thông thường, để chia 2 đa thức bạn chỉ cần lấy phần có bậc cao nhất của số chia chia lại cho phần có bậc cao nhất của số bị chia,\n" \
				   "sau đó lấy kết quả tìm được nhân lại cho số chia và trừ cho số bị chia (lưu ý kết quả mình làm chỉ nằm trong phạm vi số nguyên).\n" \
				   "Mình sẽ chỉ bạn cách làm từng bước cho phép chia sau:"
		types = "Explain"
		term = lhs / rhs
		workList.append((term, types, self.domain, sentence))

		# Bước giải
		arg = lhs
		result = 0
		first = True

		while len(arg.free_symbols) != 0:
			left = sp.LT(arg)
			right = sp.LT(rhs)

			divisor = left / right
			subtractor = sp.expand(divisor * rhs)

			oldArg = arg
			arg = arg - subtractor
			result = sp.Add(divisor, result)

			if first:
				sentence = "Đầu tiên bạn lấy phần có bậc cao nhất ở cả 2 bên chia cho nhau, thứ tự chia từ trái sang phải.\n" \
						   "Nghĩa là lấy " + str(left) + " / " + str(right) + ", bạn được " + str(divisor) + ", bạn ghi kết quả lại.\n" \
							"Sau đó nhân " + str(divisor) + " với số chia là " + str(rhs) + ", bạn được " + str(subtractor) + "\n" \
							"Cuối cùng bạn lấy đa thức bên trái " + str(oldArg) + " trừ cho số bạn vừa tìm được " + str(subtractor) + ", bạn ra phần dư " + str(arg) + "\n" \
							"Và từ phần dư đó, bạn lặp lại quá trình trên tới khi nào bậc cao nhất ở phần dư nhỏ hơn bậc cao nhất của số chia.\n" \
							"Biểu thức hiện tại:"
				types = "Explain"
				term = arg / rhs
				workList.append((term, types, self.domain, sentence))
				first = False
			else:
				sentence = "Chia bậc cao nhất ở 2 bên theo thứ tự trái qua phải: " + str(left) + " / " + str(right) + " = " + str(divisor) + ", ghi lại kết quả.\n" \
							"Lấy kết quả vừa tìm được nhân lại số chia: " + str(divisor) + " * (" + str(rhs) + ") = " + str(subtractor) + "\n" \
							"Lấy đa thức bên trái trừ số vừa tìm được: " + str(oldArg) + " - (" + str(subtractor) + ") = " + str(arg) + "\n" \
							"Kết quả hiện tại: " + str(result) + "\n" \
							"Biểu thức hiện tại: "
				types = "Explain"
				term = arg / rhs
				workList.append((term, types, self.domain, sentence))

		# Tổng kết
		sentence = "Sau khi điều kiện dừng thỏa, thì với phép chia: " + str(lhs) + " / " + str(rhs) + ", " \
					"bạn tìm được kết quả là " + str(result) + " với phần dư là " + str(arg) + "."
		types = "Done"
		workList.append((None, types, None, sentence))

		return workList
