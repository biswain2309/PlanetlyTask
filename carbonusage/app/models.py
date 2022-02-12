from django.db import models



class User(models.Model):
    '''User model defines the attributes of an User'''
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def get_user(self):
        return self.name + ' is added.'


class UsageTypes(models.Model):
    '''Usage Types model defines standard usage types available'''
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    factor = models.FloatField()


class Usage(models.Model):
    '''Usage model defines usage per user'''
    id = models.BigIntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    usage_type_id = models.ForeignKey(UsageTypes, on_delete=models.CASCADE)
    usage_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField()

    def get_usage(self):
        return self.user_id.name + ' is using ' + self.amount + 'amount.'
    
    # def __str__(self):
    #     return self.id




