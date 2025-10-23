import requests
from bs4 import BeautifulSoup
import re
import time 
from LoginSecopSinGUI import generar_cookies_secop

#*********************URLS************************#

BASE_URL = 'https://www.secop.gov.co/CO1BusinessLine/Tendering/OpportunityDossierWorkspace/Index'
SORTING_URL = 'https://www.secop.gov.co/CO1BusinessLine/Tendering/OpportunityDossierWorkspace/SelectSortingState'
SORTING_CODE = '3' # Código De Filtrado de Publicados Mas Recientes

#********************* Variables Usadas**********************#
all_data = []
TOTAL_RESULTS = 0
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://community.secop.gov.co/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U2VjdXJpdHlDb250ZXh0VG9rZW4gcDE6SWQ9Il9lOTRkZDBjNS1jZmM4LTRhMmQtYmUxMC1iNGE4ZDRhZTUyZGItNzBGRTIzREZFNzREQjdERDNFNjlENDI3MDk4NzM5OUEiIHhtbG5zOnAxPSJodHRwOi8vZG9jcy5vYXNpcy1vcGVuLm9yZy93c3MvMjAwNC8wMS9vYXNpcy0yMDA0MDEtd3NzLXdzc2VjdXJpdHktdXRpbGl0eS0xLjAueHNkIiB4bWxucz0iaHR0cDovL2RvY3Mub2FzaXMtb3Blbi5vcmcvd3Mtc3gvd3Mtc2VjdXJlY29udmVyc2F0aW9uLzIwMDUxMiI+PElkZW50aWZpZXI+dXJuOnV1aWQ6OWVkM2I2NTAtZWYzNC00MjEzLTk4MTYtMTA2YWNiNzExNTFkPC9JZGVudGlmaWVyPjxJbnN0YW5jZT51cm46dXVpZDo1NmE2NmQ1MC1kZGUxLTQ3MjYtYjMzMi03NWVjNmM3NDJjZmM8L0luc3RhbmNlPjxDb29raWUgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwNi8wNS9zZWN1cml0eSI+QUFFQUFJcVN1S1Ztc2RtWFduM0ozMDNvd2tmaTBSc3ZGeFBFMFlwRzVqWmxpb1lRSU1DUGtnQkl1SWtOTnVpc1pGa0xCaEJ1WXNIL3dKakRJSXJER290Y2VDbFZPeEZsVlpERDg1STdrZ3hTMmR1S3hjZzFFTFlsRkNwUWtiVXJFYS96U0h5cWZhallUYTJpcnZGVGtOdy9XQ3A0ekE3eVg2OFlBOEVlR1poc3dOL2pvZGo1Tm1BdVFEakZNclVxSVphdFdXb29RNjROS1lpQVRkZ2MyYTNCU09Dd3oxMlV1cnI0b1JiaDd0blNYUWJrdXh4ditqeHdIWHo4Qk9qYmUzeStJak42Y2R0eGJUS1NSYUVQbGVCMlBqYzRXL3lLclRHUWFtU1ViSWI4TW1Gbi9oa1krUlZVMkxTNzM3eDFTbWYxNGJHUTFZOXg4MllYOERaTWlUWUhpMzhSeEZCTTd3NmNWcFFDYThwRHVWd1N1c1RKd0cySGpYT0NnbUFmYVNlUG9BQUJBQUJ0ZGdTZm01WTBBellJbTRUcXhWaUFKMHpqM2svamhZQ0VJVkJsQTRvVTZid3IzVklaK1Y2V0N1WWJyR1J6eWlpb3FFU1l0VWFIT2djM24veStZVEJpUGJCTVdjK1pGUVUzbHd1eFNrc290ME5qc3ZHUGRySU9DVCtzdU1QcUJNMTQwa2pmVmZoN1lqSzJnY2J3SUovMjNJSDBCYlpBMkJTd2xZNktLM3cyeXRYUXpyZjhTLzJyaU00bWpqUnluMEkwZnMvWXdkVGZvNlFELzNBOHJzNGkrZzhaOCtXeUgyZWZ1ak9zZTkvenZybVU3NHVHMjl5QVJpTVhxUTFqZmp0bnVUMjZYb3dxQVpuOFA2Ni9KakFFVGVqTEoxaHdRL1RWYitVZXFUNWYzSkVMcW1oYW9RWDdwSS9QeU1CUVdWSkdpMzUzNDNxN1R0bmNTL1Jlb0RjSTBBTUFBQ0R6TWZkYTlVeEVQSFVPdVcyRysyNmhzbmVkYUhxaTZVY0ZBRGhmUlAyaXNGMHVTU20zTVdRekU4WTllN2h1N05hYTBubFUxMFRiZXB3WXprZC9FRW5kOFBlMlIxdFlaUFUveXhldlFVMTgwdVB6MVVFUU9kS2pOK0VYQkVKOFN3SmNyVWt3U0NrK3dzK2hEQklpWWp4NVZndEZUMU4wOWkwUTBBOEtnRFhIaGlxaTBDWTBMVEZ0UU5EdTB0VGwzTXNJdkR1Wm1MNzRQRlQwREpPa1lPVTFLVDk5MUJKOXBjT3d3MmI0Mm5vOVBRUDRzS3FlWjJFU1Q2Unlu; FedAuth1=eG0wZzJJamJIaTdVMjdVV01RMDkyaXlZK0FxOE12T2hPZ3RLTzZEVlkrTVBrVjV6VmtkQmRlRmcvdzlFNWQraUlUZUhlSWh6OHZ3K01jZmlzQUx6YW1meEthZVc5UE9neVRCeWdpcEV2S1J0RUdUN2pZak5uaGloZXNlT1VLMmluMmNaLzlzNzdSdWlqbUNYRkVieW1zdHZ6UTBSQVRNREYxakFzWmJZK1RuNWxhNzlrUk4yZ1l5b2o2b0xpZHgwcE10T3ROZTIzdUFuUlUvd2sxZGp0K2JtTDI0WmpWcytVd0VHQmdJcDJEbEJGTy8xR3FneVZ1c0JmYmFRQ3RiT0NIZ01zTlR2bmZzMGUzQTk3dEYwOG9kdEx1V2Z6a2ExMUI4M0kvVEtyTjkrUVlZMHpVUFEwcWRSTjhBN3kzWVJOVC8wZ3JNNkEzYkcxOWp0MXlTU0ZhYTQxN3h1bktKVWdIYkJJMUJLbDdFYytiNVV5cWlDM0FzTmVuV09wRTliNHBSdHBMWkh0dTF2QStIVThjZkc3c05DYjlzMVFHQU53V05aNXFVeEdYNWRJMkVJeVlCdDA4eGtsOXRJWGt6dGtCTEErQzdyOEdFZWlKQk9xMUpaMittKzJrYkJUOTdFVjlVM2dyem1sUmNJZ0JyTC9HQURHRmRDaHVUT2hhZy9uOFJmemZhS0tUSlNLVkI2MU9BNjA5R3ZHSzlwREVzbG8zUG9JdmhqTUFoT1krcE9GWDgyT2ZHTUtTYWpabGZ6c2UrallqUC84VGpYN3V5S1N2OGU5OE5GS2tpblg2L3RSbWZNS1ZncTZ3YjNCTTI0ekNBMHUwK2JFeHNVeGxpeXRNWHlNTWd6eFlOcmUwbmM3UjRObVRnWHhyNTZEczFkQlc3bTNyS1Zqc2orUjQ1UHFRdmNNdnVMdC8vS1c4WjR5aDZ3S2xaSUJHN2JuSlh0VFVSK1c0OWlDQmZOeVJQSjdJd2tvSkFaZTc4RUkyUmpJcWh3SmVxZU9vblBnQ3NjUDVqQklvTVlFNTBYU1JhRUYraTZKZE1RL2xIak0yL1JrV2hWWmxWbFl2eURVMXExWG5IbmdpM1g0MlhienJWbm9jbEQ2SktEb0JjczVFcHRnWk9YTE9nVXNZYTVPK3gybUU1bjk1YWEybmY1NTEySjZFQVI2RnorMkpscTBaM3FidEk2OGtZMGVmS1QxcWRGSUVueXk3TFBFQmVrWTEzSjJVNEJabGNuOWhkUEhnWWpuN1JtN0dWM1FoNFArUTJHdSswWStyYzVxUkJjOHFIVi9ya3hQcjNMMzExL0w2QXhPM1ZxeExXMUhBekpGSG1FT05qcWpNVDRIZ3FLWEs0bmdNczJUYVlyaWpaV3FSUHJKcDl5WlJ5cEY0PTwvQ29va2llPjwvU2VjdXJpdHlDb250ZXh0VG9rZW4+; ROUTEID_MKT=.fe_mkt_07; MarketplaceSessionCookie=hjsa2xqjani4kpjvgxg5qmvu; UserCode=38399242; CompanyCode=729265413; BusinessLineSessionCookie=4n4e40upq3pv5afmt2x4ub3d',
}

