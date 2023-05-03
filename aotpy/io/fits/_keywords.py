"""
This module contains data that defines the AOT FITS format itself, including the specific FITS keywords and tables used.
Not meant to be imported by users.
"""

import re
from dataclasses import dataclass

CURRENT_AOT_VERSION = '0.5'


@dataclass
class AOTField:
    name: str
    format: str
    unit: str
    mandatory: bool = False
    unique: bool = False
    description: str = None


class AOTFieldDict(dict):
    def __init__(self, *args: AOTField):
        super().__init__({field.name: field for field in args})


def fits_type_to_aot(fits_type: str) -> str:
    if fits_type in ['E', 'D']:
        return FLOAT_FORMAT
    if fits_type in ['B', 'I', 'J', 'K']:
        return INTEGER_FORMAT
    if re.fullmatch(r'\d*A', fits_type):
        return STRING_FORMAT
    if re.fullmatch(r'[QP][DE]\(\d*\)', fits_type):
        return LIST_FORMAT
    raise ValueError('Format not in AOT FITS')


STRING_FORMAT = 'str'  # e.g. 64A
INTEGER_FORMAT = 'int'  # e.g. K
FLOAT_FORMAT = 'flt'  # e.g. D
LIST_FORMAT = 'lst'  # e.g. QD

ROW_REFERENCE = 'ROWREF'
INTERNAL_REFERENCE = 'INTREF'
FILE_REFERENCE = 'FILEREF'
URL_REFERENCE = 'URLREF'
IMAGE_UNIT = 'BUNIT'

UNIT_DIMENSIONLESS = '1'
UNIT_COUNT = 'count'
UNIT_METERS = 'm'
UNIT_SECONDS = 's'
UNIT_RADIANS = 'rad'
UNIT_DEGREES = 'deg'
UNIT_ELECTRONS = 'electron'
UNIT_PIXELS = 'pix'
UNIT_DECIBELS = 'dB'
UNIT_FRAME = 'frame'
UNIT_HERTZ = 'Hz'
UNIT_ARCSEC = 'arcsec'

TIME_TABLE = 'AOT_TIME'
GEOMETRY_TABLE = 'AOT_GEOMETRY'
ATMOSPHERIC_PARAMETERS_TABLE = 'AOT_ATMOSPHERIC_PARAMETERS'
ABERRATIONS_TABLE = 'AOT_ABERRATIONS'
TELESCOPES_TABLE = 'AOT_TELESCOPES'
SOURCES_TABLE = 'AOT_SOURCES'
SOURCES_SODIUM_LGS_TABLE = 'AOT_SOURCES_SODIUM_LGS'
SOURCES_RAYLEIGH_LGS_TABLE = 'AOT_SOURCES_RAYLEIGH_LGS'
DETECTORS_TABLE = 'AOT_DETECTORS'
SCORING_CAMERAS_TABLE = 'AOT_SCORING_CAMERAS'
WAVEFRONT_SENSORS_TABLE = 'AOT_WAVEFRONT_SENSORS'
WAVEFRONT_SENSORS_SHACK_HARTMANN_TABLE = 'AOT_WAVEFRONT_SENSORS_SHACK_HARTMANN'
WAVEFRONT_SENSORS_PYRAMID_TABLE = 'AOT_WAVEFRONT_SENSORS_PYRAMID'
WAVEFRONT_CORRECTORS_TABLE = 'AOT_WAVEFRONT_CORRECTORS'
WAVEFRONT_CORRECTORS_DM_TABLE = 'AOT_WAVEFRONT_CORRECTORS_DM'
LOOPS_TABLE = 'AOT_LOOPS'
LOOPS_CONTROL_TABLE = 'AOT_LOOPS_CONTROL'
LOOPS_OFFLOAD_TABLE = 'AOT_LOOPS_OFFLOAD'

MANDATORY_TABLE_SET = {TIME_TABLE, GEOMETRY_TABLE, ATMOSPHERIC_PARAMETERS_TABLE, ABERRATIONS_TABLE, TELESCOPES_TABLE,
                       SOURCES_TABLE, DETECTORS_TABLE, SCORING_CAMERAS_TABLE, WAVEFRONT_SENSORS_TABLE,
                       WAVEFRONT_CORRECTORS_TABLE, LOOPS_TABLE}

