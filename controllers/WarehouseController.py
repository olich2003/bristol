from controllers.BaseController import *
from controllers.DBController import DBController
from controllers.UserController import UserController


class WarehouseController:
	# Товар может иметь 3 статуса: product - в продаже, без скидки, 
	# discount - в продаже со скидкой(уценка), off - снят с продажи.

	@staticmethod
	def get_all_product():
		return DBController.get_all_product()


	@staticmethod
	def get_all_discounted_product():
		return DBController.get_all_discounted_product()


	@staticmethod
	def add_product()->str:
		# Возвращает id добавленной записи, 0 - при ошибке
		title = request.form.get('title')
		count = int(request.form.get('count'))
		date = request.form.get('date')
		status = request.form.get('status')
		if models.check_valid_product_data(title, count, date, status) and UserController.is_auth():
			DBController.add_product(title, count, date, status)
			return str(DBController.get_last_prod_id())
		return str(0)


	@staticmethod
	def update_product_status()->str:
		prod_id = request.form.get('prod_id')
		status = request.form.get('status')
		if UserController.is_auth() and prod_id.isdigit():
			DBController.update_product_status(int(prod_id), status)
			return "True"
		return "False"