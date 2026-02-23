# import uuid
# from django.db import models
# from ..models import Organization
# from .event_sub_category import EventSubCategory
# from .event_category import EventCategory  
# from ..enums import status,GeoSite,EventStatusEnum
# from django.utils.timesince import timesince
# from django.utils import timezone
# from .district import District
# from datetime import datetime
# from .user import Register
# from dateutil.relativedelta import relativedelta
# from pytz import timezone as pytz_timezone




# class Events(models.Model):
#     _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
#     name = models.CharField(db_column='name', max_length=45)
#     start_date= models.DateTimeField(db_column='start_date',max_length=20,null=True, blank=True)
#     end_date= models.DateTimeField(db_column='end_date',max_length=20,null=True, blank=True)
#     # start_time = models.TimeField(db_column='start_time',null=True,blank=True)
#     # end_time = models.TimeField(db_column = 'end_time',null=True,blank=True)
#     brochure = models.TextField(db_column='brochure',null=True, blank=True)
#     location = models.CharField(db_column='location',max_length=100)
#     organizer_name=models.CharField(db_column='organizer_name',max_length=100,null=True, blank=True)
#     contact_details=models.CharField(db_column='contact_details',max_length=100,null=True, blank=True)
#     # organization = models.ForeignKey(Organization, db_column='organization' ,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(db_column='created_at',auto_now_add=True)
#     status=models.CharField(db_column='status',max_length=50,choices=[(e.name,e.value) for e in status],default=status.PENDING.value)
#     event_images=models.JSONField(db_column='event_images',default=list,blank=True,null=True)
#     live_stream_link=models.CharField(db_column='live_stream_link',max_length=100,null=True,blank=True)
#     category = models.ForeignKey(EventCategory, db_column='category', on_delete=models.CASCADE, null=True, blank=True)
#     # sub_category = models.ForeignKey(EventSubCategory, on_delete=models.SET_NULL, db_column='sub_category', null=True, blank=True)
#     object_id = models.ForeignKey(District, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='Events')
#     geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.DISTRICT.value)
#     event_status = models.CharField(db_column='event_status',max_length=50,choices=[(e.name, e.value) for e in EventStatusEnum],default=EventStatusEnum.UPCOMING.name)
#     user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='Events', null=True)
#     event_details=models.CharField(max_length=1000,null=True,blank=True)




#     @property
#     def relative_time(self):
#         if not self.start_date:
#             return "Unknown"

#         # Get IST timezone
#         ist_timezone = pytz_timezone('Asia/Kolkata')

#         # Get the current time in IST (timezone-aware)
#         now = timezone.now().astimezone(ist_timezone)

#         # Convert start_date to a timezone-aware datetime in IST
#         start_datetime = self.start_date
#         if timezone.is_naive(start_datetime):
#             # If start_date is naive, localize it to IST timezone
#             start_datetime = ist_timezone.localize(start_datetime)
#         else:
#             # If already timezone-aware, convert to IST
#             start_datetime = start_datetime.astimezone(ist_timezone)

#         # Check if the event has already started or not
#         if start_datetime > now:
#             diff = relativedelta(start_datetime, now)
#             if diff.years > 0:
#                 return f"{diff.years} year{'s' if diff.years > 1 else ''} to go"
#             elif diff.months > 0:
#                 return f"{diff.months} month{'s' if diff.months > 1 else ''} to go"
#             elif diff.days > 0:
#                 return f"{diff.days} day{'s' if diff.days > 1 else ''} to go"
#             elif diff.hours > 0:
#                 return f"{diff.hours} hour{'s' if diff.hours > 1 else ''} to go"
#             elif diff.minutes > 0:
#                 return f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} to go"
#             else:
#                 return "Less than a minute to go"
#         else:
#             # Event has already started, so show the time since it started
#             diff = relativedelta(now, start_datetime)
#             if diff.years > 0:
#                 return f"{diff.years} year{'s' if diff.years > 1 else ''} ago"
#             elif diff.months > 0:
#                 return f"{diff.months} month{'s' if diff.months > 1 else ''} ago"
#             elif diff.days > 0:
#                 return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
#             elif diff.hours > 0:
#                 return f"{diff.hours} hour{'s' if diff.hours > 1 else ''} ago"
#             elif diff.minutes > 0:
#                 return f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} ago"
#             else:
#                 return "Less than a minute ago"


#     def update_event_status(self):
#         now = timezone.now()

