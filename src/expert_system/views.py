from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from .models import *
from django.http import HttpResponse
from .helper import yzm
from django.utils.timezone import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import StringIO


# Create your views here.
def index(request):
    try:
        uname = request.COOKIES['username']
    except KeyError:
        return render_to_response('expert_system/', locals())
    return render_to_response('expert_system/index.html', locals())


def logout(req):
    response = HttpResponse('logout !!')
    response.delete_cookie('username')
    return response


def change_password(request):
    return render_to_response('expert_system/change_password.html', locals())


class LoginForm(forms.Form):
    ROLE_CHOICES = (('1', '用户'),
                    ('2', '管理员'))
    role = forms.ChoiceField(widget=forms.Select, choices=ROLE_CHOICES)
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                               max_length=40)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': "form-control col-lg-4"}),
                               max_length=20)
    ccode = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}), max_length=4)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5 or len(username) > 20:
            raise forms.ValidationError("请输入5-20个以字母开头,带数字的字符串")
        if not Expert.objects.filter(username__exact=username):
            raise forms.ValidationError('%s不存在' % username)
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not Expert.objects.filter(username__exact=username, password__exact=password):
            self.cleaned_data['password'] = ""
            raise forms.ValidationError('请输入正确密码')
        return password


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                               max_length=40)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': "form-control col-lg-4"}),
                               max_length=20)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': "form-control col-lg-4"}),
                                max_length=20)
    ccode = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}), max_length=4)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5 or len(username) > 20 or (not username[0].isalpha()):
            raise forms.ValidationError("请输入5-20个以字母开头,带数字的字符串")
        if Expert.objects.filter(username__exact=username):
            raise forms.ValidationError('%s已注册' % username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5 or len(password) > 20:
            raise forms.ValidationError("请输入6-20个字母的密码")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            self.cleaned_data['password2'] = ""
            raise forms.ValidationError("请输入相同的密码")
        return password2


def mindex(req):
    experts = Expert.objects.filter(capacity__evaluate__status='审核中')
    elength = experts.count()
    # assert False
    return render_to_response('expert_system/mindex.html', {'elength': elength})


def mcolumn(req):
    experts = Expert.objects.all()
    # assert False
    return render_to_response('expert_system/mcolumn.html', locals())


def m_acc(req):
    exchoose = Expert.objects.get(username__exact='usertest')
    ecap = exchoose.capacity
    if ecap.evaluate.status == '审核中':
        ev = ecap.evaluate
        ev.status = '已通过'
        ev.save()
    return HttpResponseRedirect('../../mdetail/')


def m_rej(req):
    exchoose = Expert.objects.get(username__exact='usertest')
    ecap = exchoose.capacity
    if ecap.evaluate.status == '审核中':
        ev = ecap.evaluate
        ev.status = '已驳回'
        ev.save()
    return HttpResponseRedirect('../../mdetail/')


def m_end(req):
    exchoose = Expert.objects.get(username__exact='usertest')
    ecap = exchoose.capacity
    if ecap.evaluate.status == '审核中':
        ev = ecap.evaluate
        ev.status = '已终止'
        ev.save()
    return HttpResponseRedirect('../../mdetail/')


def mdetail(req):
    exchoose = Expert.objects.get(username__exact='usertest')
    if hasattr(exchoose, 'capacity'):
        ecap = exchoose.capacity
        cur_status = ecap.evaluate.status
        if cur_status != '待填写':
            eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf = create_emp_forms()
            # assert False
            eduf = ecap.education
            conf = ecap.contract
            jobf = ecap.job
            capf = ecap
            qualf = ecap.qualification_set.all()[0]
            # assert False
            evalef = ecap.eval_exp_set.all()[0]
            jobef = ecap.job_exp_set.all()[0]
            evalf = ecap.evaluate
            recomf = evalf.re_company_set.all()[0]
    return render_to_response('expert_system/mdetail.html', locals())


def mchangepsw(req):
    return render_to_response('expert_system/mchange_psw.html', locals())


def login(req):
    error = ""
    if req.method == 'POST':
        if req.POST['role'] == '1':
            uf = LoginForm(req.POST)
            ccode = req.POST['ccode'].strip().lower()
            session_code = req.session['CheckCode'].strip().lower()
            if ccode != session_code:
                error = '验证码错误'
                return render_to_response('expert_system/login.html', {'form': uf, 'error': error})
            elif uf.is_valid():
                uname = uf.cleaned_data['username']
                response = HttpResponseRedirect('../expert_system/index/')
                response.set_cookie('username', uname, 3600)
                return response
        else:
            return HttpResponseRedirect('../expert_system/mindex')
    else:
        uf = LoginForm()
    return render_to_response('expert_system/login.html', {'form': uf})


def register(req):
    error = ""
    if req.method == 'POST':
        uf = RegisterForm(req.POST)
        ccode = req.POST['ccode'].strip().lower()
        session_code = req.session['CheckCode'].strip().lower()
        if ccode != session_code:
            error = '验证码错误'
            return render_to_response('expert_system/register.html', {'form': uf, 'error': error})
        elif uf.is_valid():
            uname = uf.cleaned_data['username']
            upass = uf.cleaned_data['password']
            e1 = Expert(username=uname, password=upass)
            e1.save()
            response = HttpResponseRedirect('../index/')
            response.set_cookie('username', uname, 3600)
            return response

    else:
        uf = RegisterForm()
    return render_to_response('expert_system/register.html', {'form': uf})


def check_code(request):
    validate_code = yzm.create_validate_code()
    img = validate_code[0]
    img.save('yzmp.png', "png")
    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    image_data = open("yzmp.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def photo(req):
    image_data = open("hhzl.jpg", "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")
class ContractForm(forms.Form):
    phone = forms.CharField(label='手机号码', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                            help_text="*",
                            max_length=255)
    email = forms.CharField(label='邮箱号码', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                            help_text="*",
                            max_length=255)
    home = forms.CharField(label='家庭电话', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                           help_text="*",
                           max_length=255)
    post_num = forms.CharField(label='邮政编码', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                               help_text="*",
                               max_length=255)
    address = forms.CharField(label='详细通讯地址', widget=forms.TextInput(attrs={'class': "form-control col-lg-4"}),
                              help_text="*",
                              max_length=255)


class EducationForm(forms.Form):
    Num = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}),
                          max_length=255)
    EDU_CHOICES = (('1', '本科'),
                   ('2', '硕士研究生'),
                   ('3', '博士'))
    edu = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=EDU_CHOICES)
    DEGREE_CHOICES = (('1', '学士学位'),
                      ('2', '硕士学位'),
                      ('3', '博士学位'))
    degree = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=DEGREE_CHOICES)
    pro = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)