SECONDARY_TABLE_SET = {SOURCES_SODIUM_LGS_TABLE, SOURCES_RAYLEIGH_LGS_TABLE, WAVEFRONT_SENSORS_SHACK_HARTMANN_TABLE,
                       WAVEFRONT_SENSORS_PYRAMID_TABLE, WAVEFRONT_CORRECTORS_DM_TABLE, LOOPS_CONTROL_TABLE,
                       LOOPS_OFFLOAD_TABLE}
TABLE_SET = MANDATORY_TABLE_SET | SECONDARY_TABLE_SET
TABLE_SEQUENCE = [TIME_TABLE, GEOMETRY_TABLE, ATMOSPHERIC_PARAMETERS_TABLE, ABERRATIONS_TABLE, TELESCOPES_TABLE,
                  SOURCES_TABLE, SOURCES_SODIUM_LGS_TABLE, SOURCES_RAYLEIGH_LGS_TABLE, DETECTORS_TABLE,
                  SCORING_CAMERAS_TABLE, WAVEFRONT_SENSORS_TABLE, WAVEFRONT_SENSORS_SHACK_HARTMANN_TABLE,
                  WAVEFRONT_SENSORS_PYRAMID_TABLE, WAVEFRONT_CORRECTORS_TABLE, WAVEFRONT_CORRECTORS_DM_TABLE,
                  LOOPS_TABLE, LOOPS_CONTROL_TABLE, LOOPS_OFFLOAD_TABLE]
TABLE_FIELDS: dict[str, AOTFieldDict] = {}

# AOSystem keywords
AOT_VERSION = 'AOT-VERS'
AOT_AO_MODE = 'AO-MODE'
AOT_AO_MODE_SET = {'SCAO', 'SLAO', 'GLAO', 'MOAO', 'LTAO', 'MCAO'}
AOT_TIMESYS = 'TIMESYS'
AOT_TIMESYS_UTC = 'UTC'
AOT_DATE_BEG = 'DATE-BEG'
AOT_DATE_END = 'DATE-END'
AOT_STREHL_RATIO = 'STREHL-R'
AOT_TEMPORAL_ERROR = 'TEMP-ERR'
AOT_CONFIG = 'CONFIG'
AOT_HEADER_SET = {AOT_VERSION, AOT_AO_MODE, AOT_TIMESYS, AOT_DATE_BEG, AOT_DATE_END, AOT_STREHL_RATIO,
                  AOT_TEMPORAL_ERROR, AOT_CONFIG}

REFERENCE_UID = 'UID'
TIME_REFERENCE = 'TIME_UID'
GEOMETRY_REFERENCE = 'GEOMETRY_UID'
ABERRATION_REFERENCE = 'ABERRATION_UID'
LASER_LAUNCH_TELESCOPE_REFERENCE = 'LLT_UID'
DETECTOR_REFERENCE = 'DETECTOR_UID'
SOURCE_REFERENCE = 'SOURCE_UID'
NCPA_REFERENCE = 'NCPA_UID'
TELESCOPE_REFERENCE = 'TELESCOPE_UID'

# AOT_TIME fields
TIME_TIMESTAMPS = 'TIMESTAMPS'
TIME_FRAME_NUMBERS = 'FRAME_NUMBERS'
TIME_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=TIME_TIMESTAMPS, format=LIST_FORMAT, unit=UNIT_SECONDS),
    AOTField(name=TIME_FRAME_NUMBERS, format=LIST_FORMAT, unit=UNIT_COUNT)
)
TABLE_FIELDS[TIME_TABLE] = TIME_FIELDS

