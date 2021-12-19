import sympy as sp


class PT:
	equation = ""
	kieuPT = "BinhThuong"

	domain = None
	isVaild = False

	bacPT = 0
	bien_x = None
	bien_m = None

	def Reset(self):
		self.equation = ""
		self.kieuPT = "BinhThuong"

		self.domain = None
		self.isVaild = False

		self.bacPT = 0
		self.bien_x = None
		self.bien_m = None

	def PassTerm(self, equation, bien_m_string=None, domain=sp.RR):
		# (term, type, domain, sentence)
		resultWork = []

		# ------------ Kiểm tra điều kiện đầu vào ------------
		if not isinstance(equation, sp.Basic) and not isinstance(equation, str):
			print("Không có phương trình để làm!!! <Debug>")
			exit(0)

		# Kiểm tra có phải phương trình mà hệ thống có thể giải được
		if isinstance(equation, str):
			indexEqual = equation.find("=")
			if indexEqual < 0:
				sentence = "Đây không phải là phương trình. Bạn kiểm tra xem có nhập sai chỗ nào không."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild
			equation = sp.Equality(sp.parse_expr(equation[:indexEqual], evaluate=False), sp.parse_expr(equation[indexEqual + 1:], evaluate=False))
		else:
			if equation.func != sp.Equality:
				sentence = "Đây không phải là phương trình. Bạn kiểm tra xem có nhập sai chỗ nào không."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		tempEq = sp.simplify(equation)

		# Kiểm tra biến phụ
		found_m = False
		symbols = tempEq.free_symbols
		bien_m = None
		bien_x = None

		if bien_m_string:
			bien_m = sp.Symbol(bien_m_string)

		for i in symbols:
			if i == bien_m:
				found_m = True
			else:
				bien_x = i

		if bien_m_string:
			# Không là đa thức
			try:
				tempPoly = sp.Poly(tempEq.lhs, bien_m)
			except:
				sentence = "Biến phụ của bạn không phải là đa thức. Bạn kiểm tra lại xem."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

			# Bậc lớn hơn 2
			tempBac = list(tempPoly.all_monoms()[0])[0]
			if tempBac > 2:
				sentence = "Xin lỗi bạn nhưng mình chỉ giải được biến phụ có bậc nhỏ hơn 2 mà thôi."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		if bien_m_string and not found_m:
			sentence = "Mình không tìm thấy biến phụ " + bien_m_string + " trong phương trình. Bạn kiểm tra lại xem."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild

		# Kiểm tra phương trình chỉ có 1 biến
		if not bien_m_string:
			if len(tempEq.free_symbols) != 1:
				sentence = "Phương trình của bạn nên chỉ có 1 biến. Bạn kiểm tra lại xem."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		# Kiểm tra phương trình có phải polynomial
		try:
			sp.Poly(tempEq.lhs, bien_x)
		except:
			sentence = "Phương trình của bạn không phải là đa thức. Bạn kiểm tra lại xem bạn nhập có đúng không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork, self.isVaild

		# Kiểm tra có phải dạng thế không
		tempResult = self.KiemTraThe(equation)
		if len(tempResult) == 0 and not bien_m_string:
			self.kieuPT = "The"
			self.bacPT = 2

		# Kiểm tra có phải trùng phương không
		tempResult = self.KiemTraTrungPhuong(equation)
		if len(tempResult) == 0 and self.kieuPT == "BinhThuong" and not bien_m_string:
			self.kieuPT = "TrungPhuong"
			self.bacPT = 2

		# Kiểm tra số bậc
		if self.kieuPT == "BinhThuong":
			tempBac = sp.degree(tempEq.lhs, gen=bien_x)
			if tempBac == 1 or tempBac == 2:
				self.bacPT = tempBac
			else:
				sentence = "Xin lỗi bạn nhưng mình chỉ giải được với phương trình bậc 1 và 2 thôi."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		# Kiểm tra ẩn phụ cho PT bậc 2
		if bien_m_string and self.bacPT == 2:
			lhs = equation.lhs - equation.rhs
			tempPoly = sp.Poly(lhs, bien_x)
			all_coeff = tempPoly.all_coeffs()

			A, B, C = all_coeff[0], all_coeff[1], all_coeff[2]
			tempBacB = sp.degree(B*B, gen=bien_m)
			tempBacA_C = sp.degree(A*C, gen=bien_m)

			if tempBacB > 2 or tempBacA_C > 2:
				sentence = "Xin lỗi bạn nhưng mình chỉ giải biến phụ với bậc 1 và 2 mà thôi."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild

		self.equation = equation
		self.domain = domain
		self.bien_x = bien_x
		self.bien_m = bien_m
		self.isVaild = True

		return resultWork, self.isVaild

	def KiemTraThe(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		lhs, rhs = equation.lhs, equation.rhs
		lhs = lhs - rhs
		rhs = rhs - rhs

		a = sp.Equality(lhs, rhs)
		count = 0
		subExpr = None

		# Lấy term nhỏ
		for arg in a.lhs.atoms(sp.Pow):
			if arg.args[1] > sp.Integer(2):
				sentence = "Xin lỗi bạn nhưng mình chỉ thế được với đa thức có bậc từ 2 trở xuống."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork
			if not isinstance(arg.args[0], sp.Symbol):
				count += 1
				subExpr = arg.args[0]

		if count != 1:
			sentence = "Xin lỗi bạn nhưng mình không thể giải được phương trình này."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Kiểm tra có thay thế được không
		subPoly = sp.Integer(0)
		subNumber = sp.Integer(0)
		targetPoly = sp.Integer(0)

		# Term nhỏ
		if subExpr.func == sp.Add:
			for arg in subExpr.args:
				if len(arg.free_symbols) == 0:
					subNumber += arg
					continue
				subPoly += arg
		else:
			subPoly = subExpr

		# Term chính
		for arg in a.lhs.args:
			if len(arg.free_symbols) == 0:
				continue
			if len(arg.atoms(sp.Pow)) > 0:
				temp = list(arg.atoms(sp.Pow))
				if len(temp) != 1:
					continue
				if not isinstance(temp[0].args[0], sp.Symbol):
					continue

			targetPoly += arg

		# Kiểm tra
		result = list(sp.div(targetPoly, subPoly, domain=sp.QQ))

		if result[1] != 0 or len(result[0].free_symbols) > 0:
			sentence = "Xin lỗi bạn nhưng đa thức này mình không thể giải được. Bạn kiểm tra lại xem có nhập sai chỗ nào không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Cộng phần số trong sub term
		replaceNumber = subNumber * result[0]
		lhs = a.lhs - targetPoly
		with sp.evaluate(False):
			lhs = lhs + result[0] * subExpr - replaceNumber
			rhs = a.rhs

		if list(a.free_symbols)[0] == sp.Symbol("t"):
			symbol = sp.Symbol("n")
		else:
			symbol = sp.Symbol("t")

		a = sp.Equality(lhs, rhs, evaluate=False)
		a = a.subs(subExpr, symbol)

		if len(a.free_symbols) != 1:
			print("Số biến không thế hết!!! <Debug>")
			exit(0)

		return resultWork

	def KiemTraTrungPhuong(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		# Rút gọn
		a = sp.expand(sp.simplify(equation))

		lhs, rhs = a.lhs, a.rhs
		lhs = lhs - rhs

		# Kiểm tra bậc
		poly = sp.Poly(sp.simplify(lhs))
		listDegree = [list(i)[0] for i in poly.monoms()]
		trungPhuong = True

		if len(listDegree) > 3:
			trungPhuong = False

		elif len(listDegree) == 3:
			if listDegree[0] != 4 or listDegree[1] != 2:
				trungPhuong = False

		elif len(listDegree) == 2:
			if listDegree[0] != 4:
				trungPhuong = False
			else:
				if listDegree[1] != 2 or listDegree[1] != 0:
					trungPhuong = False
		else:
			if listDegree[0] != 4:
				trungPhuong = False

		if not trungPhuong:
			sentence = "Xin lỗi bạn nhưng đây không phải là phương trình trùng phương."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork
		return resultWork

	def BacMot(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		# Đoạn đầu
		sentence = "Phương trình bậc một là phương trình dễ nhất. Để giải phương trình, bạn chỉ cần đưa biến về bên trái, và số về bên phải.\n" \
				   "Mình sẽ giúp bạn giải phương trình bậc một bên dưới:"
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy bước giải
		listVariable = []
		listNumber = []

		# Phân tích
		sentence = "Nếu phương trình chưa ở dạng tối giản thì bạn rút nó về. Phương trình sau khi tối giản:"
		lhs = sp.expand(equation.lhs)
		rhs = sp.expand(equation.rhs)
		equation = sp.Equality(lhs, rhs)
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Quét bên trái
		if len((sp.poly(equation.lhs)).coeffs()) < 2:
			arg = equation.lhs
			if len(arg.free_symbols) == 2:
				listVariable.append(arg)
			elif len(arg.free_symbols) == 1:
				symbol = list(arg.free_symbols)[0]
				if symbol != self.bien_m:
					listVariable.append(arg)
				else:
					listNumber.append(-arg)
			else:
				listNumber.append(-arg)
		else:
			for arg in equation.lhs.args:
				if len(arg.free_symbols) == 2:
					listVariable.append(arg)
				elif len(arg.free_symbols) == 1:
					symbol = list(arg.free_symbols)[0]
					if symbol != self.bien_m:
						listVariable.append(arg)
					else:
						listNumber.append(-arg)
				else:
					listNumber.append(-arg)
		# Quét bên phải
		if len(equation.rhs.args) < 2:
			arg = equation.rhs
			if len(arg.free_symbols) == 2:
				listVariable.append(-arg)
			elif len(arg.free_symbols) == 1:
				symbol = list(arg.free_symbols)[0]
				if symbol != self.bien_m:
					listVariable.append(-arg)
				else:
					listNumber.append(arg)
			else:
				listNumber.append(arg)
		else:
			for arg in equation.rhs.args:
				if len(arg.free_symbols) == 2:
					listVariable.append(-arg)
				elif len(arg.free_symbols) == 1:
					symbol = list(arg.free_symbols)[0]
					if symbol != self.bien_m:
						listVariable.append(-arg)
					else:
						listNumber.append(arg)
				else:
					listNumber.append(arg)

		# Tất cả biến về bên trái
		tempLeft = sp.Integer(0)
		tempString = " + ".join([sp.latex(expr) for expr in listVariable])
		tempString = "\(" + tempString + "\)"
		for expr in listVariable:
			tempLeft += expr

		tempLeft = sp.collect(tempLeft, self.bien_x)

		sentence = "Đầu tiên bạn xác định những phần nào chứa " + "\(" + sp.latex(self.bien_x) + "\)" + " trong phương trình. Sau đó bạn đẩy nó về bên trái (nhớ chuyển dấu), bạn được: " + tempString + "\n" \
					"Sau đó cộng tất cả lại, bạn được:"
		term = sp.latex(tempLeft)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Tất cả số về bên phải
		tempRight = sp.Integer(0)
		tempString = " + ".join([sp.latex(expr) for expr in listNumber])
		tempString = "\(" + tempString + "\)"
		for expr in listNumber:
			tempRight += expr

		sentence = "Tiếp theo bạn xác định những phần chỉ có số trong phương trình. Sau đó đẩy nó về bên phải (nhớ chuyển dấu), bạn được: " + tempString + "\n" \
					"Sau đó cộng tất cả lại, bạn được:"
		term = sp.latex(tempRight)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Chia dấu tại biến và kết thúc
		leadingCoef = sp.Poly(tempLeft, self.bien_x).coeff_monomial(self.bien_x)
		tempLeft = sp.simplify(tempLeft / leadingCoef)
		tempRight = tempRight / leadingCoef
		finalEquation = sp.Equality(tempLeft, tempRight)

		# Kết luận
		sentence = "Cuối cùng bạn chia 2 vế cho số trước biến là số " + "\(" + sp.latex(leadingCoef) + "\)" + ". Bạn sẽ có kết quả:\n" + "\(" + sp.latex(finalEquation) + "\)"
		if not self.bien_m:
			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		types = "Explain"
		term = None
		resultWork.append((term, types, self.domain, sentence))

		# Biện luận theo m
		listNghiem = []
		sentence = "Bạn để ý, một số không thể nào chia cho số 0 được, nên để phương trình có nghiệm thì mẫu của nó phải khác 0.\n" \
				   "Bạn nhìn xem biến " + "\(" + sp.latex(self.bien_m) + "\)" + " có nằm ở mẫu không. "

		if len(leadingCoef.free_symbols) == 1:
			soBac = sp.degree(leadingCoef, gen=self.bien_m)
			if soBac < 2:
				result = list(sp.solveset(leadingCoef, domain=sp.S.Reals))
				listNghiem.append(result[0])
				sentence += "Trong trường hợp này là có, nên bạn giải phương trình bậc 1: " + "\(" + sp.latex(leadingCoef) + " = 0\)" + ". Bạn được:"
				term = sp.latex(self.bien_m) + " = " + sp.latex(result[0])
				termLatex = "\(" + term + "\)"
				types = "Explain"
				resultWork.append((termLatex, types, self.domain, sentence))
			else:
				result = list(sp.solveset(leadingCoef, domain=sp.S.Reals))
				listNghiem += result
				sentence += "Trong trường hợp này là có, nên bạn giải phương trình bậc 2: " + "\(" + sp.latex(leadingCoef) + " = 0\)" + "\n"

				if len(result) == 0:
					# Kết luận 2
					sentence += "Vì phương trình bậc 2 này không có nghiệm, nên việc mẫu bằng 0 sẽ không bao giờ xảy ra.\n" \
								"Vậy nên phương trình " + "\(" + sp.latex(tempLeft) + " = " + sp.latex(tempRight) + "\)" + " luôn có nghiệm với mọi " + "\(" + sp.latex(self.bien_m) + "\)" + "."
					types = "Done"
					resultWork.append((None, types, None, sentence))
					return resultWork
				else:
					tempResult = [sp.latex(i) for i in result]
					tempNghiem = ", ".join(tempResult)
					nghiemString = sp.latex(self.bien_m) + " = " + tempNghiem
					a = sp.Equality(leadingCoef, sp.Integer(0))

					sentence += "Phương trình có các nghiệm là:"
					termLatex = "\(" + nghiemString + "\)"
					types = "Explain_Question"
					resultWork.append((termLatex, types, self.domain, sentence, [a], "PhuongTrinh@Giai"))

		else:
			# Kết luận 2
			sentence += "Trong trường hợp này thì không. Nên bạn có thể kết luận rằng với mọi " + "\(" + sp.latex(self.bien_m) + "\)" + " thì phương trình " + "\(" + sp.latex(tempLeft) + " = " + sp.latex(tempRight) + "\)" + " luôn có nghiệm."
			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Kết luận 3
		tempResult = [sp.latex(i) for i in listNghiem]
		tempNghiem = (r"\) và \({} \neq ".format(str(self.bien_m))).join(tempResult)
		tempNghiemBang = ("\) hoặc \({} = ".format(str(self.bien_m))).join(tempResult)
		nghiemString = "\(" + sp.latex(self.bien_m) + r" \neq " + tempNghiem + "\)"
		nghiemStringBang = "\(" + str(self.bien_m) + " = " + tempNghiemBang + "\)"

		sentence = "Sau khi tìm ra các nghiệm khiến cho mẫu bằng 0, bạn có thể kết luận rằng:\n" \
				   "+ Với " + nghiemString + " thì phương trình " + "\(" + sp.latex(tempLeft) + " = " + sp.latex(tempRight) + "\)" + " có nghiệm.\n" \
					"+ Với " + nghiemStringBang + " thì phương trình " + "\(" + sp.latex(tempLeft) + " = " + sp.latex(tempRight) + "\)" + " không có nghiệm.\n"
		types = "Done"
		resultWork.append((None, types, None, sentence))
		return resultWork

	def BacHai(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		# Đoạn đầu
		sentence = "Đối với phương trình bậc hai, mình chỉ giải theo cách chính thống. Tuy nhiên nếu bạn thấy phương trình bậc 2 có thể tách " \
				   "được theo dạng A.B với A và B là các đa thức bậc 1 thì bạn nên làm như vậy.\n" \
				   "Mình sẽ chỉ bạn cách giải chính thống cho phương trình sau:"
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy bước giải
		# Mẫu
		lhs = sp.parse_expr("A*x**2 + B*x + C")
		rhs = sp.Integer(0)
		ptMau = sp.Equality(lhs, rhs)

		# Rút gọn
		equation = sp.simplify(equation)
		lhs = sp.expand(equation.lhs - equation.rhs)
		lhs = sp.collect(lhs, self.bien_x)
		rhs = sp.Integer(0)
		equation = sp.Equality(lhs, rhs, evaluate=False)

		sentence = "Nếu phương trình chưa có đưa về dạng: " + "\(" + sp.latex(ptMau) + "\)" + " thì bạn đưa nó về. Phương trình trên trở thành:"
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Xác định A, B, C
		tempPoly = sp.Poly(lhs, self.bien_x)
		listCoef = tempPoly.all_coeffs()

		sentence = "Sau khi đưa về dạng phương trình bậc 2, bạn xác định 3 thành phần A, B, C. Ba thành phần là:"
		term = "A = " + sp.latex(listCoef[0]) + ", B = " + sp.latex(listCoef[1]) + ", C = " + sp.latex(listCoef[2])
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Tính Delta
		A, B, C = listCoef
		mauDelta = sp.parse_expr("B**2 - 4*A*C")
		delta = sp.expand(B**2 - 4*A*C)

		sentence = "Tiếp theo bạn tính Delta theo công thức: " + "\(" + sp.latex(mauDelta) + "\)" + ", ra được kết quả (mình đã thu gọn lại):"
		term = sp.latex(delta)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		if not self.bien_m:
			# Kết luận
			sentence = "Cuối cùng dựa vào Delta, bạn sẽ xác định được số nghiệm của phương trình.\n"
			types = "Done"

			if delta > 0:
				mauNghiemMot = sp.parse_expr("(-B + sqrt(delta)) / (2*A)", evaluate=False)
				mauNghiemHai = sp.parse_expr("(-B - sqrt(delta)) / (2*A)", evaluate=False)
				x1 = (-B + sp.sqrt(delta)) / (2*A)
				x2 = (-B - sp.sqrt(delta)) / (2*A)
				sentence += "Vì Delta > 0, nên phương trình sẽ có 2 nghiệm phân biệt theo công thức:\n" \
							"\(x_1 = " + sp.latex(mauNghiemMot) + "\)" + "\n" \
							"\(x_2 = " + sp.latex(mauNghiemHai) + "\)" + "\n" \
							"Kết quả: \(x_1 = " + sp.latex(x1) + ", x_2 = " + sp.latex(x2) + "\)"
			elif delta == 0:
				mauNghiemKep = sp.parse_expr("(-B) / (2*A)", evaluate=False)
				x = (-B) / (2*A)
				sentence += "Vì Delta = 0, nên phương trình sẽ có một nghiệm duy nhất theo công thức:\n" \
							"\(x = " + sp.latex(mauNghiemKep) + "\)" + "\n" \
							"Kết quả: \(x = " + sp.latex(x) + "\)"
			else:
				sentence += "Vì Delta < 0, nên phương trình sẽ không có nghiệm."

			resultWork.append((None, types, None, sentence))
			return resultWork

		# Biện luận
		# Tính A
		resultA = []
		if len(A.free_symbols) == 1:
			result = list(sp.solveset(A, domain=sp.S.Reals))
			sentence = "Vì số A có biến " + "\(" + sp.latex(self.bien_m) + "\)" + " nên bạn phải tính A = 0. Tương ứng với: " + "\(" + sp.latex(A) + " = 0\)." + "\n"

			if len(result) == 0:
				sentence += "Vì phương trình không có nghiệm nên số A sẽ luôn khác 0 với mọi " + "\(" + sp.latex(self.bien_m) + "\)."
			else:
				resultA = result
				tempResult = [sp.latex(i) for i in result]
				tempNghiem = (", {} = ".format(str(self.bien_m))).join(tempResult)
				nghiemString = "\(" + str(self.bien_m) + " = " + tempNghiem + "\)"

				sentence += "Phương trình có nghiệm " + nghiemString + "."

			term = None
			types = "Explain"
			resultWork.append((term, types, self.domain, sentence))

		# Xét các TH
		# A = 0
		listResultA = []
		nghiemStringKhac = ""
		if len(resultA) != 0:
			tempResult = [sp.latex(i) for i in resultA]
			tempNghiem = ("\) hoặc \({} = ".format(str(self.bien_m))).join(tempResult)
			nghiemString = "\(" + str(self.bien_m) + " = " + tempNghiem + "\)"

			tempNghiemKhac = (r"\) và \({} \neq".format(str(self.bien_m))).join(tempResult)
			nghiemStringKhac = "\(" + str(self.bien_m) + r" \neq " + tempNghiemKhac + "\)"

			listTerm = [lhs.subs(self.bien_m, m) for m in resultA]
			listResultA = [self.LayKQ(term, self.bien_x) for term in listTerm]

			tempResult = [(sp.latex(i) + " = 0") for i in listTerm]
			sentence = "Bạn xét trường hợp A = 0.\n" \
						"Thế " + nghiemString + " vào phương trình " + "\(" + sp.latex(lhs) + " = 0\)" + " thì phương trình đó trở thành các phương trình sau:"
			term = r" \\ ".join(tempResult)
			termLatex = "\(" + term + "\)"

			types = "Explain"
			resultWork.append((termLatex, types, self.domain, sentence))

			# Kết luận 2
			sentence = ""
			term = None
			types = "Explain"

			for index, item in enumerate(listResultA):
				if item == sp.EmptySet:
					sentence += "+ Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình vô nghiệm.\n"
				else:
					nghiem = item
					sentence += "+ Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình có nghiệm là " + "\(" + sp.latex(self.bien_x) + " = " + sp.latex(nghiem) + "\)" + "\n"
			resultWork.append((term, types, self.domain, sentence))

		# A != 0
		result = list(sp.solveset(delta, domain=sp.S.Reals))

		sentence = "Xét trường hợp A != 0.\n" \
				   "Phương trình bậc 2 có 3 trường hợp: 2 nghiệm, 1 nghiệm và vô nghiệm, tương ứng với Delta > 0, Delta = 0 và Delta < 0.\n" \
				   "Nên để biện luận thì bạn giải Delta = 0, tức là: " + "\(" + sp.latex(delta) + " = 0\)." + "\n"
		types = "Explain"

		if len(result) == 0:
			tempPoly = sp.Poly(delta, self.bien_m)
			all_coef = tempPoly.all_coeffs()
			A_m = all_coef[0]
			sentence += "Lúc này Delta = 0 vô nghiệm. Đối với trường hợp này bạn chỉ cần xem vị trí A là âm hay dương.\n"

			if A_m > 0:
				mauNghiemMot = sp.parse_expr("(-B + sqrt(delta)) / (2*A)", evaluate=False)
				mauNghiemHai = sp.parse_expr("(-B - sqrt(delta)) / (2*A)", evaluate=False)
				sentence += "\(" + "A = " + sp.latex(A_m) + "\)" + " > 0 nên Delta sẽ luôn > 0 với mọi " + "\(" + sp.latex(self.bien_m) + "\)" + ". Nên phương trình đề bài sẽ có 2 nghiệm:"
				term = "\(" + "x_1 = " + sp.latex(mauNghiemMot) + r" \\ " + "x_2 = " + sp.latex(mauNghiemHai) + "\)"
			else:
				sentence += "\(" + "A = " + sp.latex(A_m) + "\)" + " < 0 nên Delta sẽ luôn < 0 với mọi " + "\(" + sp.latex(self.bien_m) + "\)" + ". Do đó phương trình đề bài sẽ vô nghiệm."
				term = None
			resultWork.append((term, types, self.domain, sentence))

			# Kết luận 3
			sentence = "Cuối cùng bạn có:\n"
			types = "Done"
			if len(resultA) != 0:
				for index, item in enumerate(listResultA):
					if item == sp.EmptySet:
						sentence += "+ Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình vô nghiệm.\n"
					else:
						nghiem = item
						sentence += "+ Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình có nghiệm là " + "\(" + sp.latex(self.bien_x) + " = " + sp.latex(nghiem) + "\)" + "\n"

				if A_m > 0:
					x1 = (-B + sp.sqrt(delta)) / (2 * A)
					x2 = (-B - sp.sqrt(delta)) / (2 * A)

					sentence += "+ Với " + nghiemStringKhac + " thì phương trình có 2 nghiệm:\n" \
								"\(x_1 = " + sp.latex(x1) + "\)" + "\n" \
								"\(x_2 = " + sp.latex(x2) + "\)"
				else:
					sentence += "+ Với " + nghiemStringKhac + " thì phương trình vô nghiệm."

			else:
				if A_m > 0:
					x1 = (-B + sp.sqrt(delta)) / (2 * A)
					x2 = (-B - sp.sqrt(delta)) / (2 * A)

					sentence += "Phương trình luôn có 2 nghiệm với mọi " + "\(" + sp.latex(self.bien_m) + "\)" + ":\n" \
								"\(x_1 = " + sp.latex(x1) + "\)" + "\n" \
								"\(x_2 = " + sp.latex(x2) + "\)"
				else:
					sentence += "Phương trình vô nghiệm với mọi " + str(self.bien_m) + ".\n"

			resultWork.append((None, types, None, sentence))
			return resultWork

		else:
			tempResult = [sp.latex(i) for i in result]
			tempNghiem = (", {} = ".format(str(self.bien_m))).join(tempResult)
			nghiemString = "\(" + sp.latex(self.bien_m) + " = " + tempNghiem + "\)"
			sentence += "Lúc này Delta = 0 có nghiệm " + nghiemString + ". Việc tiếp theo là bạn cần xác định xem " + str(self.bien_m) + " nằm trong khoảng nào thì Delta > 0, < 0 và = 0.\n" \
						"Cách đợn giản nhất là bạn chọn " + str(self.bien_m) + " theo từng khoảng khác nhau. VD nếu nghiệm bạn ra là -1 và 1 thì bạn chọn 0 và thế vào Delta để xác định dấu của nó.\n" \
						"Vùng biến thiên trong Delta là:"

			if len(result) == 1:
				nghiem = list(result)[0]
				nghiemLonHon = int(nghiem + 1)

				if delta.subs(self.bien_m, nghiemLonHon) > 0:
					delta_lon = [sp.StrictGreaterThan(self.bien_m, nghiem)]
					delta_nho = [sp.StrictLessThan(self.bien_m, nghiem)]
					delta_bang = [sp.Equality(self.bien_m, nghiem)]
				else:
					delta_lon = [sp.StrictLessThan(self.bien_m, nghiem)]
					delta_nho = [sp.StrictGreaterThan(self.bien_m, nghiem)]
					delta_bang = [sp.Equality(self.bien_m, nghiem)]
			else:
				listResult = sorted(list(result))
				x1, x2 = listResult[0], listResult[1]
				middle = (x1+x2) / 2

				if delta.subs(self.bien_m, middle) > 0:
					delta_lon = [sp.StrictGreaterThan(self.bien_m, x1), " và ", sp.StrictLessThan(self.bien_m, x2)]
					delta_nho = [sp.StrictLessThan(self.bien_m, x1), " hoặc ", sp.StrictGreaterThan(self.bien_m, x2)]
					delta_bang = [sp.Equality(self.bien_m, x1), " hoặc ", sp.Equality(self.bien_m, x2)]
				else:
					delta_lon = [sp.StrictLessThan(self.bien_m, x1), " hoặc ", sp.StrictGreaterThan(self.bien_m, x2)]
					delta_nho = [sp.StrictGreaterThan(self.bien_m, x1), " và ", sp.StrictLessThan(self.bien_m, x2)]
					delta_bang = [sp.Equality(self.bien_m, x1), " hoặc ", sp.Equality(self.bien_m, x2)]

			if len(delta_lon) > 1:
				deltaLonString = "\(" + sp.latex(delta_lon[0]) + "\)" + str(delta_lon[1]) + "\(" + sp.latex(delta_lon[2]) + "\)"
				deltaNhoString = "\(" + sp.latex(delta_nho[0]) + "\)" + str(delta_nho[1]) + "\(" + sp.latex(delta_nho[2]) + "\)"
				deltaBangString = "\(" + sp.latex(delta_bang[0]) + "\)" + str(delta_bang[1]) + "\(" + sp.latex(delta_bang[2]) + "\)"
				term = "Delta > 0: " + deltaLonString + "\n" \
						"Delta < 0: " + deltaNhoString + "\n" \
						"Delta = 0: " + deltaBangString
			else:
				deltaLonString = "\(" + sp.latex(delta_lon[0]) + "\)"
				deltaNhoString = "\(" + sp.latex(delta_nho[0]) + "\)"
				deltaBangString = "\(" + sp.latex(delta_bang[0]) + "\)"
				term = "Delta > 0: " + deltaLonString + "\n" \
						"Delta < 0: " + deltaNhoString + "\n" \
						"Delta = 0: " + deltaBangString
			resultWork.append((term, types, self.domain, sentence))

			# Kết luận 4
			sentence = "Cuối cùng bạn có:\n"
			types = "Done"
			if len(resultA) != 0:
				for index, item in enumerate(listResultA):
					if item == sp.EmptySet:
						sentence += "Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình vô nghiệm.\n"
					else:
						nghiem = item
						sentence += "Với " + "\(" + sp.latex(self.bien_m) + " = " + sp.latex(resultA[index]) + "\)" + " thì phương trình có nghiệm là " + "\(" + sp.latex(self.bien_x) + " = " + sp.latex(nghiem) + "\)" + "\n"

			x1 = (-B + sp.sqrt(delta)) / (2 * A)
			x2 = (-B - sp.sqrt(delta)) / (2 * A)
			x = (-B) / (2*A)
			nghiemStringHai = "\(" + "x_1 = " + sp.latex(x1) + ", x_2 = " + sp.latex(x2) + "\)"
			nghiemStringMot = "\(" + "x = " + sp.latex(x) + "\)"
			sentence += "+ Với " + deltaLonString + " thì phương trình có 2 nghiệm: " + nghiemStringHai + ".\n" \
						"+ Với " + deltaBangString + " thì phương trình có 1 nghiệm: " + nghiemStringMot + ".\n" \
						"+ Với " + deltaNhoString + " thì phương trình vô nghiệm."

			resultWork.append((None, types, None, sentence))
			return resultWork

	def TrungPhuong(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		# Đoạn đầu
		symbol_x = list(equation.free_symbols)[0]
		if symbol_x != sp.Symbol("t"):
			symbol_t = sp.Symbol("t")
		else:
			symbol_t = sp.Symbol("n")

		sentence = "Đây chính là phương trình trùng phương. Để giải dạng này bạn chỉ cần đặt biến " + "\(" + sp.latex(symbol_t) + " = " + sp.latex(symbol_x**2) + "\)" + " và giải phương trình bậc 2 bình thường.\n" \
					"Nghiệm của các biến " + str(symbol_t) + " sẽ luôn > hoặc = 0 do " + "\(" + sp.latex(symbol_x**2) + "\)" + " luôn luôn là số dương, nên nếu nghiệm nào âm thì bạn bỏ.\n" \
					"Sau khi có các nghiệm thỏa điều kiện, bạn chỉ cần hạ căn bậc 2 xuống các nghiệm, và với mỗi nghiệm như vậy bạn sẽ có 2 nghiệm cộng trừ cho phương trình đề bài.\n" \
					"Mình sẽ hướng dẫn bạn giải phương trình trùng phương sau:"
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy bước giải
		# Rút gọn
		lhs, rhs = equation.lhs, equation.rhs
		lhs = lhs - rhs
		rhs = rhs - rhs

		a = sp.Equality(lhs, rhs)

		sentence = "Đầu tiên bạn chuyển tất cả thành phần ở vế phải qua vế trái và rút gọn phương trình trên. Bạn được:"
		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Thế
		a = sp.Equality(lhs, rhs, evaluate=False)
		a = a.subs(symbol_x**2, symbol_t)

		sentence = "Tiếp theo bạn đặt " + "\(" + sp.latex(symbol_t) + " = " + sp.latex(symbol_x**2) + "\)" + " và thế vào phương trình trên, bạn được:"
		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Giải phương trình
		sentence = "Sau đó bạn giải phương trình bậc 2 trên theo biến " + str(symbol_t) + ":"
		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		result = list(sp.solveset(a.lhs, domain=sp.S.Reals))
		if len(result) == 0:
			sentence = "Phương trình bậc 2 sau khi giải sẽ không có nghiệm."
		else:
			tempResult = [sp.latex(i) for i in result]
			tempNghiem = ", ".join(tempResult)
			listNghiem = "\(" + sp.latex(symbol_t) + " = " + tempNghiem + "\)"
			sentence = "Phương trình bậc 2 sau khi giải sẽ có nghiệm: " + listNghiem + "."

		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain_Question"
		resultWork.append((termLatex, types, self.domain, sentence, [a], "PhuongTrinh@Giai"))

		# Kết luận
		if len(result) == 0:
			sentence = "Vì phương trình bậc 2 trên không có nghiệm nên phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " cũng sẽ không có nghiệm."
			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Lấy nghiệm t >= 0
		tempKQ = [i for i in result if i >= 0]
		listEq = [sp.Equality(symbol_x ** 2, i) for i in tempKQ]

		# Kết luận 2
		if len(tempKQ) == 0:
			sentence = "Vì tất cả các nghiệm đều < 0 nên phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " vô nghiệm."
			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		sentence = "Tiếp theo bạn cho " + "\(" + sp.latex(symbol_x**2) + " = " + sp.latex(symbol_t) + "\)" + " với những nghiệm " + str(symbol_t) + " nào > hoặc = 0. Bạn sẽ được:"
		term = r" \\ ".join([sp.latex(eq) for eq in listEq])
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Hạ căn bậc 2
		listEq = []
		for i in tempKQ:
			listEq.append(sp.Equality(symbol_x, sp.sqrt(i)))
			listEq.append(sp.Equality(symbol_x, -sp.sqrt(i)))

		sentence = "Cuối cùng bạn hạ căn bậc 2 xuống cho 2 vế, thêm nghiệm cộng trừ cho kết quả bạn vừa hạ, bạn sẽ có các nghiệm:"
		term = r" \\ ".join([sp.latex(eq) for eq in listEq])
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Kết luận 3
		tempResult = [sp.latex(i.rhs) for i in listEq]
		tempNghiem = ", ".join(tempResult)
		listNghiem = "\(" + sp.latex(symbol_x) + " = " + tempNghiem + "\)"

		sentence = "Vậy phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " có các nghiệm " + listNghiem + "."
		types = "Done"
		resultWork.append((None, types, None, sentence))
		return resultWork

	def ThePhuongTrinhBac2(self, equation):
		# (term, type, domain, sentence)
		resultWork = []

		# Đoạn đầu
		sentence = "Để giải phương trình này thì bạn nên dùng phương pháp thế.\n" \
				   "Bạn nhìn vào phần trong ngoặc của bậc 2. Bạn rút gọn đa thức trong ngoặc đó, và biến đổi phần nằm ngoài ngoặc sao cho giống với phần trong ngoặc.\n" \
				   "Tiếp theo bạn giải như phương trình bậc 2 bình thường, nếu phương trình bậc 2 vô nghiệm thì đa thức đề bài sẽ vô nghiệm.\n" \
				   "Nếu phương trình bậc 2 có nghiệm thì bạn giải ẩn phụ mà bạn đã đặt theo nghiệm bạn vừa tìm được, số nghiệm của phương trình ban đầu sẽ là số nghiệm bạn tìm được tại ẩn phụ.\n" \
				   "Mình sẽ chỉ bạn giải phương trình sau bằng phương pháp thế:"
		term = sp.latex(equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy bước giải
		# Rút gọn
		lhs, rhs = equation.lhs, equation.rhs
		lhs = lhs - rhs
		rhs = rhs - rhs

		a = sp.Equality(lhs, rhs)
		count = 0
		subExpr = None

		sentence = "Đầu tiên bạn chuyển tất cả thành phần ở vế phải qua vế trái và rút gọn phương trình trên. Bạn được:"
		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy term nhỏ
		for arg in a.lhs.atoms(sp.Pow):
			if not isinstance(arg.args[0], sp.Symbol):
				count += 1
				subExpr = arg.args[0]

		# Kiểm tra có thay thế được không
		subPoly = sp.Integer(0)
		subNumber = sp.Integer(0)
		targetPoly = sp.Integer(0)

		# Term nhỏ
		for arg in subExpr.args:
			if len(arg.free_symbols) == 0:
				subNumber += arg
				continue
			subPoly += arg

		# Term chính
		for arg in a.lhs.args:
			if len(arg.free_symbols) == 0:
				continue
			if len(arg.atoms(sp.Pow)) > 0:
				temp = list(arg.atoms(sp.Pow))
				if len(temp) != 1:
					continue
				if not isinstance(temp[0].args[0], sp.Symbol):
					continue

			targetPoly += arg

		# Kiểm tra
		result = list(sp.div(targetPoly, subPoly, domain=sp.QQ))

		sentence = "Tiếp theo bạn nhìn vào phần chứa biến trong ngoặc: " + "\(" + sp.latex(subPoly) + "\)" + " và thành phần chứa biến ngoài ngoặc: " + "\(" + sp.latex(targetPoly) + "\)" + ".\n" \
					"Bạn phải tìm tỉ lệ giữa " + "\(" + sp.latex(targetPoly) + "\)" + " và " + "\(" + sp.latex(subPoly) + "\)" + " sao cho nó ra được một con số. Bạn chịu khó nhìn một chút thì sẽ thấy:\n" \
					"\(" + sp.latex(sp.Mul(result[0], subPoly, evaluate=False)) + " = " + sp.latex(targetPoly) + "\)" + " nên tỉ lệ giữa 2 đa thức là " + "\(" + sp.latex(result[0]) + "\). "
		term = None
		types = "Explain"
		resultWork.append((term, types, self.domain, sentence))

		# Cộng phần số trong sub term
		replaceNumber = subNumber * result[0]
		lhs = tempLhs = a.lhs - targetPoly
		with sp.evaluate(False):
			lhs = lhs + result[0] * subExpr - replaceNumber
			rhs = a.rhs

		sentence = "Sau khi có tỉ lệ, bạn biến đổi sao cho " + "\(" + sp.latex(targetPoly) + "\)" + " thành " + "\(" + sp.latex(subExpr) + "\)" + ".\n" \
					"Bạn lấy phần số trong " + "\(" + sp.latex(subExpr) + "\)" + " nhân với tỉ lệ, tức là " + "\(" + sp.latex(sp.Mul(subNumber, result[0], evaluate=False)) + " = " + sp.latex(replaceNumber) + "\)" + ".\n" \
					"Sau đó bạn trừ vế trái cho " + "\(" + sp.latex(targetPoly) + "\)" + " được " + "\(" + sp.latex(tempLhs) + "\)" + ". Tiếp theo bạn cộng tỉ lệ nhân cho phần nằm trong ngoặc: " + "\(" + sp.latex(sp.Mul(result[0], subExpr, evaluate=False)) + "\)" + " và trừ đi phần số bạn vừa tính ở trên. Bạn được:"
		term = sp.latex(lhs)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Thế
		if list(a.free_symbols)[0] == sp.Symbol("t"):
			symbol = sp.Symbol("n")
		else:
			symbol = sp.Symbol("t")

		a = sp.Equality(lhs, rhs, evaluate=False)
		a = a.subs(subExpr, symbol)

		sentence = "Tiếp theo bạn đặt " + "\(" + sp.latex(symbol) + " = " + sp.latex(subExpr) + "\)" + " và thế vào phương trình, bạn sẽ được phương trình bậc 2:"
		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		result = list(sp.solveset(a.lhs, domain=sp.S.Reals))

		# ----------------- Thêm phần giải pt tại đây ---------------
		if len(result) == 0:
			sentence = "Phương trình bậc 2 sau khi giải sẽ không có nghiệm."
		else:
			tempResult = [sp.latex(i) for i in result]
			tempNghiem = ", ".join(tempResult)
			listNghiem = "\(" + sp.latex(symbol) + " = " + tempNghiem + "\)"
			sentence = "Phương trình bậc 2 sau khi giải sẽ có nghiệm: " + listNghiem + "."

		term = sp.latex(a)
		termLatex = "\(" + term + "\)"
		types = "Explain_Question"
		resultWork.append((termLatex, types, self.domain, sentence, [a], "PhuongTrinh@Giai"))

		# Kết luận
		if len(result) == 0:
			sentence = "Vì phương trình bậc 2 trên không có nghiệm nên phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " cũng sẽ không có nghiệm."
			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		listEq = [sp.Equality(subExpr, i) for i in result]
		sentence = "Tiếp theo bạn thế các nghiệm đó vào " + str(symbol) + " và giải phương trình sau, nghiệm của các phương trình cũng chính là nghiệm của phương trình đề bài:"
		term = r" \\ ".join([sp.latex(eq) for eq in listEq])
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		# Lấy các kết quả
		listResult = []
		for eq in listEq:
			result = list(sp.solveset(eq, domain=sp.S.Reals))
			listResult += result

		# Kết luận 2
		if len(listResult) == 0:
			sentence = "Sau khi giải thì phương trình trên không có nghiệm. Từ đó phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " cũng sẽ không có nghiệm."
			types = "Done"
			resultWork.append((None, types, None, sentence))
		else:
			symbol = list(equation.free_symbols)[0]
			tempResult = [sp.latex(i) for i in listResult]
			tempNghiem = ", ".join(tempResult)
			listNghiem = "\(" + sp.latex(symbol) + " = " + tempNghiem + "\)"

			sentence = "Phương trình " + "\(" + sp.latex(equation.lhs) + " = " + sp.latex(equation.rhs) + "\)" + " có nghiệm " + listNghiem + "."
			types = "Done"
			resultWork.append((None, types, None, sentence))

		return resultWork

	def GiaiPT(self):
		if not self.isVaild:
			print("Phương trình không hợp lệ. <Debug>")
			exit(0)

		# (term, type, domain, sentence)
		resultWork = []

		# ------------ Kiểm tra xong ------------
		sentence = "Biểu thức bạn nhập vào:"
		term = sp.latex(self.equation)
		termLatex = "\(" + term + "\)"
		types = "Explain"
		resultWork.append((termLatex, types, self.domain, sentence))

		if self.bacPT == 1:
			resultWork += self.BacMot(self.equation)
		else:
			if self.kieuPT == "The":
				resultWork += self.ThePhuongTrinhBac2(self.equation)
			elif self.kieuPT == "TrungPhuong":
				resultWork += self.TrungPhuong(self.equation)
			else:
				resultWork += self.BacHai(self.equation)

		return resultWork

	def LayKQ(self, term, bien):
		result = sp.solveset(term, bien, domain=sp.S.Reals)
		for i in result.args:
			if i != sp.S.Reals:
				return i
		return sp.EmptySet
