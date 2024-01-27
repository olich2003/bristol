from flask import request, make_response, url_for, redirect, session, render_template, abort

from main import app
import models
import controllers



@app.route('/')
def index():
	return controllers.PageController().call(page='hello_page')


@app.route('/enter', methods=['GET', 'POST'])
def enter():
	return controllers.PageController().call(page='enter')


@app.route('/user')
def home_user_page():
	# user_id=-1 функция контроллера ожидает в случае, если пользователь запрашивает собственную страницу
	return controllers.PageController().call(page='user', user_id=-1)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_page(user_id):
	return controllers.PageController().call(page='user_foreign_page', user_id=int(user_id))


@app.route('/new_user', methods=['GET', 'POST'])
def create_new_user():
	return controllers.PageController().call(page='create_new_user')


@app.route('/schedule')
def schedule():
	# загружаем расписание из базы данных
	return render_template('schedule.html')


@app.route('/chat')
def chat():
	return controllers.PageController().call(page='chat_page')


@app.route('/warehouse')
def warehouse():
	return controllers.PageController().call(page='warehouse_page')




### API ###

@app.route('/chat_api', methods=['GET', 'POST'])
def chat_api():
	return controllers.ChatController().chat_proccess()


@app.route('/warehouse/all', methods=['GET', 'POST'])
def get_all_product():
	return controllers.WarehouseController().get_all_product()


@app.route('/warehouse/discounted', methods=['GET', 'POST'])
def get_all_discounted_product():
	return controllers.WarehouseController().get_all_discounted_product()

@app.route('/warehouse/add_product', methods=['POST'])
def add_product():
	return controllers.WarehouseController().add_product()


@app.route('/warehouse/update_product_status', methods=['POST'])
def update_product_status():
	return controllers.WarehouseController().update_product_status()


@app.route('/logout', methods=['POST'])
def logout():
	return controllers.UserController.logout()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404