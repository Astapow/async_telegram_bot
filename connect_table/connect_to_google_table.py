import gspread
from google.oauth2.credentials import Credentials
import asyncio
import os

TOKEN_PATH = "D:/python_bot_tested/python_bot_tested/connect_table/token.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1j8KGRO5Hv8z29IEOMhrg6RIG-ZUEoGZUwQe0RLVbhaE/edit#gid=0"


async def add_message_to_sheet_async(message_text):
    def add_message():
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(
                TOKEN_PATH, scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_url(SHEET_URL).sheet1

            last_row = len(sheet.get_all_values())
            last_id = sheet.cell(last_row, 1).value
            new_id = int(last_id) + 1 if last_id else 1

            sheet.append_row([new_id, message_text])
            return new_id
        else:
            raise FileNotFoundError(f"Token file {TOKEN_PATH} not found.")

    try:
        new_id = await asyncio.to_thread(add_message)
        return new_id
    except Exception as e:
        print(f"Ошибка при добавлении данных в Google Sheets: {e}")
        return None


async def get_info_from_sheet_async():
    def get_info():
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(
                TOKEN_PATH, scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_url(SHEET_URL).sheet1

            # Получение всех значений из листа
            all_values = sheet.get_all_values()
            return all_values
        else:
            raise FileNotFoundError(f"Token file {TOKEN_PATH} not found.")

    try:
        # Запуск синхронной функции в асинхронном контексте
        all_values = await asyncio.to_thread(get_info)
        return all_values
    except Exception as e:
        print(f"Ошибка при получении данных из Google Sheets: {e}")
        return None
