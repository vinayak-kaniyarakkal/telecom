from django.db import models


class BaseContent(models.Model):
    ACTIVE_CHOICES = ((0, 'Inactive'), (2, 'Active'),)
    active = models.PositiveIntegerField(choices=ACTIVE_CHOICES,
                                         default=2)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return super(BaseContent, self).__str__()

    class Meta:
        abstract = True

    def switch(self):
        self.active = {2: 0, 0: 2}[self.active]
        self.save()


class Customer(BaseContent):
    name = models.CharField(max_length=255, unique=True)

    class Admin:
        inlines = ['Subscription']


class Plan(BaseContent):
    name = models.CharField(max_length=255, unique=True)
    rate = models.CharField(max_length=255, unique=True)


class Subscription(BaseContent):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
