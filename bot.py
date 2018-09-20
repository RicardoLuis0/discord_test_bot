import discord;
import csv;
from discord.ext import commands;
from discord.ext.commands import Bot;
from discord.utils import get;

ADMIN_ROLE_NAME="Admins";

TOKEN = "";

with open('discord_token') as f:
	TOKEN=f.read();

bot = Bot(command_prefix=">");

def load_roles(server_name:str):
	try:
		with open(server_name+'_allowed_roles.csv','r') as f:
			reader=csv.reader(f, delimiter=',');
			arr=[];
			for row in reader:
				for column in row:
					arr.append(column);
			return arr;
	except FileNotFoundError:
		return [];
	except:
		print("load_roles FAIL");

def save_roles(server_name:str,new_roles):
	try:
		with open(server_name+'_allowed_roles.csv','w') as f:
			msg="";
			first=True;
			for role in new_roles:
				if first:
					first=False;
				else:
					msg+=",";
				msg+='"'+role+'"';
			f.write(msg);
	except:
		print("save_roles FAIL");

@bot.command(pass_context=True)
@commands.has_role(ADMIN_ROLE_NAME)
async def role_admin(context,command:str="",role:str=""):
	server=context.message.server;
	roles=load_roles(server.name);
	if(command == "add"):
		if(role==""):
			await bot.say("```Usage: add [role]```");
		else:
			if not role in roles:
				roles.append(role);
				save_roles(server.name,roles);
				await bot.say("```Role '"+role+"' inserted```");
			else:
				await bot.say("```Role '"+role+"' already exists in list```");
	elif (command == "remove"):
		if(role==""):
			await bot.say("```Usage: remove [role]```");
		else:
			if role in roles:
				roles.remove(role);
				save_roles(server.name,roles);
				await bot.say("```Role '"+role+"' removed```");
			else:
				await bot.say("```Role '"+role+"' not in list```");
	else:
		await bot.say("```Usage: [remove,add] [role]```");
	return;

@bot.command(pass_context=True)
async def role(context,command:str="",role:str=""):
	user=context.message.author;
	server=context.message.server;
	roles=load_roles(server.name);
	if (command == "get"):
		if role in roles:
			r = get(server.roles, name=role);
			if(r==None):
				await bot.say("```Role '"+role+"' in list, but not in server. @Admins```");
			else:
				await bot.add_roles(user,r);
				await bot.say("```"+(user.nick if user.nick!=None else user.name)+" Got Role '"+role+"'!```");
		else:
			await bot.say("```Role '"+role+"' not in list```");
	elif (command == "unget"):
		if role in roles:
			r = get(server.roles, name=role);
			if(r==None):
				await bot.say("```Role '"+role+"' in list, but not in server. @Admins```");
			else:
				await bot.remove_roles(user,r);
				await bot.say("```"+(user.nick if user.nick!=None else user.name)+" Ungot Role '"+role+"'!```");
		else:
			await bot.say("```Role '"+role+"' not in list```");
	elif (command == "list"):
		msg="";
		for r in roles:
			msg+="  "+r+"\n";
		await bot.say("```Roles:\n"+msg+"```");
	else:
		await bot.say("```Usage: [list,get,unget] [role]```");
	return;

@bot.event
async def on_ready():
    print('Logged in as');
    print(bot.user.name);
    print(bot.user.id);
    print('------');

bot.run(TOKEN);
