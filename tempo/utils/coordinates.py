from datetime import datetime as dt

from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from astropy.coordinates import AltAz
from astropy import units
# from astropy.utils.exceptions import AstropyDeprecationWarning
# warnings.filterwarnings("ignore", category=AstropyDeprecationWarning)
from astroplan import Observer, FixedTarget, is_observable, AtNightConstraint, AirmassConstraint, moon,\
    observability_table
import numpy as np

from tempo.utils import settings

def dct_loc():
    location_name = settings.LOCATION_NAME
    return EarthLocation.of_site(location_name)


def dct_astroplan_loc():
    location_name = settings.LOCATION_NAME
    return Observer.at_site(location_name)

def radec_to_altaz(
        ra, dec, unit,
        observing_location=dct_loc(),
):
    observing_time = Time(str(dt.utcnow()))
    aa = AltAz(location=observing_location, obstime=observing_time)
    coord = SkyCoord(ra, dec, unit=unit)
    altaz_coord = coord.transform_to(aa)
    alt = altaz_coord.alt.degree
    az = altaz_coord.az.degree
    return alt, az

def airmass_horizon(airmass):
    z = np.arccos(1/airmass)
    horizon = np.pi/2 - z
    return horizon * units.rad


def calculate_time_observable_minutes(
        location, coords, constraints, time_range
):
    ot = observability_table(
        constraints, location, [coords], time_range=time_range, time_grid_resolution=0.05 * units.h
    )
    time_range_total_minutes = (time_range[1].to_datetime() - time_range[0].to_datetime()).total_seconds()/60
    time_observable = time_range_total_minutes * ot['fraction of time observable'][0]
    return time_observable


class TargetVisibilityAtDCT:
    def __init__(self, ra, dec, unit, error_radius):
        self.airmass_horizon = airmass_horizon(settings.AIRMASS_LIMIT)
        self.coord = SkyCoord(ra, dec, unit=unit)
        self.error_radius = error_radius * units.Unit(unit)
        # self.time = Time(utc_time)
        self.time_now = Time(str(dt.utcnow()))
        self.dct = dct_astroplan_loc()
        assert isinstance(self.dct, Observer)
        self.is_night = self.dct.is_night(self.time_now, horizon=-18*units.degree)  # horizon set to astronomical twilight
        if self.is_night:
            twilight_evening_which, twilight_morning_which = (u'previous', u'next')
        else:
            twilight_evening_which, twilight_morning_which = (u'next', u'next')
        self.target = FixedTarget(name='Target', coord=self.coord)
        self.target_is_up = self.dct.target_is_up(self.time_now, self.target, horizon=self.airmass_horizon)
        if self.target_is_up:
            target_rise_which, target_set_which = (u'previous', u'next')
        else:
            target_rise_which, target_set_which = (u'next', u'next')
        self.target_rise_time = self.dct.target_rise_time(
            self.time_now, self.target, which=target_rise_which, horizon=self.airmass_horizon
        )
        self.target_set_time = self.dct.target_set_time(
            self.time_now, self.target, which=target_set_which, horizon=self.airmass_horizon
        )
        # self.target_rise_time_local = self.target_rise_time.datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
        self.twilight_evening = self.dct.twilight_evening_astronomical(self.time_now, which=twilight_evening_which)
        self.twilight_morning = self.dct.twilight_morning_astronomical(self.time_now, which=twilight_morning_which)
        constraints = (AirmassConstraint(settings.AIRMASS_LIMIT), AtNightConstraint.twilight_astronomical())
        self.target_is_observable = is_observable(
            constraints=constraints, observer=self.dct, targets=self.target,
            time_range=(self.twilight_evening, self.twilight_morning)
        )[0]
        print(self.target_is_observable)
        self.time_observable_minutes = calculate_time_observable_minutes(
            self.dct, self.target, constraints, (self.twilight_evening, self.twilight_morning)
        )
        if self.time_observable_minutes < settings.OBSERVABLE_TIME_MINIMUM_MINUTES:
            self.target_is_observable = False