#         if self.end_date:
#             # Check if end_date is naive, if so, make it timezone-aware
#             if timezone.is_naive(self.end_date):
#                 end_datetime = timezone.make_aware(self.end_date.replace(hour=23, minute=59, second=59))
#             else:
#                 end_datetime = self.end_date.replace(hour=23, minute=59, second=59)

#             if end_datetime < now and self.event_status != EventStatusEnum.COMPLETED.name:
#                 self.event_status = EventStatusEnum.COMPLETED.name
#                 self.save(update_fields=['event_status'])

#         elif self.start_date:
#             # Check if start_date is naive, if so, make it timezone-aware
#             if timezone.is_naive(self.start_date):
#                 start_datetime = timezone.make_aware(self.start_date.replace(hour=0, minute=0, second=0))
#             else:
#                 start_datetime = self.start_date.replace(hour=0, minute=0, second=0)

#             if start_datetime < now and self.event_status != EventStatusEnum.COMPLETED.name:
#                 self.event_status = EventStatusEnum.COMPLETED.name
#                 self.save(update_fields=['event_status'])


#     def save(self, *args, **kwargs):
#     # Update event status before saving
#         self.update_event_status()
#         super(Events, self).save(*args, **kwargs)


                
#     class Meta:
#         db_table = 'event'














import uuid
from django.db import models
from ..enums import *
from .event_category import EventCategory
from .user import Register
from .village import Village
from datetime import datetime
from django.utils import timezone
class Event(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    category = models.ForeignKey(EventCategory, db_column='category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(db_column='name', max_length=200)
    # status = models.CharField(db_column='status', max_length=15, blank=True, null=True, db_comment='Active/Inactive')
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(db_column='end_date')
    start_time = models.TimeField(db_column='start_time', null=True, blank=True)
    end_time = models.TimeField(db_column='end_time', null=True, blank=True)
    tag = models.CharField(db_column='tag', max_length=200, choices=[(e.name, e.value) for e in EventTag], default=None, blank=True, null=True)
    tag_id = models.CharField(null=True, max_length=200)
    tag_type_id = models.CharField(max_length=200, null=True, blank=True)
    geo_site = models.CharField(max_length=200, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
    object_id = models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    # content_type_id = models.IntegerField(null=True, blank=True)
    map_location = models.CharField(db_column='map_location', max_length=200, blank=True, null=True)
    address = models.CharField(db_column='address',max_length=200, blank=True, null=True)
    contact_name = models.CharField(db_column='contact_name', max_length=45, blank=True, null=True)
    contact_phone = models.CharField(db_column='contact_phone', max_length=10, blank=True, null=True)
    contact_email = models.EmailField(db_column='contact_email', max_length=200, blank=True, null=True)
    desc = models.TextField(db_column='desc',blank=True, null=True)
    status = models.CharField(db_column='status', max_length=200, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value)
    user = models.ForeignKey(Register,db_column='user_id', on_delete=models.SET_NULL, related_name='events', null=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True, default=list)

    event_status = models.CharField(db_column='event_status', max_length=200, choices=[(e.name, e.value) for e in EventStatusEnum], default=EventStatusEnum.UPCOMING.name)
    @property
    def relative_time(self):
        if not self.start_date or not self.start_time:
            return "Unknown"
        try:
            start_date = self.start_date
            start_time = self.start_time
            start_datetime = timezone.make_aware(datetime.combine(start_date, start_time))
        except ValueError as e:
            return f"Invalid date or time format: {e}"
        now = timezone.now()
        if start_datetime > now:
            diff = start_datetime - now
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes to go"
            elif diff.days == 1:
                return "1 day to go"
            else:
                return f"{diff.days} days to go"
        else:
            diff = now - start_datetime
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes ago"
            elif diff.days == 1:
                return "1 day ago"
            else:
                return f"{diff.days} days ago"
    def update_event_status(self):
        now = timezone.now()
        if self.end_date and self.end_time:
            end_datetime_str = f"{self.end_date} {self.end_time.strftime('%H:%M:%S')}"
            try:
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
                end_datetime = timezone.make_aware(end_datetime)
                if end_datetime < now:
                    self.event_status = EventStatusEnum.COMPLETED.name
                else:
                    self.event_status = EventStatusEnum.UPCOMING.name
                self.save()
            except ValueError as e:
                print(f"Error updating event status: {e}")
    class Meta:
        managed = True
        db_table = 'event'