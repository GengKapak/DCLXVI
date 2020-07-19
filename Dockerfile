# We're using Debian slim buster
FROM dasbastard/slim-buster:dclxvi

#
# Clone repo and prepare working directory
#
RUN git clone -b master https://github.com/GengKapak/DCLXVI /home/dclxvi/
RUN mkdir /home/dclxvi/bin/
WORKDIR /home/dclxvi/

CMD ["python3","-m","userbot"]
