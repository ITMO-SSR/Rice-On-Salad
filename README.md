[English](README_EN.md)
# Rice-On-Salad
**Цель проекта:**
    Разработать доступный для воспроизведения проект гусеничной платформы с возможностью удаленного управления через ПК и ориентации в пространстве через камеры.
****
**Описание:**
    Полностью Open-Source проект с возможностью легкого повторения. Все детали для печати будут лежать в открытом доступе. 
****
**Задачи проекта:**
 - Рзработать и собрать гусеничную платформу
 - Подобрать необходимую электронику
 - Реализовать удаленное управление платформой через ПК
 - Добавить автоматическое управление
****
**Желаемый результат:**
    Получить полностью управляемую и самостоятельно ориентирующуюся в пространстве гусеничную платформу
***
<details>
    <summary>История разработки гусеницы</summary>
    <p>Начальная задача: придумать оптимальные гусеницы для робоплатформы.</p>
    <p>Основные параметры: ширина гусеницы, расстояние между центрами вращения траков.</p>
    <p>Если касаемо ширины трака все было довольно однозначно: берем среднее соотношение ширины траков и корпуса у вездеходов средней весовой категории, что составило 0.67 (сумма ширины траков к ширине корпуса без учета траков), то есть при заданной ширине 150 мм ширина каждого трака составила 50 мм.</p>
    <p>Длина трака подбиралась под диаметр ведущего колеса, в чем очень помог Советский учебник по расчету гусеничных шасси. (“Расчет и конструирование гусеничных машин Н.А. Носова издательство “Машиностроение” Ленинград 1972”)</p>
    <p>После определения параметров пришло время определиться с зацеплением.</p>
    <p>В первом прототипе использовалось захождение 2 в 3 ушка, однако от этого было решено отказаться из-за большого масштаба и недостаточного разрешения FDM 3D печати.</p>
    <p>Вторым прототипом было зацепление 1 в 2 ушка, которое и было выбрано для дальнейшей работы. </p>
    <p>Кроме того, был переработан паз для зацепления с ведущим катком. </p>
    <p>Для первой версии были использованы квадратные окна, повторяющие профиль зуба в серединном сечении, которые не обеспечивали достаточного захождения зацепного зуба на колесе в трак, а так же обеспечивали слишком малый контакт зацепления, что могло привести к прокручиванию и разуванию гусеницы.</p>
    <p>Для второго прототипа были выбраны торчащие по бокам гусеницы штыри, которые размещались в полость между зубцами колеса, что обеспечивает отличный контакт и хорошее вхождение в зацепление. Таким образом, 2 версия уже является хорошим траком из-за легкости, прочности, воспроизводимости на FDM принтере и зацепляемости проволкой от 0.8 до 1.2 мм в диаметре.</p>
    <p>К 3-м тракам 2-й версии было напечатано 24 трака 3-й версии для оценки соединений на большом количестве траков, а так же ощей гибкости и упругости гусеничного полотна.</p>
    <p>Дальнейшие изменения трака лишь вносили небольшие коррективы. Третий прототип немногим отличается от второго. Было добавлено 2 отверстия в траке, которые в дальнейшем позволят дооснащать гусеничное полотно различными грунтозацепами, повышая приспособленность гусеницы под различные условия без необходимости изготовления новой.</p>
    <p>Четвертой и финальной версией был закрыт вопрос с препятствованием разуванию и оптимальному взаимодействию с опорными катками. Было добавлено два зуба толщиной по 1.5 мм на расстоянии 19 мм, что при печати из PETG пластика обеспечивает достаточную прочность для сопротивления к поперечным нагрузкам и размещению и прокатыванию между ними опорного катка шириной 18.8 мм.</p>
    
![Prototype 1](images/proto-1.jpg)
![Prototype 2&3](images/proto-2-3.jpg)
![Prototype 4](images/proto-4.jpg)
</details>

***
# Установка ROS на Raspberry Pi
В данной статье мы опишем процесс установки ROS на Raspberry Pi, а также расскажем о том, как подключить робота к своему компьютеру.

