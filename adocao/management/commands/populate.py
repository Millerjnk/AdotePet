from decimal import Decimal
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from adocao.models import (
    Especie,Raca,Pet,RegistroMedico,CronogramaVisita,TermoAdocao,AplicacaoAdocao,Endereco
)

class Command(BaseCommand):
    help = "Popula o banco de dados com dados fictícios usando Faker"
    def handle(self, *args, **options):
        fake = Faker("pt_BR")
        User = get_user_model()
        adotantes = []
        responsaveis = []
        for i in range(80):
            usuario = User.objects.create_user(
                username = f"adotante{i+1}",
                password ="123456",
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email = f"adotante{i+1}@gmail.com",
                telefone = fake.phone_number(),
                tipo_usuario = "A",
            )
            adotantes.append(usuario)
        for i in range(20):
            usuario = User.objects.create_user(
                username=f"responsavel{i + 1}",
                password="123456",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=f"responsavel{i + 1}@email.com",
                telefone=fake.phone_number(),
                tipo_usuario="R",
            )
            responsaveis.append(usuario)

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(adotantes)} adotantes encontrados."
                f"{len(responsaveis)} responsáveis encontrados."
            )
        )
        usuarios = adotantes + responsaveis
        for usuario in usuarios:
            Endereco.objects.create(
                usuario = usuario,
                cep = fake.postcode(),
                logradouro = fake.street_name(),
                numero = str(random.randint(1, 2000)),
                complemento = random.choice(["", "Apto 101", "Apto 202", "Casa", "Bloco B", ""]),
                bairro = fake.bairro(),
                cidade = fake.city(),
                uf = fake.estado_sigla(),
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(usuarios)} endereços criados"
            )
        )
        especies_nomes=[
            "Cachorro","Gato","Coelho","Hamster","Porquinho-da-índia",
        ]
        especies=[]
        for nome in especies_nomes:
            especie, created = Especie.objects.get_or_create(nome=nome)
            especies.append(especie)
        self.stdout.write(self.style.SUCCESS("5 espécies criadas."))
        racas_por_especie = {
            "Cachorro": [
                "Labrador","Golden Retriever","Poodle","Bulldog","Beagle","Pinscher","Shih-tzu","Vira-lata",
            ],
            "Gato": [
                "Siamês","Persa","Maine Coon","Angorá",
            ],
            "Coelho": [
                "Mini Lop","Rex","Holandês",
            ],
            "Hamster": [
                "Sírio","Anão Russo","Chinês",
            ],
            "Porquinho-da-índia": [
                "Abissínio","Americano",
            ],
        }
        racas =[]
        for especie in especies:
            for nome in racas_por_especie[especie.nome]:
                raca =Raca.objects.create(
                    nome=nome,
                    especie=especie,
                )
                racas.append(raca)

        self.stdout.write(
            self.style.SUCCESS(f"{len(racas)} raças criadas.")
        )
        pets = []
        for _ in range(100):
            raca = random.choice(racas)
            pet = Pet.objects.create(
                nome=fake.first_name(),
                cor=random.choice([
                    "Preto","Branco", "Marrom","Caramelo","Cinza","Branco e preto","Marrom e branco",
                ]),
                data_nascimento=fake.date_between(
                    start_date="-12y",
                    end_date="-1y",
                ),
                sexo=random.choice(["M", "F"]),
                porte=random.choice(["P", "M", "G"]),
                peso=Decimal(str(round(random.uniform(1.0, 35.0), 2))),
                status=random.choice(["D", "A", "C"]),
                raca=raca,
                responsavel=random.choice(responsaveis),
            )
            pets.append(pet)
        self.stdout.write(
            self.style.SUCCESS(f"{len(pets)} pets criados.")
        )
        tipos =[
            "Vacina","Consulta","Exame","Medicação","Cirurgia","Castração","Outro",
        ]

        for _ in range(200):
            tipo= random.choice(tipos)
            RegistroMedico.objects.create(
                pet= random.choice(pets),
                tipo= tipo,
                data = fake.date_between(
                    start_date="-3y",
                    end_date="today",
                ),
                descricao_outro=(
                    fake.sentence()
                    if tipo == "Outro"
                    else ""
                ),
                descricao=fake.sentence(),
                veterinario=fake.name(),
                clinica=fake.company(),
            )

        self.stdout.write(
            self.style.SUCCESS("200 registros médicos criados.")
        )
        aplicacoes = []
        combinacoes_usadas = set()
        while len(aplicacoes) < 100:
            pet = random.choice(pets)
            adotante = random.choice(adotantes)
            combinacao = (pet.id, adotante.id)
            if combinacao in combinacoes_usadas:
                continue
            aplicacao = AplicacaoAdocao.objects.create(
                pet= pet,
                adotante=adotante,
                data_solicitacao=fake.date_between(
                    start_date="-2y",
                    end_date="today",
                ),
                status=random.choices(["P", "A", "R", "C"], weights=[20, 55, 15, 10], k=1)[0],
                motivacao=fake.paragraph(nb_sentences=3),
                outros_animais = random.choice([True, False]),
                tipo_moradia = random.choice(["A", "C", "O"]),
            )
            combinacoes_usadas.add(combinacao)
            aplicacoes.append(aplicacao)
        self.stdout.write(
            self.style.SUCCESS("100 aplicações de adoção criadas.")
        )
        for _ in range(100):
            CronogramaVisita.objects.create(
                aplicacao = random.choice(aplicacoes),
                data=fake.date_between(
                    start_date="-1y",
                    end_date="+6m",
                ),
                horario=fake.time(),
                local=random.choice([
                    "Abrigo AdotePet","Clínica Veterinária","Parque Municipal","Sede da ONG",
                ]),
                status=random.choice(["A", "R", "C"]),
                observacoes=fake.sentence(),
            )

        self.stdout.write(
            self.style.SUCCESS("100 visitas criadas.")
        )
    
        aplicacoes_para_termo = random.sample(aplicacoes, 50)
        for aplicacao in aplicacoes_para_termo:
            TermoAdocao.objects.create(
                aplicacao = aplicacao,
                responsavel=random.choice(responsaveis),
                data_adocao=fake.date_between(
                    start_date="-2y",
                    end_date="today",
                ),
                termos_aceitos=random.choice([True, False]),
                observacoes=fake.sentence(),
            )

        self.stdout.write(
            self.style.SUCCESS("50 termos de adoção criados.")
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Banco populado com sucesso!"
            )
        )
