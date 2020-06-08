from rauth import OAuth2Service
import json
from pprint import pprint
from peewee import *
import datetime
import time 
import pickle

db = MySQLDatabase('tesla', user='user', password='password', host='127.0.0.1', port=3306)  

optionCodes = {
    'MDLS':'Model S',
    'MS03':'Model S',
    'MS04':'Model S',
    'MDLX':'Model X',
    'MDL3':'Model 3',
    'RENA':'Region: North America',
    'RENC':'Region: Canada',
    'REEU':'Region: Europe',
    'AD02':'NEMA 14-50',
    'AD04':'European 3-Phase',
    'AD05':'European 3-Phase, IT',
    'AD06':'Schuko (1 phase, 230V 13A)',
    'AD07':'Red IEC309 (3 phase, 400V 16A)',
    'AD15':'',
    'ADPX2':'Type 2 Public Charging Connector',
    'ADX8':'Blue IEC309 (1 phase, 230V 32A)',
    'AF00':'No HEPA Filter',
    "AF02": "HEPA Filter",
    'AH00':'No Accessory Hitch',
    'APE1':'Enhanced Autopilot',
    "APF0": "Autopilot Firmware 2.0 Base",
    "APF1": "Autopilot Firmware 2.0 Enhanced",
    "APF2": "Full Self-Driving Capability",
    'APH0':'Autopilot 2.0 Hardware',
    'APH2':'Autopilot 2.0 Hardware',
    'APH3':'Autopilot 2.5 Hardware',
    'APH4':'Autopilot 3.0 Hardware Full Self-Driving Computer',
    "APPA": "Autopilot Hardware 1",
    "APPB": "Enhanced Autopilot",
    'AU00':'No Audio Package',
    "AU01": "Premium Sound",
    'BC0B':'Tesla Black Brake Calipers',
    "BC0R": "Tesla Red Brake Calipers",
    'BCMB':'Black Brake Calipers',
    "BP00": "No Ludicrous",
    "BP01": "Ludicrous Speed Upgrade",
    'BR00':'No Battery Firmware Limit',
    'BR03':'Battery Firmware Limit (60kWh)',
    'BR05':'Battery Firmware Limit (75kWh)',
    'BS00':'General Production Flag',
    'BS01':'Special Production Flag',
    'BT37':'75 kWh (Model 3)',
    'BT40':'40 kWh',
    'BT60':'60 kWh',
    'BT70':'70 kWh',
    'BT85':'85 kWh',
    "BTX4": "Model X 90D",
    "BTX5": "Model X 75D",
    "BTX6": "Model X 100D",
    'BTX7':'75 kWh',
    'BTX8':'85 kWh',
    "CC01": "Five Seat Interior",
    "CC02": "Six Seat Interior",
    "CC04": "Seven Seat Interior",
    "CC12": "Six Seat Interior with Center Console",
    "CDM0": "No CHAdeMO Charging Adaptor",
    'CH00':'Standard Charger (40 Amp)',
    'CH01':'Dual Chargers (80 Amp)',
    "CH04": "72 Amp Charger (Model S/X)",
    'CH05':'48 Amp Charger (Model S/X)',
    'CH07':'48 Amp Charger (Model 3)',
    'COL0':'Signature',
    'COL1':'Solid',
    'COL2':'Metallic',
    'COL3':'Tesla Multi-Coat',
    'COUS':'Country: United States',
    'CONL':'Country: Netherlands',
    'CW00':'No Cold Weather Package',
    'CW02':'Subzero Weather Package',
    'DA00':'No Autopilot',
    'DA01':'Active Safety (ACC,LDW,SA)',
    'DA02':'Autopilot Convenience Features',
    'DCF0':'Autopilot Convenience Features (DCF0)',
    'DRLH':'Left Hand Drive',
    'DRRH':'Right Hand Drive',
    'DSH5':'PUR Dash Pad',
    'DSH7':'Alcantara Dashboard Accents',
    'DSHG':'PUR Dash Pad',
    'DU00':'Drive Unit - IR',
    'DU01':'Drive Unit - Infineon',
    'DV2W':'Rear-Wheel Drive',
    "DV4W": "All-Wheel Drive",
    'FG00':'No Exterior Lighting Package',
    'FG01':'Exterior Lighting Package',
    "FG02": "Exterior Lighting Package",
    'FR01':'Base Front Row',
    "FR02": "Ventilated Front Seats",
    'FR03':'',
    'FR04':'',
    'FMP6':'',
    'HC00':'No Home Charging installation',
    'HC01':'Home Charging Installation',
    'HP00':'No HPWC Ordered',
    'HP01':'HPWC Ordered',
    'ID3W':'(Model 3) Wood Decor',
    "IDBA": "Dark Ash Wood Decor",
    "IDBO": "Figured Ash Wood Decor",
    "IDCF": "Carbon Fiber Upgrade",
    "IDOK": "Oak Décor",
    'IDOM':'Matte Obeche Wood Decor',
    'IDOG':'Gloss Obeche Wood Decor',
    'IDLW':'Lacewood Decor',
    'IDPB':'Piano Black Decor',
    'IN3BB':'All Black Partial Premium Interior',
    'IN3PB':'All Black Premium Interior',
    'INBBW':'White',
    'INBFP':'Classic Black',
    'INBPP':'Black',
    'INBTB':'Multi-Pattern Black',
    'INFBP':'Black Premium',
    'INLPC':'Cream',
    'INLPP':'Black / Light Headliner',
    'INWPT':'Tan Interior',
    'IVBPP':'All Black Interior',
    'IVBSW':'Ultra White Interior',
    'IVBTB':'All Black Interior',
    'IVLPC':'Vegan Cream',
    "INBDS": "Black Premium",
    "INBFW": "White Premium",
    "INBTB": "Black Textile Interior",
    "INBWS": "White Premium",
    "INFBP": "Black Premium",
    "INLFC": "Cream Premium",
    "INLFP": "Black Premium / Light Headliner",
    'IX00':'No Extended Nappa Leather Trim',
    'IX01':'Extended Nappa Leather Trim',
    'LLP1':'',
    'LLP2':'',
    'LP01':'Premium Interior Lighting',
    "LT00": "Vegan interior",
    "LT01": "Standard interior",
    'LT3W':'',
    'LT4B':'',
    'LT4C':'',
    'LT4W':'',
    'LT5C':'',
    'LT5P':'',
    'LT6P':'',
    "ME02": "Memory Seats",
    'MI00':'2015 Production Refresh',
    'MI01':'2016 Production Refresh',
    'MI02':'2017 Production Refresh',
    'MI03':'2018 Production Refresh',
    'MT301':'Standard Range Plus Rear-Wheel Drive',
    'MT305':'Mid Range Rear-Wheel Drive',
    'PA00':'No Paint Armor',
    'PBCW':'Catalina White',
    'PBSB':'Sierra Black',
    'PBT8':'Performance 85kWh',
    'PF00':'No Performance Legacy Package',
    'PF01':'Performance Legacy Package',
    'PI00':'No Premium Interior',
    'PI01':'Premium Upgrades Package',
    'PK00':'LEGACY No Parking Sensors',
    'PMAB':'Anza Brown Metallic',
    'PMBL':'Obsidian Black Multi-Coat',
    'PMMB':'Monterey Blue Metallic',
    'PMMR':'Multi-Coat Red',
    'PMNG':'Midnight Silver Metallic',
    'PMSG':'Sequoia Green Metallic',
    'PMSS':'San Simeon Silver Metallic',
    'PMTG':'Dolphin Grey Metallic',
    'PPMR':'Muir Red Multi-Coat',
    'PPSB':'Deep Blue Metallic',
    "PPSR": "Signature Red Paint",
    'PPSW':'Shasta Pearl White Multi-Coat',
    'PPTI':'Titanium Metallic',
    'PRM30':'Partial Premium Interior',
    'PRM31':'Premium Interior',
    'PS00':'No Parcel Shelf',
    'PS01':'Parcel Shelf',
    'PX00':'No Performance Plus Package',
    'PX01':'Performance Plus',
    "PX6D": "Model X P100D: Zero to 60 in 2.5 sec",
    'P85D':'P85D',
    'OSSB':'',
    "QLBS": "Black Premium Interior",
    "QLFC": "Cream Premium Interior",
    "QLFP": "Black Premium Interior",
    "QLFW": "White Premium Interior",
    "QLWS": "White Premium Interior",
    'QNET':'Tan NextGen',
    "QPBT": "Black Textile Interior",
    'QPMP':'Black seats',
    'QTBW':'White Premium Seats',
    'QTFP':'Black Premium Seats',
    'QTPC':'Cream Premium Seats',
    'QTPP':'Black Premium Seats',
    'QTPT':'Tan Premium Seats',
    'QTTB':'Multi-Pattern Black Seats',
    'QVBM':'Multi-Pattern Black Seats',
    'QVPC':'Vegan Cream Seats',
    'QVPP':'Vegan Cream Seats',
    'QVSW':'White Tesla Seats',
    'RCX0':'No Rear Console',
    'RF3G':'Model 3 Glass Roof',
    'RFBK':'Black Roof',
    'RFBC':'Body Color Roof',
    'RFFG':'Glass Roof',
    'RFP0':'All Glass Panoramic Roof',
    'RFP2':'Sunroof',
    'RFPX':'Model X Roof',
    'S02P':'',
    'S31B':'',
    'S32C':'',
    'S32P':'',
    'S32W':'',
    'SC00':'No Supercharging',
    'SC01':'Supercharging Enabled',
    'SC04':'Pay Per Use Supercharging',
    "SC05": "Free Supercharging",
    'SP00':'No Security Package',
    'SR01':'Standard 2nd row',
    "SR06": "Seven Seat Interior",
    'SR07':'Standard 2nd row',
    'ST00':'Non-leather Steering Wheel',
    'ST01':'Non-heated Leather Steering Wheel',
    'SU00':'Standard Suspension',
    'SU01':'Smart Air Suspension',
    'TIC4':'All-Season Tires',
    'TM00':'General Production Trim',
    'TM02':'General Production Signature Trim',
    'TM0A':'ALPHA PRE-PRODUCTION NON-SALEABLE',
    'TM0B':'BETA PRE-PRODUCTION NON-SALEABLE',
    'TM0C':'PRE-PRODUCTION SALEABLE',
    'TP01':'Tech Package - No Autopilot',
    'TP02':'Tech Package with Autopilot',
    'TP03':'Tech Package with Enhanced Autopilot',
    'TR00':'No Third Row Seat',
    'TR01':'Third Row Seating',
    "TRA1": "Third Row HVAC",
    'TW00':'No Towing Package',
    "TW01": "Towing Package",
    'UM01':'Universal Mobile Charger - US Port (Single)',
    'UTAB':'Black Alcantara Headliner',
    'UTAW':'Light Headliner',
    "UTPB": "Dark Headliner",
    "UTSB": "Dark Headliner",
    "UTZW": "Light Headliner",
    'W38B':'18" Aero Wheels: For the Model 3 and Model Y',
    'W39B':'19" Sport Wheels',
    'WT20':'20" Silver Slipstream Wheels',
    'WT22':'22" Silver Turbine Wheels',
    'WTAS':'19" Silver Slipstream Wheels',
    'WTDS':'19" Grey Slipstream Wheels',
    'WTSG':'21" Turbine Wheels',
    'WTSP':'21" Turbine Wheels',
    'WTSS':'21" Turbine Wheels',
    'WTTB':'19" Cyclone Wheels',
    'WTW4':'19" Winter Tire Set',
    'WTW5':'21" Winter Tire Set',
    'WTX1':'19" Michelin Primacy Tire Upgrade',
    'WXW4':'No 19" Winter Tire Set',
    'WXW5':'No 21" Winter Tire Set',
    "WTSC": "20\" Sonic Carbon Wheels",
    "WTUT": "22\" Onyx Black Turbine Wheels",
    'X001':'Override: Power Liftgate',
    'X003':'Maps & Navigation',
    'X004':'Override: No Navigation',
    'X007':'Daytime running lights',
    'X010':'Base Mirrors',
    'X011':'Override: Homelink',
    'X012':'Override: No Homelink',
    'X013':'Override: Satellite Radio',
    'X014':'Override: No Satellite Radio',
    'X019':'Carbon Fiber Spoiler',
    'X020':'No Performance Exterior',
    "X021": "No Active Spoiler",
    'X024':'Performance Package',
    'X025':'No Performance Package',
    'X027':'Lighted Door Handles',
    'X028':'Battery Badge',
    'X029':'Remove Battery Badge',
    'X030':'Override: No Passive Entry Pkg',
    'X031':'Keyless Entry',
    'X037':'Powerfolding Mirrors',
    'X039':'DAB Radio',
    'X040':'No DAB Radio',
    'X043':'No Phone Dock Kit',
    'X044':'Phone Dock Kit',
    'YF00':'No Yacht Floor',
    'YF01':'Matching Yacht Floor',
    'YFCC':'',
    'YFFC':'Integrated Center Console'
    }

