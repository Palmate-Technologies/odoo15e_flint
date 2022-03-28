from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT,DEFAULT_SERVER_DATE_FORMAT

import pytz
# import numpy as np

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    flexible_daily_break = fields.Float(string='Break', help='This break will be counted only when the attendance mode is flexible and cycle is daily.')
    # no_of_days_in_month = fields.Float(string="No of days in Month", default=30)
    no_of_days_in_month = fields.Selection([
        ('standard_30', 'Standard 30'),
        ('calendar_30', 'Calendar 30'),
        ('no_of_working_days', 'No of Working Days'),
        ], string='No of Days in Month', default='standard_30')

    def _get_weekmask(self):
        weekmask_dict = {'0': False, '1': False, '2':False, '3':False, '4':False, '5':False, '6':False}
        for cal_attendance in self.attendance_ids:
            weekmask_dict[cal_attendance.dayofweek] = True
        
        weekmask = []
        for key in sorted(weekmask_dict.iterkeys()):
            weekmask.append(weekmask_dict[key])
        return weekmask
    
    def _get_busdaycalednar(self):
        # print "inside _get_busdaycalednar"
        weekmask = self._get_weekmask()
        return np.busdaycalendar(weekmask=weekmask)
    
    # @api.multi
    def count_weekends(self, date_from, date_to):
        date_from = datetime.strptime(date_from, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
        date_to = datetime.strptime(date_to, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
        date_range = np.arange(np.datetime64(date_from), np.datetime64(date_to) + np.timedelta64(1,'D'))
        busdaycal = self._get_busdaycalednar()
        busday_bool = np.is_busday(date_range, busdaycal=busdaycal)
        return busday_bool.size - np.count_nonzero(busday_bool)

        
    def get_non_working_hours(self, check_in_time, check_out_time, non_working_hours):
        res = 0.0
        for each_non_working_hours in non_working_hours:
            # print "each_non_working_hours: ",each_non_working_hours
            #### Working inside non working hours
            if check_in_time >= each_non_working_hours[0] and check_out_time <= each_non_working_hours[1]:
                res += check_out_time - check_in_time
                # print "res0: ",check_out_time - check_in_time, res
            
            ### Full working during non working hours
            if check_in_time < each_non_working_hours[0] and check_out_time > each_non_working_hours[1]:
                res += each_non_working_hours[1] - each_non_working_hours[0]
                # print "res1: ",each_non_working_hours[1] - each_non_working_hours[0], res
                
            ### Check out time falls in non working hours
            if check_in_time < each_non_working_hours[0] and check_out_time > each_non_working_hours[0] and check_out_time <= each_non_working_hours[1]:
                res += check_out_time - each_non_working_hours[0]
                # print "res2: ",check_out_time - each_non_working_hours[0], res
                
            ### Check in time falls in non working hours
            if check_in_time > each_non_working_hours[0] and check_in_time < each_non_working_hours[1] and check_out_time > each_non_working_hours[1]:
                res += each_non_working_hours[1] - check_in_time
                # print "res3: ",each_non_working_hours[1] - check_in_time, res
            
        return res
    
    # @api.multi
    def get_working_intervals_of_day_timezone(self, timezone, start_dt=None, end_dt=None,
                                     leaves=None, compute_leaves=False, resource_id=None,
                                     default_interval=None):
        intervals = self.get_working_intervals_of_day(start_dt, end_dt, leaves, compute_leaves, resource_id, default_interval)
        if not intervals:
            return intervals
        
        timezone_intervals = []
        for interval in intervals:
#            interval_str = interval[0].strftime("%Y-%m-%d %H:%M:%S")
#            interval_new = datetime.strptime(interval_str, DEFAULT_SERVER_DATETIME_FORMAT)
#            print "interval interval_new", interval, type(interval), interval_new, type(interval_new)
#            print "interval.now(): ",interval[0].now()
            dt1 = pytz.utc.localize(interval[0])
            dt1 = dt1.astimezone(timezone)
            
            dt2 = pytz.utc.localize(interval[1])
            dt2 = dt2.astimezone(timezone)
            
            timezone_intervals.append((dt1,dt2))

        return timezone_intervals
    
class ResourceCalendarAttendance(models.Model):
    _inherit = "resource.calendar.attendance"
    
    # @api.multi
    def get_not_working_hours_interval(self):
        # print "get_not_working_hours self: ",self
        res = []
        if len(self) == 1:
            res.append((0,self.hour_from))
            res.append((self.hour_to,24.0))
            return res
        
        count = 0
        res.append((0,self[0].hour_from))
        for line in self:
            if len(self) == count + 1:
                res.append((line.hour_to, 24.0))
            else:
                res.append((line.hour_to, self[count+1].hour_from))
            count = count + 1
        
        return res
                