def extract_row_data(html_content):

    """Extrae la descripción, etiquetas, fechas, estado, operación y referencia de cada fila."""
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all("tr", class_="FltTr")

    data = []
    for row in rows:
        # 1. Descripción (ws_rc_description)
        description = " ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_description")
        ])

        # 2. Etiquetas (ws_rc_dataLabel)
        label = " | ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_dataLabel")
        ])

        # 3. Fechas (ws_rc_date)
        date_value = " | ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_date")
        ])

        # 4. Estado (ws_rc_state)
        state = " | ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_state")
        ])

        # 5. Operación comercial (ws_rc_businessOperationLabel)
        business_operation = " | ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_businessOperationLabel")
        ])

        # 6. Referencia (ws_rc_reference)
        reference = " | ".join([
            s.get_text(strip=True) for s in row.find_all("span", class_="ws_rc_reference")
        ])

        # Agregamos un diccionario con toda la info
        data.append({
            "description": description,
            "label": label,
            "date": date_value,
            "state": state,
            "business_operation": business_operation,
            "reference": reference,
        })

    return data

def extract_mkey(html_content):
    """Busca y extrae la clave dinámica 'mkey' del código fuente de la página."""
    soup = BeautifulSoup(html_content, "html.parser")

    # El mkey es a menudo un parámetro de la URL dentro de los enlaces de la tabla.
    # Buscaremos un enlace de paginación/ordenamiento o el contenedor de la tabla.

    # 1. Buscar en el contenedor principal del 'FlatTree'
    container = soup.find("div", id="fltOpportunityDossierListFT")
    if container and 'mkey' in container.get('data-init-args', ''):
        # Si el mkey está en los atributos de inicialización (común en Vortal/SharePoint)
        # Esto requiere inspección manual, pero es un buen intento:
        # Ejemplo: data-init-args="{..., "mkey":"7c99d354_7e2e_44a2_8a51_16e1d94cb290",...}"
        match = re.search(r'"mkey":"([a-f0-9_]+)"', container['data-init-args'])
        if match:
            return match.group(1)

    # 2. Buscar en cualquier enlace o botón que inicie una acción
    mkey_tag = soup.find(lambda tag: tag.has_attr('href') and 'mkey=' in tag['href'])
    if mkey_tag:
        match = re.search(r'mkey=([a-f0-9_]+)', mkey_tag['href'])
        if match:
            return match.group(1)

    # 3. Buscar en el código JavaScript (como última opción)
    js_match = re.search(r'mkey["\']:\s*["\']([a-f0-9_]+)["\']', html_content)
    if js_match:
        return js_match.group(1)

    return None


