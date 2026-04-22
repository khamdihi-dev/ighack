import random

class InstagramClient:
    def __init__(self):
        with open('asset/igversi.txt', 'r') as f:
            self.ig_versi = [line.strip() for line in f if line.strip()]

        self.ig_app_versi, self.ig_app_versi_code = random.choice(self.ig_versi).split(':')

    def NewUserAgentApps(self):
        DEVICE_PROFILES = [
            {
                "manufacturer": "samsung", "brand": "samsung",
                "model": "SM-G991B", "device": "o1s",
                "chipset": "exynos2100", "resolution": "1080x2400", "dpi": "480",
                "android_versions": [("11", "30"), ("12", "31"), ("13", "33")],
            },
            {
                "manufacturer": "samsung", "brand": "samsung",
                "model": "SM-S918B", "device": "dm3q",
                "chipset": "snapdragon8gen2", "resolution": "1080x2340", "dpi": "480",
                "android_versions": [("13", "33"), ("14", "34")],
            },
            {
                "manufacturer": "Google", "brand": "google",
                "model": "Pixel 6", "device": "oriole",
                "chipset": "tensor", "resolution": "1080x2400", "dpi": "411",
                "android_versions": [("12", "31"), ("13", "33"), ("14", "34")],
            },
            {
                "manufacturer": "Google", "brand": "google",
                "model": "Pixel 7", "device": "panther",
                "chipset": "tensor_g2", "resolution": "1080x2400", "dpi": "416",
                "android_versions": [("13", "33"), ("14", "34")],
            },
            {
                "manufacturer": "OnePlus", "brand": "OnePlus",
                "model": "IN2020", "device": "OnePlus8",
                "chipset": "snapdragon865", "resolution": "1080x2400", "dpi": "400",
                "android_versions": [("11", "30"), ("12", "31")],
            },
            {
                "manufacturer": "OnePlus", "brand": "OnePlus",
                "model": "CPH2411", "device": "OnePlus10Pro",
                "chipset": "snapdragon8gen1", "resolution": "1440x3216", "dpi": "525",
                "android_versions": [("12", "31"), ("13", "33")],
            },
            {
                "manufacturer": "Xiaomi", "brand": "Redmi",
                "model": "M2101K7AG", "device": "sunny",
                "chipset": "snapdragon678", "resolution": "1080x2400", "dpi": "395",
                "android_versions": [("11", "30"), ("12", "31")],
            },
            {
                "manufacturer": "Xiaomi", "brand": "Xiaomi",
                "model": "2201123G", "device": "zeus",
                "chipset": "snapdragon8gen1", "resolution": "1440x3200", "dpi": "521",
                "android_versions": [("12", "31"), ("13", "33")],
            },
            {
                "manufacturer": "motorola", "brand": "motorola",
                "model": "moto g(30)", "device": "caprip",
                "chipset": "snapdragon662", "resolution": "720x1600", "dpi": "269",
                "android_versions": [("11", "30"), ("12", "31")],
            },
            {
                "manufacturer": "OPPO", "brand": "OPPO",
                "model": "CPH2173", "device": "OP4F7F",
                "chipset": "snapdragon870", "resolution": "1080x2400", "dpi": "460",
                "android_versions": [("11", "30"), ("12", "31")],
            },
            {
                "manufacturer": "Sony", "brand": "Sony",
                "model": "XQ-AS52", "device": "pdx203",
                "chipset": "snapdragon865", "resolution": "1080x2520", "dpi": "449",
                "android_versions": [("11", "30"), ("12", "31")],
            },
            {
                "manufacturer": "realme", "brand": "realme",
                "model": "RMX3085", "device": "RMX3085",
                "chipset": "snapdragon888", "resolution": "1080x2400", "dpi": "400",
                "android_versions": [("11", "30"), ("12", "31")],
            },
        ]

        LOCALES = ["en_US"]

        device = random.choice(DEVICE_PROFILES)
        android_ver, api_level = random.choice(device["android_versions"])
        locale = random.choice(LOCALES)

        dpi_final = int(device["dpi"]) + random.randint(-4, 4)

        user_agent = (
            f"Instagram {self.ig_app_versi} "
            f"Android ({api_level}/{android_ver}; "
            f"{dpi_final}dpi; "
            f"{device['resolution']}; "
            f"{device['manufacturer']}; "
            f"{device['model']}; "
            f"{device['device']}; "
            f"{device['chipset']}; "
            f"{locale}; "
            f"{self.ig_app_versi_code})"
        )

        return user_agent


