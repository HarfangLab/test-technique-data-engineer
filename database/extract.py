"""
Mimics an extraction process by generating a list of random elements that can
populate our Tables
"""
from datetime import datetime
from functools import cache

from tqdm import tqdm

from malware_families import MALWARE_FAMILIES
from database.fake import get_faker, TAGS
from database.models.analysis import Analysis
from database.models.analyzer import Analyzer
from database.models.sample import Sample
from database.models.tag import Tag, TagType
from database.models.malware_family import MalwareFamily


class ExtractData:
    def __init__(self):
        self.faker = get_faker()

    @cache
    def list_samples(self, nb_rows=20) -> list[Sample]:
        samples_list = []

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

            samples_list.append(sample)

        return samples_list

    @cache
    def list_analyzers(self, nb_rows=20) -> list[Analyzer]:
        analyzers_list = []

        for _ in tqdm(range(nb_rows), desc="Creating analyzers", leave=False):
            analyzer = Analyzer(
                id=self.faker.uuid4(),
                name=self.faker.analyzer(),
                analyzer_date=self.faker.date_between(datetime(2017,1, 1), datetime(2024, 2, 2))
            )

            analyzers_list.append(analyzer)

        return analyzers_list

    @cache
    def list_analysis(self, nb_rows=20) -> list[Analysis]:
        analysis_list = []
        samples_list = self.list_samples()
        analyzers_list = self.list_analyzers()

        for _ in tqdm(range(nb_rows * 2), desc="Creating analysis", leave=False):
            analyzer = self.faker.random_element(analyzers_list)
            analysis = Analysis(
                id=self.faker.uuid4(),
                sample=self.faker.random_element(samples_list),
                analyzer=analyzer,
                analysis_date=self.faker.date_between(analyzer.analyzer_date, datetime(2024, 3, 3)),
                is_malware=self.faker.random.randint(1, 100) > 80,
            )

            analysis_list.append(analysis)

        return analysis_list

    @cache
    def list_tags(self, nb_rows=20) -> list[Tag]:
        tags_list = []
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

            tags_list.append(tag)

        return tags_list

    @cache
    def list_tag_types(self) -> list[TagType]:
        return [TagType(id=self.faker.uuid4(), name=t) for t in TAGS]


    @cache
    def list_malware_families(self) -> list[MalwareFamily]:
        return [MalwareFamily(id=self.faker.uuid4(), name=f[1], alias=f[2]) for f in MALWARE_FAMILIES]
