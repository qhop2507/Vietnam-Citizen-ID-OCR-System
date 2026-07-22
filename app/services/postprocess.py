import re
from typing import Dict


class PostProcessor:
    """
    Chuẩn hóa kết quả OCR của CCCD.
    """

    @staticmethod
    def normalize_space(text: str) -> str:
        if not text:
            return ""

        text = str(text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def normalize_date(text: str) -> str:
        """
        Chuẩn hóa:
            1-1-2000
            1.1.2000
            1/1/2000

        thành:

            01/01/2000
        """

        if not text:
            return ""

        text = PostProcessor.normalize_space(text)

        text = text.replace("-", "/")
        text = text.replace(".", "/")

        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)

        if not m:
            return text

        day, month, year = m.groups()

        return f"{int(day):02d}/{int(month):02d}/{year}"

    @staticmethod
    def normalize_id(text: str) -> str:
        """
        Chuẩn hóa số CCCD.
        """

        if not text:
            return ""

        text = text.upper()

        replace_map = {
            "O": "0",
            "Q": "0",
            "D": "0",
            "I": "1",
            "L": "1",
            "|": "1",
            "S": "5",
            "B": "8",
            "Z": "2"
        }

        for old, new in replace_map.items():
            text = text.replace(old, new)

        digits = re.findall(r"\d", text)

        return "".join(digits)[:12]

    @staticmethod
    def normalize_gender(text: str) -> str:

        if not text:
            return ""

        text = PostProcessor.normalize_space(text).upper()

        if re.search(r"\bNAM\b", text):
            return "Nam"

        if re.search(r"\b(NỮ|NU)\b", text):
            return "Nữ"

        return text.title()

    @staticmethod
    def normalize_nationality(text: str) -> str:

        if not text:
            return ""

        text = PostProcessor.normalize_space(text).upper()

        if any(x in text for x in [
            "VIỆT",
            "VIET",
            "VIETNAM",
            "VIỆT NAM",
            "VN"
        ]):
            return "Việt Nam"

        return text.title()

    @staticmethod
    def normalize_name(text: str) -> str:

        if not text:
            return ""

        text = PostProcessor.normalize_space(text)

        return text.upper()

    @staticmethod
    def normalize_address(text: str) -> str:

        if not text:
            return ""

        text = PostProcessor.normalize_space(text)

        text = re.sub(r"\s*,\s*", ", ", text)

        return text

    def process(self, result: Dict) -> Dict:
        """
        Chuẩn hóa toàn bộ kết quả OCR.
        """

        output = dict(result)

        output["id"] = self.normalize_id(
            output.get("id", "")
        )

        output["name"] = self.normalize_name(
            output.get("name", "")
        )

        output["dob"] = self.normalize_date(
            output.get("dob", "")
        )

        output["issue_date"] = self.normalize_date(
            output.get("issue_date", "")
        )

        output["expire_date"] = self.normalize_date(
            output.get("expire_date", "")
        )

        output["gender"] = self.normalize_gender(
            output.get("gender", "")
        )

        output["nationality"] = self.normalize_nationality(
            output.get("nationality", "")
        )

        output["origin_place"] = self.normalize_address(
            output.get("origin_place", "")
        )

        output["current_place"] = self.normalize_address(
            output.get("current_place", "")
        )

        return output