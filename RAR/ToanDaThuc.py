import sympy as sp


class DaThuc:
	listTerm = []
	domain = None
	is_vaild = False

	def CheckTerm(self, term):
		resultWork = []

		if not isinstance(term, sp.Basic) and not isinstance(term, str):
			print("Không có đa thức để làm!!! <Debug>")
			exit(0)

		# Kiểm tra term có phải là đa thức không
		is_Poly = True
		poly_term = None

		if isinstance(term, str):
			try:
				poly_term = sp.parse_expr(term, evaluate=False)
				if not poly_term.is_polynomial():
					is_Poly = False
			except:
				is_Poly = False
		else:
			poly_term = term

			if not poly_term.is_polynomial():
				is_Poly = False

		if not is_Poly:
			sentence = "Biểu thức " + term + " không phải là đa thức, bạn kiểm tra lại xem biểu thức có nhập đúng không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, None

		return resultWork, poly_term

	def PassTerm(self, listTerm, domain=sp.RR):
		resultWork = []

		# ------------ Kiểm tra điều kiện đầu vào ------------
		for term in listTerm:
			tempWork, poly_term = self.CheckTerm(term)

			# Kiểm tra sai
			if len(tempWork) != 0:
				resultWork += tempWork
				return resultWork, self.is_vaild
			else:
				self.listTerm.append(poly_term)

		self.domain = domain
		self.is_vaild = True

		return resultWork, self.is_vaild

	def NhanDaThuc(self):
		# Phải ở dạng đa thức tối giản
		lhs = sp.expand(sp.simplify(self.listTerm[0]))
		workList = []  # (term, type, domain, sentence)
		totalResult = sp.Integer(0)

		# Đoạn đầu
		sentence = "Giống như phép nhân thông thường, để nhân các đa thức thì bạn chọn 2 đa thức bên trái và phải lần lượt từ trái qua,\n" \
				   "với mỗi phần trong đa thức bên trái, bạn nhân lần lượt mỗi phần trong đa thức bên phải, bao gồm cả phần có chữ và phần số (còn gọi là nhân phân phối).\n" \
				   "Sau khi nhân xong hết, bạn chỉ việc cộng các thành phần có cùng chữ phía sau lại, những phần nào không có chữ thì bạn cộng hết lại.\n" \
				   "Mình sẽ chỉ bạn cách làm từng bước cho phép nhân sau, sau khi mình đã rút gọn biểu thức:"
		types = "Explain"
		term = sp.Mul(*self.listTerm, evaluate=False)
		termLatex = "\(" + sp.latex(term) + "\)"
		workList.append((termLatex, types, self.domain, sentence))

		# Nhân từng đa thức trong list
		for i in range(1, len(self.listTerm)):
			rhs = sp.expand(sp.simplify(self.listTerm[i]))

			sentence = "Nhân đa thức:"
			types = "Explain"
			term = sp.Mul(lhs, rhs, evaluate=False)
			termLatex = "\(" + sp.latex(term) + "\)"
			workList.append((termLatex, types, self.domain, sentence))

			# Bước giải
			listTerm = []
			result = 0
			first = True

			# Nhân phân phối
			for arg in lhs.args:
				if first:
					sentence = "Đầu tiên các bạn nhân " + "\(" + sp.latex(arg) + "\)" + " với từng phần trong " + "\(" + sp.latex(rhs) + "\)" + " lại. Số nhân với số, chữ nhân với chữ,\n" \
								"nếu có nhiều hơn 2 chữ giống nhau nhân lại thì chỉ cần bạn ghi lại 1 chữ đó và ghi thêm 1 con số nhỏ tương đương với số lần xuất hiện của chữ đó trên đầu bên phải.\n" \
								"VD. x*x*x*x*x có thể viết thành " + "\(" + sp.latex(sp.Pow(sp.Symbol('x'), sp.Integer(5))) + "\)" + " và cũng có thể viết thành " + "\(" + sp.latex(sp.Mul(sp.Pow(sp.Symbol('x'), sp.Integer(2)), sp.Pow(sp.Symbol('x'), sp.Integer(3)), evaluate=False)) + "\)" + "\n" \
								"Sau khi nhân xong, bạn được:"
					types = "Explain"
					term = sp.expand(arg * rhs)
					listTerm.append(term)
					termLatex = "\(" + sp.latex(term) + "\)"
					workList.append((termLatex, types, self.domain, sentence))
					first = False
				else:
					sentence = "Nhân " + "\(" + sp.latex(arg) + "\)" + " cho " + "\(" + sp.latex(rhs) + "\)" + " được:"
					types = "Explain"
					term = sp.expand(arg * rhs)
					listTerm.append(term)
					termLatex = "\(" + sp.latex(term) + "\)"
					workList.append((termLatex, types, self.domain, sentence))

			# Cộng các term lại
			sentence = "Sau khi nhân các thành phần xong, bạn chỉ cần cộng các đa thức sau lại theo chữ phía sau. Chữ nào giống cộng lại, số nào không có chữ thì bạn cộng chung lại.\n" \
					   "Các đa thức sau khi đã nhân xong:"
			term = r" \\ ".join([sp.latex(temp) for temp in listTerm])
			termLatex = "\(" + term + "\)"
			workList.append((termLatex, types, self.domain, sentence))

			tempResult = sp.Integer(0)
			for tempTerm in listTerm:
				tempResult += tempTerm

			for arg in tempResult.args:
				if len(arg.free_symbols) == 0:
					sentence = "Cộng tất cả các phần không có chữ số lại, bạn được: " + "\(" + sp.latex(arg) + "\)" + ". Kết quả hiện tại:"
				else:
					sentence = "Cộng tất cả các phần có chữ " + "\(" + sp.latex(sp.LM(arg)) + "\)" + " lại, bạn được: " + "\(" + sp.latex(arg) + "\)" + ". Kết quả hiện tại:"

				result += arg
				term = result
				termLatex = "\(" + sp.latex(term) + "\)"
				workList.append((termLatex, types, self.domain, sentence))

			# Kết quả
			sentence = "Phép nhân: " + "\(" + sp.latex(lhs * rhs) + "\)" + " có kết quả là:"
			types = "Explain"
			termLatex = "\(" + sp.latex(result) + "\)"
			workList.append((termLatex, types, self.domain, sentence))

			# Đặt lhs là result và cộng vào totalResult
			lhs = result
			totalResult += result

		sentence = "Cuối cùng, phép nhân: " + "\(" + sp.latex(sp.Mul(*self.listTerm)) + " = " + sp.latex(totalResult) + "\)"
		types = "Done"
		workList.append((None, types, None, sentence))

		return workList

	def ChiaDaThuc(self):
		if not self.is_vaild:
			print("Đa thức này không hợp lệ. <Debug>")
			exit(0)

		# Phải ở dạng đa thức tối giản
		lhs = sp.expand(sp.simplify(self.listTerm[0]))
		rhs = sp.expand(sp.simplify(self.listTerm[1]))
		workList = []  # (term, type, domain, sentence)

		# Đoạn đầu
		sentence = "Giống như phép chia thông thường, để chia 2 đa thức bạn chỉ cần lấy phần có bậc cao nhất của số chia chia lại cho phần có bậc cao nhất của số bị chia,\n" \
				   "sau đó lấy kết quả tìm được nhân lại cho số chia và trừ cho số bị chia (lưu ý kết quả mình làm chỉ nằm trong phạm vi số nguyên).\n" \
				   "Mình sẽ chỉ bạn cách làm từng bước cho phép chia sau:"
		types = "Explain"
		term = lhs / rhs
		termLatex = "\(" + sp.latex(term) + "\)"
		workList.append((termLatex, types, self.domain, sentence))

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
						   "Nghĩa là lấy " + "\(" + sp.latex(left) + "\)" + " / " + "\(" + sp.latex(right) + "\)" + ", bạn được " + "\(" + sp.latex(divisor) + "\)" + ", bạn ghi kết quả lại.\n" \
							"Sau đó nhân " + "\(" + sp.latex(divisor) + "\)" + " với số chia là " + "\(" + sp.latex(rhs) + "\)" + ", bạn được " + "\(" + sp.latex(subtractor) + "\)" + "\n" \
							"Cuối cùng bạn lấy đa thức bên trái " + "\(" + sp.latex(oldArg) + "\)" + " trừ cho số bạn vừa tìm được " + "\(" + sp.latex(subtractor) + "\)" + ", bạn ra phần dư " + "\(" + sp.latex(arg) + "\)" + "\n" \
							"Và từ phần dư đó, bạn lặp lại quá trình trên tới khi nào bậc cao nhất ở phần dư nhỏ hơn bậc cao nhất của số chia.\n" \
							"Biểu thức hiện tại:"
				types = "Explain"
				term = arg / rhs
				termLatex = "\(" + sp.latex(term) + "\)"
				workList.append((termLatex, types, self.domain, sentence))
				first = False
			else:
				sentence = "Chia bậc cao nhất ở 2 bên theo thứ tự trái qua phải: " + "\(" + sp.latex(left) + "\)" + " / " + "\(" + sp.latex(right) + "\)" + " = " + "\(" + sp.latex(divisor) + "\)" + ", ghi lại kết quả.\n" \
							"Lấy kết quả vừa tìm được nhân lại số chia: " + "\(" + sp.latex(divisor) + "\)" + " * (" + "\(" + sp.latex(rhs) + "\)" + ") = " + "\(" + sp.latex(subtractor) + "\)" + "\n" \
							"Lấy đa thức bên trái trừ số vừa tìm được: " + "\(" + sp.latex(oldArg) + "\)" + " - (" + "\(" + sp.latex(subtractor) + "\)" + ") = " + "\(" + sp.latex(arg) + "\)" + "\n" \
							"Kết quả hiện tại: " + "\(" + sp.latex(result) + "\)" + "\n" \
							"Biểu thức hiện tại: "
				types = "Explain"
				term = arg / rhs
				termLatex = "\(" + sp.latex(term) + "\)"
				workList.append((termLatex, types, self.domain, sentence))

		# Tổng kết
		sentence = "Sau khi điều kiện dừng thỏa, thì với phép chia: " + "\(" + sp.latex(lhs) + "\)" + " / " + "\(" + sp.latex(rhs) + "\)" + ", " \
					"bạn tìm được kết quả là " + "\(" + sp.latex(result) + "\)" + " với phần dư là " + "\(" + sp.latex(arg) + "\)"
		types = "Done"
		workList.append((None, types, None, sentence))

		return workList