def init_comercial_page():
    cookies = generar_cookies_secop()
    resp_base = requests.get(BASE_URL, cookies=cookies, headers=headers)

    if resp_base.status_code != 200:
        print(f"❌ Error al cargar BASE_URL: {resp_base.status_code}. Abortando.")
        exit()

    DYNAMIC_MKEY = extract_mkey(resp_base.text)
    if not DYNAMIC_MKEY:
        print("⚠️ No se pudo extraer mkey dinámico. Usando valor estático.")
        DYNAMIC_MKEY = "2ce4978f_5979_4396_a57d_8bf0fae24251"
    else:
        print(f"✅ mkey dinámico extraído: {DYNAMIC_MKEY}")

    return DYNAMIC_MKEY, cookies




def procesar_datos_func():

    DYNAMIC_MKEY, cookies = init_comercial_page()
    """Procesa la extracción completa sin depender del contexto Flask."""
    print("📩 Iniciando proceso de extracción...")

    # 1️⃣ Establecer ordenamiento
    sorting_params = {
        "code": SORTING_CODE,
        "mkey": DYNAMIC_MKEY,
        "_": str(int(time.time() * 1000)),
    }

    sorting_response = requests.get(SORTING_URL, params=sorting_params, cookies=cookies, headers=headers)
    if sorting_response.status_code != 200:
        return {"error": f"Error en ordenamiento: {sorting_response.status_code}"}

    # 2️⃣ Cargar la página ordenada
    final_response = requests.get(BASE_URL, cookies=cookies, headers=headers)
    if final_response.status_code != 200:
        return {"error": f"Error al cargar datos: {final_response.status_code}"}

    # 3️⃣ Extraer datos
    rows_data = extract_row_data(final_response.text)
    if not rows_data:
        return {"warning": "No se encontraron filas."}

    print(f"✅ Se extrajeron {len(rows_data)} registros.")
    return {
        "status": "success",
        "records_count": len(rows_data),
        "records": rows_data
    }