## Шаг 1.
Для работы Raspberry Pi требуется операционная система, которая хранится на карте microSD. В нашем проекте мы используем образ Ubuntu 16.04 с уже установленным ROS, который вы можете скачать по [ссылке](https://downloads.ubiquityrobotics.com/pi.html). Для записи образа на SD-карту вам потребуется программа [balenaEtcher](https://www.balena.io/etcher/).

## Шаг 2.
Для дальнейшей работы с Raspberry Pi вам нужно установить и настроить ROS на компьютере, с которого вы планируете подключаться к вашему роботу. Наиболее простой вариант - запустить образ Ubuntu с предустановленным ROS с помощью виртуальной машины.
1. Скачайте виртуальную машину [VirtualBox](https://www.virtualbox.org/wiki/Downloads) и установите её.
2. Скачайте образ Ubuntu по [ссылке](https://downloads.ubiquityrobotics.com/vm.html).
3. Разархивируйте файл, который вы скачали. В результате получится папка, внутри которой будет файл с расширением .vbox. Запустите его. В результате откроется менеджер Virtual Box.
4. Проверьте параметры виртуальной машины и запустите её. Имя пользователя - `ubuntu`, пароль - `ubuntu`.

## Шаг 3.
Теперь, когда все необходимое ПО было установлено, рассмотрим процесс подключения к Raspberry Pi через SSH.
1. При первом включении Raspberry будет работать в режиме точки доступа Wi-Fi, к которой нужно будет подключиться с вашего компьютера. Имя сети - `ubiquityrobotXXXX`, где `XXXX` - комбинация цифр. Пароль для подключения - `robotseverywhere`.
2. После подключения к сети, откройте терминал в Ubuntu и введите команду `ssh ubuntu@10.42.0.1`. Далее введите пароль `ubuntu`.
3. Для того, чтобы в дальнейшем подключаться к роботу через вашу Wi-Fi сеть, нужно добавить её в список. Для просмотра доступных сетей наберите команду `pifi list seen`. Для добавления вашей сети воспользуйтесь командой `sudo pifi add MyNetwork password`, где `MyNetwork` и `password` - имя и пароль вашей сети. Далее, введите `sudo reboot` в терминале. Это приведет к перезапуску робота, который теперь будет автоматически подключаться к вашей сети.
4. Подключитесь к данной сети с вашего компьютера и снова откройте терминал Ubuntu. Теперь, чтобы подключиться к роботу, воспользуйтесь командой `ssh ubuntu@address`, где `address` - IP-адрес вашего робота. Для того, чтобы узнать его, выполните следующие действия:
   1. Введите в терминале команду `ifconfig`. В ответ вы получите информацию по сетевым интерфейсам:
```
    `eth0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
           ether b8:27:eb:5b:d7:ae  txqueuelen 1000  (Ethernet)
           RX packets 0  bytes 0 (0.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 0  bytes 0 (0.0 B)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
           inet 127.0.0.1  netmask 255.0.0.0
           inet6 ::1  prefixlen 128  scopeid 0x10<host>
           loop  txqueuelen 1000  (Local Loopback)
           RX packets 0  bytes 0 (0.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 0  bytes 0 (0.0 B)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
           inet 192.168.1.2  netmask 255.255.255.0  broadcast 192.168.1.255
           inet6 fe80::1e3a:e952:1094:4fda  prefixlen 64  scopeid 0x20<link>
           ether 00:e0:4c:06:6f:dc  txqueuelen 1000  (Ethernet)
           RX packets 257  bytes 33734 (32.9 KiB)
           RX errors 0  dropped 14  overruns 0  frame 0
           TX packets 153  bytes 26653 (26.0 KiB)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```           
Обратите внимание на адрес `inet 192.168.1.2.`. IP-адрес Raspberry Pi будет иметь вид `192.168.1.x`, где `x` - число от 1 до 255.
   2. Теперь, для того, чтобы найти адрес Raspberry Pi, можно воспользоваться приложением [Advanced IP Scanner](https://www.advanced-ip-scanner.com). Запустите приложение, введите `192.168.1.1-255` и нажмите "Сканировать". В результате вы увидите список устройств, подключенных к вашей сети, среди которых будет и Raspberry.
3. Поздравляем! Вы подключились к своему роботу!