# AOT_GEOMETRY fields
GEOMETRY_ROTATION = 'ROTATION'
GEOMETRY_TRANSLATION_X = 'TRANSLATION_X'
GEOMETRY_TRANSLATION_Y = 'TRANSLATION_Y'
GEOMETRY_MAGNIFICATION_X = 'MAGNIFICATION_X'
GEOMETRY_MAGNIFICATION_Y = 'MAGNIFICATION_Y'
GEOMETRY_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=TIME_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=GEOMETRY_ROTATION, format=LIST_FORMAT, unit=UNIT_RADIANS),
    AOTField(name=GEOMETRY_TRANSLATION_X, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=GEOMETRY_TRANSLATION_Y, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=GEOMETRY_MAGNIFICATION_X, format=LIST_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=GEOMETRY_MAGNIFICATION_Y, format=LIST_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[GEOMETRY_TABLE] = GEOMETRY_FIELDS

# AOT_ATMOSPHERIC_PARAMETERS fields
ATMOSPHERIC_PARAMETERS_WAVELENGTH = 'WAVELENGTH'
ATMOSPHERIC_PARAMETERS_R0 = 'R0'
ATMOSPHERIC_PARAMETERS_FWHM = 'FWHM'
ATMOSPHERIC_PARAMETERS_TAU0 = 'TAU0'
ATMOSPHERIC_PARAMETERS_THETA0 = 'THETA0'
ATMOSPHERIC_PARAMETERS_LAYERS_WEIGHT = 'LAYERS_WEIGHT'
ATMOSPHERIC_PARAMETERS_LAYERS_HEIGHT = 'LAYERS_HEIGHT'
ATMOSPHERIC_PARAMETERS_LAYERS_L0 = 'LAYERS_LO'
ATMOSPHERIC_PARAMETERS_LAYERS_WIND_SPEED = 'LAYERS_WIND_SPEED'
ATMOSPHERIC_PARAMETERS_LAYERS_WIND_DIRECTION = 'LAYERS_WIND_DIRECTION'
ATMOSPHERIC_PARAMETERS_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=ATMOSPHERIC_PARAMETERS_WAVELENGTH, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=TIME_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_R0, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_FWHM, format=LIST_FORMAT, unit=UNIT_ARCSEC),
    AOTField(name=ATMOSPHERIC_PARAMETERS_TAU0, format=LIST_FORMAT, unit=UNIT_SECONDS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_THETA0, format=LIST_FORMAT, unit=UNIT_RADIANS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_LAYERS_WEIGHT, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_LAYERS_HEIGHT, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_LAYERS_L0, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_LAYERS_WIND_SPEED, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ATMOSPHERIC_PARAMETERS_LAYERS_WIND_DIRECTION, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[ATMOSPHERIC_PARAMETERS_TABLE] = ATMOSPHERIC_PARAMETERS_FIELDS

# AOT_ABERRATIONS fields
ABERRATION_MODES = 'MODES'
ABERRATION_COEFFICIENTS = 'COEFFICIENTS'
ABERRATION_X_OFFSETS = 'X_OFFSETS'
ABERRATION_Y_OFFSETS = 'Y_OFFSETS'
ABERRATION_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=ABERRATION_MODES, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=ABERRATION_COEFFICIENTS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=ABERRATION_X_OFFSETS, format=LIST_FORMAT, unit=UNIT_RADIANS),
    AOTField(name=ABERRATION_Y_OFFSETS, format=LIST_FORMAT, unit=UNIT_RADIANS)
)
TABLE_FIELDS[ABERRATIONS_TABLE] = ABERRATION_FIELDS

