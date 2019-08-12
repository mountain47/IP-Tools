import requests, json, discord, re
from hidden import token, theapi_key

def send_request(ip_address, api_key):
    response = requests.get('https://api.ipdata.co/%s?api-key=%s' % (ip_address, api_key))
    response_json = json.loads(response.text)
    return f'''
```
IP: {str(response_json['ip'])}

IP LOCATION INFO

City: {str(response_json['city'])}
Region: {str(response_json['region'])}
Region code: {str(response_json['region_code'])}
Country: {str(response_json['country_name'])}
Country code: {str(response_json['country_code'])}
Flag: {str(response_json['emoji_flag'])}
Continent: {str(response_json['continent_name'])}
Continent code: {str(response_json['continent_code'])}
Postal code: {str(response_json['postal'])}
Latitude: {str(response_json['latitude'])}
Longitude: {str(response_json['longitude'])}
Calling code: {str(response_json['calling_code'])}
Time zone: {str(response_json['time_zone']['name'])}
Time zone current time: {str(response_json['time_zone']['current_time'])}
Currency: {str(response_json['currency']['name'])}
Currency code: {str(response_json['currency']['code'])}
Currency symbol: {str(response_json['currency']['symbol'])}
Language: {str(response_json['languages'][0]['name'])}
Native language: {str(response_json['languages'][0]['native'])}


BASIC INFO

Organisation: {str(response_json['organisation'])}
asn: {str(response_json['asn'])}


EXTRA INFO 

TOR: {str(response_json['threat']['is_tor'])}
Proxy: {str(response_json['threat']['is_proxy'])}
Anonymous: {str(response_json['threat']['is_anonymous'])}
Abuser: {str(response_json['threat']['is_known_abuser'])}
Threat: {str(response_json['threat']['is_threat'])}
Bogon: {str(response_json['threat']['is_bogon'])}```'''

client = discord.Client()

#bot start
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with IPS'))
    print('Bot is ready!')
    print(f'serving {len(client.guilds)} guilds')
    
async def info(ctx):
    embed = discord.Embed(title='IP Tools', description='This discord bot lets you geolocate ip addresses.', color=0xeee657)

    # give info about you here
    embed.add_field(name='Made by', value='lixer.net')

    # Shows the number of servers the bot is member of.
    embed.add_field(name='Server count', value=f'{len(client.guilds)}')

    # give users a link to invite thsi bot to their server
    embed.add_field(name='Invite', value='https://discordapp.com/api/oauth2/authorize?client_id=592734034912870400&permissions=2146958847&redirect_uri=https%3A%2F%2Fdiscord.gg%2FcpRpK3X&scope=bot')

    await ctx.send(embed=embed)

@client.event
async def on_message(m):
    message=m.content
    if message.lower().startswith('.geo '):
        message_split = message.split(' ')
        if message_split[1]:
            ip_address = re.match(r"^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$", message_split[1])
            if ip_address:
                ip_address = ip_address.group(0)
                response = send_request(ip_address, 'theapi_key')
                await m.channel.send(response) 
            else:
                await m.channel.send('Invalid IP-address')
                
    elif message.lower() == '.ping':
        await m.channel.send(f'Pong! {round(client.latency * 1000)}ms')

    elif message.lower() == '.info':
        embed = discord.Embed(title='IP Tools', description='This discord bot lets you geolocate ip addresses.', color=0xeee657)
        embed.add_field(name='Made by', value='lixer.net')
        embed.add_field(name='Server count', value=f'{len(client.guilds)}')
        embed.add_field(name='Invite', value='https://discordapp.com/api/oauth2/authorize?client_id=592734034912870400&permissions=2146958847&redirect_uri=https%3A%2F%2Fdiscord.gg%2FcpRpK3X&scope=bot')
        embed.add_field(name='Our support server', value='https://discord.gg/cpRpK3X')
        embed.add_field(name='Shoutout', value='Shoutout to Artemis#8032 who helped me build this.\nCalendar bot: https://discord.gg/hxKbHEN')
        await m.channel.send(embed=embed)        


    elif message.startswith('.'):
        await m.channel.send(':x: INVALID COMMAND :x:')
        
client.run(token)
