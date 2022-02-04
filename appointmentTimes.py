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

    def get_times(self) -> dict:
        # iterate over the columns 1-7 representing monday-sunday
        for i in range(1,8):
            # make sure that the day key is in the curr_times dict
            curr_day_times = self.curr_sheet.sheet1.col_values(i)
            if curr_day_times[0] not in self.curr_times:
                self.curr_times[curr_day_times[0]] = []
            # iterate through the possible AM appointment times and add if schedule permits
            for x in range(1,7):
                if curr_day_times[x] != '':
                    self.curr_times[curr_day_times[0]].append('{} AM'.format(curr_day_times[x]))
            # iterate through the PM appointment times and add if schedule permits
            for x in range(8,len(curr_day_times)):
                if curr_day_times[x] != '':
                    self.curr_times[curr_day_times[0]].append('{} PM'.format(curr_day_times[x]))
        return self.curr_times


