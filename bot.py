import discord
from discord.ext import commands
from config import token  # Botun tokenini config dosyasından içe aktarma

intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanızı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    
    if "https://" in message.content:
        try:
            
            await message.guild.ban(message.author, reason="Link / Reklam paylaşımı yasak!")
            await message.channel.send(f"{message.author.mention} link paylaştığı için banlandı!")
        except Exception as e:
            print(f"Banlama işlemi başarısız oldu: {e}")

    
    await client.process_commands(message)

@bot.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        await channel.send(f'Hoş geldiniz: {member.mention}!')


bot.run(token)