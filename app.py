from flask import Flask, jsonify, render_template, Request, request
from src.Flask.Payslip_Generator import Payslip_Script
from src.Flask import cpa_sql
import random

app = Flask(__name__, template_folder='src/Flask/templates')
app.config['WKHTMLTOPDF_PATH'] = '/usr/bin/wkhtmltopdf' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login/<string:userName>/<string:password>")
def login_verify(userName: str,password: str):
    result = cpa_sql.login_verify(userName,password)

    return jsonify(match=str(result[0]),role=str(result[1]),setup=str(result[2]))

@app.route("/register/<string:userName>/<string:password>")
def register_check(userName: str,password: str):
    result = cpa_sql.register_check(userName,password)

    return jsonify(match=str(result[0]),config=str(result[1]))

@app.route("/registerAccount/<string:userName>/<string:firstName>/<string:lastName>/<string:email>/<string:address>/<string:suburb>/<string:postCode>/<string:phone>")
def register_account(userName: str,firstName: str,lastName: str,email: str,address: str,suburb: str,postCode: str,phone: str):
    result = cpa_sql.register_account(userName,firstName,lastName,email,address,suburb,postCode,phone)

    return jsonify(success=str(result[0]),error=str(result[1])) 

@app.route(f"/sendpayslip/<string:username>")
def sendpayslip(username: str):
    Payslip_Script.Payslip_Script(username)
    return jsonify(message="Payslip delivered succesfully")

@app.route("/settings/manager/<string:userName>")
def get_manager_settings(userName: str):
    result = cpa_sql.get_manager_settings(userName)

    return jsonify(userName=str(result[0]),password=str(result[1]),firstName=str(result[2]),lastName=str(result[3]),email=str(result[4]),address=str(result[5]),suburb=str(result[6]),contactMethod=str(result[7]),businessName=str(result[8]),entityName=str(result[9]),phone=str(result[10]))

@app.route("/settings/manager/update/<string:userNameOld>/<string:userName>/<string:password>/<string:firstName>/<string:lastName>/<string:email>/<string:phone>/<string:address>/<string:suburb>/<string:contactMethod>/<string:businessName>/<string:entityName>")
def update_manager_settings(userNameOld: str,userName: str,password: str,firstName: str,lastName: str,email: str,phone: str,address: str,suburb: str,contactMethod: str,businessName: str,entityName: str):
    result = cpa_sql.update_manager_settings(userNameOld,userName,password,firstName,lastName,email,phone,address,suburb,contactMethod,businessName,entityName)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/registerAccount/manager/<string:userName>/<string:password>/<string:firstName>/<string:lastName>/<string:email>/<string:address>/<string:suburb>/<string:businessName>/<string:phone>/<string:entityName>/<string:contactMethod>")
def create_manager(userName: str,password: str,firstName: str,lastName: str,email: str,address: str,suburb: str,businessName: str,phone: str,entityName: str,contactMethod: str):
    result = cpa_sql.create_manager(userName,password,firstName,lastName,email,phone,address,suburb,contactMethod,businessName,entityName)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/settings/employee/<string:userName>")
def get_employee_settings(userName: str):
    result = cpa_sql.get_employee_settings(userName)

    return jsonify(userName=str(result[0]),password=str(result[1]),firstName=str(result[2]),lastName=str(result[3]),email=str(result[4]),address=str(result[5]),suburb=str(result[6]),postCode=str(result[7]),phone=str(result[8]))

@app.route("/settings/employee/update/<string:userNameOld>/<string:userName>/<string:password>/<string:firstName>/<string:lastName>/<string:email>/<string:phone>/<string:address>/<string:suburb>/<string:postCode>")
def update_employee_settings(userNameOld: str,userName: str,password: str,firstName: str,lastName: str,email: str,phone: str,address: str,suburb: str,postCode: str):
    result = cpa_sql.update_employee_settings(userNameOld,userName,password,firstName,lastName,email,phone,address,suburb,postCode)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/manager/employee-list/<string:userName>")
def get_manager_employees(userName: str):
    result = cpa_sql.get_manager_employees(userName)

    class Employee() :
        def __init__(self,employee):
            self.username = employee[0]
            self.first_name = employee[1]
            self.last_name = employee[2]
            self.phone = employee[3]
            self.email = employee[4]
            self.pay_rate = employee[5].__str__()
            self.bank_account = employee[6]
            self.ird_number = employee[7]
            self.tax_code = employee[8]
            self.kiwisaver = employee[9].__str__()
            self.student_loan = employee[10].__str__()
            self.one_off_deduction = employee[11].__str__()
            self.tax_rate = employee[12].__str__()
            self.final_pay = employee[13].__str__()
            self.weekly_allowance = employee[14].__str__()
            self.weekly_allowance_nontax = employee[15].__str__()
            self.year_to_date = employee[16].__str__()
            self.child_support = employee[17].__str__()
            self.tax_credit = employee[18].__str__()
            self.benefits = employee[19].__str__()
            self.created_on = employee[20].__str__()
        def string(self):
            return {
                'username':self.username,
                'first_name':self.first_name,
                'last_name':self.last_name,
                'phone':self.phone,
                'email':self.email,
                'pay_rate':self.pay_rate,
                'bank_account':self.bank_account,
                'ird_number':self.ird_number,
                'tax_code':self.tax_code,
                'kiwisaver':self.kiwisaver,
                'student_loan':self.student_loan,
                'one_off_deduction':self.one_off_deduction,
                'tax_rate':self.tax_rate,'final_pay':self.final_pay,
                'weekly_allowance':self.weekly_allowance,
                'weekly_allowance_nontax':self.weekly_allowance_nontax,
                'year_to_date':self.year_to_date,
                'child_support':self.child_support,
                'tax_credit':self.tax_credit,
                'benefits':self.benefits,
                'created_on':self.created_on}

    employees = []

    for i in result:
        emp = Employee(i)
        employees.append(emp)

    response = []
    for i in employees:
        response.append(i.string())
        

    return jsonify(results = response)

