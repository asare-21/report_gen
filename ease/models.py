from django.db import models


# Create your models here.
class UserModel(models.Model):
    # link to the user model
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    nsp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class NotificationModel(models.Model):
    # link to the user model
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}  Message: {self.message}"


class FMModel(models.Model):
    # link to the user model
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name_of_station = models.CharField(max_length=100, default="")
    station_officer = models.CharField(max_length=100,  default="")
    staff_strength = models.IntegerField(default=0)
    # External
    security_post = models.BooleanField(default=False)
    security_post_comment = models.TextField(default='', blank=True)
    signage_board = models.BooleanField(default=False)
    signage_board_comment = models.TextField(default='', blank=True)
    epa_permit = models.BooleanField(default=False)
    epa_permit_comment = models.TextField(default='', blank=True)
    fire_permit = models.BooleanField(default=False)
    fire_permit_comment = models.TextField(default='', blank=True)
    #ANTENNA / TOWER
    lighting_arrestor = models.BooleanField(default=False)
    lighting_arrestor_comment = models.TextField(default='', blank=True)
    aviation_obstruction_light = models.BooleanField(default=False)
    aviation_obstruction_light_comment = models.TextField(
        default='', blank=True)
    mast_earthed = models.BooleanField(default=False)
    mast_earthed_comment = models.TextField(default='', blank=True)
    mast_right_colors = models.BooleanField(default=False)
    mast_right_colors_comment = models.TextField(default='', blank=True)
    directional_antenna = models.BooleanField(default=False)
    directional_antenna_comment = models.TextField(default='', blank=True)
    cavity_filter = models.BooleanField(default=False)
    cavity_filter_comment = models.TextField(default='', blank=True)
    backup_power = models.BooleanField(default=False)
    backup_power_comment = models.TextField(default='', blank=True)
    # Internal / Studio
    equipment_sheet = models.BooleanField(default=False)
    equipment_sheet_comment = models.TextField(default='', blank=True)
    on_air_lighting = models.BooleanField(default=False)
    on_air_lighting_comment = models.TextField(default='', blank=True)
    ventillation_equipment = models.BooleanField(default=False)
    ventillation_equipment_comment = models.TextField(
        default='', blank=True, null=True)
    acoustic_panel = models.BooleanField(default=False)
    acoustic_panel_comment = models.TextField(default='', blank=True)
    secure_door = models.BooleanField(default=False)
    secure_door_comment = models.TextField(default='', blank=True)
    reception = models.BooleanField(default=False)
    reception_comment = models.TextField(default='', blank=True)
    # Technical Parameters
    mast_height = models.FloatField(
        default=0.0,)
    antenna_gain = models.FloatField(
        default=0.0, )
    make_and_model_antenna = models.CharField(max_length=100, default='')
    operating_frequency = models.FloatField(
        default=0.0,)
    physical_location = models.CharField(max_length=100, default='')
    coords = models.CharField(max_length=100, default='')
    ghana_post_gps = models.CharField(max_length=100, default='')
    comments_remarks = models.TextField(default='', blank=True)
    # Complete
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "{}'s Station Officer: {}".format(self.name_of_station, self.name)


class TVModel(models.Model):
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name_of_station = models.CharField(max_length=100, default="")
    station_officer = models.CharField(max_length=100, default="")
    staff_strength = models.IntegerField(default=0)
    # External
    security_post = models.BooleanField(default=False)
    security_post_comment = models.TextField(default='', blank=True)
    signage_board = models.BooleanField(default=False)
    signage_board_comment = models.TextField(default='', blank=True)
    epa_permit = models.BooleanField(default=False)
    epa_permit_comment = models.TextField(default='', blank=True)
    fire_permit = models.BooleanField(default=False)
    fire_permit_comment = models.TextField(default='', blank=True)
    # LINK
    lighting_arrestor = models.BooleanField(default=False)
    lighting_arrestor_comment = models.TextField(default='', blank=True)
    aviation_obstruction_light = models.BooleanField(default=False)
    aviation_obstruction_light_comment = models.TextField(
        default='', blank=True)
    mast_earthed = models.BooleanField(default=False)
    mast_earthed_comment = models.TextField(default='', blank=True)
    mast_right_colors = models.BooleanField(default=False)
    mast_right_colors_comment = models.TextField(default='', blank=True)
    backup_power = models.BooleanField(default=False)
    backup_power_comment = models.TextField(default='', blank=True)
    # ISP
    isp = models.CharField(max_length=100, default='')
    satellite_provider = models.CharField(max_length=100, default='')
    satellite_provider_comment = models.TextField(default='', blank=True)
    # Internal / Studio
    equipment_sheet = models.BooleanField(default=False)
    equipment_sheet_comment = models.TextField(default='', blank=True)
    on_air_lighting = models.BooleanField(default=False)
    on_air_lighting_comment = models.TextField(default='', blank=True)
    ventillation_equipment = models.BooleanField(default=False)
    ventillation_equipment_comment = models.TextField(default='', blank=True)
    acoustic_panel = models.BooleanField(default=False)
    acoustic_panel_comment = models.TextField(default='', blank=True)
    secure_door = models.BooleanField(default=False)
    secure_door_comment = models.TextField(default='', blank=True)
    reception = models.BooleanField(default=False)
    reception_comment = models.TextField(default='', blank=True)
    # Technical Parameters
    mast_height = models.FloatField(
        default=0.0,)
    antenna_gain = models.FloatField(
        default=0.0, )
    make_and_model_antenna = models.CharField(max_length=100, default='')
    operating_frequency = models.FloatField(
        default=0.0,)
    physical_location = models.CharField(max_length=100, default='')
    coords = models.CharField(max_length=100, default='')
    ghana_post_gps = models.CharField(max_length=100, default='')
    comments_remarks = models.TextField(default='', blank=True)
    # Complete
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "Station Officer {} ".format(self.name)
