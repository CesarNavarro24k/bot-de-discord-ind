import discord
import asyncio, random 
from discord.ext import commands 
from google import genai
import webserver 
from dotenv import load_dotenv 
import os 

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents=intents)
@bot.command()
async def saludo(ctx):
    await ctx.send("Hola, bienvenido a mi servidor de discord!")

@bot.command()
async def suma(ctx, num1:int, num2:int):
    await ctx.send(f"La suma es: {num1 + num2}")

@bot.command()
async def ia(ctx, *, pregunta):
    await ctx.send("Estoy pensando...")
    client = genai.Client(api_key=GEMINI_API_KEY)

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=pregunta
    )

    respuesta = interaction.output_text

    for i in range(0, len(respuesta), 2000):
        await ctx.send(respuesta[i:i + 2000])

@bot.command()
async def ppt(ctx):
    opciones = ["piedra", "papel", "tijera"]
    gana = {"piedra":"tijera", "papel":"piedra","tijera":"papel"}

    victorias = 0
    derrotas = 0
    empates = 0

    await ctx.send("Piedra, papel o tijera, escribe tu jugada o escribe salir para dejar de jugar:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("Pasaron 2 minutos sin jugar, juego terminado")
            break 
        jugada = msg.content.lower()
        if jugada == "salir":
            break 
        if jugada not in opciones:
            await ctx.send("Opcion no valida, escribe una opcion valida")
            continue
        bot_jugada = random.choice(opciones)

        if jugada == bot_jugada:
            resultado = "Empate"
            empates += 1
        elif gana[jugada] == bot_jugada:
            resultado = "Ganaste"
            victorias += 1
        else:
            resultado = "Perdiste"
            derrotas += 1
        await ctx.send(f"Tu has elegido: {jugada}")
        await ctx.send(f"El bot a elegido: {bot_jugada}")
        await ctx.send(f"El resultado es: {resultado}")

        await ctx.send("Los marcadores son:")
        await ctx.send(f"Ganadas: {victorias}")
        await ctx.send(f"Perdidas: {derrotas}")
        await ctx.send(f"Empates: {empates}")

webserver.keep_alive()
bot.run(DISCORD_TOKEN)