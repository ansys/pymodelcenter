"""Integration tests around Engine functionality."""
import os
from typing import Collection, Mapping

import ansys.engineeringworkflow.api as ewapi

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


def test_can_create_a_new_workflow(engine) -> None:
    # Arrange
    workflow_name = "new_workflow_test.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), workflow_name)
    if os.path.isfile(workflow_path):
        os.remove(workflow_path)  # delete the file if it already exists

    # Act
    with engine.new_workflow(name=workflow_path, workflow_type=mcapi.WorkflowType.DATA) as workflow:
        # Assert
        assert workflow.workflow_file_name == workflow_name
        assert os.path.isfile(workflow_name)


def test_can_load_a_workflow(engine) -> None:
    # Arrange
    workflow_name = "all_types.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), "test_files", workflow_name)

    # Act
    with engine.load_workflow(file_name=workflow_path) as workflow:
        # Assert
        assert workflow.workflow_file_name == workflow_name


def test_can_read_engine_preferences(engine) -> None:
    # Act
    preference: str = engine.get_preference(pref="Default New Model Type")

    # Assert
    assert preference == "Prompt user"


def test_can_set_engine_preferences(engine) -> None:
    # Arrange
    preference: str = "Script Component Editor H"
    initial_value: int = int(engine.get_preference(preference))
    new_value: int = initial_value * 2

    try:
        # Act
        engine.set_preference(pref=preference, value=new_value)

        # Assert
        assert int(engine.get_preference(pref=preference)) == new_value

    finally:
        # Restore the initial preference
        engine.set_preference(pref=preference, value=initial_value)


def test_can_get_list_of_supported_units(engine) -> None:
    # Act
    units: Mapping[str, Collection[str]] = engine.get_units()

    # Assert
    assert units == expected_units


def test_can_get_engine_info(engine) -> None:
    # Act
    info: ewapi.WorkflowEngineInfo = engine.get_server_info()

    # Assert
    assert info.release_year == 23
    assert info.release_id == 2
    assert info.build == 0
    assert info.version_as_string == "23.2.0"

    assert info.build_type == ""
    assert info.server_type == ""
    assert info.base_url is None

    # TODO: See if we can have these be the right values for local and nightly builds
    # assert info.is_release_build == False
    # assert info.install_location == "C:\\SVN\\SourceCode\\ModelCenter\\install"


def test_can_start_multiple_engines() -> None:
    # Arrange/Act
    with grpcmc.Engine() as engine1, grpcmc.Engine() as engine2, grpcmc.Engine() as engine3:
        # Assert
        assert engine1.process_id != engine2.process_id
        assert engine1.process_id != engine3.process_id
        assert engine2.process_id != engine3.process_id


