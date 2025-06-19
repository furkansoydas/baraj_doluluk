# Temel imaj olarak Ubuntu kullanıyoruz
FROM ubuntu:20.04

# Non-interaktif modda çalıştırma
ENV DEBIAN_FRONTEND=noninteractive

# Sistem güncellemeleri ve temel araçların kurulumu
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    unzip \
    zip \
    git \
    nano \
    wget \
    locales \
    neovim \ 
    && apt-get clean

# Yerel ayarları yapılandırma
RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

# PHP'nin en son sürümünü (PHP 8.3) ve gerekli uzantıları kurma
RUN add-apt-repository ppa:ondrej/php -y && apt-get update && apt-get install -y \
    php8.3 \
    php8.3-cli \
    php8.3-mbstring \
    php8.3-xml \
    php8.3-bcmath \
    php8.3-curl \
    php8.3-zip \
    php8.3-mysql \
    php8.3-gd \
    && apt-get clean


# Apache kurulumu
RUN apt-get install -y apache2 libapache2-mod-php8.2 && apt-get clean

# MySQL istemcisi ve sunucusu kurulumu
RUN apt-get install -y mysql-client mysql-server && apt-get clean

# Composer kurulumu
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Node.js ve npm kurulumu
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs && apt-get clean

# Laravel için gerekli klasör izinlerini ayarlama
WORKDIR /var/www/html
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Apache ayarlarını etkinleştirme
RUN a2enmod rewrite

# Apache giriş noktası
CMD ["apache2ctl", "-D", "FOREGROUND"]

# Gerekli portları açma
EXPOSE 80