# AOT_TELESCOPES fields
TELESCOPE_TYPE = 'TYPE'
TELESCOPE_LATITUDE = 'LATITUDE'
TELESCOPE_LONGITUDE = 'LONGITUDE'
TELESCOPE_ELEVATION = 'ELEVATION'
TELESCOPE_AZIMUTH = 'AZIMUTH'
TELESCOPE_PARALLACTIC = 'PARALLACTIC'
TELESCOPE_PUPIL_MASK = 'PUPIL_MASK'
TELESCOPE_PUPIL_ANGLE = 'PUPIL_ANGLE'
TELESCOPE_ENCLOSING_D = 'ENCLOSING_D'
TELESCOPE_INSCRIBED_D = 'INSCRIBED_D'
TELESCOPE_OBSTRUCTION_D = 'OBSTRUCTION_D'
TELESCOPE_SEGMENTS_TYPE = 'SEGMENT_TYPE'
TELESCOPE_SEGMENTS_SIZE = 'SEGMENT_SIZE'
TELESCOPE_SEGMENTS_X = 'SEGMENTS_X'
TELESCOPE_SEGMENTS_Y = 'SEGMENTS_Y'
TELESCOPE_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=TELESCOPE_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=TELESCOPE_LATITUDE, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=TELESCOPE_LONGITUDE, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=TELESCOPE_ELEVATION, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=TELESCOPE_AZIMUTH, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=TELESCOPE_PARALLACTIC, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=TELESCOPE_PUPIL_MASK, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=TELESCOPE_PUPIL_ANGLE, format=FLOAT_FORMAT, unit=UNIT_RADIANS),
    AOTField(name=TELESCOPE_ENCLOSING_D, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=TELESCOPE_INSCRIBED_D, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=TELESCOPE_OBSTRUCTION_D, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=TELESCOPE_SEGMENTS_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=TELESCOPE_SEGMENTS_SIZE, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=TELESCOPE_SEGMENTS_X, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=TELESCOPE_SEGMENTS_Y, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ABERRATION_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[TELESCOPES_TABLE] = TELESCOPE_FIELDS
TELESCOPE_TYPE_MAIN = 'Main Telescope'
TELESCOPE_TYPE_LLT = 'Laser Launch Telescope'
TELESCOPE_SEGMENT_TYPE_MONOLITHIC = 'Monolithic'
TELESCOPE_SEGMENT_TYPE_HEXAGON = 'Hexagon'
TELESCOPE_SEGMENT_TYPE_CIRCLE = 'Circle'

# AOT_SOURCES fields
SOURCE_TYPE = 'TYPE'
SOURCE_RIGHT_ASCENSION = 'RIGHT_ASCENSION'
SOURCE_DECLINATION = 'DECLINATION'
SOURCE_ELEVATION_OFFSET = 'ELEVATION_OFFSET'
SOURCE_AZIMUTH_OFFSET = 'AZIMUTH_OFFSET'
SOURCE_WIDTH = 'WIDTH'
SOURCE_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=SOURCE_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=SOURCE_RIGHT_ASCENSION, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=SOURCE_DECLINATION, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=SOURCE_ELEVATION_OFFSET, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=SOURCE_AZIMUTH_OFFSET, format=FLOAT_FORMAT, unit=UNIT_DEGREES),
    AOTField(name=SOURCE_WIDTH, format=FLOAT_FORMAT, unit=UNIT_RADIANS)
)
TABLE_FIELDS[SOURCES_TABLE] = SOURCE_FIELDS
SOURCE_TYPE_SCIENCE_STAR = 'Science Star'
SOURCE_TYPE_NATURAL_GUIDE_STAR = 'Natural Guide Star'
SOURCE_TYPE_SODIUM_LASER_GUIDE_STAR = 'Sodium Laser Guide Star'
SOURCE_TYPE_RAYLEIGH_LASER_GUIDE_STAR = 'Rayleigh Laser Guide Star'

# AOT_SOURCES_SODIUM_LGS fields
SOURCE_SODIUM_LGS_HEIGHT = 'HEIGHT'
SOURCE_SODIUM_LGS_PROFILE = 'PROFILE'
SOURCE_SODIUM_LGS_ALTITUDES = 'ALTITUDES'
SOURCE_SODIUM_LGS_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=SOURCE_SODIUM_LGS_HEIGHT, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=SOURCE_SODIUM_LGS_PROFILE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=SOURCE_SODIUM_LGS_ALTITUDES, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=LASER_LAUNCH_TELESCOPE_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[SOURCES_SODIUM_LGS_TABLE] = SOURCE_SODIUM_LGS_FIELDS