expected_units = {
    "Quantity": ["%", "mol", "‰", "‱"],
    "Catalytic Activity": ["kat"],
    "Currency": ["USD", "GBP", "EUR", "JPY", "RMB"],
    "Data": [
        "b",
        "kb",
        "Mb",
        "Gb",
        "Tb",
        "Pb",
        "Kib",
        "Mib",
        "Gib",
        "Tib",
        "Pib",
        "B",
        "kB",
        "MB",
        "GB",
        "TB",
        "PB",
        "KiB",
        "MiB",
        "GiB",
        "TiB",
        "PiB",
    ],
    "Data Rate/Throughput": [
        "bps",
        "kb/s",
        "Mb/s",
        "Gb/s",
        "Tb/s",
        "Kib/s",
        "Mib/s",
        "Gib/s",
        "Tib/s",
        "Bps",
        "kB/s",
        "MB/s",
        "GB/s",
        "TB/s",
        "KiB/s",
        "MiB/s",
        "GiB/s",
        "TiB/s",
    ],
    "Page Rate": ["SPM"],
    "Tempo": ["BPM"],
    "Resolution": ["DPI"],
    "Uptime/Downtime": [
        "minutes per year",
        "hours per year",
        "days per year",
        "seconds per month",
        "minutes per month",
        "hours per month",
        "days per month",
    ],
    "Angle": ["mdeg", "°", "µrad", "mrad", "rad"],
    "Solid Angle": ["nsr", "µsr", "msr", "sr"],
    "Temperature": ["K", "°C", "°R", "°F"],
    "Length/Distance": [
        "Å",
        "nm",
        "µm",
        "mm",
        "cm",
        "m",
        "km",
        "au",
        "ly",
        "pc",
        "kpc",
        "Mpc",
        "Gpc",
        "in",
        "ft",
        "kft",
        "yd",
        "mi",
        "inm",
        "U",
    ],
    "Area": ["mm²", "cm²", "m²", "km²", "in²", "ft²", "mi²", "ha", "acre"],
    "Volume": ["mm³", "cm³", "m³", "µL", "mL", "L", "in³", "ft³", "yd³", "fl oz", "gal"],
    "Reciprocal Length": ["m⁻¹", "cm⁻¹"],
    "Time": ["ns", "µs", "ms", "s", "min", "h", "d", "mo", "a", "Ma", "Ga"],
    "Frequency": ["Hz", "kHz", "MHz", "GHz", "THz", "rad/s", "RPM"],
    "Velocity": ["m/s", "mm/s", "cm/s", "km/h", "km/s", "mph", "in/s", "ft/s", "kn"],
    "Acceleration": ["m/s²", "ft/s²", "g-force"],
    "Mass": ["µg", "mg", "g", "kg", "u", "oz", "t oz", "lbm", "slug", "ton", "tonne"],
    "Mass Flowrate": [
        "µg/s",
        "mg/s",
        "g/s",
        "kg/s",
        "u/s",
        "oz/s",
        "t oz/s",
        "lbm/s",
        "slug/s",
        "ton/s",
        "tonne/s",
    ],
    "Force/Weight": ["mN", "cN", "N", "kN", "kgf", "lbf", "kip", "ton-force", "tonne-force", "dyn"],
    "Pound": ["lb"],
    "Torque": ["N·m", "lbf·ft"],
    "Pressure": ["Pa", "kPa", "MPa", "GPa", "atm", "bar", "mbar", "torr", "inHg", "psi"],
    "Density": ["kg/m³", "kg/L", "g/mL", "g/cm³", "lb/ft³", "oz/in³"],
    "Specific Volume": ["m³/kg"],
    "Concentration": ["m⁻³", "L⁻¹", "mol/m³", "mol/L"],
    "Energy": [
        "μJ",
        "mJ",
        "J",
        "kJ",
        "MJ",
        "GJ",
        "cal",
        "kcal",
        "Ws",
        "Wh",
        "kWh",
        "MWh",
        "GWh",
        "eV",
        "keV",
        "MeV",
        "GeV",
        "TeV",
        "Btu",
        "thm",
        "ft·lbf",
    ],
    "Power": [
        "aW",
        "fW",
        "pW",
        "nW",
        "µW",
        "mW",
        "W",
        "kW",
        "MW",
        "GW",
        "TW",
        "erg",
        "hp",
        "ft·lbf/min",
        "ft·lbf/s",
        "Btu/s",
    ],
    "Current": ["µA", "mA", "A"],
    "Charge": ["pC", "nC", "µC", "mC", "C"],
    "Capacitance": ["pF", "nF", "µF", "mF", "F"],
    "Inductance": ["H"],
    "Electric Potential": ["pV", "nV", "µV", "mV", "V", "kV", "MV"],
    "Resistance": ["µΩ", "mΩ", "Ω", "kΩ", "MΩ", "GΩ"],
    "Conductance": ["S"],
    "Current Density": ["A/m²"],
    "Magnetic Flux Density": ["nT", "T", "mG", "G"],
    "Magnetic Flux": ["nWb", "µWb", "mWb", "Wb"],
    "Magnetic Field Strength": ["Oe", "A/m"],
    "Radioactive Activity": ["Bq", "kBq", "MBq", "GBq", "TBq", "PBq", "EBq", "Ci", "mCi", "µCi"],
    "Absorbed Radiation Dose": ["Gy", "mGy", "µGy", "µrads", "mrads", "rads"],
    "Effective Radiation Dose": ["Sv", "rem", "mSv", "mrem", "µSv"],
    "Luminous Flux": ["lm"],
    "Luminous Intensity": ["cd"],
    "Luminance": ["cd/m²"],
    "Illuminance": ["lx"],
}