class TeslaAPI:
    def __init__(self,email,password):
        self.access_token = None

        self.service = OAuth2Service(
            client_id='81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384',
            client_secret='c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3',
            access_token_url="https://owner-api.teslamotors.com/oauth/token",
            authorize_url="https://owner-api.teslamotors.com/oauth/token",
            base_url="https://owner-api.teslamotors.com/",
        )

        self.get_access_token(email,password)
        self.start_session()

    def get_access_token(self,email,password):
        data = {"grant_type": "password",
              "client_id": '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384',
              "client_secret": 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3',
              "email": email,
              "password": password}

        session = self.service.get_auth_session(data=data, decoder=json.loads)
        #print(session)
        self.access_token = session.access_token
    
    def start_session(self):
        self.my_session = self.service.get_session(token=self.access_token)
    
    def vehicle_info(self):
        vehicle_endpoint = 'api/1/vehicles/'
        self.vehicle_dict = self.my_session.get(
            self.service.base_url+vehicle_endpoint).json()['response'][0]
        info = {#'vin':self.vehicle_dict['vin'],
                'name':self.vehicle_dict['display_name'],
                'options':self.options(self.vehicle_dict)}
        self.id_s = self.vehicle_dict['id_s']
        self.vehicle_id = self.vehicle_dict['vehicle_id']
        return info
    
    def options(self,opt):
        codes = self.vehicle_dict['option_codes'].split(',')
        results = []
        for i in codes:
            if i in optionCodes.keys():
                results.append(optionCodes[i])
            else:
                optionCodes[i]=''
        return results
        
    def products(self):
        self.vehicle_info()
        return self.my_session.get('api/1/products/').json()['response']

    def vehicles(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/').json()['response']

    def vehicle(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s).json()['response']
    
    def vehicle_data_legacy(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/data').json()['response']

    def vehicle_data(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/vehicle_data').json()['response']

    def service_data(self):
        self.vehicle_info()
        return self.my_session.get("api/1/vehicles/"+ self.id_s +"/service_data").json()['response']

    def mobile_enabled(self):
        self.vehicle_info()
        return self.my_session.get("api/1/vehicles/"+ self.id_s +"/mobile_enabled").json()['response']
    
    def charge_state(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/data_request/charge_state').json()['response']
    
    def climate_state(self):
        self.vehicle_info()
        return self.my_session.get('/api/1/vehicles/'+ self.id_s +'/data_request/climate_state').json()['response']

    def drive_state(self):
        self.vehicle_info()
        return self.my_session.get('/api/1/vehicles/'+ self.id_s +'/data_request/drive_state').json()['response']
    
    def nearby_charging_sites(self):
        self.vehicle_info()
        return self.my_session.get('/api/1/vehicles/'+ self.id_s +'/nearby_charging_sites').json()['response']
    
    def gui_settings(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/data_request/gui_settings').json()['response']
    
    def vehicle_state(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/data_request/vehicle_state').json()['response']
    
    def vehicle_config(self):
        self.vehicle_info()
        return self.my_session.get('api/1/vehicles/'+ self.id_s +'/data_request/vehicle_config').json()['response']

class database_tesla():
    def __init__(self, v_id):
        class BaseModel(Model):
            class Meta:
                database = db

        class tesla(BaseModel):
            id = BigIntegerField(default=None)
            user_id = IntegerField(default=None)
            vehicle_id = IntegerField(default=None)
            vin = CharField(default=None)
            display_name = CharField(default=None)
            option_codes = TextField(default=None)
            color = CharField(default=None)
            tokens = CharField(default=None)
            state = CharField(default=None)
            in_service = BooleanField(default=None)
            id_s = BigIntegerField(default=None)
            calendar_enabled = BooleanField(default=None)
            api_version = IntegerField(default=None)
            backseat_token = CharField(default=None)
            backseat_token_updated_at = CharField(default=None)
            gps_as_of = IntegerField(default=None)
            heading = IntegerField(default=None)
            latitude = FloatField(default=None)
            longitude = FloatField(default=None)
            native_latitude = FloatField(default=None)
            native_location_supported = IntegerField(default=None)
            native_longitude = FloatField(default=None)
            native_type = CharField(default=None)
            power = IntegerField(default=None)
            shift_state = CharField(default=None)
            speed = CharField(default=None)
            timestamp = DateTimeField(default=None)
            battery_heater = BooleanField(default=None)
            battery_heater_no_power = BooleanField(default=None)
            climate_keeper_mode = CharField(default=None)
            defrost_mode = IntegerField(default=None)
            driver_temp_setting = FloatField(default=None)
            fan_status = IntegerField(default=None)
            inside_temp = CharField(default=None)
            is_auto_conditioning_on = CharField(default=None)
            is_climate_on = BooleanField(default=None)
            is_front_defroster_on = BooleanField(default=None)
            is_preconditioning = BooleanField(default=None)
            is_rear_defroster_on = BooleanField(default=None)
            left_temp_direction = CharField(default=None)
            max_avail_temp = FloatField(default=None)
            min_avail_temp = FloatField(default=None)
            outside_temp = CharField(default=None)
            passenger_temp_setting = FloatField(default=None)
            remote_heater_control_enabled = BooleanField(default=None)
            right_temp_direction = CharField(default=None)
            seat_heater_left = IntegerField(default=None)
            seat_heater_rear_center = IntegerField(default=None)
            seat_heater_rear_left = IntegerField(default=None)
            seat_heater_rear_left_back = IntegerField(default=None)
            seat_heater_rear_right = IntegerField(default=None)
            seat_heater_rear_right_back = IntegerField(default=None)
            seat_heater_right = IntegerField(default=None)
            side_mirror_heaters = BooleanField(default=None)
            steering_wheel_heater = BooleanField(default=None)
            wiper_blade_heater = BooleanField(default=None)
            battery_heater_on = BooleanField(default=None)
            battery_level = IntegerField(default=None)
            battery_range = FloatField(default=None)
            charge_current_request = IntegerField(default=None)
            charge_current_request_max = IntegerField(default=None)
            charge_enable_request = BooleanField(default=None)
            charge_energy_added = FloatField(default=None)
            charge_limit_soc = IntegerField(default=None)
            charge_limit_soc_max = IntegerField(default=None)
            charge_limit_soc_min = IntegerField(default=None)
            charge_limit_soc_std = IntegerField(default=None)
            charge_miles_added_ideal = FloatField(default=None)
            charge_miles_added_rated = FloatField(default=None)
            charge_port_cold_weather_mode = BooleanField(default=None)
            charge_port_door_open = BooleanField(default=None)
            charge_port_latch = CharField(default=None)
            charge_rate = FloatField(default=None)
            charge_to_max_range = BooleanField(default=None)
            charger_actual_current = IntegerField(default=None)
            charger_phases = CharField(default=None)
            charger_pilot_current = IntegerField(default=None)
            charger_power = IntegerField(default=None)
            charger_voltage = IntegerField(default=None)
            charging_state = CharField(default=None)
            conn_charge_cable = CharField(default=None)
            est_battery_range = FloatField(default=None)
            fast_charger_brand = CharField(default=None)
            fast_charger_present = BooleanField(default=None)
            fast_charger_type = CharField(default=None)
            ideal_battery_range = FloatField(default=None)
            managed_charging_active = BooleanField(default=None)
            managed_charging_start_time = CharField(default=None)
            managed_charging_user_canceled = BooleanField(default=None)
            max_range_charge_counter = IntegerField(default=None)
            minutes_to_full_charge = IntegerField(default=None)
            not_enough_power_to_heat = BooleanField(default=None)
            scheduled_charging_pending = BooleanField(default=None)
            scheduled_charging_start_time = CharField(default=None)
            time_to_full_charge = FloatField(default=None)
            trip_charging = BooleanField(default=None)
            usable_battery_level = IntegerField(default=None)
            user_charge_enable_request = CharField(default=None)
            gui_24_hour_time = BooleanField(default=None)
            gui_charge_rate_units = CharField(default=None)
            gui_distance_units =  CharField(default=None)
            gui_range_display = CharField(default=None)
            gui_temperature_units = CharField(default=None)
            show_range_units = BooleanField(default=None)
            api_version = IntegerField(default=None)
            autopark_state_v2 =  CharField(default=None)
            autopark_state_v3 =  CharField(default=None)
            autopark_style = CharField(default=None)
            calendar_supported = BooleanField(default=None)
            car_version = CharField(default=None)
            center_display_state = IntegerField(default=None)
            df = IntegerField(default=None)
            dr = IntegerField(default=None)
            fd_window = IntegerField(default=None)
            fp_window = IntegerField(default=None)
            ft = IntegerField(default=None)
            homelink_device_count = IntegerField(default=None)
            homelink_nearby = BooleanField(default=None)
            is_user_present = BooleanField(default=None)
            last_autopark_error = CharField(default=None)
            locked = BooleanField(default=None)
            remote_control_enabled = BooleanField(default=None)
            notifications_supported = BooleanField(default=None)
            odometer = FloatField(default=None)
            parsed_calendar_supported = BooleanField(default=None)
            pf = IntegerField(default=None)
            pr = IntegerField(default=None)
            rd_window = IntegerField(default=None)
            remote_start = BooleanField(default=None)
            remote_start_enabled = BooleanField(default=None)
            remote_start_supported = BooleanField(default=None)
            rp_window = IntegerField(default=None)
            rt = IntegerField(default=None)
            sentry_mode = BooleanField(default=None)
            sentry_mode_available = BooleanField(default=None)
            smart_summon_available = BooleanField(default=None)
            download_perc = IntegerField(default=None)
            expected_duration_sec = IntegerField(default=None)
            install_perc = IntegerField(default=None)
            scheduled_time_ms = BigIntegerField(default=None)
            status = CharField(default=None)
            version = CharField(default=None)
            active = BooleanField(default=None)
            current_limit_mph = FloatField(default=None)
            max_limit_mph = IntegerField(default=None)
            min_limit_mph = IntegerField(default=None)
            pin_code_set = BooleanField(default=None)
            summon_standby_mode_enabled = BooleanField(default=None)
            sun_roof_percent_open = IntegerField(default=None)
            sun_roof_state = CharField(default=None)
            valet_mode = BooleanField(default=None)
            valet_pin_needed = BooleanField(default=None)
            vehicle_name = CharField(default=None)
            can_accept_navigation_requests = BooleanField(default=None)
            can_actuate_trunks = BooleanField(default=None)
            car_special_type = CharField(default=None)
            car_type = CharField(default=None)
            charge_port_type = CharField(default=None)
            ece_restrictions = BooleanField(default=None)
            eu_vehicle = BooleanField(default=None)
            exterior_color = CharField(default=None)
            has_air_suspension = BooleanField(default=None)
            has_ludicrous_mode = BooleanField(default=None)
            key_version = IntegerField(default=None)
            motorized_charge_port = BooleanField(default=None)
            perf_config = CharField(default=None)
            plg = BooleanField(default=None)
            rear_seat_heaters = IntegerField(default=None)
            rear_seat_type = IntegerField(default=None)
            rhd = BooleanField(default=None)
            roof_color = CharField(default=None)
            seat_type = IntegerField(default=None)
            spoiler_type = CharField(default=None)
            sun_roof_installed = IntegerField(default=None)
            third_row_seats = CharField(default=None)
            trim_badging = CharField(default=None)
            use_range_badging = BooleanField(default=None)
            wheel_type = CharField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_tesla"

        class idle(BaseModel):
            state = CharField(default=None)
            shift_state = CharField(default=None)
            charging_state = CharField(default=None)
            battery_range = FloatField(default=None)
            outside_temp = CharField(default=None)
            inside_temp = CharField(default=None)
            driver_temp_setting = FloatField(default=None)
            fan_status = IntegerField(default=None)
            is_auto_conditioning_on = CharField(default=None)
            locked = BooleanField(default=None)
            df = IntegerField(default=None)
            dr = IntegerField(default=None)
            pf = IntegerField(default=None)
            pr = IntegerField(default=None)
            idle_time = IntegerField(default=0)
            logger = CharField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_idle"

        class charge_state(BaseModel):
            battery_heater_on = BooleanField(default=None)
            battery_level = IntegerField(default=None)
            battery_range = FloatField(default=None)
            charge_current_request = IntegerField(default=None)
            charge_current_request_max = IntegerField(default=None)
            charge_enable_request = BooleanField(default=None)
            charge_energy_added = FloatField(default=None)
            charge_limit_soc = IntegerField(default=None)
            charge_limit_soc_max = IntegerField(default=None)
            charge_limit_soc_min = IntegerField(default=None)
            charge_limit_soc_std = IntegerField(default=None)
            charge_miles_added_ideal = FloatField(default=None)
            charge_miles_added_rated = FloatField(default=None)
            charge_port_cold_weather_mode = BooleanField(default=None)
            charge_port_door_open = BooleanField(default=None)
            charge_port_latch = CharField(default=None)
            charge_rate = FloatField(default=None)
            charge_to_max_range = BooleanField(default=None)
            charger_actual_current = IntegerField(default=None)
            charger_phases = CharField(default=None)
            charger_pilot_current = IntegerField(default=None)
            charger_power = IntegerField(default=None)
            charger_voltage = IntegerField(default=None)
            charging_state = CharField(default=None)
            conn_charge_cable = CharField(default=None)
            est_battery_range = FloatField(default=None)
            fast_charger_brand = CharField(default=None)
            fast_charger_present = BooleanField(default=None)
            fast_charger_type = CharField(default=None)
            ideal_battery_range = FloatField(default=None)
            managed_charging_active = BooleanField(default=None)
            managed_charging_start_time = CharField(default=None)
            managed_charging_user_canceled = BooleanField(default=None)
            max_range_charge_counter = IntegerField(default=None)
            minutes_to_full_charge = IntegerField(default=None)
            not_enough_power_to_heat = BooleanField(default=None)
            scheduled_charging_pending = BooleanField(default=None)
            scheduled_charging_start_time = CharField(default=None)
            time_to_full_charge = FloatField(default=None)
            trip_charging = BooleanField(default=None)
            usable_battery_level = IntegerField(default=None)
            user_charge_enable_request = CharField(default=None)
            latitude = FloatField(default=None)
            longitude = FloatField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_charge_state"

        class climate_state(BaseModel):
            battery_heater = BooleanField(default=None)
            battery_heater_no_power = BooleanField(default=None)
            climate_keeper_mode = CharField(default=None)
            defrost_mode = IntegerField(default=None)
            driver_temp_setting = FloatField(default=None)
            fan_status = IntegerField(default=None)
            inside_temp = CharField(default=None)
            is_auto_conditioning_on = CharField(default=None)
            is_climate_on = BooleanField(default=None)
            is_front_defroster_on = BooleanField(default=None)
            is_preconditioning = BooleanField(default=None)
            is_rear_defroster_on = BooleanField(default=None)
            left_temp_direction = CharField(default=None)
            max_avail_temp = FloatField(default=None)
            min_avail_temp = FloatField(default=None)
            outside_temp = CharField(default=None)
            passenger_temp_setting = FloatField(default=None)
            remote_heater_control_enabled = BooleanField(default=None)
            right_temp_direction = CharField(default=None)
            seat_heater_left = IntegerField(default=None)
            seat_heater_rear_center = IntegerField(default=None)
            seat_heater_rear_left = IntegerField(default=None)
            seat_heater_rear_left_back = IntegerField(default=None)
            seat_heater_rear_right = IntegerField(default=None)
            seat_heater_rear_right_back = IntegerField(default=None)
            seat_heater_right = IntegerField(default=None)
            side_mirror_heaters = BooleanField(default=None)
            steering_wheel_heater = BooleanField(default=None)
            wiper_blade_heater = BooleanField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_climate_state"

        class drive_state(BaseModel):
            gps_as_of = IntegerField(default=None)
            heading = IntegerField(default=None)
            latitude = FloatField(default=None)
            longitude = FloatField(default=None)
            native_latitude = FloatField(default=None)
            native_location_supported = IntegerField(default=None)
            native_longitude = FloatField(default=None)
            native_type = CharField(default=None)
            power = IntegerField(default=None)
            shift_state = CharField(default=None)
            speed = CharField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_drive_state"

        class gui_settings(BaseModel):
            gui_24_hour_time = BooleanField(default=None)
            gui_charge_rate_units = CharField(default=None)
            gui_distance_units = CharField(default=None)
            gui_range_display = CharField(default=None)
            gui_temperature_units = CharField(default=None)
            show_range_units = BooleanField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_gui_settings"

        class vehicle_state(BaseModel):
            api_version = IntegerField(default=None)
            autopark_state_v2 = CharField(default=None)
            autopark_state_v3 = CharField(default=None)
            autopark_style = CharField(default=None)
            calendar_supported = BooleanField(default=None)
            car_version = CharField(default=None)
            center_display_state = IntegerField(default=None)
            df = IntegerField(default=None)
            dr = IntegerField(default=None)
            fd_window = IntegerField(default=None)
            fp_window = IntegerField(default=None)
            ft = IntegerField(default=None)
            homelink_device_count = IntegerField(default=None)
            homelink_nearby = BooleanField(default=None)
            is_user_present = BooleanField(default=None)
            last_autopark_error = CharField(default=None)
            locked = BooleanField(default=None)
            remote_control_enabled = BooleanField(default=None)
            notifications_supported = BooleanField(default=None)
            odometer = FloatField(default=None)
            parsed_calendar_supported = BooleanField(default=None)
            pf = IntegerField(default=None)
            pr = IntegerField(default=None)
            rd_window = IntegerField(default=None)
            remote_start = BooleanField(default=None)
            remote_start_enabled = BooleanField(default=None)
            remote_start_supported = BooleanField(default=None)
            rp_window = IntegerField(default=None)
            rt = IntegerField(default=None)
            sentry_mode = BooleanField(default=None)
            sentry_mode_available = BooleanField(default=None)
            smart_summon_available = BooleanField(default=None)
            download_perc = IntegerField(default=None)
            expected_duration_sec = IntegerField(default=None)
            install_perc = IntegerField(default=None)
            scheduled_time_ms = BigIntegerField(default=None)
            status = CharField(default=None)
            version = CharField(default=None)
            active = BooleanField(default=None)
            current_limit_mph = FloatField(default=None)
            max_limit_mph = IntegerField(default=None)
            min_limit_mph = IntegerField(default=None)
            pin_code_set = BooleanField(default=None)
            summon_standby_mode_enabled = BooleanField(default=None)
            sun_roof_percent_open = IntegerField(default=None)
            sun_roof_state = CharField(default=None)
            valet_mode = BooleanField(default=None)
            valet_pin_needed = BooleanField(default=None)
            vehicle_name = CharField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_vehicle_state"

        class vehicle_config(BaseModel):
            can_accept_navigation_requests = BooleanField(default=None)
            can_actuate_trunks = BooleanField(default=None)
            car_special_type = CharField(default=None)
            car_type = CharField(default=None)
            charge_port_type = CharField(default=None)
            ece_restrictions = BooleanField(default=None)
            eu_vehicle = BooleanField(default=None)
            exterior_color = CharField(default=None)
            has_air_suspension = BooleanField(default=None)
            has_ludicrous_mode = BooleanField(default=None)
            key_version = IntegerField(default=None)
            motorized_charge_port = BooleanField(default=None)
            perf_config = CharField(default=None)
            plg = BooleanField(default=None)
            rear_seat_heaters = IntegerField(default=None)
            rear_seat_type = IntegerField(default=None)
            rhd = BooleanField(default=None)
            roof_color = CharField(default=None)
            seat_type = IntegerField(default=None)
            spoiler_type = CharField(default=None)
            sun_roof_installed = IntegerField(default=None)
            third_row_seats = CharField(default=None)
            trim_badging = CharField(default=None)
            use_range_badging = BooleanField(default=None)
            wheel_type = CharField(default=None)
            timestamp = DateTimeField(default=None)
            class Meta:
                table_name = "test_" + v_id + "_vehicle_config"

        class timestamp(BaseModel):
            timestamp = DateTimeField(default=None)
            gui_24_hour_time = BooleanField(default=None)
            gui_charge_rate_units = CharField(default=None)
            gui_distance_units = CharField(default=None)
            gui_range_display = CharField(default=None)
            gui_temperature_units = CharField(default=None)
            show_range_units = BooleanField(default=None)
            class Meta:
                table_name = "test_" + v_id + "timestamp"

        db.create_tables([tesla, idle, charge_state, climate_state, drive_state, gui_settings, vehicle_state, vehicle_config])
        self.tesla = tesla()
        self.idle = idle()
        self.charge_state = charge_state()
        self.climate_state = climate_state()
        self.drive_state = drive_state()
        self.gui_settings = gui_settings()
        self.vehicle_state = vehicle_state()
        self.vehicle_config = vehicle_config()

    def inserting_data(self, data):
        self.dictionary = {}
        for key, value in data.items():
            if isinstance(value, dict):
                data2 = value
                for key2, value2 in data2.items():
                    if isinstance(value2, dict):
                        data3 = value2
                        for key3, value3 in data3.items():
                            self.dictionary.update({key3: value3})
                    else:
                        self.dictionary.update({key2: value2})
            else:
                if isinstance(value, list):
                    d = str(value[0]) + ', ' + str(value[1])
                    self.dictionary.update({key: d})
                else:
                    self.dictionary.update({key: value})

        del_key_list = []
        for k, v in self.dictionary.items():
            if v is None:
                del_key_list.append(k)
        
        for k in del_key_list:
            del(self.dictionary[k])

        dt = datetime.datetime.fromtimestamp(self.dictionary["timestamp"]/1000)
        dt = dt + datetime.timedelta(hours=9)
        self.dictionary["timestamp"] = dt
        
        self.idle_list = ['state', 'shift_state', 'charging_state', 'battery_range', 'outside_temp', 'inside_temp', 'driver_temp_setting', 'fan_status', 'is_auto_conditioning_on', 'locked', 'df', 'dr', 'pf', 'pr', 'timestamp']
        self.charge_state_list = ['battery_heater_on', 'battery_level', 'battery_range', 'charge_current_request', 'charge_current_request_max', 'charge_enable_request', 'charge_energy_added', 'charge_limit_soc', 'charge_limit_soc_max', 'charge_limit_soc_min', 'charge_limit_soc_std', 'charge_miles_added_ideal', 'charge_miles_added_rated', 'charge_port_cold_weather_mode', 'charge_port_door_open', 'charge_port_latch', 'charge_rate', 'charge_to_max_range', 'charger_actual_current', 'charger_phases', 'charger_pilot_current', 'charger_power', 'charger_voltage', 'charging_state', 'conn_charge_cable', 'est_battery_range', 'fast_charger_brand', 'fast_charger_present', 'fast_charger_type', 'ideal_battery_range', 'managed_charging_active', 'managed_charging_start_time', 'managed_charging_user_canceled', 'max_range_charge_counter', 'minutes_to_full_charge', 'not_enough_power_to_heat', 'scheduled_charging_pending', 'scheduled_charging_start_time', 'time_to_full_charge', 'trip_charging', 'usable_battery_level', 'user_charge_enable_request', 'latitude', 'longitude', 'timestamp']
        self.climate_state_list = ['battery_heater', 'battery_heater_no_power', 'climate_keeper_mode', 'defrost_mode', 'driver_temp_setting', 'fan_status', 'inside_temp', 'is_auto_conditioning_on', 'is_climate_on', 'is_front_defroster_on', 'is_preconditioning', 'is_rear_defroster_on', 'left_temp_direction', 'max_avail_temp', 'min_avail_temp', 'outside_temp', 'passenger_temp_setting', 'remote_heater_control_enabled', 'right_temp_direction', 'seat_heater_left', 'seat_heater_rear_center', 'seat_heater_rear_left', 'seat_heater_rear_left_back', 'seat_heater_rear_right', 'seat_heater_rear_right_back', 'seat_heater_right', 'side_mirror_heaters', 'steering_wheel_heater', 'wiper_blade_heater', 'timestamp']
        self.drive_state_list = ['gps_as_of', 'heading', 'latitude', 'longitude', 'native_latitude', 'native_location_supported', 'native_longitude', 'native_type', 'power', 'shift_state', 'speed', 'timestamp']
        self.gui_settings_list = ['gui_24_hour_time', 'gui_charge_rate_units', 'gui_distance_units', 'gui_range_display', 'gui_temperature_units', 'show_range_units', 'timestamp']
        self.vehicle_state_list = ['api_version', 'autopark_state_v2', 'autopark_state_v3', 'autopark_style', 'calendar_supported', 'car_version', 'center_display_state', 'df', 'dr', 'fd_window', 'fp_window', 'ft', 'homelink_device_count', 'homelink_nearby', 'is_user_present', 'last_autopark_error', 'locked', 'remote_control_enabled', 'notifications_supported', 'odometer', 'parsed_calendar_supported', 'pf', 'pr', 'rd_window', 'remote_start', 'remote_start_enabled', 'remote_start_supported', 'rp_window', 'rt', 'sentry_mode', 'sentry_mode_available', 'smart_summon_available', 'download_perc', 'expected_duration_sec', 'install_perc', 'scheduled_time_ms', 'status', 'version', 'active', 'current_limit_mph', 'max_limit_mph', 'min_limit_mph', 'pin_code_set', 'summon_standby_mode_enabled', 'sun_roof_percent_open', 'sun_roof_state', 'valet_mode', 'valet_pin_needed', 'vehicle_name', 'timestamp']
        self.vehicle_config_list = ['can_accept_navigation_requests', 'can_actuate_trunks', 'car_special_type', 'car_type', 'charge_port_type', 'ece_restrictions', 'eu_vehicle', 'exterior_color', 'has_air_suspension', 'has_ludicrous_mode', 'key_version', 'motorized_charge_port', 'perf_config', 'plg', 'rear_seat_heaters', 'rear_seat_type', 'rhd', 'roof_color', 'seat_type', 'spoiler_type', 'sun_roof_installed', 'third_row_seats', 'trim_badging', 'use_range_badging', 'wheel_type', 'timestamp']
        
        self.idle_dict = self.change_to_each_table(self.idle_list)
        self.charge_state_dict = self.change_to_each_table(self.charge_state_list)
        self.climate_state_dict = self.change_to_each_table(self.climate_state_list)
        self.drive_state_dict = self.change_to_each_table(self.drive_state_list)
        self.gui_settings_dict = self.change_to_each_table(self.gui_settings_list)
        self.vehicle_state_dict = self.change_to_each_table(self.vehicle_state_list)
        self.vehicle_config_dict = self.change_to_each_table(self.vehicle_config_list)
        
        #pprint(self.dictionary)
        if self.dictionary["center_display_state"] is 0:
            self.idle.create(**self.idle_dict)
        else:
            self.tesla.create(**self.dictionary)
            self.charge_state.create(**self.charge_state_dict)
            self.climate_state.create(**self.climate_state_dict)
            self.drive_state.create(**self.drive_state_dict)
            self.gui_settings.create(**self.gui_settings_dict)
            self.vehicle_state.create(**self.vehicle_state_dict)
            self.vehicle_config.create(**self.vehicle_config_dict)
            
    def change_to_each_table(self, each_list):
        each_dict = {}
        for i in each_list:
            for k, v in self.dictionary.items():
                if k == i:
                    each_dict.update({k: v})
        return each_dict

def record_error(e):
    try:
        with open('error_about_tesla.txt', 'rb') as fp:
            record = pickle.load(fp)
    except FileNotFoundError:
        record = []
    except EOFError:
        record = []
    record.append(e)
    with open('record.txt', 'wb+') as fp:
        pickle.dump(record, fp)

class tesla_main(TeslaAPI, database_tesla):
    def __init__(self, email, password):
        self.tesla_api = TeslaAPI(email, password)
        #pprint(self.tesla_api.vehicle_info())
    
    def tesla_main(self):
        v_id = self.tesla_api.vehicle_data()['vehicle_id']

        for i in range(2880):
            try:
                data = self.tesla_api.vehicle_data()
                database_tesla(str(v_id)).inserting_data(data)
                time.sleep(59)
            except KeyError as k:
                record_error(k)
                pass
            except IndexError as i:
                record_error(i)
                pass
            except AttributeError as a:
                record_error(a)
                pass

if __name__ == '__main__':
#def make_tesla_table_with_celery(email, password):
    db.connect()

    email = "boyoung.gratia.kim@gmail.com"
    password = "zerooneai01"

    t = tesla_main(email, password)
    t.tesla_main()