class JobForm(forms.Form):
    BOOL_CHOICES = ((True, '是'),
                    (False, '否'))

    TIME_CHOICES = (('十年', '十年'),
                    ('五年', '五年'),
                    ('两年', '两年'),
                    ('一年', '一年'),
                    ('半年', '半年'))
    achievement = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "10", 'cols': "150"}))
    expertise = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "10", 'cols': "150"}))
    comp = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    part = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=BOOL_CHOICES)
    retire = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=BOOL_CHOICES)
    # retire = forms.BooleanField()
    # part=forms.BooleanField()
    job = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    time_len = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=TIME_CHOICES)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)


class CapacityBaseForm(forms.Form):
    SEX_CHOICES = (('male', '男'),
                   ('female', '女'))
    agency = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    politic = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    type_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'readonly': 'readonly'}),
        max_length=255, initial='居民身份证')
    sex = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=SEX_CHOICES)
    birth = forms.DateField()
    card_num = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)


class QualificationForm(forms.Form):
    num = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    q_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)


class CertificateForm(forms.Form):
    num = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    date = models.DateField()


class EvalExpForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    task = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    type = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    time = forms.DateField()


class JobExpForm(forms.Form):
    company = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    job = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    witness = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    start = forms.DateField()
    end = forms.DateField()


class EvaluateForm(forms.Form):
    # current = models.BooleanField()
    field = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'readonly': 'readonly'}),
                            max_length=255)
    other = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "10", 'cols': "150"}))
    # reason = forms.CharField(widget=forms.Textarea(attrs={'rows': "10", 'cols': "150"}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                             max_length=255)


class ReCompanyForm(forms.Form):
    BOOL_CHOICES = ((True, '是'),
                    (False, '否'))
    com_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255)
    work = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=BOOL_CHOICES)


