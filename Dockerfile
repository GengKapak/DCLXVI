# Cz we are Arch User
FROM gengkapak/archlinux:latest
USER gengkapak

#
# Clone repo and prepare working directory
#
RUN git clone -b master https://github.com/GengKapak/DCLXVI /home/gengkapak/dclxvi/
RUN mkdir /home/gengkapak/dclxvi/bin/
WORKDIR /home/gengkapak/dclxvi/

CMD ["python3","-m","userbot"]
