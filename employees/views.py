from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Employee
from .forms import EmployeeForm
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import random
from math import ceil, floor
from django_seed import Seed


def profile(request, pk):

	empl = Employee.objects.get(pk = pk)
	context = {
		'empl': empl
	}
	return render(request, 'employees/profile.html', context)


def update(request, pk):

	empl = Employee.objects.get(pk = pk)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, 
			request.FILES, 
			instance = empl)
		if form.is_valid():
			form.save()
			return redirect('empl-profile', pk = pk)
	else:
		form = EmployeeForm(instance = empl)

	context = {
		'empl': empl,
		'form': form
	}
	return render(request, 'employees/update.html', context)


def delete(request, pk):

	Employee.objects.get(pk = pk).delete()
	return redirect('empl-list')


def create(request):

	if request.method == 'POST':
		form = EmployeeForm(request.POST)		
		if form.is_valid():
			form.save()
			new_empl = Employee.objects.last()
			return redirect('empl-profile', pk = new_empl.id)
	else:
		form = EmployeeForm()

	return render(request, 'employees/create.html',
	 {'form': form})


def seeder(tree_height, empl_num):

	if Employee.objects.last():
		id_shift = Employee.objects.last().id
	else:
		id_shift= 0	
	Employee.objects.all().delete()

	# Seed without hierarcy
	seeder = Seed.seeder()
	seeder.add_entity(Employee, empl_num, {
		'superviser': None
    })
	inserted_pks = seeder.execute()

	# "init_num" is number of employee on top of hierarcy
	init_num = floor((empl_num / 2) ** (1 / tree_height))
	depth = 0
	len_forloop = init_num
	empl_id = id_shift + 1

	#Loop "tree_height" times to get required number
	# of hierarcy levels
	while True:
		for i in range(1, len_forloop + 1):

			if depth > 0:
				superv_id = ceil(i / init_num)
				empl = Employee.objects.get(id = empl_id)
				empl.superviser_id = id_shift + superv_id
				empl.save()							
			empl_id += 1
			if empl_id >= id_shift + empl_num:
				return

		len_forloop = len_forloop * init_num
		depth += 1


@login_required
def seed(request):

	seeder(5, 500)
	return redirect('empl-list')


@login_required
def list(request):

	paginator = Paginator(Employee.objects.all(), 10)
	empl_list = paginator.page(1)
	html = make_empl_list(empl_list)

	context = {
		'html': html
	}
	return render(request, 'employees/list.html', context)


def make_empl_list(empl_list):

	html = ''
	for empl in empl_list:
		html += '<div class="border p-3"><div class="media">\
				<div class="media-left"><img src="{}"\
				class="media-object img-responsive img-rounded"\
				style="max-width: 100px"></div><div\
				class="media-body ml-3"><h4 class="media-heading">\
				<a href="{}"> {} {} {}</a></h4>\
				<p>id: {}</p><p>position: {}</p>\
				<p">salary: {}</p><p>employment date: {}</p>\
				<p>superviser id: {}</p></div></div></div><br>'.\
				 format(empl.image.url, 'http://127.0.0.1:8000/employees/' 
				 	+ str(empl.id), empl.first_name, empl.middle_name, 
				 	empl.last_name, empl.id, empl.position, empl.salary, 
				 	empl.empl_date, empl.superviser_id)

	# Page buttons
	if empl_list.has_other_pages:		
		for i in empl_list.paginator.page_range:
			if empl_list.number == i:
				html += '<a class="btn btn-info mb-5 mr-2" \
				name = "page" id="{}">{}</a>'.format(i, i)
			elif i - 3 < empl_list.number < i + 3:
				html += '<a class="btn btn-outline-info mb-5 mr-2" \
				name = "page" id="{}">{}</a>'.format(i, i)

	return html


@login_required
def search(request):

	if request.method == 'GET':

		empl_list = Employee.objects
		page = request.GET.get('page', 1)
		sort_param = request.GET.get('sort_param', None)
		empl_id = request.GET.get('id', None)
		first_name = request.GET.get('first_name', None)
		middle_name = request.GET.get('middle_name', None)
		last_name = request.GET.get('last_name', None)
		position = request.GET.get('position', None)
		empl_date = request.GET.get('empl_date', None)
		salary = request.GET.get('salary', None)
		superviser_id = request.GET.get('superviser_id', None)

		if empl_id:
			empl_list = empl_list.filter(id = empl_id)
		if first_name:
			empl_list = empl_list.filter(first_name = first_name)
		if middle_name:
			empl_list = empl_list.filter(middle_name = middle_name)
		if last_name:
			empl_list = empl_list.filter(last_name = last_name)
		if position:
			empl_list = empl_list.filter(position = position)
		if empl_date:
			empl_list = empl_list.filter(empl_date = empl_date)
		if salary:
			empl_list = empl_list.filter(salary = salary)
		if superviser_id:
			empl_list = empl_list.filter(superviser_id = superviser_id)
		if sort_param:
			empl_list = empl_list.order_by(sort_param)
		if page:
			paginator = Paginator(empl_list.all(), 10)
			try:
				empl_list = paginator.page(page)
			except:
				empl_list = paginator.page(1)

		if empl_list:
			html = make_empl_list(empl_list)
		else:
			html = ''

	return JsonResponse({'html': html})


''' Lazy tree '''

def make_lazy_tree(empl_list, cur_depth):

	if cur_depth < 2:
		str_html = '<ul>'

		for empl in empl_list:
			str_html += '<li draggable="true" id="{}">id: {}, \
			fullname: {} {} {}, salary: {}, \
			position: {}, super id: {}. \
			</li>'.format(empl.id, empl.id, 
				empl.first_name, empl.middle_name, empl.last_name, 
				empl.salary, empl.position, empl.superviser_id)
			und_empl_list = Employee.objects.filter(superviser = empl)

			if und_empl_list:
				str_html += make_lazy_tree(und_empl_list, 
					cur_depth + 1)

		str_html += '</ul>'		
		return str_html
	else:
		return ''


@login_required
def tree(request):

	init_empl = Employee.objects.filter(superviser__isnull=True)
	html = make_lazy_tree(init_empl, 0)

	context = {
		'employees': Employee.objects.all(),
		'tree': html
	}
	return render(request, 'employees/lazy_tree.html', context)


@login_required
def tree_lazy_open(request):

	if request.method == 'GET':
		id = request.GET.get('id', None)
		empl = Employee.objects.get(pk=id)
		und_empl_list = Employee.objects.filter(superviser = empl)
		if und_empl_list:
			html = make_lazy_tree(und_empl_list, 0)
		else:
			html = ''

	return JsonResponse({'html': html})


@login_required
def change_super(request):

	if request.method == 'GET':

		empl_id = request.GET.get('empl_id', None)
		empl = Employee.objects.get(pk=empl_id)

		super_id = request.GET.get('super_id', None)

		empl.superviser_id = super_id
		empl.save()