# AOT_SOURCES_RAYLEIGH_LGS fields
SOURCE_RAYLEIGH_LGS_DISTANCE = 'DISTANCE'
SOURCE_RAYLEIGH_LGS_DEPTH = 'DEPTH'
SOURCE_RAYLEIGH_LGS_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=SOURCE_RAYLEIGH_LGS_DISTANCE, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=SOURCE_RAYLEIGH_LGS_DEPTH, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=LASER_LAUNCH_TELESCOPE_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[SOURCES_RAYLEIGH_LGS_TABLE] = SOURCE_RAYLEIGH_LGS_FIELDS

# AOT_DETECTORS fields
DETECTOR_TYPE = 'TYPE'
DETECTOR_SAMPLING_TECHNIQUE = 'SAMPLING_TECHNIQUE'
DETECTOR_SHUTTER_TYPE = 'SHUTTER_TYPE'
DETECTOR_FLAT_FIELD = 'FLAT_FIELD'
DETECTOR_READOUT_NOISE = 'READOUT_NOISE'
DETECTOR_PIXEL_INTENSITIES = 'PIXEL_INTENSITIES'
DETECTOR_INTEGRATION_TIME = 'INTEGRATION_TIME'
DETECTOR_COADDS = 'COADDS'
DETECTOR_DARK = 'DARK'
DETECTOR_WEIGHT_MAP = 'WEIGHT_MAP'
DETECTOR_QUANTUM_EFFICIENCY = 'QUANTUM_EFFICIENCY'
DETECTOR_PIXEL_SCALE = 'PIXEL_SCALE'
DETECTOR_BINNING = 'BINNING'
DETECTOR_BANDWIDTH = 'BANDWIDTH'
DETECTOR_TRANSMISSION_WAVELENGTH = 'TRANSMISSION_WAVELENGTH'
DETECTOR_TRANSMISSION = 'TRANSMISSION'
DETECTOR_SKY_BACKGROUND = 'SKY_BACKGROUND'
DETECTOR_GAIN = 'GAIN'
DETECTOR_EXCESS_NOISE = 'EXCESS_NOISE'
DETECTOR_FILTER = 'FILTER'
DETECTOR_BAD_PIXEL_MAP = 'BAD_PIXEL_MAP'
DETECTOR_DYNAMIC_RANGE = 'DYNAMIC_RANGE'
DETECTOR_READOUT_RATE = 'READOUT_RATE'
DETECTOR_FRAME_RATE = 'FRAME_RATE'
DETECTOR_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=DETECTOR_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_SAMPLING_TECHNIQUE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_SHUTTER_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_FLAT_FIELD, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_READOUT_NOISE, format=FLOAT_FORMAT,
             unit=f'{UNIT_ELECTRONS}*{UNIT_SECONDS}^-1*{UNIT_PIXELS}^-1'),
    AOTField(name=DETECTOR_PIXEL_INTENSITIES, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_INTEGRATION_TIME, format=FLOAT_FORMAT, unit=UNIT_SECONDS),
    AOTField(name=DETECTOR_COADDS, format=INTEGER_FORMAT, unit=UNIT_COUNT),
    AOTField(name=DETECTOR_DARK, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_WEIGHT_MAP, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_QUANTUM_EFFICIENCY, format=FLOAT_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_PIXEL_SCALE, format=FLOAT_FORMAT, unit=f'{UNIT_RADIANS}*{UNIT_PIXELS}^-1'),
    AOTField(name=DETECTOR_BINNING, format=INTEGER_FORMAT, unit=UNIT_COUNT),
    AOTField(name=DETECTOR_BANDWIDTH, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=DETECTOR_TRANSMISSION_WAVELENGTH, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=DETECTOR_TRANSMISSION, format=LIST_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_SKY_BACKGROUND, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_GAIN, format=FLOAT_FORMAT, unit=UNIT_ELECTRONS),
    AOTField(name=DETECTOR_EXCESS_NOISE, format=FLOAT_FORMAT, unit=UNIT_ELECTRONS),
    AOTField(name=DETECTOR_FILTER, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_BAD_PIXEL_MAP, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_DYNAMIC_RANGE, format=FLOAT_FORMAT, unit=UNIT_DECIBELS),
    AOTField(name=DETECTOR_READOUT_RATE, format=STRING_FORMAT, unit=f'{UNIT_PIXELS}*{UNIT_SECONDS}^-1'),
    AOTField(name=DETECTOR_FRAME_RATE, format=STRING_FORMAT, unit=f'{UNIT_FRAME}*{UNIT_SECONDS}^-1'),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[DETECTORS_TABLE] = DETECTOR_FIELDS

