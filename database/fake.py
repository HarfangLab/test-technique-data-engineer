"""
A set of constants and classes used to generate synthetic data
"""
import os
import random
import string

from database.models.tag import TagType
from faker import Faker
from faker.providers import BaseProvider
from malware_families import MALWARE_FAMILIES

SEED = os.getenv("DB_SEED", 0)


def generate_random_string(length: int = None, min_length: int = 0) -> str:
    if length is None:
        length = random.randint(min_length, 25)
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


FILE_TYPES = [
    (
        "application/x-dosexec",
        "PE32+ executable (GUI) x86-64, for MS Windows",
    ),
    (
        "application/x-dosexec",
        "PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows",
    ),
    (
        "application/x-dosexec",
        "PE32 executable (GUI) Intel 80386 (stripped to external PDB), for MS Windows",
    ),
    (
        "application/x-executable",
        "ELF 32-bit MSB executable, PowerPC or cisco 4500, version 1 (SYSV)",
    ),
    (
        "application/x-sharedlib",
        "ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)",
    ),
    (
        "application/x-mach-binary",
        "Mach-O universal binary with 2 architectures: [x86_64:Mach-O 64-bit x86_64 executable, flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>] [arm64:Mach-O 64-bit arm64 executable, flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>]",
    ),
]

FAMILY_ALIASES = [f[2] for f in MALWARE_FAMILIES]

TAGS = {
    "FAMILY": FAMILY_ALIASES,
    "FAMILY_FROM_SCRAPER": FAMILY_ALIASES,
    "FAMILY_FROM_ANALYSIS": FAMILY_ALIASES,
    "UNKNOWN": ["unknown"],
    "HAS_BEEN_DETECTED_IN_PROD": [True, False]
}

ANALYZERS = ["AUTO_A", "AUTO_B", "NON_RELIABLE_ANALYZER_A", "NON_RELIABLE_ANALYZER_B", "AUTO_C", "AUTO_D", "AUTO_E", "AUTO_F"]


class AnalyzerFaker(BaseProvider):
    def analyzer(self) -> str:
        return random.choice(ANALYZERS)


class SampleFaker(BaseProvider):
    def file_type(self) -> tuple[str, str]:
        is_random_str = random.choice([True, False])
        if is_random_str:
            return generate_random_string(min_length=5), generate_random_string(min_length=5)
        return random.choice(FILE_TYPES)


class TagFaker(BaseProvider):
    def tag(self, tag_type: TagType) -> tuple[str, str]:
        tag_value = random.choice(TAGS[tag_type.name])
        if isinstance(tag_value, str):
            return generate_random_string() + tag_value + generate_random_string()
        return tag_value

def get_faker() -> Faker:
    random.seed(SEED)
    Faker.seed(SEED)

    faker = Faker()

    faker.add_provider(TagFaker)
    faker.add_provider(SampleFaker)
    faker.add_provider(AnalyzerFaker)

    return faker
