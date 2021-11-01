from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT=10
class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def test_can_start_a_list_for_one_user(self):
        
        #Edith ouviu falar de uma nova aplicação online interessante para
        #lista de tarefas. Ela decide verificar sua homepage
        self.browser.get(self.live_server_url)

        #Ela percebe que o título da página e o cabeçalho mencionam lista de tarefas (to-do)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)        
        
        #Ela é convidada a inserir um item de tarefa imediatamente
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #Ela digita "Buy peacock feathers" (comprar penas dde pavão) em uma
        #Caixa de texto (o hobby de Edith é fazer iscas para pesca com fly)
        input_box.send_keys('Buy peacock feathers')

        #Quando ela tecla enter, a página é atualizada, e agora a página lista
        #"1: Buy peacock feathers" como um item da lista de tarefas
        input_box.send_keys(Keys.ENTER)        
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #Ainda continua havendo uma caixa de texto convidadndo-a a acrescentar
        #outro item. Ela insere "Use peacock feathers to make a fly"
        #(Usar penas de pavão para fazer um fly)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)        

        #A página é atualizada novamente e agora mostra os dois itens em sua lista
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #Satisfeita, ela volta a  dormir

    def test_multiples_users_can_start_lists_at_different_urls(self):
        #Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #Ela percebe que sua lista tem um URL único
        edith_lists_url = self.browser.current_url
        self.assertRegex(edith_lists_url, '/lists/.+')

        #Agora um novo usuário, Francis, chega ao site.
        
        ##Nova sessão do navegador
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #Francis acessa a página inicial. Não há nenhum sinal da lista de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis inicia uma nova lista inserindo um item novo. Ele
        #é menos interessante que Edith
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Francis obtem seu prórpio URL exclusivo
        francis_lists_url = self.browser.current_url
        self.assertRegex(francis_lists_url, '/lists/.+')
        self.assertNotEqual(francis_lists_url, edith_lists_url)

        #Novamente, não há nenhum sinal da lista de Edith
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfeitos ambos voltam a dormir