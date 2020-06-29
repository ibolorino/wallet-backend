from rest_framework.serializers import (
    CharField,
    DateField,
    ValidationError,
    ModelSerializer
)
from django.db.models import Q
from .models import Person
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserCreateSerializer(ModelSerializer):
    repassword = CharField(write_only=True, label="Repeat password")
    name = CharField(write_only=True)
    cpf = CharField(write_only=True)
    birthday = DateField(write_only=True, format="%d/%m/%Y")

    class Meta:
        model = User
        fields = ['username', 'password', 'repassword', 'email', 'name', 'cpf', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        repassword = data.get('repassword', None)
        email = data.get('email', None)
        name = data.get('name', None)
        cpf = data.get('cpf', None)
        birthday = data.get('birthday', None)
        if (password != repassword):
            raise ValidationError("Passwords fields must be equals.")
        else:
            if len(Person().get_by_cpf(cpf)) >= 1:
                raise ValidationError("CPF already registred.")
            else:
                user, created = User.objects.get_or_create(username=username, email=email)
                if created:
                        user.set_password(password)
                        user.save()
                user = User.objects.get(username=username)
                person = Person(name=name, cpf=cpf, birthday=birthday, user_id=user.id).save()
        return data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Invalid username.")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Invalid password.")
        data['token'] = "Esse é o token"
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.person.name
        token['username'] = user.username
        return token