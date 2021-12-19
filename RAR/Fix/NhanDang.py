import re


def ChuyenDeThanhDangToan(stringDe: str):
	s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
	s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

	# Lấy phương trình
	tempEquation = re.findall(r'"([^"]*)"', stringDe)
	equation = []

	# Sửa ^ -> ** và 3x -> 3*x
	for eq in tempEquation:
		newEq = eq.replace("^", "**")
		newEq = re.sub(r'([a-z])([0-9])', r'\1*\2', newEq)
		newEq = re.sub(r'([0-9])([a-z])', r'\1*\2', newEq)
		equation.append(newEq)

	# Xóa dấu
	newString = ''

	for s in stringDe:
		if s in s1:
			newString += s0[s1.index(s)]
		else:
			newString += s

	newString = newString.lower()
	newString = newString.replace(":", " ").replace(";", " ")

	stringList = newString.split()
	newStringList = []

	oldTerm = []
	connectTerm = ["he", "phuong", "xac", "bien", "luan"]
	endTerm = ["trinh", "dinh", ]
	for term in stringList:
		if term in connectTerm:
			oldTerm.append(term)
			continue
		if term in endTerm and len(oldTerm) != 0:
			oldTerm.append(term)
			newStringList.append('_'.join(oldTerm))
			oldTerm = []
			continue
		newStringList.append(term)

	# Xác định dạng
	baiToan = ''
	giai = ["giai", "lam"]
	timN = ["xac_dinh", "tim"]
	nhan = ["nhan"]
	chia = ["chia"]
	bienLuan = ["bien_luan"]

	dangToan = ''
	phuongTrinh = ["phuong_trinh"]
	hePT = ["he_phuong_trinh"]


	bienPhu = False
	for term in newStringList:
		if bienPhu:
			if len(term) == 1 and term.isalpha():
				baiToan += "_" + term
				bienPhu = False
				continue

		# Bài toán
		if term in giai:
			baiToan = "Giai"
		elif term in timN:
			baiToan = "TimN_DeNguyen"
		elif term in nhan:
			baiToan = "NhanDaThuc"
		elif term in chia:
			baiToan = "ChiaDaThuc"
		elif term in bienLuan:
			baiToan = "BienLuan"
			bienPhu = True

		# Dạng toán
		if term in phuongTrinh:
			dangToan = "PhuongTrinh"
		elif term in hePT:
			dangToan = "HPT"

	if dangToan == '':
		if len(equation) > 1:
			dangToan = "DaThuc"
		elif len(equation) == 1:
			dangToan = "UocBoi"
		else:
			dangToan = "unknown"

	if baiToan == '':
		baiToan = "unknown"

	dangCuoiCung = dangToan + "@" + baiToan
	result = "; ".join(equation)
	result += "; " + dangCuoiCung

	return result
