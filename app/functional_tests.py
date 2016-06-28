from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import unittest


class TesteVelocidadeFixa(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.maximize_window()
		self.browser.implicitly_wait(5)

		user = User.objects.create_user(username='asdf', email='teste@teste.com', password='asdf1234')

		#Abrindo o link a ser testado
		self.browser.get('http://localhost:8000/login')

		#Encontrando os elementos na página de login
		usuario = self.browser.find_element_by_id('id_username')
		senha = self.browser.find_element_by_id('id_password')
		entrar = self.browser.find_element_by_id('id_entrar')

		#Inserindo os dados do usuário
		usuario.send_keys('asdf')
		senha.send_keys('asdf1234')

		#Enviando o formulário
		entrar.send_keys(Keys.RETURN)

	def tearDown(self):
		self.browser.quit()

	def teste_iniciar_teste_velocidade_fixa_when_no_login(self):
		#Abrindo o link da página de teste por velocidade fixa
		self.browser.get('http://localhost:8000/iniciarTesteVelocidadeFixa')

		#Encontrando elementos na página teste por velocidade fixa
		codigo = self.browser.find_element_by_id('id_amortecedor_codigo')
		diametro = self.browser.find_element_by_id('id_amortecedor_diametro_externo')
		nome = self.browser.find_element_by_id('id_teste_nome')
		ciclo = self.browser.find_element_by_id('id_teste_quantidade_ciclo')
		curso = self.browser.find_element_by_id('curso')
		velocidade = self.browser.find_element_by_id('testeVF_velocidade')
		observacoes =  self.browser.find_element_by_id('id_teste_observacoes')
		iniciar = self.browser.find_element_by_id('id_enviar')

		#Preenchendo dados do amortecedor
		codigo.send_keys('123456')
		diametro.send_keys('6')

		#Preenchendo dados do teste
		nome.send_keys('Teste 1')
		ciclo.send_keys('10')
		curso.send_keys('10')
		velocidade.send_keys('10')
		observacoes.send_keys('observacoes')

		#Enviando formulário
		iniciar.send_keys(Keys.RETURN)
		

if __name__ == '__main__':
    unittest.main(warnings='ignore') 




		