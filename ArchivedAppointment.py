import mongoengine as db
import datetime


class ArchivedAppointment(db.DynamicDocument):
    meeting_time = db.DateTimeField()
    customer_id = db.IntField()
    appointment_type = db.StringField()
    rank_at_time = db.StringField()
    role_at_time = db.StringField()
    feedback = db.StringField()