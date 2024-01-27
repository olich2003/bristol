# 
# DROP TABLE tablename;
# SHOW DATABASES;
# USE shopDB; SHOW TABLES; SHOW TABLES FROM shopDB;


from mysql.connector import connect, Error


class DBController:
	# класс отвечающий за взаимодействие бд. Основной класс который будет использовать приложение.

	__CONN = connect(
	        host="localhost",
	        user="root",
	        password="root",
	        db="shopDB"
	    ) # При окончании использования класса, нужно закрывать коннект.


	@staticmethod
	def get_cursor():
		# курсор для работы с запросами к БД. Предназначен для использования в конструкции with
		# для гарантии что поток закроется по окончании использования
		return DBController.__CONN.cursor()

	@staticmethod
	def db_commit():
		# По умолчанию коннектор MySQL не выполняет автоматическую фиксацию транзакций. 
		# В MySQL модификации, упомянутые в транзакции, происходят только тогда, когда мы используем в конце команду COMMIT. 
		# Чтобы внести изменения в таблицу, вызываем этот метод после каждой транзакции.
		DBController.__CONN.commit()


	@staticmethod
	def get_passhash_from_login(login:str)->tuple:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select password from users where login='"+login+"';")
				result = cursor.fetchone()
				return None if result == None else result[0]

	@staticmethod
	def get_role_from_login(login:str)->tuple:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select role from users where login='"+login+"';")
				result = cursor.fetchone()
				return None if result == None else result[0]

	@staticmethod
	def get_user_data_from_login(login:str)->tuple:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select * from users where login='"+login+"';")
				return cursor.fetchone()		

	@staticmethod
	def get_user_data_from_id(user_id:int)->tuple:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select * from users where id_user='"+str(user_id)+"';")
				return cursor.fetchone()


	@staticmethod
	def create_new_user(name:str, login:str, password:str, color_in_chat:str):
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				sql = "insert into users(name, login, password, date_reged, role, color_in_chat) VALUES " + \
				f"('{name}', '{login}', '{password}', now(), 'user', '{color_in_chat}');"
				cursor.execute(sql)
				conn.commit()


	@staticmethod
	def get_all_product()->list[tuple]:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT prod_id, title, count, DATE_FORMAT(date_for_off, '%d-%m-%Y'), status FROM warehouse WHERE status != 'off';")
				return cursor.fetchall()
	
	@staticmethod
	def get_all_discounted_product()->list[tuple]:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT prod_id, title, count, DATE_FORMAT(date_for_off, '%d-%m-%Y') FROM warehouse WHERE status = 'discount';")
				return cursor.fetchall()


	@staticmethod
	def add_product(title:str, count:int, date:str, status:str):
		assert status in ["product", "off", "discount"]

		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				sql = "insert into warehouse(title, count, date_for_off, status) VALUES " + \
				f"('{title}', {count}, STR_TO_DATE('{date}', '%d-%m-%Y'), '{status}');"
				cursor.execute(sql)
				conn.commit()

	@staticmethod
	def get_last_prod_id()->int:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select prod_id from warehouse order by prod_id DESC limit 1;")
				return cursor.fetchone()[0]


	@staticmethod
	def update_product_status(prod_id:int, new_status:str):
		assert new_status in ["product", "off", "discount"]

		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				sql = f"UPDATE warehouse SET status = '{new_status}' WHERE prod_id = {prod_id};"
				cursor.execute(sql)
				conn.commit()



	@staticmethod
	def get_all_messeges()->list:
		# Используем inner join для получения данных из связных таблиц. Получаем лист вида:
		# [ ( id_user | name  | message  | date_sent | color_in_chat),
		#   ...
		# ]
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT u.id_user, u.name, m.message, DATE_FORMAT(m.date_sent, '%H:%i %d.%m'), u.color_in_chat FROM users AS u INNER JOIN msg_storage AS m ON u.id_user=m.from_user_id ORDER BY m.id_msg;")
				return cursor.fetchall()


	@staticmethod
	def get_last_msg_id()->int:
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("select id_msg from msg_storage order by id_msg DESC limit 1;")
				return cursor.fetchone()[0]


	@staticmethod
	def get_last_n_msg(n:int)->list:
		# Заведомо известно что n не больше последнего msg_id.
		# Возвращаются данные вида:
		# [ (id_msg | from_user_id | message | date_sent | color_in_chat)
		#   ...
		# ]
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT u.id_user, u.name, m.message, DATE_FORMAT(m.date_sent, '%H:%i %d.%m'), u.color_in_chat FROM users AS u INNER JOIN msg_storage AS m ON u.id_user=m.from_user_id order by id_msg DESC limit "+str(n)+";")
				return cursor.fetchall()


	@staticmethod
	def send_msg(user_id:int, msg_text:str):
		with connect(host="localhost", user="root", password="root", db="shopDB") as conn:
			with conn.cursor() as cursor:
				sql = "insert into msg_storage(from_user_id, message, date_sent) VALUES " + \
				f"({user_id}, '{msg_text}', now());"
				cursor.execute(sql)
				conn.commit()



