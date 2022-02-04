import gspread
import gspread_dict

class appointmentTimes():
    connection_status = False
    gc = None
    curr_sheet = None
    curr_times = dict()
    def establishConnection(self) -> None:
        self.gc = gspread.service_account_from_dict(gspread_dict.c)
        self.curr_sheet = self.gc.open('Strova_Schedule')
        self.connection_status = True
    
    def connection_active(self) -> bool:
        return self.connection_status