# AOT_SCORING_CAMERAS fields
SCORING_CAMERA_PUPIL_MASK = 'PUPIL_MASK'
SCORING_CAMERA_WAVELENGTH = 'WAVELENGTH'
SCORING_CAMERA_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=SCORING_CAMERA_PUPIL_MASK, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=SCORING_CAMERA_WAVELENGTH, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ABERRATION_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[SCORING_CAMERAS_TABLE] = SCORING_CAMERA_FIELDS

# AOT_WAVEFRONT_SENSORS
WAVEFRONT_SENSOR_TYPE = 'TYPE'
WAVEFRONT_SENSOR_DIMENSIONS = 'DIMENSIONS'
WAVEFRONT_SENSOR_N_VALID_SUBAPERTURES = 'N_VALID_SUBAPERTURES'
WAVEFRONT_SENSOR_MEASUREMENTS = 'MEASUREMENTS'
WAVEFRONT_SENSOR_REF_MEASUREMENTS = 'REF_MEASUREMENTS'
WAVEFRONT_SENSOR_SUBAPERTURE_MASK = 'SUBAPERTURE_MASK'
WAVEFRONT_SENSOR_MASK_X_OFFSETS = 'MASK_X_OFFSETS'
WAVEFRONT_SENSOR_MASK_Y_OFFSETS = 'MASK_Y_OFFSETS'
WAVEFRONT_SENSOR_SUBAPERTURE_SIZE = 'SUBAPERTURE_SIZE'
WAVEFRONT_SENSOR_SUBAPERTURE_INTENSITIES = 'SUBAPERTURE_INTENSITIES'
WAVEFRONT_SENSOR_WAVELENGTH = 'WAVELENGTH'
WAVEFRONT_SENSOR_OPTICAL_GAIN = 'OPTICAL_GAIN'
WAVEFRONT_SENSOR_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=WAVEFRONT_SENSOR_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=SOURCE_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=WAVEFRONT_SENSOR_DIMENSIONS, format=INTEGER_FORMAT, unit=UNIT_COUNT, mandatory=True),
    AOTField(name=WAVEFRONT_SENSOR_N_VALID_SUBAPERTURES, format=INTEGER_FORMAT, unit=UNIT_COUNT, mandatory=True),
    AOTField(name=WAVEFRONT_SENSOR_MEASUREMENTS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_REF_MEASUREMENTS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_SUBAPERTURE_MASK, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_MASK_X_OFFSETS, format=LIST_FORMAT, unit=UNIT_PIXELS),
    AOTField(name=WAVEFRONT_SENSOR_MASK_Y_OFFSETS, format=LIST_FORMAT, unit=UNIT_PIXELS),
    AOTField(name=WAVEFRONT_SENSOR_SUBAPERTURE_SIZE, format=STRING_FORMAT, unit=UNIT_PIXELS),
    AOTField(name=WAVEFRONT_SENSOR_SUBAPERTURE_INTENSITIES, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_WAVELENGTH, format=FLOAT_FORMAT, unit=UNIT_METERS),
    AOTField(name=WAVEFRONT_SENSOR_OPTICAL_GAIN, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=DETECTOR_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ABERRATION_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=NCPA_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[WAVEFRONT_SENSORS_TABLE] = WAVEFRONT_SENSOR_FIELDS
WAVEFRONT_SENSOR_TYPE_SHACK_HARTMANN = 'Shack-Hartmann'
WAVEFRONT_SENSOR_TYPE_PYRAMID = 'Pyramid'

# AOT_WAVEFRONT_SENSORS_SHACK_HARTMANN
WAVEFRONT_SENSOR_SHACK_HARTMANN_CENTROIDING_ALGORITHM = 'CENTROIDING_ALGORITHM'
WAVEFRONT_SENSOR_SHACK_HARTMANN_CENTROID_GAINS = 'CENTROID_GAINS'
WAVEFRONT_SENSOR_SHACK_HARTMANN_SPOT_FWHM = 'SPOT_FWHM'
WAVEFRONT_SENSOR_SHACK_HARTMANN_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=WAVEFRONT_SENSOR_SHACK_HARTMANN_CENTROIDING_ALGORITHM, format=STRING_FORMAT,
             unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_SHACK_HARTMANN_CENTROID_GAINS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_SENSOR_SHACK_HARTMANN_SPOT_FWHM, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[WAVEFRONT_SENSORS_SHACK_HARTMANN_TABLE] = WAVEFRONT_SENSOR_SHACK_HARTMANN_FIELDS

# AOT_WAVEFRONT_SENSORS_PYRAMID
WAVEFRONT_SENSOR_PYRAMID_N_SIDES = 'N_SIDES'
WAVEFRONT_SENSOR_PYRAMID_MODULATION = 'MODULATION'
WAVEFRONT_SENSOR_PYRAMID_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=WAVEFRONT_SENSOR_PYRAMID_N_SIDES, format=INTEGER_FORMAT, unit=UNIT_COUNT, mandatory=True),
    AOTField(name=WAVEFRONT_SENSOR_PYRAMID_MODULATION, format=FLOAT_FORMAT, unit=UNIT_METERS),
)
TABLE_FIELDS[WAVEFRONT_SENSORS_PYRAMID_TABLE] = WAVEFRONT_SENSOR_PYRAMID_FIELDS

