from discord import app_commands
import discord

LANGUAGE_CSV = "language.csv"
table: dict[str, dict[str, str]] = {}
locales = []

class Translator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContextTypes):
        return tr(string.message, locale)

def load():
    global table, locales
    with open(LANGUAGE_CSV, encoding="utf-8-sig") as f:
        locales = f.readline().split('\t')
        locales[-1] = locales[-1].strip()
        line = f.readline()
        while line:
            strings = line.split('\t')
            row = {}
            for i in range(1,len(strings)):
                row[locales[i]] = strings[i].strip().replace('\\n', '\n')
            table[strings[0]] = row
            line = f.readline()

def tr(key: str, locale: discord.Locale) -> str:
    global table, locales
    language_code = locale.language_code.split('-')[0]
    if key not in table:
        return key
    
    entry = table.get(key)
    if locale not in locales:
        return entry.get("en", key)
    return entry.get(language_code)

load()