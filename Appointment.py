import mongoengine as db
import datetime


class Appointment(db.DynamicDocument):
    meeting_time = db.DateTimeField()
    customer_id = db.IntField()
    appointment_type = db.StringField()
    current_role = db.StringField()