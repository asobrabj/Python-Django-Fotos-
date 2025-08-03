from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from accounts.models import CustomUser
import requests
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Cria usuários fake com bio e foto de perfil'

    def handle(self, *args, **kwargs):
        total_users = 10  # Quantos usuários você quer criar

        for _ in range(total_users):
            username = fake.user_name()
            email = fake.email()
            bio = fake.text(max_nb_chars=200)

            # Baixa uma imagem fake da internet (pode usar este serviço de placeholder)
            image_url = f"https://i.pravatar.cc/300?img={random.randint(1, 70)}"
            response = requests.get(image_url)

            if response.status_code == 200:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='123456',  # Senha padrão para todos os fakes
                    bio=bio
                )

                user.profile_picture.save(f"{username}.jpg", ContentFile(response.content))
                user.save()

                self.stdout.write(self.style.SUCCESS(f'Usuário "{username}" criado com sucesso!'))
            else:
                self.stdout.write(self.style.ERROR('Erro ao baixar a imagem fake'))