class DBIniter:
	# Класс отвечающий за инициализацию/миграция бд. 
	
	create_db_sql = "CREATE DATABASE IF NOT EXISTS shopDB CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
	drop_db_sql = "DROP DATABASE IF EXISTS shopDB;"
	show_db_sql = "SHOW DATABASES;"
	
	create_user_table = """create table IF NOT EXISTS users (
			id_user int (10) AUTO_INCREMENT,
			name varchar(20) NOT NULL,
			login varchar(50) NOT NULL UNIQUE,
			password varchar(64) NOT NULL,
			date_reged datetime NOT NULL,
			role varchar(20) NOT NULL,
			PRIMARY KEY (id_user),
			FOREIGN KEY (role) REFERENCES roles (name)
			);"""
	create_role_table = """create table IF NOT EXISTS roles (name varchar(20) NOT NULL UNIQUE);"""

	create_msg_storage_table = """create table IF NOT EXISTS msg_storage (
			id_msg int(10) AUTO_INCREMENT,
			from_user_id int(10) NOT NULL,		
			message text NOT NULL,
			date_sent datetime NOT NULL,
			PRIMARY KEY (id_msg),
			FOREIGN KEY (from_user_id) REFERENCES users (id_user) 
			); """

	create_warehouse_table = """create table  IF NOT EXISTS warehouse (
			prod_id int(10) AUTO_INCREMENT,
			title varchar(20) NOT NULL,
			count int(10) NOT NULL,
			date_for_off date NOT NULL,
			status varchar(20) NOT NULL,
			PRIMARY KEY (prod_id)
			); """


	@staticmethod
	def create_app_database(cursor):
		# здесь считаем что база данных приложения уже создана

		# создаём таблицу ролей 
		cursor.execute(DBIniter.create_role_table)
		# создаём таблицу пользователей
		cursor.execute(DBIniter.create_user_table)
		# создаём таблицу для хранения сообщений
		cursor.execute(DBIniter.create_msg_storage_table)
		# создаём таблицу склада
		cursor.execute(DBIniter.create_warehouse_table)

		# Создаём записи в созданных талицах.
		DBIniter.create_roles(cursor)
		DBIniter.create_primary_users(cursor)
		DBIniter.create_first_msg(cursor)

		print("Инициализация базы данных выполнена!")


	@staticmethod
	def create_roles(cursor):
		# Создаём поля ролей, которые будут иметь авторизованные пользователи приложения.
		cursor.execute("insert into roles(name) VALUES ('user'),('admin');")

	@staticmethod
	def create_primary_users(cursor):
		# Создаём начальных пользователей приложения. user1 - пароль user1, admin1 - admin1
		cursor.execute("""insert into users(name, login, password, date_reged, role)
			VALUES 
			('Имя Фамилия', 'user1', '77d9d48d2ac6ca6fff103f5f87d3c05531349e8ba805ea88dbd76e266a9cd16f', now(), 'user'),
			('Name Surname', 'admin1', '750ac79b05b8246dfc4de67dd77f37c39da1b37114870766d5de886bc67d9c1c', now(), 'admin');""")

	@staticmethod
	def create_first_msg(cursor):
		# Добавляем тестовые сообщение, что бы таблица не была пустой.
		cursor.execute("""insert into msg_storage(from_user_id, message, date_sent)
			VALUES
			(1, 'Всем привет!', now()),
			(2, 'Тестовое сообщение.', now()),
			(1, 'Hello world! 123 Hello world! 123  Hello world! 123  Hello world! 123 ', now()),
			(2, 'create_first_msg create_first_msg create_first_msg', now()),
			(2, 'Пятое сообщение!!!!', now());""")


	@staticmethod
	def create_first_product(cursor):
		cursor.execute("""insert into warehouse (title, count, date_for_off, status)
			VALUES 
			('Coca-cola', 20, STR_TO_DATE("10-17-2021", "%m-%d-%Y"), "product"),
			('J7', 10, STR_TO_DATE("10-07-2024", "%m-%d-%Y"), "product"),
			('Mentos', 100, STR_TO_DATE("05-11-2024", "%m-%d-%Y"), "product");""")
	

	@staticmethod
	def refresh_db(cursor):
		cursor.execute(DBIniter.drop_db_sql)
		print("Удаление базы данных выполнено!")
		DBIniter.create_app_database(cursor)



def test1():
	try:
		with DBController.get_cursor() as cursor:
			print(cursor)
			DBIniter.create_app_database(cursor)
			print(cursor)

			#cursor.execute(DBIniter.show_db_sql)
			#result = cursor.fetchall()
			#for row in result:
			#	print(row)
	except Error as e:
		print(e)

	DBController.db_commit()

def test2():
	print(DBController.get_passhash_from_login("user1") == "77d9d48d2ac6ca6fff103f5f87d3c05531349e8ba805ea88dbd76e266a9cd16f")
	print(DBController.get_passhash_from_login("user111111") == "")

	print(DBController.get_user_data_from_login("user1"))
	print(DBController.get_user_data_from_login("user111111") == None)

	print(DBController.get_user_data_from_login("user1")[4].strftime("%Y-%m-%d %H:%M"))


def test3():
	# Тестируем апи склада
	cursor = DBController.get_cursor()
	
	DBController.add_product("Gelette", 5, "31-12-2030")
	DBController.add_product("Milk", 10, "20-12-2023", "discount")
	
	DBController.update_product_status(2, 'off')
	DBController.update_product_status(3, 'discount')

	#DBController.db_commit()


	print("На уценке:", DBController.get_all_discounted_product())
	print("Весь товар:", DBController.get_all_product())



if __name__ == '__main__':
	#test2()

	#print(isinstance(DBController.get_last_msg_id(), int))
	#print(DBController.get_last_n_msg(1))

	#DBController.send_msg(1, "Ogdgfdhfdh")
	#DBController.db_commit()

	
	#DBIniter.create_first_product(cursor)
	#DBController.db_commit()
	#DBController.add_product("Fanta", 10, "31-12-2023")
	#DBController.off_product(24);
	#print(DBController.get_all_product())

	#test3()

	pass