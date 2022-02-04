import mongoengine as db
import datetime
from Appointment import Appointment
from ArchivedAppointment import ArchivedAppointment

class user(db.DynamicDocument):
    discord_id = db.IntField(unique=True)
    league_name = db.StringField()
    current_rank = db.StringField()
    current_role = db.StringField()
    date_created = db.DateTimeField()
    current_meeting = db.ReferenceField(Appointment)

    meta = {
        "indexes" : ["discord_id"],
        "ordering" : ["-date_created"]
    }
