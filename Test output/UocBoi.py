import sympy as sp
import ToanDaThuc

class UocBoi:
	termString = ""
	term = None
	isVaild = False
	domain = None

	def PassTerm(self, p_term, domain=sp.ZZ):
		# (term, type, domain, sentence)
		resultWork = []

		# ------------ Kiểm tra điều kiện đầu vào ------------
		if not p_term:
			print("Không có term để làm!!! <Debug>")
			exit(0)

		if isinstance(p_term, str):
			try:
				poly = sp.parse_expr(p_term, evaluate=False)
			except:
				sentence = "Phương trình " + p_term + " không phải là dạng mình có thể làm được, bạn kiểm tra lại xem biểu thức có nhập đúng không."
				types = "Abort"
				resultWork.append((None, types, None, sentence))
				return resultWork, self.isVaild
		else:
			poly = p_term

		self.term = sp.simplify(poly)
		self.domain = domain
		self.termString = p_term
		self.isVaild = True

		return resultWork, self.isVaild

	def TimN_DeNguyen(self):
		if not self.isVaild:
			print("Phương trình không hợp lệ. <Debug>")
			exit(0)

		# (term, type, domain, sentence)
		resultWork = []
		poly = self.term

		# ------------ Kiểm tra điều kiện đầu vào ------------
		# Kiểm tra chỉ có 1 dấu /
		if self.termString.count("/") > 1:
			sentence = "Phương trình " + self.termString + " không phải là dạng mình có thể làm được, bạn kiểm tra lại xem biểu thức có nhập đúng không."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Nếu số biến không phải 1
		if len(poly.free_symbols) > 1:
			sentence = "Mình chỉ có thể làm với biểu thức có 1 biến mà thôi."
			types = "Abort"
			resultWork.append((None, types, None, sentence))
			return resultWork
		if len(poly.free_symbols) == 0:
			isInteger = sp.simplify(poly).is_Integer

			if isInteger:
				sentence = "Phương trình của bạn luôn có nghiệm nguyên."
			else:
				sentence = "Phương trình của bạn không bao giờ có nghiệm nguyên."

			types = "Done"
			resultWork.append((None, types, None, sentence))
			return resultWork

		# Kiểm tra bậc tử và mẫu
		for arg in poly.args:
			# Mẫu
			if arg.func == sp.Pow:
				tempPoly = arg.base
				# Kiểm tra bậc là số nguyên
				for argLower in tempPoly.args:
					if argLower.func == sp.Pow:
						if not argLower.exp.is_Integer:
							sentence = "Xin lỗi bạn nhưng mình chỉ có thể giải được với các bậc là số nguyên."
							types = "Abort"
							resultWork.append((None, types, None, sentence))
							return resultWork
				# Kiểm tra mẫu là bậc 1
				if sp.degree(tempPoly) > 1:
					sentence = "Xin lỗi bạn nhưng mình chỉ có thể giải được biểu thức với mẫu bậc 1 thôi."
					types = "Abort"
					resultWork.append((None, types, None, sentence))
					return resultWork
			# Tử
			else:
				tempPoly = arg
				# Kiểm tra bậc là số nguyên
				for argUpper in tempPoly.args:
					if argUpper.func == sp.Pow:
						if not argUpper.exp.is_Integer:
							sentence = "Xin lỗi bạn nhưng mình chỉ có thể giải được với các bậc là số nguyên."
							types = "Abort"
							resultWork.append((None, types, None, sentence))
							return resultWork

		# ------------ Kiểm tra xong ------------
		sentence = "Biểu thức bạn nhập vào: "
		types = "Explain"
		resultWork.append((poly, types, self.domain, sentence))

		# Nếu args > 2 thì rút gọn
		if len(poly.args) > 2:
			sentence = "Bạn rút gọn biểu thức trên:"
			poly = sp.together(sp.expand(poly))
			types = "Explain"
			resultWork.append((poly, types, self.domain, sentence))

		# Chia biểu thức
		upper = lower = poly.args[0]
		for arg in poly.args:
			if arg.func == sp.Pow:
				lower = arg.base
			else:
				upper = arg

		sentence = "Để biết được biểu thức có là số nguyên hay không, bạn cần biến hóa sao cho biểu thức của bạn có dạng  (số / biểu thức) \n" \
				   "Cách dễ nhất là bạn lấy biểu thức ở trên chia cho biểu thức ở dưới.\n" \
				   "Sau khi có kết quả, bạn viết lại biểu thức theo dạng: Kết quả + (Phần dư / biểu thức chia)."
		divisor, remainder = sp.div(upper, lower, domain=self.domain)
		poly = sp.Add(divisor, remainder / lower)
		types = "Explain"
		resultWork.append((poly, types, self.domain, sentence))

		# Giải thích chia đa thức
		daThuc = ToanDaThuc.DaThuc()
		_, vaild = daThuc.PassTerm(upper, lower)

		if not vaild:
			print("Sai phần pass đa thức. <Debug>")
			exit(0)

		tempWork = daThuc.ChiaDaThuc()
		resultWork += tempWork

		# Kết luận
		targetPoly = remainder / lower
		all_divisors = sp.divisors(remainder)
		sentence = "Theo đề bài, các biến trong biểu thức đều thuộc số nguyên, nên với những phần nào không có số chia, phần đó chắc chắn sẽ là số nguyên.\n" \
				   "Việc còn lại là bạn xác định giá trị của biểu thức có số chia sao cho kết quả biểu thức đó cũng là số nguyên.\n" \
				   "Bạn để ý, để biểu thức " + str(targetPoly) + " có kết quả nguyên thì " + str(lower) + " phải là ước của " + str(remainder) + "\n" \
					"Nói cách khác, " + str(lower) + " phải bằng với các ước của " + str(remainder) + "\n" \
					"Các số chia hết (hay ước) của " + str(remainder) + " là {}".format(all_divisors)

		types = "Explain"
		resultWork.append((targetPoly, types, self.domain, sentence))

		# Kết quả
		result = []
		symbol = list(lower.free_symbols)[0]

		for divisor in all_divisors:
			result += sp.solve(lower - divisor, symbol)

		sentence = "Kết quả: " + str(symbol) + " = {}".format(result) + " thì biểu thức để bài là số nguyên."
		types = "Done"
		resultWork.append((None, types, None, sentence))

		return resultWork
