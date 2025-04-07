# Glassdoor Scraper
 
## Contenido del repositorio:
- **Source**: contiene GlassdoorBot.py que es un archivo que inicializa un bot usando selenium y contiene diferentes métodos bajo una única clase. Luego tenemos en main.ipynb un notebook donde configuramos los parámetros y ejecutamos el bot.
- **Dataset**: contiene los distintos datasets obtenidos.

## Como podemos ejecutar el scraper?

1. Creamos un entorno virtual


   - Linux/macOS
    ```bash
    python3 -m venv venv_scraper --system-site-packages

    source venv_scraper/bin/activate
    ```

   - Windows
    ```cmd
    python3 -m venv venv_scraper

    venv_scraper\Scripts\activate
    ```

   - Actualizar pip
    ```bash
    python -m pip install --upgrade pip
    ```
    - Instalar requirements
    ```bash
    pip install -r requirements.txt
    ```

2. Debemos hacer una busqueda en el navegador con la siguiente estructura: *"Sueldos [job_position] en [city] glassdoor"* y copiar la URL, además debemos de fijarnos en el número total de páginas que contiene.
3. Abrimos nuestro notebook main.ipynb, en el debemos insertar:
    - Email usado al crear una cuenta de glassdoor
    - Contraseña
    - URL que deseamos scrapear
    - Máximo de páginas
    - Parametro headless, si headless = False veremos el proceso de scraping en una ventana emergente.
    - Nombre de nuestro dataset

4. Ejecutar el notebook.

---

**IMPORTANTE:** 
- Los datos han sido recopilados con fines exclusivamente académicos.
- Puede estar sujeto a restricciones de uso según los términos de Glassdoor.
- El autor no se responsabiliza por el uso no autorizado. Si hay algún problema legal, se atenderá cualquier solicitud de revisión o retirada.