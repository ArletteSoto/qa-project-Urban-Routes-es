import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    pedir_un_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_button = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_field = (By.ID, 'phone')
    code_field = (By.ID, 'code')
    np_siguiente_button = (By.XPATH, "//div[@class='buttons']/button[text()='Siguiente']")
    confirmar_button = (By.XPATH, "//button[text()='Confirmar']")
    paid_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_option = (By.CLASS_NAME, 'pp-plus-container')
    card_number_field = (By.ID, 'number')
    code_card_field = (By.CSS_SELECTOR, "input.card-input[name='code']")
    agregar_button = (By.XPATH, "//button[contains(@class, 'button full') and text()='Agregar']")
    close_payment_method_button = (By.XPATH,
                    "//div[contains(@class, 'section') and .//div[text()='Método de pago']]//button[contains(@class, 'close-button')]")
    message_for_driver_field = (By.ID, 'comment')
    ask_for_blanket_switch = (By.XPATH,
                              "//div[@class='r-sw-container'][div[@class='r-sw-label' and contains(text(), 'Manta y pañuelos')]]//span[@class='slider round']")
    ice_cream_counter = (By.XPATH, "//div[@class='r-counter-container'][div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-plus']")
    ice_cream_counter_value = (By.XPATH,
                               "//div[@class='r-counter-container'][div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-value']")

    smart_button = (By.XPATH, "//button[contains(@class, 'smart-button')]")
    search_car_modal = (By.XPATH, "//div[contains(@class, 'order') and .//div[contains(text(), 'Buscar automóvil')]]")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)
        
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_pedir_un_taxi_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.pedir_un_taxi_button)
        )

    def click_on_pedir_un_taxi_button(self):
        self.get_pedir_un_taxi_button().click()

    def get_comfort_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.comfort_button)
        )

    def click_on_comfort_button(self):
        self.get_comfort_button().click()

    def get_phone_number_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.phone_number_button)
        )

    def click_on_phone_number_button(self):
        self.get_phone_number_button().click()

    def get_phone_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.phone_number_field)
        )

    def set_phone_number(self):
        self.get_phone_number_field().send_keys(data.phone_number)

    def get_np_siguiente_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.np_siguiente_button)
        )

    def click_on_np_siguiente_button(self):
        self.get_np_siguiente_button().click()

    def get_code_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.code_field)
        )

    def set_code_number(self):
        code = retrieve_phone_code(self.driver)
        code_input = self.get_code_field()
        code_input.clear()
        code_input.send_keys(code)

    def get_confirmar_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.confirmar_button)
        )

    def click_on_confirmar_button(self):
        self.get_confirmar_button().click()

    def get_paid_method_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.paid_method_button)
        )

    def click_on_paid_method_button(self):
        self.get_paid_method_button().click()


    def get_add_card_option(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.add_card_option)
        )

    def click_on_add_card_option(self):
        self.get_add_card_option().click()

    def get_card_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.card_number_field)
        )

    def set_card_number_field(self):
        self.get_card_number_field().click()
        self.get_card_number_field().send_keys(data.card_number)
        self.get_card_number_field().send_keys(Keys.TAB)

    def get_code_card_field(self):
        return WebDriverWait(self.driver, 5).until(
           EC.visibility_of_element_located(self.code_card_field)
        )

    def set_code_card_field(self):
        self.get_code_card_field().send_keys(data.card_code)
        self.get_code_card_field().send_keys(Keys.TAB)

    def get_agregar_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.agregar_button)
        )

    def click_on_agregar_button(self):
        self.get_agregar_button().click()

    def get_close_payment_method_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.close_payment_method_button)
        )

    def click_on_close_payment_method_button(self):
        self.get_close_payment_method_button().click()

    def get_message_for_driver_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.message_for_driver_field)
        )

    def set_message_for_driver_field(self):
        field = self.get_message_for_driver_field()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", field)
        field.clear()
        field.send_keys(data.message_for_driver)

    def get_ask_for_blanket_switch(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.ask_for_blanket_switch)
        )

    def click_on_ask_for_blanket_switch(self):
        self.get_ask_for_blanket_switch().click()

    def get_ice_cream_counter(self):
        return  WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.ice_cream_counter)
        )

    def click_on_ice_cream_counter(self):
        self.get_ice_cream_counter().click()
        self.get_ice_cream_counter().click()

    def get_ice_cream_counter_value(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ice_cream_counter_value)
        ).text

    def get_smart_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.smart_button)
        )

    def click_on_smart_button(self):
        self.get_smart_button().click()

    def get_search_car_modal(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.search_car_modal)
        )


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_rate(self):
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_pedir_un_taxi_button()
        routes_page.click_on_comfort_button()
        assert routes_page.get_comfort_button().text in "Comfort"

    def test_filled_phone_number(self):
        self.test_select_comfort_rate()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_phone_number_button()
        routes_page.set_phone_number()
        assert data.phone_number == routes_page.get_phone_number_field().get_property('value')
        routes_page.click_on_np_siguiente_button()
        routes_page.set_code_number()
        routes_page.click_on_confirmar_button()

    def test_payment_method(self):
        self.test_filled_phone_number()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_paid_method_button()
        routes_page.click_on_add_card_option()
        routes_page.set_card_number_field()
        assert data.card_number == routes_page.get_card_number_field().get_property('value')
        routes_page.set_code_card_field()
        assert data.card_code == routes_page.get_code_card_field().get_property('value')
        routes_page.click_on_agregar_button()
        routes_page.click_on_close_payment_method_button()

    def test_message_for_driver(self):
        self.test_payment_method()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message_for_driver_field()
        assert data.message_for_driver == routes_page.get_message_for_driver_field().get_property('value')

    def test_ask_for_blanket(self):
        self.test_message_for_driver()
        routes_page = UrbanRoutesPage(self.driver)

        initial_color = routes_page.get_ask_for_blanket_switch().value_of_css_property("background-color")

        routes_page.click_on_ask_for_blanket_switch()

        final_color = routes_page.get_ask_for_blanket_switch().value_of_css_property("background-color")

        assert initial_color != final_color

    def test_ice_cream_counter(self):
        self.test_ask_for_blanket()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_ice_cream_counter()
        assert routes_page.get_ice_cream_counter_value() == "2"


    def test_search_car_modal(self):
        self.test_ice_cream_counter()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_smart_button()
        modal = routes_page.get_search_car_modal()
        assert modal.is_displayed()

    @classmethod
    def teardown_class(cls):
       cls.driver.quit()
