from p2k2_converter.p2k2 import JobBuilder, BarBuilder, CutBuilder
import argparse
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.serializers import XmlSerializer

parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-t", "--type", type=str, help="The sheet type")
parser.add_argument("-o", "--output", type=str, help="The output file name.")

args = parser.parse_args()


bars = []
# Operations for "profilo doga"
number_of_pieces = 10
length = 741
trim_length = 34    # mm

normal_cut = CutBuilder()\
            .add_left_cutting_angle(90)\
            .add_right_cutting_angle(90)\
            .add_cut_length(length)


length_of_bar = 6000
total_length = 0
current_bar = BarBuilder("PELLEGRINO", "CLOSE", "PROFILO SOGLIA")\
                .add_length(length_of_bar)\
                .add_height(100)

for i in range(number_of_pieces):
    total_length += length
    if total_length > length_of_bar:
        bars.append(current_bar.build())
        current_bar = BarBuilder("PELLEGRINO", "CLOSE", "PROFILO SOGLIA").add_length(length_of_bar) \
                .add_height(100)

        total_length = 0
        current_bar.add_cut(CutBuilder().add_left_cutting_angle(90).add_right_cutting_angle(90).add_cut_length(length).build())

    else:
        if i == number_of_pieces - 1:
            # Define the offset of the holes based on the length of the piece
            cut = CutBuilder()\
                    .add_left_cutting_angle(90) \
                    .add_right_cutting_angle(90) \
                    .add_cut_length(length - trim_length)\
                    .add_machining("FORO ANTA", 20) \
                    .add_machining("FORO ANTA", 53) \
                    .build()
            current_bar.add_cut(cut)
            bars.append(current_bar.build())
        else:
            if i == 0:
                # Define the offset of the holes based on the length of the piece
                cut = CutBuilder()\
                        .add_left_cutting_angle(90) \
                        .add_right_cutting_angle(90) \
                        .add_cut_length(length) \
                        .add_machining("FORO ANTA", 20) \
                        .add_machining("FORO ANTA", 53) \
                        .build()
                current_bar.add_cut(cut)

            elif i == number_of_pieces / 2:
                cut = CutBuilder()\
                        .add_left_cutting_angle(90) \
                        .add_right_cutting_angle(90) \
                        .add_cut_length(length) \
                        .add_machining("FORO ANTA", 20) \
                        .add_machining("FORO ANTA", 53) \
                        .build()
                current_bar.add_cut(cut)
            else:
                current_bar.add_cut(normal_cut.build())

# Operations for "Canalino verticale"
number_of_pieces = 2
length = 1970           # mm
angle_left = 45         # degrees
angle_right = 45        # degrees
length_of_bar = 6000    # mm

cut = CutBuilder()\
        .add_left_cutting_angle(angle_left)\
        .add_right_cutting_angle(angle_right)\
        .add_cut_length(length)\
        .build()

bar = BarBuilder("PELLEGRINO", "CLOSE", "CANALINO VERTICALE")\
        .add_length(length_of_bar)\
        .add_height(100)\

for i in range(number_of_pieces):
    bar.add_cut(cut)

bars.append(bar.build())

# Operations for "Canalino orizzontale"
number_of_pieces = 2
length = 760            # mm
angle_left = 45         # degrees
angle_right = 45        # degrees
length_of_bar = 6000    # mm

bar = BarBuilder("PELLEGRINO", "CLOSE", "ORIZZONTALE")\
        .add_length(length_of_bar)\
        .add_height(100)

cut = CutBuilder()\
        .add_left_cutting_angle(angle_left)\
        .add_right_cutting_angle(angle_right)\
        .add_cut_length(length)\
        .build()

for i in range(number_of_pieces):
    bar.add_cut(cut)

bars.append(bar.build())

# Operations for "Profilo telaio ad elle"
# 1. Montante Sx

bar = BarBuilder("PELLEGRINO", "CLOSE", "MONTANTE SX")\
        .add_length(length_of_bar)\
        .add_height(100)

cut = CutBuilder()\
        .add_left_cutting_angle(90)\
        .add_right_cutting_angle(45)\
        .add_cut_length(2000)\
        .build()

bar.add_cut(cut)
bars.append(bar.build())

# 2. Montante Dx
bar = BarBuilder("PELLEGRINO", "CLOSE", "TRAVERSO SUP")\
        .add_length(length_of_bar)\
        .add_height(100)

cut = CutBuilder()\
        .add_left_cutting_angle(45)\
        .add_right_cutting_angle(90)\
        .add_cut_length(804)\
        .build()

bar.add_cut(cut)
bars.append(bar.build())

# 3. Montante Dx
bar = BarBuilder("PELLEGRINO", "CLOSE", "MONTANTE DX")\
        .add_length(length_of_bar)\
        .add_height(100)

cut = CutBuilder()\
        .add_left_cutting_angle(45)\
        .add_right_cutting_angle(45)\
        .add_cut_length(2000)\
        .build()

bar.add_cut(cut)
bars.append(bar.build())

# Operations for "Profilo soglia"
bar = BarBuilder("PELLEGRINO", "CLOSE", "PROFILO SOGLIA")\
        .add_length(length_of_bar)\
        .add_height(100)

cut = CutBuilder()\
        .add_left_cutting_angle(90)\
        .add_right_cutting_angle(90)\
        .add_cut_length(804)\
        .build()

bar.add_cut(cut)
bars.append(bar.build())


config = SerializerConfig(pretty_print=True)
serializer = XmlSerializer(config=config)


job = JobBuilder()
for bar in bars:
    job.add_bar(bar)

output = job.build()
print(serializer.render(output))



# this is the main module of your app
# it is only required if your project must be runnable
# this is the script to be executed whenever some users writes `python -m p2k2_converter` on the command line, eg.
#x = p2k2_converter.MyClass().my_method()
#print(x)
