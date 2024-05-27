import logging

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from p2k2_converter.core import Parser
from p2k2_converter.p2k2.translation import p2k2_translation
from xsdata.formats.dataclass.serializers import XmlSerializer


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('p2k2_converter')


def xlsm_to_p2k2(file_to_convert, config_path, output_path):
    file_parser = Parser(workbook_path=file_to_convert, config_file=config_path)
    order = file_parser.parse()

    job = p2k2_translation(*order)

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)

    with open(output_path, "w") as file:
        file.write(serializer.render(job))

    logger.info(f"Conversion completed. The output file is saved at {output_path}")


# let this be the last line of this file
logger.info("p2k2_converter loaded")