# AOT_WAVEFRONT_CORRECTORS fields
WAVEFRONT_CORRECTOR_TYPE = 'TYPE'
WAVEFRONT_CORRECTOR_N_VALID_ACTUATORS = 'N_VALID_ACTUATORS'
WAVEFRONT_CORRECTOR_PUPIL_MASK = 'PUPIL_MASK'
WAVEFRONT_CORRECTOR_TFZ_NUM = 'TFZ_NUM'
WAVEFRONT_CORRECTOR_TFZ_DEN = 'TFZ_DEN'
WAVEFRONT_CORRECTOR_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=WAVEFRONT_CORRECTOR_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=TELESCOPE_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=WAVEFRONT_CORRECTOR_N_VALID_ACTUATORS, format=INTEGER_FORMAT, unit=UNIT_COUNT),
    AOTField(name=WAVEFRONT_CORRECTOR_PUPIL_MASK, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_CORRECTOR_TFZ_NUM, format=LIST_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_CORRECTOR_TFZ_DEN, format=LIST_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=GEOMETRY_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=ABERRATION_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[WAVEFRONT_CORRECTORS_TABLE] = WAVEFRONT_CORRECTOR_FIELDS
WAVEFRONT_CORRECTOR_TYPE_DM = 'Deformable Mirror'
WAVEFRONT_CORRECTOR_TYPE_TTM = 'Tip-Tilt Mirror'
WAVEFRONT_CORRECTOR_TYPE_LS = 'Linear Stage'

# AOT_WAVEFRONT_CORRECTORS_DM fields
WAVEFRONT_CORRECTOR_DM_ACTUATORS_X = 'ACTUATORS_X'
WAVEFRONT_CORRECTOR_DM_ACTUATORS_Y = 'ACTUATORS_Y'
WAVEFRONT_CORRECTOR_DM_INFLUENCE_FUNCTION = 'INFLUENCE_FUNCTION'
WAVEFRONT_CORRECTOR_DM_STROKE = 'STROKE'
WAVEFRONT_CORRECTOR_DM_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=WAVEFRONT_CORRECTOR_DM_ACTUATORS_X, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=WAVEFRONT_CORRECTOR_DM_ACTUATORS_Y, format=LIST_FORMAT, unit=UNIT_METERS),
    AOTField(name=WAVEFRONT_CORRECTOR_DM_INFLUENCE_FUNCTION, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=WAVEFRONT_CORRECTOR_DM_STROKE, format=FLOAT_FORMAT, unit=UNIT_METERS)
)
TABLE_FIELDS[WAVEFRONT_CORRECTORS_DM_TABLE] = WAVEFRONT_CORRECTOR_DM_FIELDS