@app.route("/manager/employee-list/update/<string:bank_account>/<string:benefits>/<string:child_support>/<string:email>/<string:final_pay>/<string:first_name>/<string:kiwisaver>/<string:last_name>/<string:one_off_deduction>/<string:pay_rate>/<string:phone>/<string:student_loan>/<string:tax_credit>/<string:tax_rate>/<string:username>/<string:username_old>/<string:weekly_allowance>/<string:weekly_allowance_nontax>/<string:ird_number>/<string:tax_code>")
def update_manager_employee_list(bank_account: str,benefits: str,child_support: str,email: str,final_pay: str,first_name: str,kiwisaver: str,last_name: str,one_off_deduction: str,pay_rate: str,phone: str,student_loan: str,tax_credit: str,tax_rate: str,username: str,username_old: str,weekly_allowance: str,weekly_allowance_nontax: str,ird_number: str,tax_code: str):
    result = cpa_sql.update_manager_employee_list(bank_account,benefits,child_support,email,final_pay,first_name,kiwisaver,last_name,one_off_deduction,pay_rate,phone,student_loan,tax_credit,tax_rate,username,username_old,weekly_allowance,weekly_allowance_nontax,ird_number,tax_code)

    return jsonify(success=str(result[0]),error=str(result[1]))


@app.route("/manager/employee-list/delete/<string:userName>")
def delete_manager_employee_list(userName: str):
    result = cpa_sql.delete_manager_employee_list(userName)
    
    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/employee/timesheet/<string:userName>")
def get_timesheet(userName: str):
    result = cpa_sql.get_timesheet(userName)

    return jsonify(results=result[0],entry_start_date=result[1],entry_end_date=result[2])

@app.route("/employee/timesheet-entrys/<string:userName>/<string:startDate>/<string:endDate>")
def get_timesheet_entry(userName: str,startDate: str,endDate: str):
    result = cpa_sql.get_timesheet_entry(userName,startDate,endDate)

    class Timesheet_entry() :
        def __init__(self,sheet):
            self.timesheet_entry_id = sheet[0]
            self.date = sheet[1].__str__()
            self.start_time = sheet[2].__str__()
            self.end_time = sheet[3].__str__()
            self.unpaid_break = sheet[4].__str__()
            self.pay_type = sheet[5]
            self.comments = sheet[6]
        def string(self):
            return {'timesheet_entry_id': self.timesheet_entry_id,
                     'date' : self.date,
                     'start_time' : self.start_time,
                     'end_time' : self.end_time,
                     'unpaid_break' : self.unpaid_break,
                     'pay_type' : self.pay_type,
                     'comments' : self.comments}
    
   
    entrys = []

    for i in result:
        ent = Timesheet_entry(i)
        entrys.append(ent)

    response = []
    for i in entrys:
        response.append(i.string())
        

    return jsonify(results = response)

@app.route("/employee/timesheet-entrys/update/<string:timesheet_entry_id>/<string:date>/<string:start_time>/<string:end_time>/<string:unpaid_break>/<string:pay_type>/<string:comment>")
def update_timesheet_entry(timesheet_entry_id: str,date: str,start_time: str,end_time: str,unpaid_break: str,pay_type: str,comment: str):
    result = cpa_sql.update_timesheet_entry(timesheet_entry_id,date,start_time,end_time,unpaid_break,pay_type,comment)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/employee/timesheet-entrys/delete", methods=['POST'])
def delete_timesheet_entrys():

    data_array = request.get_json()
    print(data_array)
    
    data_tuple = tuple(data_array)
    print(data_tuple)

    result = cpa_sql.delete_timesheet_entrys(data_tuple)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/employee/timesheet-entrys/new/<string:username>/<string:date>/<string:start_time>/<string:end_time>/<string:unpaid_break>/<string:pay_type>/<string:comment>")
def new_timesheet_entry(username: str,date: str,start_time: str,end_time: str,unpaid_break: str,pay_type: str,comment: str):
    
    result = cpa_sql.new_timesheet_entry(username,date,start_time,end_time,unpaid_break,pay_type,comment)

    return jsonify(success=str(result[0]),error=str(result[1]))

