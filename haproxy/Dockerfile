FROM amazonlinux:2

RUN yum install -y gcc make openssl-devel pcre-devel tar gzip \
    && curl -O http://www.haproxy.org/download/2.9/src/haproxy-2.9.3.tar.gz \
    && tar xzf haproxy-2.9.3.tar.gz \
    && cd haproxy-2.9.3 \
    && make TARGET=linux-glibc USE_OPENSSL=1 USE_PCRE=1 \
    && make install

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

EXPOSE 80

CMD ["/usr/local/sbin/haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