# AOT_LOOPS fields
LOOPS_TYPE = 'TYPE'
LOOPS_COMMANDED = 'COMMANDED_UID'
LOOPS_STATUS = 'STATUS'
LOOPS_COMMANDS = 'COMMANDS'
LOOPS_REF_COMMANDS = 'REF_COMMANDS'
LOOPS_FRAMERATE = 'FRAMERATE'
LOOPS_DELAY = 'DELAY'
LOOPS_TIME_FILTER_NUM = 'TIME_FILTER_NUM'
LOOPS_TIME_FILTER_DEN = 'TIME_FILTER_DEN'
LOOPS_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=LOOPS_TYPE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=LOOPS_COMMANDED, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=TIME_REFERENCE, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_STATUS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_COMMANDS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_REF_COMMANDS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_FRAMERATE, format=FLOAT_FORMAT, unit=UNIT_HERTZ),
    AOTField(name=LOOPS_DELAY, format=FLOAT_FORMAT, unit=UNIT_FRAME),
    AOTField(name=LOOPS_TIME_FILTER_NUM, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_TIME_FILTER_DEN, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[LOOPS_TABLE] = LOOPS_FIELDS
LOOPS_TYPE_CONTROL = 'Control Loop'
LOOPS_TYPE_OFFLOAD = 'Offload Loop'
LOOPS_STATUS_OPEN = 'Open'
LOOPS_STATUS_CLOSED = 'Closed'

# AOT_LOOPS_CONTROL fields
LOOPS_CONTROL_INPUT_SENSOR = 'INPUT_SENSOR_UID'
LOOPS_CONTROL_CONTROL_MATRIX = 'CONTROL_MATRIX'
LOOPS_CONTROL_MEASUREMENTS_TO_MODES = 'MEASUREMENTS_TO_MODES'
LOOPS_CONTROL_MODES_TO_COMMANDS = 'MODES_TO_COMMANDS'
LOOPS_CONTROL_INTERACTION_MATRIX = 'INTERACTION_MATRIX'
LOOPS_CONTROL_COMMANDS_TO_MODES = 'COMMANDS_TO_MODES'
LOOPS_CONTROL_MODES_TO_MEASUREMENTS = 'MODES_TO_MEASUREMENTS'
LOOPS_CONTROL_RESIDUAL_COMMANDS = 'RESIDUAL_COMMANDS'
LOOPS_CONTROL_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=LOOPS_CONTROL_INPUT_SENSOR, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=LOOPS_CONTROL_CONTROL_MATRIX, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_MEASUREMENTS_TO_MODES, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_MODES_TO_COMMANDS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_INTERACTION_MATRIX, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_COMMANDS_TO_MODES, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_MODES_TO_MEASUREMENTS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS),
    AOTField(name=LOOPS_CONTROL_RESIDUAL_COMMANDS, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[LOOPS_CONTROL_TABLE] = LOOPS_CONTROL_FIELDS

# AOT_LOOPS_OFFLOAD fields
LOOPS_OFFLOAD_INPUT_CORRECTOR = 'INPUT_CORRECTOR_UID'
LOOPS_OFFLOAD_OFFLOAD_MATRIX = 'OFFLOAD_MATRIX'
LOOPS_OFFLOAD_FIELDS = AOTFieldDict(
    AOTField(name=REFERENCE_UID, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True, unique=True),
    AOTField(name=LOOPS_OFFLOAD_INPUT_CORRECTOR, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS, mandatory=True),
    AOTField(name=LOOPS_OFFLOAD_OFFLOAD_MATRIX, format=STRING_FORMAT, unit=UNIT_DIMENSIONLESS)
)
TABLE_FIELDS[LOOPS_OFFLOAD_TABLE] = LOOPS_OFFLOAD_FIELDS
