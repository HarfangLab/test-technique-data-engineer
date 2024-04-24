"""
Mimics an extraction process by generating a list of random elements that can
populate our Tables
"""
from datetime import datetime

from tqdm import tqdm

from malware_families import MALWARE_FAMILIES
from database.fake import get_faker, TAGS
from database.models.analysis import Analysis
from database.models.analyzer import Analyzer
from database.models.sample import Sample
from database.models.tag import Tag, TagType
from database.models.malware_family import MalwareFamily


class ExtractData:
    samples_list = []
    analyzers_list = []
    analysis_list = []
    tags_list = []
    tag_types = []
    malware_families = []

    def __init__(self):
        self.faker = get_faker()

    def list_samples(self, nb_rows=20) -> list[Sample]:
        if self.samples_list:
            return self.samples_list

        for _ in tqdm(range(nb_rows), desc="Creating samples", leave=False):
            sha256 = self.faker.sha256()
            mime, magic = self.faker.file_type()

            sample = Sample(
                id=self.faker.uuid4(),
                hash=sha256,
                filename=sha256,
                mime=mime,
                magic=magic,
            )

            self.samples_list.append(sample)

        return self.samples_list

    def list_analyzers(self, nb_rows=20) -> list[Analyzer]:
        if self.analyzers_list:
            return self.analyzers_list

        for _ in tqdm(range(nb_rows), desc="Creating analyzers", leave=False):
            analyzer = Analyzer(
                id=self.faker.uuid4(),
                name=self.faker.analyzer(),
                analyzer_date=self.faker.date_between(
                    datetime(2017, 1, 1), datetime(2024, 2, 2)
                ),
            )

            self.analyzers_list.append(analyzer)

        return self.analyzers_list

    def list_analysis(self, nb_rows=20) -> list[Analysis]:
        if self.analysis_list:
            return self.analysis_list

        samples_list = self.list_samples()
        analyzers_list = self.list_analyzers()

        for _ in tqdm(range(nb_rows * 2), desc="Creating analysis", leave=False):
            analyzer = self.faker.random_element(analyzers_list)
            analysis = Analysis(
                id=self.faker.uuid4(),
                sample=self.faker.random_element(samples_list),
                analyzer=analyzer,
                analysis_date=self.faker.date_between(
                    analyzer.analyzer_date, datetime(2024, 3, 3)
                ),
                is_malware=self.faker.random.randint(1, 100) > 80,
            )

            self.analysis_list.append(analysis)

        return self.analysis_list

    def list_tags(self, nb_rows=20) -> list[Tag]:
        if self.tags_list:
            return self.tags_list

        samples_list = self.list_samples()
        tag_types_list = self.list_tag_types()

        for _ in tqdm(range(nb_rows), desc="Creating tags", leave=False):
            tag_type = self.faker.random_element(tag_types_list)
            value = self.faker.tag(tag_type)

            tag = Tag(
                id=self.faker.uuid4(),
                value=value,
                tag_type=tag_type,
                sample=self.faker.random_element(samples_list),
            )

            self.tags_list.append(tag)

        return self.tags_list

    def list_tag_types(self) -> list[TagType]:
        if self.tag_types:
            return self.tag_types

        self.tag_types = [TagType(id=self.faker.uuid4(), name=t) for t in TAGS]

        return self.tag_types

    def list_malware_families(self) -> list[MalwareFamily]:
        if self.malware_families:
            return self.malware_families

        self.malware_families = [
            MalwareFamily(id=self.faker.uuid4(), name=f[1], alias=f[2])
            for f in MALWARE_FAMILIES
        ]

        return self.malware_families
