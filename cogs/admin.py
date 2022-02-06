import discord
from discord.ext import commands
from dbManager import dbManager
from UserErrors import *
dbm = dbManager()


class admin(commands.Cog, name='admin'):
	global appoint_dict
	appoint_dict = dict()

	def __init__(self, bot):
		self.bot = bot
		dbm.start_connection()
		if dbm.connection_active():
			print("active connection")
		print("COGS ADMIN RELOADED")


	async def cog_check(self, ctx):
		admin_ids = [self.bot.author_id]
		if ctx.author.id not in admin_ids:
			await ctx.channel.send("Sorry you do not have permissions for that command")
		return ctx.author.id in admin_ids

	@commands.command()
	async def test(self,ctx):
		await ctx.channel.send("user is an admin")


	@commands.command()
	async def bookAppointForUser(self,ctx,num, disc_id):
		""" Books an appointment for a specified user
        Parameters
        ----------
        mum
			Number correlating to the appointment as listed by allAppointments()
		
		disc_id
			discord ID of the user to book an appointment for 

        Raises
        ------
        None
        """

		app_list = dbm.get_avail_appointments()
		try:
			dbm.book_appointment(app_list[int(num)-1][1], disc_id)
			await ctx.channel.send("Booked user {} for appointment at {}".format(disc_id,app_list[int(num)-1][0]))
		except UserDoesntExist:
			await ctx.channel.send("That user doesnt exist")
		except AppointmentDoesntExist:
			await ctx.channel.send("That appointment doesnt exist")
		except IndexError:
			await ctx.channel.send("Not a valid appointment number")
		# need to add in feature to get date time object from 
		# avail appointment list to accurately book appointments

	@commands.command()
	async def deleteAppointment(self, ctx, num):
		""" Deletes an appointment specified by a user

        Parameters
        ----------
        num
            the number relating to the specified appointment

        Raises
        ------     
		None
        """

		num = int(num)
		app_list = dbm.get_all_appointments()
		print(app_list)
		try:
			usr = dbm.delete_appointment(app_list[num-1][1])
			print(app_list)
			print(usr)
			if usr:
				await ctx.channel.send("Deleted appointment {} at {} which was booked by {}".format(num, app_list[num-1][0],usr))
			else:
				await ctx.channel.send("Deleted appointment {} at {}".format(num, app_list[num-1][0]))
		except AppointmentDoesntExist:
			await ctx.channel.send("The appointment you attempted to delete doesn't exist")
		except IndexError:
			await ctx.channel.send("Not a valid appointment number")

	@commands.command()
	async def allAppointments(self,ctx):
		""" Gets a list of all appointment documents in the cluster

        Parameters
        ----------
        None

        Raises
        ------     
		None
        """

		app_list = dbm.get_all_appointments()
		print_str="```"
		if app_list:
			for ind, (app_time, time_date) in enumerate(app_list):
				appoint_dict[str(ind+1)] = (app_time, time_date)
				print_str += "{}: {}\n".format(ind+1,app_time)
			await ctx.channel.send(print_str + "```")
		else:
			await ctx.channel.send("```Sorry but no appointments are available right now. Check in later! ```")
		
	@commands.command()
	async def createAppointments(self,ctx):
		""" Calls the dbm.Create_appointments() to create appointments from the google_sheet

        Parameters
        ----------
        None

        Raises
        ------     
		None
        """

		dbm.create_appointments()
		await self.allAppointments(ctx)

	@commands.command()
	async def deleteUser(self, ctx, disc_id):
		""" Deletes a user specified by disc_id

        Parameters
        ----------
        disc_id
			Discord ID of the user to delete

        Raises
        ------     
		None
        """

		try:
			dbm.delete_user(disc_id)
			await ctx.channel.send("Deleted user {}".format(disc_id))
		except UserDoesntExist:
			await ctx.channel.send("That user doesn't exist")
		
	@commands.command()
	async def unbookAppointmentAdmin(self, ctx, num):
		""" Calls the unbook_appointment_admin function to unbook a specific appointment by number

        Parameters
        ----------
        num
			Number specifiyng the appointment to unbook

        Raises
        ------     
		None
        """

		app_list = dbm.get_all_appointments()
		try:
			dbm.unbook_appointment_admin(app_list[num-1][1])
			await ctx.channel.send("Unbooked appointment {} at {}".format(num,app_list[num-1][0]))
		except AppointmentDoesntExist:
			await ctx.channel.send("This appointment doesn't exist")

	@commands.command()
	async def archiveAppointment(self, ctx, num):
		""" Archives an appointment by number

        Parameters
        ----------
        num
			Number specifiyng the appointment to archive

        Raises
        ------     
		None
        """

		app_list = dbm.get_all_appointments()
		if num > len(app_list):
			try:
				dbm.archive_appointment(app_list[num-1][1])
				await ctx.channel.send("Archived appointment {} at {}".format(num,app_list[num-1][0]))
			except AppointmentDoesntExist:
				await ctx.channel.send("Sorry that appointment doesnt exist")
		else:
			await ctx.channel.send("Please enter a valid number of appointment")

		
	@commands.commad()
	async def adminCommands(self,ctx):
		admin_commands_str = "```bookAppointForUser:\nParameters: number - appointment to book. Discord ID of user to book it for\nDeleteAppointment:\nParameters: number of appointment to delete\nallAppointments:\nParameters - None\nCreateAppointments:\nParameters - None\nDeleteUser"
		ctx.channel.send(admin_commands_str)

	

def setup(bot):
	bot.add_cog(admin(bot))