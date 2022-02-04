import discord
from discord.ext import commands
from UserErrors import AppointmentDoesntExist, UserDoesntExist, UserExists
from dbManager import dbManager

dbm = dbManager()


class Scheduling(commands.Cog, name='scheduling'):
	'''These are the developer commands'''
	global appoint_dict
	appoint_dict = dict()
	def __init__(self, bot):
		self.bot = bot
		dbm.start_connection()
		if dbm.connection_active():
			print("active connection")
		print("COGS SCHEDULING RELOADED")
		

	async def cog_check(self, ctx):  
		'''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
		return True

	@commands.command()
	async def createUser(self,ctx,league_name, role, rank):
		""" Creates a user document in the cluster

        Parameters
        ----------
        league_name
			league name of the user

		role
			league role of the user

		rank
			league rank of the user

        Raises
        ------     
		None
        """

		# Create user
		try:
			dbm.create_user(ctx.author.id,league_name,rank,role)
			await ctx.channel.send("User Created")
		except UserExists:
			await ctx.channel.send("This user already exists")


	@commands.command()
	async def availAppointments(self,ctx):
		""" Gets a list of available appointments

        Parameters
        ----------
		None

        Raises
        ------     
		None
        """

		appointments_list = dbm.get_avail_appointments()
		global appoint_dict
		appoint_dict = dict()
		print_str = "```"
		if appointments_list:
			for ind, (app_time, time_date) in enumerate(appointments_list):
				appoint_dict[str(ind+1)] = (app_time, time_date)
				print_str += "{}: {}\n".format(ind+1,app_time)
			await ctx.channel.send(print_str + "```")
		else:
			await ctx.channel.send("```Sorry but no appointments are available right now. Check in later! ```")
		
		

	@commands.command()
	async def bookAppointment(self,ctx,num):
		""" Books an appointment based off the user number

        Parameters
        ----------
		Num
			Num to specify appointment

        Raises
        ------     
		None
        """

		app_list = dbm.get_avail_appointments()
		num = int(num)
		if num > len(app_list):
			await ctx.channel.send("Sorry that is not a valid appointment number")
		else:
			try:
				dbm.book_appointment(app_list[num-1][1], ctx.author.id)
				await ctx.channel.send("Booked appointment {} at {}".format(num, app_list[num-1][0]))
			except UserDoesntExist:
				await ctx.channel.send("You must create a user before booking an appointment")
			except AppointmentDoesntExist:
				await ctx.channel.send("Sorry, we have encountered an error and cannot book that appointment at this time")
				

		
		

	@commands.command()
	async def unbookAppointment(self,ctx):
		""" Unbooks an appointment based on author discord id

        Parameters
        ----------
		None

        Raises
        ------     
		None
        """

		try:
			dbm.unbook_appointment(ctx.author.id)
			await ctx.channel.send("Your appointment has been canceled")
		except UserDoesntExist:
			await ctx.channel.send("Sorry you havent created a user yet")
		except AppointmentDoesntExist:
			await ctx.channel.send("Sorry you don't have an appointment")

	@commands.command()
	async def updateAccount(self,ctx,name,role,rank):
		""" Unbooks an appointment based on author discord id

        Parameters
        ----------
		name
			league name of the user

		role
			league role of the user

		rank
			league rank of the user

        Raises
        ------     
		None
        """

		try:
			dbm.update_user(self, ctx.author.id,name,role,rank)
			await ctx.channel.send("Your account has been updated")
		except UserDoesntExist:
			await ctx.channel.send("Please create an account first")
		

	

def setup(bot):
	bot.add_cog(Scheduling(bot))