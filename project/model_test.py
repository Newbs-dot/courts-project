import spacy
test1 = "Арбитражный суд Московской области в составе: судьи Бекетовой Е.А. при ведении протокола судебного заседания секретарем судебного заседания Старковой А.Ю., рассмотрев в судебном заседании дело по заявлению акционерного общества «МОСЭНЕРГОСБЫТ» (ИНН 7736520080, ОГРН 1057746557329) к врио начальника – старшего судебного пристава МО по ИОВИП №2 ГУФССП России по Московскй области Мкртчян А.А., судебному приставу – исполнителю МО по ИОВИП №2 ГУФССП России по Московской области Алханову Ш.К., ГУФССП России по Московской области о признании незаконным бездействия, третьи лица - Муниципальное унитарное предприятие городского округа Подольск «ДИРЕКЦИЯ ЕДИНОГО ЗАКАЗЧИКА» (ИНН 5036055450, ОГРН 1035007219301), при участии в судебном заседании: лиц согласно протоколу,"
test2 = """Арбитражный суд Новосибирской области в составе судьи Морозовой Л.Н., при ведении протокола судебного заседания секретарем судебного заседания Падериной К.Ю., рассмотрев в открытом судебном заседании дело по исковому заявлению акционерного общества «Разрез Колыванский» (ИНН 5406192366), Новосибирская область, Искитимский район, п. Листвянский, к обществу с ограниченной ответственностью "Сервис-Интегратор" (ИНН 7729395092), г. Москва, третье лицо, не заявляющее самостоятельных требований относительно предмета спора, общество с ограниченной ответственностью «РЕГИОНСКАН» (ИНН 5446019030), г. Искитим, Новосибирская область, о взыскании штрафа размере 1 000 000 рублей,"""
test3 = """Арбитражный суд Новосибирской области в составе судьи Хлоповой А.Г., при ведении протокола судебного заседания помощником судьи Кодиловой А.Г., рассмотрев в открытом судебном заседании дело по иску акционерного общества "Сибирский Антрацит" (ОГРН 1025404670620) к обществу с ограниченной ответственностью фирма "ФАЛАР" (ОГРН 1034205007847) о взыскании убытков, связанных с приобретением комплектующих деталей на некачественный товар грохот ГИСЛ-62 (верхние сита штампов яч25х25, нижн. сита шпальт. Щ 1,6мм) зав.№0115, поставленный по договору поставки от 31.07.2014 №ТП-31/07/14 в размере 1 329 208 руб. 64 коп., расходов на проведение досудебной экспертизы в размере 55 000 руб.,"""
test4 = """Арбитражный суд Краснодарского края 350063, г. краснодар, ул. постовая, 32  именем российской федерации р е ш е н и е  12 октября 2022 года дело № а32-12934/2022 г. краснодар  резолютивная часть решения объявлена 20 сентября 2022 года. полный текст решения изготовлен 12 октября 2022 года.   арбитражный суд краснодарского края в составе судьи куликова о.б., при ведении протокола судебного заседания помощником судьи авагимовым г.м., рассмотрел в судебном заседании дело по исковому заявлению общества с ограниченной ответственностью «поле сукко» (инн 7728747680, огрн 1107746724854) к публичному акционерному обществу «вымпел-коммуникации» (инн 7713076301, огрн 1027700166636) о взыскании 2 120 048 рублей 45 копеек, при участии в заседании представителя ответчика шурминой о.с., установил следующее.  в арбитражный суд краснодарского края обратилось общество с ограниченной ответственностью «поле сукко» (далее – общество, ооо «поле сукко») с исковым заявлением к публичному акционерному обществу «вымпел-коммуникации»  (далее – компания, пао «вымпел-коммуникации») о взыскании 2 120 048 рублей 45 копеек, из которых 1 копейка основного долга, 63 824 рубля 05 копеек неустойки, 1 979 086 рублей 26 копеек штрафа, 77 138 рублей 13 копеек процентов за пользование чужими денежными средствами. представитель истца в судебное заседание не явился, о времени  и месте рассмотрения дела извещен надлежащим образом. представитель ответчика в судебном заседании возражал против удовлетворения исковых требований, по основаниям изложенным в отзыве на иск, представил платежное поручение об оплате основного долга."""

test5 = """публичное акционерное общество «Газпром» (далее – истец, Общество) обратилось в Арбитражный суд Новгородской области с исковым заявлением к Межрегиональному территориальному управлению Федерального агентства по управлению государственным имуществом в Псковской и Новгородской областях (далее – ответчик, Агентство) о признании права собственности на объект недвижимости – сооружение «Кабельные линии электроснабжения КС-Новгород», протяженностью 1 267 м., расположенное по адресу: 173008, Российская Федерация, Новгородская область, г.Великий Новгород, ул.Большая Санкт-Петербургская, д. 190. Определением от 07.08.2023 исковое заявление Общества принято судом к производству и назначено к рассмотрению по общим правилам искового производства, к участию в деле в качестве третьего лица, не заявляющего самостоятельных требований """
test6 = """третьи лица, не заявляющие самостоятельных требований относительно предмета спора: 1. Пожитков Константин Владимирович, Оренбургская область, г. Абдулино, 2. Зобова Мария Сергеевна, Оренбургская область, г.Абдулино, об обязании прекратить использовать словесное обозначение в фирменном наименовании «Газпром» о взыскании 300 000 руб. Стороны о времени и месте судебного заседания извещены надлежащим образом в соответствии со статьями 121, 123 Арбитражного процессуального кодекса Российской Федерации по юридическим адресам и адресам проживания, а также путем размещения информации на официальном сайте суда в информационно-"""
test7 = """Арбитражный суд Республики Крым в составе судьи Плотникова И.В., рассмотрев заявление взыскателя – Федерального государственного унитарного предприятия «Охрана» Федеральной службы войск национальной гвардии Российской Федерации (ОГРН: 1057747117724, ИНН: 7719555477) в лице Филиала ФГУП «Охрана» Росгвардии по Республике Крым к должнику – Обществу с ограниченной ответственностью «ПМК «КРЫМИНВЕСТ» (ОГРН: 1179102017137, ИНН: 9102231290) о выдаче судебного приказа о взыскании задолженности по Договору № 8311016580 от 01.12.2018 в сумме 413,20 руб. за период с 01.06.2019 по 30.06.2019, пени в сумме 413,20 куб. и штрафа в сумме 203,60 руб."""

nlp1 = spacy.load(r".\output100\model-best") #load the best model
doc = nlp1(test7) # input sample text

for ent in doc.ents:
    print(ent.text,ent.label_)



print(spacy.displacy.serve(doc, style="ent",port=3000)) # display in Jupyter