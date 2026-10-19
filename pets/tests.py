from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import Especie, Raca, Pet, RegistroMedico
from adocoes.models import AplicacaoAdocao


class EditarRemoverPetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.dono = User.objects.create_user(username='dono', tipo_usuario='R')
        cls.outro = User.objects.create_user(username='outro', tipo_usuario='R')
        cls.adotante = User.objects.create_user(username='adotante', tipo_usuario='A')
        especie = Especie.objects.create(nome='Cachorro')
        cls.raca = Raca.objects.create(nome='SRD', especie=especie)
        cls.pet = Pet.objects.create(nome='Bolinha', cor='Preto', sexo='M', porte='P',
                                    raca=cls.raca, responsavel=cls.dono, foto='pets/existente.jpg')

    def setUp(self):
        self.editar = reverse('editar_pet', args=[self.pet.pk])
        self.remover = reverse('remover_pet', args=[self.pet.pk])
        self.dados = {'nome': 'Bolinha editado', 'raca': self.raca.pk,
                      'sexo': 'M', 'porte': 'P', 'status': 'D'}
        self.client.force_login(self.dono)

    def test_editar_preserva_foto_cor_e_responsavel(self):
        self.dados['responsavel'] = self.outro.pk
        response = self.client.post(self.editar, self.dados, follow=True)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Bolinha editado')
        self.assertEqual(self.pet.responsavel_id, self.dono.pk)
        self.assertEqual(self.pet.cor, 'Preto')
        self.assertEqual(self.pet.foto.name, 'pets/existente.jpg')
        self.assertContains(response, 'Pet atualizado com sucesso!')

    def test_edicao_invalida_nao_grava(self):
        self.dados['nome'] = 'B'
        response = self.client.post(self.editar, self.dados)
        self.assertContains(response, 'pelo menos 2 caracteres')
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Bolinha')

    def test_formulario_preenchido(self):
        response = self.client.get(self.editar)
        self.assertEqual(response.context['form'].initial['nome'], 'Bolinha')
        self.assertContains(response, 'multipart/form-data')

    def test_outro_responsavel_bloqueado_get_e_post(self):
        self.client.force_login(self.outro)
        for url in [self.editar, self.remover]:
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url, self.dados).status_code, 403)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Bolinha')

    def test_adotante_bloqueado_mesmo_associado_ao_pet(self):
        Pet.objects.filter(pk=self.pet.pk).update(responsavel=self.adotante)
        self.client.force_login(self.adotante)
        for url in [self.editar, self.remover]:
            self.assertEqual(self.client.post(url, self.dados).status_code, 403)

    def test_visitante_redirecionado_para_login_existente(self):
        self.client.logout()
        for url in [self.editar, self.remover]:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Entre na sua conta')

    def test_get_nao_exclui_e_post_exclui_com_registros_medicos(self):
        RegistroMedico.objects.create(pet=self.pet, tipo='Consulta', data=date.today(), descricao='Exame')
        self.assertContains(self.client.get(self.remover), 'Confirmar remoção')
        self.assertTrue(Pet.objects.filter(pk=self.pet.pk).exists())
        response = self.client.post(self.remover, follow=True)
        self.assertContains(response, 'Pet removido com sucesso!')
        self.assertFalse(Pet.objects.filter(pk=self.pet.pk).exists())
        self.assertEqual(RegistroMedico.objects.count(), 0)

    def test_adocao_impede_exclusao_inclusive_post_direto(self):
        AplicacaoAdocao.objects.create(pet=self.pet, adotante=self.adotante,
                                      data_solicitacao=date.today(), motivacao='Companhia', tipo_moradia='C')
        self.assertNotContains(self.client.get(self.remover), 'Confirmar remoção')
        response = self.client.post(self.remover, follow=True)
        self.assertContains(response, 'não pode ser removido')
        self.assertTrue(Pet.objects.filter(pk=self.pet.pk).exists())

    def test_csrf_obrigatorio(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.dono)
        for url in [self.editar, self.remover]:
            self.assertEqual(client.post(url, self.dados).status_code, 403)

    def test_botoes_apenas_para_dono(self):
        url = reverse('detalhe_pet', args=[self.pet.pk])
        self.assertContains(self.client.get(url), self.editar)
        self.client.force_login(self.outro)
        self.assertNotContains(self.client.get(url), self.editar)
        self.assertNotContains(self.client.get(url), self.remover)

    def test_pet_inexistente(self):
        for nome in ['editar_pet', 'remover_pet']:
            self.assertEqual(self.client.get(reverse(nome, args=[999999])).status_code, 404)

    def test_data_preenchida_no_formato_html(self):
        Pet.objects.filter(pk=self.pet.pk).update(data_nascimento=date(2020, 5, 12))
        self.assertContains(self.client.get(self.editar), 'value="2020-05-12"')

    def test_substituir_foto(self):
        import io
        import tempfile
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        with tempfile.TemporaryDirectory() as pasta, self.settings(MEDIA_ROOT=pasta):
            imagem = io.BytesIO()
            Image.new('RGB', (4, 4)).save(imagem, format='PNG')
            self.dados['foto'] = SimpleUploadedFile('nova.png', imagem.getvalue(), content_type='image/png')
            self.assertEqual(self.client.post(self.editar, self.dados).status_code, 302)
            self.pet.refresh_from_db()
            self.assertTrue(self.pet.foto.name.startswith('pets/nova'))
            self.assertTrue(self.pet.foto.storage.exists(self.pet.foto.name))
