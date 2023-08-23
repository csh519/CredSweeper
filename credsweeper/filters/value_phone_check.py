from credsweeper.config import Config
from credsweeper.credentials import LineData
from credsweeper.file_handler.analysis_target import AnalysisTarget
from credsweeper.filters import Filter


class ValuePhoneCheck(Filter):
    """Check that value may be a phone number"""

    PREFIX_LENGTH = {
        "1": 10,
        "20": 10,
        "211": 7,
        "212": 9,
        "213": 9,
        "216": 8,
        "218": 10,
        "220": 7,
        "221": 9,
        "222": 8,
        "223": 8,
        "224": 9,
        "225": 8,
        "226": 8,
        "227": 8,
        "228": 8,
        "229": 8,
        "230": 8,
        "231": (8, 9),
        "232": 8,
        "233": 9,
        "234": 8,
        "235": 6,
        "236": 8,
        "237": 9,
        "238": 7,
        "239": 7,
        "240": 9,
        "241": 7,
        "242": 9,
        "243": 7,
        "244": 9,
        "245": 9,
        "246": 7,
        "248": 7,
        "249": 7,
        "250": 9,
        "251": 9,
        "252": (8, 9),
        "253": 10,
        "254": 10,
        "255": 7,
        "256": 7,
        "257": 8,
        "258": 12,
        "260": 9,
        "261": 7,
        "262": (9, 10),
        "263": 9,
        "264": 7,
        "265": [7, 9],
        "266": 8,
        "267": 7,
        "268": 8,
        "269": 7,
        "27": 9,
        "290": 4,
        "291": 7,
        "297": 7,
        "298": 5,
        "299": 6,
        "30": 10,
        "31": 9,
        "32": 9,
        "33": 9,
        "34": 9,
        "350": 8,
        "351": 9,
        "352": 9,
        "353": 9,
        "354": 7,
        "355": 9,
        "356": 8,
        "357": 8,
        "358": (8, 11),
        "359": 9,
        "36": 9,
        "370": 8,
        "371": 8,
        "372": 8,
        "373": 8,
        "374": 6,
        "375": 9,
        "376": 6,
        "377": 8,
        "378": 10,
        "379": 10,
        "380": 9,
        "381": 9,
        "382": 8,
        "383": 8,
        "385": 9,
        "386": 9,
        "387": 8,
        "389": 8,
        "39": 10,
        "40": 10,
        "41": 9,
        "420": 9,
        "421": 9,
        "423": 7,
        "43": (10, 11),
        "44": 10,
        "45": 8,
        "46": 7,
        "47": (8, 10),
        "48": 9,
        "49": 10,
        "500": 5,
        "501": 7,
        "502": 8,
        "503": 8,
        "504": 8,
        "505": 8,
        "506": 8,
        "507": 8,
        "508": 6,
        "509": 8,
        "51": 9,
        "52": 10,
        "53": 8,
        "54": 10,
        "55": 11,
        "56": 9,
        "57": 10,
        "58": 7,
        "590": [9, 12],
        "591": 9,
        "592": 7,
        "593": 9,
        "594": 9,
        "595": 9,
        "596": 9,
        "597": (6, 7),
        "598": 8,
        "599": 7,
        "60": 7,
        "61": (9, 10),
        "62": 11,
        "63": 10,
        "64": (8, 9),
        "65": 8,
        "66": 9,
        "670": 7,
        "672": [6, 9],
        "673": 7,
        "674": 7,
        "675": 8,
        "676": 5,
        "677": 7,
        "678": 5,
        "679": 7,
        "680": 7,
        "681": 6,
        "682": 5,
        "683": 4,
        "685": 5,
        "686": 8,
        "687": 6,
        "688": 5,
        "689": 8,
        "690": 5,
        "691": 7,
        "692": 7,
        "7": 10,
        "81": 10,
        "82": (9, 10),
        "84": 9,
        "850": (3, 10),
        "852": 8,
        "853": 8,
        "855": 9,
        "856": (8, 9),
        "86": 11,
        "870": 9,
        "880": 10,
        "886": 9,
        "90": 11,
        "91": 10,
        "92": 10,
        "93": 9,
        "94": 7,
        "95": (7, 10),
        "960": 7,
        "961": (7, 8),
        "962": (8, 9),
        "963": 7,
        "964": 10,
        "965": 8,
        "966": 9,
        "967": 9,
        "968": 8,
        "970": 9,
        "971": 9,
        "972": 9,
        "973": 8,
        "974": 8,
        "975": 7,
        "976": 8,
        "977": 10,
        "98": 11,
        "992": 9,
        "993": 8,
        "994": 9,
        "995": 9,
        "996": 9,
        "998": 9,
    }

    def __init__(self, config: Config = None) -> None:
        self.prefix_limit = 1 + max(len(x) for x in self.PREFIX_LENGTH.keys())
        pass

    def run(self, line_data: LineData, target: AnalysisTarget) -> bool:
        """Run filter checks on received credential candidate data 'line_data'.

        Args:
            line_data: credential candidate data
            target: multiline target from which line data was obtained

        Return:
            False, if the sequence is not card number. True if it is

        """
        if line_data.value is None:
            return True

        # https://en.wikipedia.org/wiki/List_of_country_calling_codes
        # https://en.wikipedia.org/wiki/List_of_mobile_telephone_prefixes_by_country

        # until rule regex requires '+' at start
        value = line_data.value[1:]
        value_len = len(value)

        for prefix_size in range(1, self.prefix_limit):
            key = value[:prefix_size]
            if key in self.PREFIX_LENGTH:
                phone_length = value_len - prefix_size
                length = self.PREFIX_LENGTH[key]
                if isinstance(length, int) and phone_length == length:
                    break
                elif isinstance(length, list) and phone_length in length:
                    break
                elif isinstance(length, tuple) and length[0] <= phone_length <= length[1]:
                    break
        else:
            return True
        return False