def enter_info(req):
    uname = req.COOKIES['username']
    # assert False
    if req.method == 'POST':
        eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf = create_forms(req)
        edum = conm = jobm = capm = qualm = evalem = jobem = recomm = evalm = object
        # 如果验证无效,后面的都不用验证
        formset = (eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf)
        flag = True
        for userform in formset:
            if flag and userform.is_valid():
                pass
            else:
                flag = False
        if not flag:
            # assert False
            return render_to_response('expert_system/enter_info.html', {'uname': uname,
                                                                        'eduf': eduf, 'conf': conf, 'jobf': jobf,
                                                                        'capf': capf, 'qualf': qualf, 'evalef': evalef,
                                                                        'jobef': jobef, 'recomf': recomf, 'evalf': evalf
                                                                        })
        elif evalf.cleaned_data['status'] == "待填写":
            # assert False
            # evalm.status = '已修改'
            evalf.cleaned_data['status'] = '已修改'
            # newevalf=EvaluateForm(initial=evalf)
            e = EvaluateForm(evalf.cleaned_data)
            # assert False
            return render_to_response('expert_system/enter_info.html', {'uname': uname,
                                                                        'eduf': eduf, 'conf': conf, 'jobf': jobf,
                                                                        'capf': capf, 'qualf': qualf, 'evalef': evalef,
                                                                        'jobef': jobef, 'recomf': recomf, 'evalf': e
                                                                        })
        elif evalf.cleaned_data['status'] == '已修改':
            evalf.cleaned_data['status'] = '审核中'
            e = EvaluateForm(evalf.cleaned_data)
            conm = Contract(**conf.cleaned_data)
            conm.save()
            edum = Education(**eduf.cleaned_data)
            edum.save()
            jobm = Job(**jobf.cleaned_data)
            jobm.save()
            c = capf.cleaned_data
            expert = Expert.objects.get(username__exact=uname)
            c.setdefault('expert', expert)
            c.setdefault('contract', conm)
            c.setdefault('education', edum)
            c.setdefault('job', jobm)
            # assert False
            capm = Capacity(**c)
            capm.save()
            e_c = evalef.cleaned_data
            e_c.setdefault('capacity', capm)
            evalem = Eval_exp(**e_c)
            evalem.save()
            j = jobef.cleaned_data
            j.setdefault('capacity', capm)
            jobem = Job_exp(**j)
            jobem.save()
            q = qualf.cleaned_data
            q.setdefault('capacity', capm)
            qualm = Qualification(**q)
            qualm.save()
            cert = Certificate(c_num="321123", date='2008-08-18')
            cert.save()
            ev = evalf.cleaned_data
            ev.setdefault('certificate', cert)
            ev.setdefault('capacity', capm)
            evalm = Evaluate(**ev)
            evalm.status = '审核中'
            evalm.save()
            re = recomf.cleaned_data
            re.setdefault('evaluate', evalm)
            recomm = Re_company(**re)
            recomm.save()
            return render_to_response('expert_system/enter_info.html', {'uname': uname,
                                                                        'eduf': eduf, 'conf': conf, 'jobf': jobf,
                                                                        'capf': capf, 'qualf': qualf, 'evalef': evalef,
                                                                        'jobef': jobef, 'recomf': recomf, 'evalf': e
                                                                        })
        else:
            return render_to_response('expert_system/enter_info.html', {'uname': uname,
                                                                        'eduf': eduf, 'conf': conf, 'jobf': jobf,
                                                                        'capf': capf, 'qualf': qualf, 'evalef': evalef,
                                                                        'jobef': jobef, 'recomf': recomf, 'evalf': evalf
                                                                        })
    else:
        exchoose = Expert.objects.get(username__exact=uname)
        if hasattr(exchoose, 'capacity'):
            ecap = exchoose.capacity
            cur_status = ecap.evaluate.status
            if cur_status != '待填写':
                eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf = create_emp_forms()
                # assert False
                eduf = ecap.education
                conf = ecap.contract
                jobf = ecap.job
                capf = ecap
                qualf = ecap.qualification_set.all()[0]
                # assert False
                evalef = ecap.eval_exp_set.all()[0]
                jobef = ecap.job_exp_set.all()[0]
                evalf = ecap.evaluate
                recomf = evalf.re_company_set.all()[0]
        else:
            eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf = create_emp_forms()
        return render_to_response('expert_system/enter_info.html', {'uname': uname,
                                                                    'eduf': eduf, 'conf': conf, 'jobf': jobf,
                                                                    'capf': capf, 'qualf': qualf, 'evalef': evalef,
                                                                    'jobef': jobef, 'recomf': recomf, 'evalf': evalf
                                                                    })


def create_emp_forms():
    eduf = EducationForm()
    conf = ContractForm()
    jobf = JobForm()
    capf = CapacityBaseForm()
    qualf = QualificationForm()
    evalef = EvalExpForm()
    jobef = JobExpForm()
    recomf = ReCompanyForm()
    evalf = EvaluateForm()
    return eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf


def create_forms(req):
    eduf = EducationForm(req.POST)
    conf = ContractForm(req.POST)
    jobf = JobForm(req.POST)
    capf = CapacityBaseForm(req.POST)
    qualf = QualificationForm(req.POST)
    evalef = EvalExpForm(req.POST)
    jobef = JobExpForm(req.POST)
    recomf = ReCompanyForm(req.POST)
    evalf = EvaluateForm(req.POST)
    return eduf, conf, jobf, capf, qualf, evalef, jobef, recomf, evalf
