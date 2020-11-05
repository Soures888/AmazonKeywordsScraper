from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, \
    SoftwareType, HardwareType

# Settings
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.ANDROID.value]
hardware_type = [HardwareType.MOBILE__PHONE.value]
software_types = [SoftwareType.WEB_BROWSER.value]


def generate_random_useragent() -> str:
    """Generate random mobile user agent"""

    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   hardware_type=hardware_type,
                                   software_types=software_types)

    return user_agent_rotator.get_random_user_agent()

