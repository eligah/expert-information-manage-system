from django.db import models


# Create your models here.
class Expert(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Contract(models.Model):
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    home = models.CharField(max_length=255)
    post_num = models.CharField(max_length=255)

    def __str__(self):
        return "%s,%s,%s,%s,%s" % (self.phone, self.address, self.email, self.home, self.post_num)


class Education(models.Model):
    Num = models.CharField(max_length=255, primary_key=True)
    degree = models.CharField(max_length=255)
    edu = models.CharField(max_length=255)
    pro = models.CharField(max_length=255)

    def __str__(self):
        return "%s,%s,%s,%s" % (self.Num, self.degree, self.edu, self.pro)


class Job(models.Model):
    achievement = models.TextField(max_length=300, blank=True)
    comp = models.CharField(max_length=255)
    expertise = models.TextField(max_length=300, blank=True)
    part = models.BooleanField()
    retire = models.BooleanField()
    job = models.CharField(max_length=255)
    time_len = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.achievement, self.comp, self.expertise, self.part, self.retire,
                                            self.job, self.time_len, self.title)


class Capacity(models.Model):
    expert = models.OneToOneField(Expert, primary_key=True)
    agency = models.CharField(max_length=255)
    birth = models.DateField()
    image = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    politic = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    intype = models.CharField(max_length=255, default="注册")
    type_card = models.CharField(max_length=255)
    card_num = models.CharField(max_length=255)
    contract = models.ForeignKey(Contract)
    education = models.ForeignKey(Education)
    job = models.ForeignKey(Job)

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (self.expert, self.agency, self.birth, self.image, self.name,
                                                           self.politic, self.sex, self.intype, self.type_card,
                                                           self.card_num,
                                                           self.contract, self.education, self.job)


class Eval_exp(models.Model):
    description = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    time = models.DateTimeField()
    capacity = models.ForeignKey(Capacity)


class Job_exp(models.Model):
    company = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    witness = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    capacity = models.ForeignKey(Capacity)


class Qualification(models.Model):
    num = models.CharField(max_length=255)
    q_name = models.CharField(max_length=255)
    capacity = models.ForeignKey(Capacity)


class Certificate(models.Model):
    c_num = models.CharField(max_length=255)
    date = models.DateField()


class Evaluate(models.Model):
    # current = models.BooleanField()
    capacity = models.OneToOneField(Capacity, primary_key=True)
    field = models.CharField(max_length=255)
    other = models.TextField(max_length=300, blank=True)
    reason = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=255)
    certificate = models.ForeignKey(Certificate)


class Re_company(models.Model):
    com_name = models.CharField(max_length=255)
    work = models.BooleanField()
    evaluate = models.ForeignKey(Evaluate)


class Adm(models.Model):
    adm_name = models.CharField(max_length=40)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