@app.route("/manager/timesheets/<string:userName>")
def get_employee_timesheets(userName: str):
    result = cpa_sql.get_employee_timesheets(userName)

    return jsonify(results = result)

@app.route("/employee/leave/<string:userName>")
def get_employee_leave(userName: str):
    result = cpa_sql.get_employee_leave(userName)

    return jsonify(leave_balance = str(result[0]),leave_balance_hours = str(result[1]),leave_entrys = result[2])

@app.route("/employee/leave/update/<string:userName>/<string:leave_start_date>/<string:leave_end_date>/<string:leave_type>")
def update_employee_leave(userName: str,leave_start_date: str,leave_end_date: str,leave_type: str):
    result = cpa_sql.update_employee_leave(userName,leave_start_date,leave_end_date,leave_type)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/employee/leave/new/<string:userName>/<string:leave_start_date>/<string:leave_end_date>/<string:leave_type>")
def new_employee_leave_entry(userName: str,leave_start_date: str,leave_end_date: str,leave_type: str):
    result = cpa_sql.new_employee_leave_entry(userName,leave_start_date,leave_end_date,leave_type)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/manager/employee-leave/<string:userName>")
def manager_employee_leave(userName: str):
    result = cpa_sql.manager_employee_leave(userName)

    return jsonify(results=result)

@app.route("/manager/employee-leave/decline/<string:leave_entry_id>")
def manager_employee_leave_decline(leave_entry_id: str):
    result = cpa_sql.manager_employee_leave_decline(leave_entry_id)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/manager/employee-leave/accept/<string:leave_entry_id>")
def manager_employee_leave_accept(leave_entry_id: str):
    result = cpa_sql.manager_employee_leave_accept(leave_entry_id)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/manager/pay-run/<string:userName>")
def pay_run_info(userName: str):
    result = cpa_sql.pay_run_info(userName)

    return jsonify(results=result)

@app.route("/manager/pay-run/execute/all/<string:userName>")
def pay_run_execute_all(userName: str):
    result = cpa_sql.pay_run_execute_all(userName)

    if result[0] == 'Failed':

        return jsonify(success = str(result[0]),error = str(result[1]))

    else:
        for id in result[0]:
            Payslip_Script.Payslip_Script(id)

        return jsonify(success = 'Success',error = 'n/a')
        
@app.route("/manager/employee-list/new/<string:bank_account>/<string:benefits>/<string:child_support>/<string:final_pay>/<string:kiwisaver>/<string:one_off_deduction>/<string:pay_rate>/<string:student_loan>/<string:tax_credit>/<string:tax_rate>/<string:username>/<string:weekly_allowance>/<string:weekly_allowance_nontax>/<string:ird_number>/<string:tax_code>/<string:manager>")
def new_manager_employee(bank_account: str,benefits: str,child_support: str,final_pay: str,kiwisaver: str,one_off_deduction: str,pay_rate: str,student_loan: str,tax_credit: str,tax_rate: str,username: str,weekly_allowance: str,weekly_allowance_nontax: str,ird_number: str,tax_code: str,manager: str):
    string= list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    random.shuffle(string)
    password_string = ''.join(string)[:9]

    result = cpa_sql.new_manager_employee(password_string,bank_account,benefits,child_support,final_pay,kiwisaver,one_off_deduction,pay_rate,student_loan,tax_credit,tax_rate,username,weekly_allowance,weekly_allowance_nontax,ird_number,tax_code,manager)

    return jsonify(success=str(result[0]),error=str(result[1]),password=str(result[2]))

@app.route("/manager/pay-run/add-stat/<string:username>/<string:date>/<string:stat_length>")
def add_new_stat_day(username: str,date: str,stat_length:str):
    result = cpa_sql.add_new_stat_day(username,date,stat_length)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/manager/pay-run/execute/selected", methods=['POST'])
def pay_run_execute_selected():
    data_array = request.get_json()
    print(data_array)
    
    list_of_tuples = [tuple(data.split(',')) for data in data_array]
    print(list_of_tuples)
    result = cpa_sql.pay_run_execute_selected(list_of_tuples)

    if result[0] == 'Failed':

        return jsonify(success = str(result[0]),error = str(result[1]))

    else:
        for id in result[0]:
            Payslip_Script.Payslip_Script(id)

        return jsonify(success = 'Success',error = 'n/a')

@app.route("/auth/add/<string:username>/<string:authKey>")
def auth_add(username: str,authKey: str):
    
    result = cpa_sql.auth_add(username,authKey)

    return jsonify(success = str(result[0]),error = str(result[1]))

@app.route("/auth/validate/<string:username>/<string:authKey>")
def auth_validate(username: str,authKey: str):
    
    result = cpa_sql.auth_validate(username,authKey)

    return jsonify(success = str(result[0]),error = str(result[1]),match = str(result[2]))
    
if __name__ == "__main__":
    app.run(debug=True)
