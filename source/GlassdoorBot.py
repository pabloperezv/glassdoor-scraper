from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

class GlassdoorBot:

    def __init__(self, email, password, headless=True) -> None:
        self.email = email
        self.password = password
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        while 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
            user_agent = ua.random
        if headless:
            options.add_argument("--headless=new")
        else:
            options.add_argument("start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        print(self.driver.execute_script("return navigator.userAgent;"))

    
    def scrape_salary_list_page(self):
        sleep(5)
        salary_cards = self.driver.find_elements(By.CLASS_NAME, "salary-card_SalaryCard__U6U4w")
        extracted_data = []

        for card in salary_cards:
            try:
                company = card.find_element(By.CLASS_NAME, "salary-card_EmployerName__y02_p").text
                rating = card.find_element(By.CLASS_NAME, "salary-card_Rating__EUxG2").text
                salary_range = card.find_element(By.CLASS_NAME, "salary-card_TotalPay__qajkN").text
                salary_frequency = card.find_element(By.CLASS_NAME, "salary-card_TotalPaySection__cebIS").text
                average_salary_raw = card.find_element(By.CLASS_NAME, "salary-card_BreakdownBold__o0N1l").text
                job_description = card.find_element(By.CLASS_NAME, "salary-card_TitleTrim__HAigD").text

                # Convertir € a EUR
                salary_range = salary_range.replace('€', 'EUR')
                average_salary_raw = average_salary_raw.replace('€', 'EUR')

                # Convertir frequencia
                frequency = salary_frequency.split('/')[-1].split('\n')[0]
                frequency = frequency.replace('h', 'hourly')
                frequency = frequency.replace('año', 'yearly')
                frequency = frequency.replace('mes', 'monthly')

                # Procesar salarios
                min_salary_raw, max_salary_raw = salary_range.strip().split(" - ")

                def clean_salary(salary_text):

                    if 'EUR' in salary_text:
                        currency = 'EUR'
                    else:
                        currency = 'unknown'
                    
                    salary_text = salary_text.replace('EUR', '').strip()

                    # Cambiar 'mil' por '000'
                    if 'mil' in salary_text:
                        salary_text = salary_text.replace('mil', '').strip()
                        salary_value = float(salary_text.replace(',', '').replace(' ', '')) * 1000
                    else:
                        salary_value = float(salary_text.replace(',', '').replace(' ', ''))

                    return int(salary_value), currency
        
                min_salary, currency_min = clean_salary(min_salary_raw)
                max_salary, currency_max = clean_salary(max_salary_raw)
                average_salary, currency_median = clean_salary(average_salary_raw)

                extracted_data.append({
                    "company": company,
                    "job_description": job_description,
                    "rating": rating,
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "median_salary": average_salary,
                    "currency": currency_min,
                    "frequency": frequency
                })
            except Exception as e:
                print("Error extracting card:", e)
                continue

        return extracted_data


    def scrape_all_pages(self, max_pages):
        all_data = []
        login_popup_handled = False

        for page in range(max_pages):
            print(f"Escrapeando página {page + 1}...")

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "salary-card_SalaryCard__U6U4w"))
            )
            data = self.scrape_salary_list_page()
            all_data.extend(data)

            try:
                try:
                    cookie_accept = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                    )
                    cookie_accept.click()
                    print("✅ Banner de cookies cerrado.")
                    sleep(1)
                except:
                    pass

                try:
                    close_popup = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "close"))
                    )
                    close_popup.click()
                    print("✅ Popup cerrado.")
                    sleep(1)
                except:
                    pass

                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='next-page']"))
                )
                next_button.click()

                if not login_popup_handled:
                    try:
                        sleep(2)

                        email_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.ID, "hardsellUserEmail"))
                        )
                        email_input.clear()
                        email_input.send_keys(self.email)
                        print("✅ Email insertado con éxito.")
                        sleep(2)

                        continue_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='email-form-button']"))
                        )
                        continue_button.click()
                        print("✅ Botón de continuar pulsado con éxito.")
                        sleep(2)

                        password_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.ID, "hardsellUserPassword"))
                        )
                        password_input.clear()
                        password_input.send_keys(self.password)
                        print("✅ Contraseña insertada con éxito.")
                        sleep(2)

                        login_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                        )
                        login_button.click()
                        print("✅ Botón de login pulsado con éxito.")

                        login_popup_handled = True

                    except Exception as e:
                        print("ℹ️ No aparece el popup de login o error al rellenarlo", e)
                        login_popup_handled = True

            except Exception as e:
                print("No se pudo hacer clic en 'Siguiente':", e)
                break

        return all_data
