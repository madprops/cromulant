import time


class Utils:
    @staticmethod
    def now() -> float:
        return int(time.time())

    @staticmethod
    def singular_or_plural(num: float, singular: str, plural: str) -> str:
        if num == 1:
            return singular

        return plural

    @staticmethod
    def time_ago(start_time: float, end_time: float) -> str:
        diff = end_time - start_time
        seconds = int(diff)

        if seconds < 60:
            word = Utils.singular_or_plural(seconds, "second", "seconds")
            return f"{seconds} {word} ago"

        minutes = seconds // 60

        if minutes < 60:
            word = Utils.singular_or_plural(minutes, "minute", "minutes")
            return f"{minutes} {word} ago"

        hours = minutes / 60

        if hours < 24:
            word = Utils.singular_or_plural(hours, "hour", "hours")
            return f"{hours:.1f} {word} ago"

        days = hours / 24

        if days < 30:
            word = Utils.singular_or_plural(days, "day", "days")
            return f"{days:.1f} {word} ago"

        months = days / 30

        if months < 12:
            word = Utils.singular_or_plural(months, "month", "months")
            return f"{months:.1f} {word} ago"

        years = months / 12
        word = Utils.singular_or_plural(years, "year", "years")
        return f"{years:.1f} {word} ago"

    @staticmethod
    def print(text: str) -> None:
        print(text)  # noqa: T201
