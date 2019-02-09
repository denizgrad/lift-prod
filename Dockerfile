FROM lift
ADD . /app
RUN cp /app/liftnec-nginx /etc/nginx/conf.d/nginx.conf
RUN cp /app/build/etc/supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN usermod -u 1000 nginx
RUN usermod -G staff root

WORKDIR /app
EXPOSE 80
CMD ["/start.sh"]