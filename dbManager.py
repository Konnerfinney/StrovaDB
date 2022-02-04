from logging import exception
import mongoengine as db
from datetime import datetime,date
from Appointment import Appointment
from UserErrors import UserDoesntExist, AppointmentDoesntExist, UserExists
from user import user
from ArchivedAppointment import ArchivedAppointment
from appointmentTimes import appointmentTimes
import pytz
import dayConversion
import os

# from dotenv import load_dotenv

# load_dotenv()

passw = os.environ.get('passw')
database_name = "StrovaDB"
DB_URI="mongodb+srv://test:{}@cluster0.o9obh.mongodb.net/{}?ssl=true&ssl_cert_reqs=CERT_NONE".format(passw,database_name)



class dbManager():
    connection_status = False
    def start_connection(self) -> None:
        """ Starts connection to the MongoDB cluster
        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        if not self.connection_status:
            db.connect(db=database_name,username='test',password=passw,host=DB_URI)
        self.connection_status = True

    def connection_active(self) -> bool:
        """ Returns connection status of class dbManager

        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        return self.connection_status
 
    def get_current_date(self) -> tuple:
        """ Creates datetime object for current date and returns it as a tuple

        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        my_date = date.today()
        # returns -> year,week_num,day_of_week
        return(my_date.isocalendar())

    def create_appointments(self) -> None:
        """ Creates Appointment documents in the MongoDB Cluster based on Google Sheet times entered

        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        times = self.get_gsheet_times()
        today = datetime.now()
        m = today.strftime("%m")
        curr_year,curr_week,curr_day = self.get_current_date()
        datetime.weekday

        for key in times.keys():
            day_name = key
            curr_day = dayConversion.dc[day_name]
            for t in times[key]:       
                curr_time = t.split()[0]
                curr_meridian = t.split()[1]
                curr_date = "{}-{}-{}-{}-{}-{}".format(curr_year,curr_week,m,curr_day,curr_time,curr_meridian)
                date_format = date_format_week = "%Y-%W-%m-%d-%I-%p"
                print(curr_date)
                t_date = datetime.strptime(curr_date,date_format).replace(tzinfo = None)
                try:
                    pt = Appointment.objects(meeting_time = t_date).get()
                    print("already exists")              
                except db.DoesNotExist:
                    pt = Appointment(meeting_time = t_date)
                    pt.save()

    def get_gsheet_times(self):
        """ Creates a instance of the appointmentTimes class and verifies cluster connection before calling appointmentTimes.get_times()

        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        at = appointmentTimes()
        if not at.connection_active():
            at.establishConnection()
        return(at.get_times())

    def appointment_exists(self,dt_object) -> bool:
        """ Verifies the existence of a specific Appointment in the MongoDB Cluster by datetime object

        Parameters
        ----------
        dt_object
            datetime object for retrieving Appointment documents from the MongoDB Cluster

        Raises
        ------
        UserErrors.AppointmentDoesntExist
            If the appointment does not exist in the cluster
        """

        try:
            apt = Appointment.objects(meeting_time = dt_object).get()
        except db.DoesNotExist:
            raise AppointmentDoesntExist
        return True

    def create_user(self,disc_id: int, league_ign: str, rank: str, role: str) -> None:
        """ Creates a user document in the MongoDB Cluser

        Parameters
        ----------
        disc_id
            Discord ID of the user

        league_ign
            League user name of the user
        
        rank
            League rank of the user in the format "Diamond2"

        role
            League main role of the user in the form "Jungle"

        Raises
        ------
        UserErrors.UserExists
            Thrown if the user already exists
        """

        if self.user_exists(disc_id) == False:
            u = user(
                discord_id = disc_id,
                league_name = league_ign,
                current_rank = rank,
                current_role = role,
                date_created = datetime.now()
            ).save()
        else:
            raise UserExists


    def book_appointment(self, time: datetime, disc_id: int):
        """ Assigns an Appointment Document to a user via a customer_id field and role on the Appointment Document
        and a Appointment ReferenceField on the User document

        Parameters
        ----------
        time
            datetime object related to that specific Appointment

        disc_id
            Discord ID of the user booking the appointment

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID is not in the MongoDB cluster
        
        UserErrors.AppointmentDoesntExist
            If the Appointment specified by the datetime object is not in the MongoDB cluster
        
        """

        try:
            usr = self.get_user(disc_id)
            app = self.get_appointment(time)
            app.customer_id = disc_id
            app.role = usr.current_role
            app.save()
            usr.current_meeting = app
            usr.save()
        except UserDoesntExist:
            raise UserDoesntExist()
        except AppointmentDoesntExist:
            raise AppointmentDoesntExist()
        

    def archive_appointment(self,time):
        """ Creates a ArchivedAppointment document in the cluster and assigns it attributes from the specified Appointment document

        Parameters
        ----------
        time
            datetime object related to that specific Appointment

        Raises
        ------     
        UserErrors.AppointmentDoesntExist
            If the Appointment specified by the datetime object is not in the MongoDB cluster
        """

        try:
            app = self.get_appointment(time)
            usr = self.get_user(app.customer_id)
            a_app = ArchivedAppointment(
                meeting_time = time,
                customer_id = app.customer_id,
                appointment_type = app.appointment_type,
                rank_at_time = usr.current_rank,
                role_at_time = app.current_role
            ).save()
            usr.current_meeting = None
            usr.save()
            app.delete()
        except AppointmentDoesntExist:
            raise AppointmentDoesntExist()

    def delete_appointment(self,time: datetime):
        """ Deletes a specified Appointment document in the MongoDB Cluster

        Parameters
        ----------
        time
            datetime object related to that specific Appointment

        Raises
        ------     
        UserErrors.AppointmentDoesntExist
            If the Appointment specified by the datetime object is not in the MongoDB cluster
        
        """

        try:
            app = self.get_appointment(time)
            usr = None
            if app.customer_id != None:
                usr = self.get_user(app.customer_id)
                print("this appointment is booked by {}".format(usr.league_name))
                usr.current_meeting = None
                usr.save()
            app.delete()
            if usr != None:
                return usr.league_name
        except AppointmentDoesntExist:
            raise AppointmentDoesntExist()

    def delete_user(self, disc_id: int):
        """ Deletes a user document in the cluster as specified by the discord ID

        Parameters
        ----------

        disc_id
            Discord ID of the user booking the appointment

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID is not in the MongoDB cluster       
        """

        try:
            usr = self.get_user(disc_id)
            usr.current_meeting.customer = None
            usr.current_meeting.save()
            usr.delete()
        except UserDoesntExist:
            raise UserDoesntExist

    def unbook_appointment(self, disc_id: int):
        """ Removes the customer_ID and Role attributes of a Appointment Document that was set as the specified user's meeting
        user is found through the discord id

        Parameters
        ----------
        disc_id
            Discord ID of the user booking the appointment

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID is not in the MongoDB cluster
        
        UserErrors.AppointmentDoesntExist
            If the user.current_meeting attribute is None
        
        """

        try:
            usr = self.get_user(disc_id)
            if usr.current_meeting != None:
                app = usr.current_meeting
                app.customer_id = None
                app.role = None
                app.save()
                usr.current_meeting = None
                usr.save()
            else:
                raise AppointmentDoesntExist
        except UserDoesntExist:
            raise UserDoesntExist()

    def user_exists(self, disc_id: int) -> bool:
        """ Removes the customer_ID and Role attributes of a Appointment Document that was set as the specified user's meeting
        user is found through the discord id

        Parameters
        ----------
        disc_id
            Discord ID of the user booking the appointment

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID is not in the MongoDB cluster
        
        UserErrors.AppointmentDoesntExist
            If the user.current_meeting attribute is None
        """

        try:
            usr = user.objects(discord_id=disc_id).get()
            return True
        except db.DoesNotExist:
            raise UserDoesntExist()
        
    def update_user(self,disc_id: int, league_ign: str, rank: str, role: str) -> None:
        """ Creates a user document in the MongoDB Cluser

        Parameters
        ----------
        disc_id
            Discord ID of the user

        league_ign
            League user name of the user
        
        rank
            League rank of the user in the format "Diamond2"

        role
            League main role of the user in the form "Jungle"

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID isnt in the cluster
        """

        try:
            usr = self.get_user(disc_id)
            usr.league_name = league_ign
            usr.current_rank = rank
            usr.current_role = role
        except UserDoesntExist:
            raise UserDoesntExist


    def get_user(self, disc_id: int) -> user:
        """ Retrieves the user document from the MongoDB cluster

        Parameters
        ----------
        disc_id
            Discord ID of the user 

        Raises
        ------
        UserErrors.UserDoesntExist
            If the user specified by the discord ID is not in the MongoDB cluster
        """

        try:
            print("User Exists")
            self.user_exists(disc_id)
            return user.objects(discord_id=disc_id).get()
        except UserDoesntExist:
            raise UserDoesntExist()

    def get_appointment(self, mt: datetime):
        """ Retrieves the Appointment document from the MongoDB cluster

        Parameters
        ----------
        mt
            datetime object for appointment retrieval

        Raises
        ------
        UserErrors.AppointmentDoesntExist
            If the Appointment document is not in the cluster
        """

        try:
            self.appointment_exists(mt)
            return Appointment.objects(meeting_time = mt).get()
        except AppointmentDoesntExist:
            raise AppointmentDoesntExist
            


    def get_avail_appointments(self):
        """ Retrieves all Appointment documents without a customer_id 

        Parameters
        ----------
        None
        
        Raises
        ------
        None
        """

        ret_list = list()
        date_format_month = "%A-%I-%p"
        gen = Appointment.objects(customer_id = None)
        for app in gen:
            print(app.meeting_time)
            ret_list.append((app.meeting_time.strftime(date_format_month),app.meeting_time))
        return ret_list
    
    def delete_user(self, disc_id:int) -> None:
        """ Deletes a specified User Document in the cluster

        Parameters
        ----------
        disc_id
            The discord ID of the user to be deleted

        Raises
        ------
        UserErrors.UserDoesntExist
            If the User Document is not in the cluster
        """

        try:
            usr = self.get_user(disc_id)
            usr.delete()
        except UserDoesntExist:
            raise UserDoesntExist


    def get_all_appointments(self):
        """ Gets all appointments regardless of their availability

        Parameters
        ----------
        None

        Raises
        ------
        None
        """

        ret_list = list()
        gen = Appointment.objects()
        date_format_month = "%A-%I-%p"
        for app in gen:
            print(app.meeting_time)
            ret_list.append((app.meeting_time.strftime(date_format_month),app.meeting_time))
        return ret_list
    
    def unbook_appointment_admin(self, app_time: datetime) -> None:
        """ Removes customer_id attributes of a appointment document and the subsequent user document if there is one

        Parameters
        ----------
        app_time
            datetime object to specify the appointment

        Raises
        ------
        UserErrors.AppointmentDoesntExist
            If the Appointment specified does not exist in the cluster
        """

        try:
            app = self.get_appointment(app_time)
            if app.customer_id != None:
                usr = self.get_user(app.customer_id)
                usr.current_meeting = None
                usr.save()
            app.customer_id = None
            app.role = None
            app.save()
        except AppointmentDoesntExist:
            raise AppointmentDoesntExist
