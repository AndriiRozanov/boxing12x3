# December "This day in boxing": data. Source: owner's PDF (Nov 2026) + results checked for 7 entries.
# (day, year, title_ua, title_en, place_ua, place_en, text_ua, text_en, youtube_id)
# Excluded on purpose: entries from the "Chronicle WBC" with no pair/result, entries without pair and result,
# Jesus Ramos (6 Dec 2025), Hopkins-Mercado 1995 (wrong in PDF), Gomez-Castro 2000 (result not found).
E = []
def e(d, y, tu, te, pu, pe, xu, xe, v=None): E.append((d, y, tu, te, pu, pe, xu, xe, v))

# ---- 1-2
e(1, 1973, "Боб Фостер – П'єр Фур'є", "Bob Foster – Pierre Fourie", "Йоганнесбург, ПАР", "Johannesburg, South Africa",
  "Перемога Фостера рішенням суддів. Захист титулу WBC у напівважкій вазі.", "Foster won on the judges' decision, defending the WBC light heavyweight title.")
e(1, 1980, "Іларіо Сапата – Рейнальдо Бесерра", "Hilario Zapata – Reynaldo Becerra", "Каракас, Венесуела", "Caracas, Venezuela",
  "Перемога Сапати. Захист титулу WBC у першій найлегшій вазі.", "Zapata won and defended the WBC light flyweight title.")
e(1, 1995, "Азума Нельсон KO 5 Габріель Руелас", "Azumah Nelson KO 5 Gabriel Ruelas", "Палм-Спрінгс, США", "Palm Springs, USA",
  "Бій за титул WBC у другій напівлегкій вазі.", "Bout for the WBC super featherweight title.")
e(1, 2007, "Вернон Форрест KO 11 Мікеле Піччірілло", "Vernon Forrest KO 11 Michele Piccirillo", "Машантакет, США", "Mashantucket, USA",
  "Бій за титул WBC у першій середній вазі.", "Bout for the WBC super welterweight title.")
e(1, 2018, "Деонтей Вайлдер D-SD 12 Тайсон Ф'юрі", "Deontay Wilder D-SD 12 Tyson Fury", "Лос-Анджелес, США", "Los Angeles, USA",
  "Нічия. Вайлдер зберіг титул WBC у надважкій вазі.", "A draw. Wilder kept the WBC heavyweight title.")
e(1, 2018, "Олександр Гвоздик KO 11 Адоніс Стівенсон", "Oleksandr Gvozdyk KO 11 Adonis Stevenson", "Квебек, Канада", "Quebec City, Canada",
  "Нокаут у 11-му раунді (2:49). Гвоздик завоював титули WBC та лінійний у напівважкій вазі.", "A knockout in round 11 (2:49). Gvozdyk won the WBC and lineal light heavyweight titles.")
e(2, 1963, "Сандро Маццінгі TKO 13 Ральф Дюпас", "Sandro Mazzinghi TKO 13 Ralph Dupas", "Сідней, Австралія", "Sydney, Australia",
  "Маццінгі завоював титул у першій середній вазі.", "Mazzinghi won the super welterweight title.")
e(2, 1965, "Сальваторе Бурруні KO 13 Рокі Гаттелларі", "Salvatore Burruni KO 13 Rocky Gattellari", "Сідней, Австралія", "Sydney, Australia",
  "Бій у найлегшій вазі.", "A flyweight bout.")
e(2, 1972, "Бруно Аркарі UD 15 Еверальдо Коста", "Bruno Arcari UD 15 Everaldo Costa", "Турин, Італія", "Turin, Italy",
  "Бій у першій напівсередній вазі.", "A super lightweight bout.")
e(2, 1977, "Карлос Сарате TKO 5 Хуан Франсіско Родрігес", "Carlos Zarate TKO 5 Juan Francisco Rodriguez", "Мадрид, Іспанія", "Madrid, Spain",
  "Бій у легшій вазі.", "A bantamweight bout.")
e(2, 1978, "Марвін Джонсон TKO 10 Мате Парлов", "Marvin Johnson TKO 10 Mate Parlov", "Марсала, Італія", "Marsala, Italy",
  "Джонсон завоював титул у напівважкій вазі.", "Johnson won the light heavyweight title.")
e(2, 1986, "Цуйоші Хамада – Ронні Шилдс", "Tsuyoshi Hamada – Ronnie Shields", "Токіо, Японія", "Tokyo, Japan",
  "Перемога Хамади рішенням суддів за 12 раундів. Бій у першій напівсередній вазі.", "Hamada won on the judges' decision over 12 rounds in a super lightweight bout.")
e(2, 1995, "Вейн Маккаллох TKO 8 Джонні Бредаль", "Wayne McCullough TKO 8 Johnny Bredahl", "Белфаст, Північна Ірландія", "Belfast, Northern Ireland",
  "Бій у легшій вазі.", "A bantamweight bout.")
e(2, 2017, "Рей Варгас UD 12 Оскар Негрете", "Rey Vargas UD 12 Oscar Negrete", "Нью-Йорк, США", "New York, USA",
  "Бій у другій легшій вазі.", "A super bantamweight bout.")
# ---- 3-4
e(3, 2005, "Джермейн Тейлор UD 12 Бернард Хопкінс", "Jermain Taylor UD 12 Bernard Hopkins", "Лас-Вегас, США", "Las Vegas, USA",
  "Реванш «No Respect» за титули WBA (Undisputed), WBC та інші. Усі троє суддів виставили 115–113 на користь Тейлора.",
  "The “No Respect” rematch for the WBA (Undisputed), WBC and other titles. All three judges scored it 115–113 for Taylor.", "amR5-wTihUo")
e(3, 2025, "WBC позбавила Теренса Кроуфорда чемпіонського титулу", "WBC strips Terence Crawford of his title", "", "",
  "WBC позбавила Теренса Кроуфорда свого чемпіонського титулу. Рішення організації.", "The WBC stripped Terence Crawford of its championship title.")
e(4, 1931, "Поєдинок Джеймса Дж. Бреддока", "James J. Braddock bout", "Нью-Гейвен, США", "New Haven, USA",
  "10-раундовий поєдинок, зафіксований із результатом NC (No Contest).", "A 10-round bout recorded as a no contest (NC).")
e(4, 1993, "Кевін Келлі UD 12 Гойо Варгас", "Kevin Kelley UD 12 Goyo Vargas", "Рено, США", "Reno, USA",
  "Келлі завоював титул WBC у напівлегкій вазі.", "Kelley won the WBC featherweight title.")
e(4, 1998, "Менні Пак'яо KO 8 Чатчай Сасакул", "Manny Pacquiao KO 8 Chatchai Sasakul", "Пхуттхамонтхон (передмістя Бангкока), Таїланд", "Phutthamonthon (Bangkok suburb), Thailand",
  "Пак'яо завоював перший у кар'єрі титул чемпіона світу – WBC у найлегшій вазі.", "Pacquiao won his first world title, the WBC flyweight belt.")
e(4, 1999, "Фернандо Варгас MD 12 Вінкі Райт", "Fernando Vargas MD 12 Winky Wright", "Лінкольн-Сіті, США", "Lincoln City, USA",
  "Захист титулу IBF у першій середній вазі.", "Defence of the IBF super welterweight title.")
e(4, 2004, "Хосе Луїс Кастільйо SD 12 Хоель Касамайор", "Jose Luis Castillo SD 12 Joel Casamayor", "Лас-Вегас, США", "Las Vegas, USA",
  "Захист титулу WBC у легкій вазі.", "Defence of the WBC lightweight title.", "YFnbvNsYYGw")
# ---- 5-6
e(5, 1947, "Джо Луїс SD 15 Джерсі Джо Волкотт", "Joe Louis SD 15 Jersey Joe Walcott", "Нью-Йорк, США", "New York, USA",
  "15-раундовий бій за звання абсолютного чемпіона у надважкій вазі (Луїс – фаворит 1 до 10). Луїс зберіг титул суперечливим роздільним рішенням суддів.",
  "A 15-round fight for the undisputed heavyweight title (Louis was a 10-to-1 favourite). Louis kept his title on a controversial split decision.")
e(6, 1968, "Лайонел Роуз – Хесус Кастільйо", "Lionel Rose – Jesus Castillo", "Інґлвуд, США", "Inglewood, USA",
  "Перемога Роуза рішенням суддів. Титул WBC у легшій вазі.", "Rose won on the judges' decision. WBC bantamweight title.")
e(6, 1969, "Леотіс Мартін KO 9 Сонні Лістон", "Leotis Martin KO 9 Sonny Liston", "Лас-Вегас, США", "Las Vegas, USA",
  "Мартін нокаутував Лістона в дев'ятому раунді.", "Martin knocked out Liston in round nine.")
e(6, 1975, "Джон Стрейсі KO 6 Хосе Наполес", "John Stracey KO 6 Jose Napoles", "Мехіко, Мексика", "Mexico City, Mexico",
  "Стрейсі завоював титул WBC у напівсередній вазі.", "Stracey won the WBC welterweight title.")
e(6, 1996, "Марсело Домінгес KO 8 Хосе Аріматеа", "Marcelo Dominguez KO 8 Jose Arimatea", "Буенос-Айрес, Аргентина", "Buenos Aires, Argentina",
  "Титул WBC у важкій вазі.", "WBC cruiserweight title.")
e(6, 1997, "Луїсіто Еспіноса KO 6 Карлос Альберто Ріос", "Luisito Espinosa KO 6 Carlos Alberto Rios", "Філіппіни", "Philippines",
  "Титул WBC у напівлегкій вазі.", "WBC featherweight title.")
e(6, 1997, "Оскар Де Ла Хойя KO 8 Вільфредо Рівера", "Oscar De La Hoya KO 8 Wilfredo Rivera", "Атлантік-Сіті, США", "Atlantic City, USA",
  "Титул WBC у напівсередній вазі.", "WBC welterweight title.")
e(6, 2008, "Карл Фроч – Жан Паскаль", "Carl Froch – Jean Pascal", "Ноттінгем, Англія", "Nottingham, England",
  "Перемога Фроча рішенням суддів. Фроч завоював титул WBC у другій середній вазі.", "Froch won on the judges' decision and took the WBC super middleweight title.")
e(6, 2008, "Менні Пак'яо RTD 8 Оскар Де Ла Хойя", "Manny Pacquiao RTD 8 Oscar De La Hoya", "Лас-Вегас, США", "Las Vegas, USA",
  "Поєдинок в MGM Grand. Де Ла Хойя не вийшов на дев'ятий раунд.", "The fight at the MGM Grand. De La Hoya did not come out for round nine.", "wDqOnlqRlLo")
e(6, 2013, "Кшиштоф Влодарчик KO Джакоббе Фрагомені", "Krzysztof Wlodarczyk KO Giacobbe Fragomeni", "Чикаго, США", "Chicago, USA",
  "Перемога Влодарчика нокаутом. Титул WBC у важкій вазі.", "Wlodarczyk won by knockout. WBC cruiserweight title.")
e(6, 2013, "Акіра Йегаші – Едгар Соса", "Akira Yaegashi – Edgar Sosa", "Токіо, Японія", "Tokyo, Japan",
  "Перемога Йегаші рішенням суддів. Титул WBC у найлегшій вазі.", "Yaegashi won on the judges' decision. WBC flyweight title.")
# ---- 7-8
e(7, 1963, "Джої Джарделло PTS 15 Дік Тайгер", "Joey Giardello PTS 15 Dick Tiger", "Атлантік-Сіті, США", "Atlantic City, USA",
  "Джарделло завоював титули WBA, WBC та The Ring у середній вазі. Бій оцінював єдиний рефері-суддя.", "Giardello won the WBA, WBC and The Ring middleweight titles. The bout was scored by a single referee-judge.")
e(7, 1970, "Ербіто Салаваррія KO 2 Чартчай Чіоной", "Erbito Salavarria KO 2 Chartchai Chionoi", "Бангкок, Таїланд", "Bangkok, Thailand",
  "Титул WBC у найлегшій вазі.", "WBC flyweight title.")
e(7, 1974, "Родольфо Мартінес KO 4 Рафаель Еррера", "Rodolfo Martinez KO 4 Rafael Herrera", "Мерида, Мексика", "Merida, Mexico",
  "Титул WBC у легшій вазі.", "WBC bantamweight title.")
e(7, 1992, "Умберто Гонсалес – Мельчор Коб Кастро", "Humberto Gonzalez – Melchor Cob Castro", "Інґлвуд, США", "Inglewood, USA",
  "Перемога Гонсалеса рішенням суддів. Титул WBC у першій найлегшій вазі.", "Gonzalez won on the judges' decision. WBC light flyweight title.")
e(7, 1996, "Рікардо Лопес KO 1 Мюнсуп Пак", "Ricardo Lopez KO 1 Mun-Soop Park", "Індіо, США", "Indio, USA",
  "Титул WBC у мінімальній вазі.", "WBC minimumweight title.")
e(7, 2002, "Флойд Мейвезер UD 12 Хосе Луїс Кастільйо", "Floyd Mayweather UD 12 Jose Luis Castillo", "Лас-Вегас, США", "Las Vegas, USA",
  "Реванш. Рахунок 116–113, 115–113, 115–113. Захист титулів WBC і The Ring у легкій вазі.", "A rematch. Scores 116–113, 115–113, 115–113. Defence of the WBC and The Ring lightweight titles.")
e(7, 2019, "Ентоні Джошуа UD 12 Енді Руїс", "Anthony Joshua UD 12 Andy Ruiz Jr", "Ед-Дірійя, Саудівська Аравія", "Diriyah, Saudi Arabia",
  "Рахунок 118–110, 118–110, 119–109. Джошуа повернув собі титули WBA Super, IBF, WBO та IBO у надважкій вазі.", "Scores 118–110, 118–110, 119–109. Joshua regained the WBA Super, IBF, WBO and IBO heavyweight titles.")
e(7, 2019, "Джермалл Чарло KO 7 Деніс Гоган", "Jermall Charlo KO 7 Dennis Hogan", "Бруклін, США", "Brooklyn, USA",
  "Два нокдауни. Захист титулу WBC у середній вазі.", "Two knockdowns. Defence of the WBC middleweight title.")
e(8, 1931, "Народився Боб Арум", "Bob Arum was born", "", "",
  "Народився відомий американський боксерський промоутер.", "The famous American boxing promoter was born.")
e(8, 1979, "Марвін Камель D Мате Парлов", "Marvin Camel D Mate Parlov", "Югославія", "Yugoslavia",
  "Нічия в поєдинку за титул WBC у важкій вазі.", "A draw in the fight for the WBC cruiserweight title.")
e(8, 1984, "Азума Нельсон KO 11 Вільфредо Гомес", "Azumah Nelson KO 11 Wilfredo Gomez", "Сан-Хуан, Пуерто-Рико", "San Juan, Puerto Rico",
  "Титул WBC у напівлегкій вазі.", "WBC featherweight title.")
e(8, 1990, "Хуліо Сесар Чавес KO 3 Кьондук Ан", "Julio Cesar Chavez KO 3 Kyung-Duk Ahn", "Атлантік-Сіті, США", "Atlantic City, USA",
  "Титул WBC у першій напівсередній вазі.", "WBC super lightweight title.")
e(8, 2007, "Флойд Мейвезер KO 10 Ріккі Хаттон", "Floyd Mayweather KO 10 Ricky Hatton", "Лас-Вегас, США", "Las Vegas, USA",
  "Титул WBC у напівсередній вазі.", "WBC welterweight title.")
# ---- 9-10
e(9, 1955, "Шугар Рей Робінсон KO 2 Бобо Олсон", "Sugar Ray Robinson KO 2 Bobo Olson", "США", "USA",
  "Робінсон завоював третій титул у середній вазі.", "Robinson won the middleweight title for the third time.")
e(9, 1959, "Помер Тоні Канцонері", "Tony Canzoneri died", "США", "USA",
  "Помер у віці 51 року. Колишній чемпіон світу в трьох вагових категоріях.", "He died aged 51. A former world champion in three weight classes.")
e(9, 1989, "Умберто Гонсалес UD 12 Чон Ку Чан", "Humberto Gonzalez UD 12 Jung-Koo Chang", "Тегу, Південна Корея", "Daegu, South Korea",
  "Титул WBC у першій найлегшій вазі.", "WBC light flyweight title.")
e(9, 1991, "Даніель Сарагоса TKO Пол Бенк", "Daniel Zaragoza TKO Paul Banke", "", "",
  "Перемога Сарагоси. Бій зупинено через розсічення в Бенка.", "Zaragoza won. The fight was stopped because of a cut on Banke.")
e(9, 2017, "Василь Ломаченко RTD 6 Гільєрмо Рігондо", "Vasyl Lomachenko RTD 6 Guillermo Rigondeaux", "Нью-Йорк, США", "New York, USA",
  "Рахунок 60–53, 59–54, 59–54. Захист титулу WBO у другій напівлегкій вазі.", "Scores 60–53, 59–54, 59–54. Defence of the WBO super featherweight title.", "yvu2ch3U7Fo")
e(10, 1965, "Еміль Гріффіт UD 15 Мануель Гонсалес", "Emile Griffith UD 15 Manuel Gonzalez", "Нью-Йорк, США", "New York, USA",
  "Бій у напівсередній вазі.", "A welterweight bout.")
e(10, 1968, "Джо Фрейзер UD 15 Оскар Бонавена", "Joe Frazier UD 15 Oscar Bonavena", "Філадельфія, США", "Philadelphia, USA",
  "Другий бій. Лінійний титул у надважкій вазі.", "The second fight. Lineal heavyweight title.")
e(10, 1975, "Альфредо Ескалера TKO 9 Свен Ерік Паульсен", "Alfredo Escalera TKO 9 Sven-Erik Paulsen", "Осло, Норвегія", "Oslo, Norway",
  "Бій у другій напівлегкій вазі.", "A super featherweight bout.")
e(10, 1982, "Майкл Доукс TKO 1 Майк Вівер", "Michael Dokes TKO 1 Mike Weaver", "Лас-Вегас, США", "Las Vegas, USA",
  "Суперечлива перемога Доукса зупинкою рефері в першому раунді (1:03). Титул WBA у надважкій вазі.", "Dokes won controversially, the referee stopping the bout in round one (1:03). WBA heavyweight title.")
e(10, 1985, "Дж. Б. Вільямсон – Прінс Мухаммад", "J.B. Williamson – Prince Mohammed", "Інґлвуд, США", "Inglewood, USA",
  "Перемога Вільямсона рішенням суддів за 12 раундів. Напівважка вага.", "Williamson won on the judges' decision over 12 rounds. A light heavyweight bout.")
e(10, 1986, "Сот Чіталада – Габріель Берналь", "Sot Chitalada – Gabriel Bernal", "Бангкок, Таїланд", "Bangkok, Thailand",
  "Перемога Чіталади рішенням суддів за 12 раундів. Найлегша вага.", "Chitalada won on the judges' decision over 12 rounds. A flyweight bout.")
e(10, 1986, "Самарт Паякарун TKO 12 Хуан Меса", "Samart Payakaroon TKO 12 Juan Meza", "Бангкок, Таїланд", "Bangkok, Thailand",
  "Бій у другій легшій вазі.", "A super bantamweight bout.")
e(10, 1988, "Азума Нельсон KO 3 Сідні Дал Ровере", "Azumah Nelson KO 3 Sidney Dal Rovere", "", "",
  "Перемога Нельсона нокаутом у третьому раунді.", "Nelson won by a third-round knockout.")
e(10, 1994, "Хуліо Сесар Чавес TKO 10 Тоні Лопес", "Julio Cesar Chavez TKO 10 Tony Lopez", "Монтеррей, Мексика", "Monterrey, Mexico",
  "Бій у першій напівсередній вазі.", "A super lightweight bout.")
e(10, 1994, "Рікардо Лопес KO 1 Яміль Карабальйо", "Ricardo Lopez KO 1 Yamil Caraballo", "Монтеррей, Мексика", "Monterrey, Mexico",
  "Бій у мінімальній вазі.", "A minimumweight bout.")
# ---- 11-13
e(11, 1964, "Сандро Маццінгі UD 15 Фортунато Манка", "Sandro Mazzinghi UD 15 Fortunato Manca", "", "",
  "Перемога Маццінгі одностайним рішенням суддів.", "Mazzinghi won on a unanimous decision.")
e(11, 1982, "Боббі Чакон – Рафаель Лімон", "Bobby Chacon – Rafael Limon", "", "",
  "Перемога Чакона. Це був його другий виграш над Лімоном.", "Chacon won, his second victory over Limon.")
e(11, 2004, "Віталій Кличко TKO 8 Денні Вільямс", "Vitali Klitschko TKO 8 Danny Williams", "Лас-Вегас, США", "Las Vegas, USA",
  "Титульний поєдинок за пояси WBC та The Ring у надважкій вазі.", "A title fight for the WBC and The Ring heavyweight belts.")
e(11, 2010, "Скасований бій: Володимир Кличко – Дерек Чісора", "Cancelled fight: Wladimir Klitschko – Derek Chisora", "Німеччина", "Germany",
  "Скасований 8 грудня поєдинок у надважкій вазі через розрив м'яза преса в Кличка.", "The heavyweight bout was called off on 8 December because Klitschko tore an abdominal muscle.")
e(12, 1912, "Народився Генрі Армстронг", "Henry Armstrong was born", "США", "USA",
  "Народився легендарний американський боксер, чемпіон світу в трьох дивізіонах.", "The legendary American boxer, a world champion in three divisions, was born.")
e(12, 1954, "Помер Ед «Великий Ед» Сандерс", "Ed “Big Ed” Sanders died", "США", "USA",
  "Помер олімпійський чемпіон 1952 року у надважкій вазі.", "The 1952 Olympic heavyweight champion died.")
e(12, 1969, "Рубен Оліварес KO 2 Алан Раткін", "Ruben Olivares KO 2 Alan Rudkin", "Інґлвуд, США", "Inglewood, USA",
  "Бій у легшій вазі.", "A bantamweight bout.")
e(12, 1981, "Сальвадор Санчес UD 15 Пет Коуделл", "Salvador Sanchez UD 15 Pat Cowdell", "Г'юстон, США", "Houston, USA",
  "Бій у напівлегкій вазі.", "A featherweight bout.")
e(12, 1986, "Хуліо Сесар Чавес UD 12 Хуан Лапорте", "Julio Cesar Chavez UD 12 Juan Laporte", "Нью-Йорк, США", "New York, USA",
  "Бій у другій напівлегкій вазі.", "A super featherweight bout.")
e(12, 1986, "Джеймс Сміт – Тім Візерспун", "James Smith – Tim Witherspoon", "США", "USA",
  "Перемога Сміта та завоювання титулу WBA у надважкій вазі (турнір Дона Кінга).", "Smith won and took the WBA heavyweight title (a Don King tournament).")
e(12, 1992, "Найджел Бенн TKO 11 Ніккі Пайпер", "Nigel Benn TKO 11 Nicky Piper", "Лондон, Англія", "London, England",
  "Бій у другій середній вазі.", "A super middleweight bout.")
e(12, 1997, "Ерік Моралес TKO 8 Джон Лоуї", "Erik Morales TKO 8 John Lowey", "Тіхуана, Мексика", "Tijuana, Mexico",
  "Бій у другій легшій вазі.", "A super bantamweight bout.")
e(12, 1998, "Хуан Карлос Гомес KO 2 Родні Гордон", "Juan Carlos Gomez KO 2 Rodney Gordon", "Франкфурт, Німеччина", "Frankfurt, Germany",
  "Бій у важкій вазі.", "A cruiserweight bout.")
e(12, 2000, "Масаморі Токуяма UD 12 Акіхіко Наго", "Masamori Tokuyama UD 12 Akihiko Nago", "Осака, Японія", "Osaka, Japan",
  "Бій у другій найлегшій вазі.", "A super flyweight bout.")
e(12, 2009, "Віталій Кличко UD 12 Кевін Джонсон", "Vitali Klitschko UD 12 Kevin Johnson", "Берн, Швейцарія", "Bern, Switzerland",
  "Кличко виграв усі раунди на картках суддів. Титул WBC у надважкій вазі.", "Klitschko won every round on the scorecards. WBC heavyweight title.")
e(12, 2020, "Шакур Стівенсон UD 10 Тока Хан Кларі", "Shakur Stevenson UD 10 Toka Kahn Clary", "Лас-Вегас, США", "Las Vegas, USA",
  "10-раундовий поєдинок у «Баблі» MGM Grand.", "A 10-round bout in the MGM Grand “Bubble”.")
e(13, 2008, "Володимир Кличко TKO 7 Хасім Рахман", "Wladimir Klitschko TKO 7 Hasim Rahman", "Мангайм, Німеччина (SAP-Арена)", "Mannheim, Germany (SAP Arena)",
  "Титульний бій «X-Plosive» за пояси IBF та WBO у надважкій вазі.", "The “X-Plosive” title fight for the IBF and WBO heavyweight belts.")
e(14, 1964, "Народився Анатолій Ломаченко", "Anatoly Lomachenko was born", "Україна", "Ukraine",
  "Народився український тренер, батько й наставник Василя Ломаченка.", "The Ukrainian coach, father and mentor of Vasyl Lomachenko, was born.")
e(14, 1968, "Педро Адіґе UD 15 Адольф Пруїтт", "Pedro Adigue UD 15 Adolph Pruitt", "Кесон-Сіті, Філіппіни", "Quezon City, Philippines",
  "Адіґе завоював вакантний титул WBC у першій напівсередній вазі.", "Adigue won the vacant WBC super lightweight title.")
# ---- 16-19
e(16, 1940, "Джо Луїс TKO 6 Ел Маккой", "Joe Louis TKO 6 Al McCoy", "Бостон, США", "Boston, USA",
  "Захист титулу у надважкій вазі.", "Defence of the heavyweight title.")
e(16, 1966, "Дік Тайгер UD 15 Хосе Торрес", "Dick Tiger UD 15 Jose Torres", "Нью-Йорк, США", "New York, USA",
  "Тайгер повернув собі титул у напівважкій вазі.", "Tiger regained the light heavyweight title.")
e(16, 1971, "Боб Фостер TKO 3 Браян Келлі", "Bob Foster TKO 3 Brian Kelly", "Оклахома-Сіті, США", "Oklahoma City, USA",
  "Бій у напівважкій вазі.", "A light heavyweight bout.")
e(16, 1972, "Хосе Легра TKO 10 Клементе Санчес", "Jose Legra TKO 10 Clemente Sanchez", "Монтеррей, Мексика", "Monterrey, Mexico",
  "Титул WBC у напівлегкій вазі.", "WBC featherweight title.")
e(16, 1979, "Чан Хі Пак TKO 2 Гуті Еспадас", "Chan-Hee Park TKO 2 Guty Espadas", "Пусан, Південна Корея", "Busan, South Korea",
  "Титул WBC у найлегшій вазі.", "WBC flyweight title.")
e(16, 1989, "Хуліо Сесар Чавес TKO 3 Альберто Кортес", "Julio Cesar Chavez TKO 3 Alberto Cortes", "Мехіко, Мексика", "Mexico City, Mexico",
  "Перемога Чавеса технічним нокаутом.", "Chavez won by technical knockout.")
e(16, 1995, "Террі Норріс UD 12 Пол Ваден", "Terry Norris UD 12 Paul Vaden", "Філадельфія, США", "Philadelphia, USA",
  "Титул WBC у першій середній вазі.", "WBC super welterweight title.")
e(16, 2005, "Хорхе Арсе TKO 10 Адоніс Рівас", "Jorge Arce TKO 10 Adonis Rivas", "Монтеррей, Мексика (Arena Monterrey)", "Monterrey, Mexico (Arena Monterrey)",
  "Тимчасовий титул WBC у найлегшій вазі.", "Interim WBC flyweight title.")
e(17, 1952, "Арчі Мур PTS 15 Джої Максім", "Archie Moore PTS 15 Joey Maxim", "США", "USA",
  "Перемога Мура за очками. Мур став чемпіоном світу в напівважкій вазі.", "Moore won on points and became the light heavyweight world champion.")
e(17, 1978, "Народився Менні Пак'яо", "Manny Pacquiao was born", "Філіппіни", "Philippines",
  "Народився видатний філіппінський боксер.", "The outstanding Filipino boxer was born.")
e(17, 1996, "Народився Давід Бенавідес", "David Benavidez was born", "США", "USA",
  "Народився американський боксер, чемпіон світу.", "The American boxer and world champion was born.")
e(18, 1901, "Барбадоський Джо Волкотт TKO 5 Джеймс «Руб» Фернс", "Barbados Joe Walcott TKO 5 James “Rube” Ferns", "Форт-Ері, Канада", "Fort Erie, Canada",
  "Два нокдауни в п'ятому раунді. Волкотт завоював титул у напівсередній вазі.", "Two knockdowns in round five. Walcott won the welterweight title.")
e(18, 1916, "Джиммі Вайлд TKO 11 Янг Зулу Кід", "Jimmy Wilde TKO 11 Young Zulu Kid", "Лондон, Велика Британія", "London, Great Britain",
  "Вайлд став першим в історії чемпіоном світу в найлегшій вазі.", "Wilde became the first world flyweight champion in history.")
e(18, 1942, "Бо Джек KO 3 Тіппі Ларкін", "Beau Jack KO 3 Tippy Larkin", "Нью-Йорк, США", "New York, USA",
  "Бо Джек завоював титул NYSAC у легкій вазі.", "Beau Jack won the NYSAC lightweight title.")
e(18, 1993, "Саймон Браун KO 4 Террі Норріс", "Simon Brown KO 4 Terry Norris", "Пуебла, Мексика", "Puebla, Mexico",
  "Нокаут на 1:06 четвертого раунду. Браун завоював титул WBC у першій середній вазі. «Апсет року» за версією The Ring та WBC.",
  "A knockout at 1:06 of round four. Brown won the WBC super welterweight title. The Ring and WBC “Upset of the Year”.")
e(18, 1993, "Хуліо Сесар Чавес TKO 5 Енді Голліган", "Julio Cesar Chavez TKO 5 Andy Holligan", "Пуебла, Мексика", "Puebla, Mexico",
  "Захист титулу WBC у першій напівсередній вазі.", "Defence of the WBC super lightweight title.")
e(19, 1980, "Лупе Пінтор – Альберто Давіла", "Lupe Pintor – Alberto Davila", "Лас-Вегас, США", "Las Vegas, USA",
  "Перемога Пінтора рішенням суддів. Титул WBC у легшій вазі.", "Pintor won on the judges' decision. WBC bantamweight title.")
e(19, 1986, "Хільберто Роман – Конгторані Паякарун", "Gilberto Roman – Kongtoranee Payakaroon", "Бангкок, Таїланд", "Bangkok, Thailand",
  "Перемога Романа. Титул WBC у другій найлегшій вазі.", "Roman won. WBC super flyweight title.")
e(19, 1997, "Тулане Малінга – Робін Рід", "Thulane Malinga – Robin Reid", "Лондон, Англія", "London, England",
  "Перемога Малінги рішенням суддів за 12 раундів. Титул WBC у другій середній вазі.", "Malinga won on the judges' decision over 12 rounds. WBC super middleweight title.")
e(19, 1997, "Насім Хамед KO 4 Кевін Келлі", "Naseem Hamed KO 4 Kevin Kelley", "Нью-Йорк, США", "New York, USA",
  "Дебют британця в США.", "The Briton's American debut.")
e(19, 1998, "Флойд Мейвезер KO 2 Анхель Манфреді", "Floyd Mayweather KO 2 Angel Manfredy", "Маямі, США", "Miami, USA",
  "Титул WBC у другій напівлегкій вазі.", "WBC super featherweight title.", "jfxVbZUgfI0")
e(19, 2009, "Едвін Валеро KO 7 Гектор Веласкес", "Edwin Valero KO 7 Hector Velazquez", "Каракас, Венесуела", "Caracas, Venezuela",
  "Титул WBC у легкій вазі.", "WBC lightweight title.")
e(19, 2009, "Келлі Павлік KO 5 Мігель Анхель Еспіно", "Kelly Pavlik KO 5 Miguel Angel Espino", "Янгстаун, США", "Youngstown, USA",
  "Титул у середній вазі.", "Middleweight title.")
e(19, 2014, "Адоніс Стівенсон KO 5 Дмитро Сухоцький", "Adonis Stevenson KO 5 Dmitry Sukhotsky", "Квебек, Канада", "Quebec City, Canada",
  "Нокаут на 2:42 п'ятого раунду. Титули WBC та The Ring у напівважкій вазі.", "A knockout at 2:42 of round five. WBC and The Ring light heavyweight titles.")
e(19, 2020, "Ілунга Макабу KO 7 Оланреваджу Дуродола", "Ilunga Makabu KO 7 Olanrewaju Durodola", "Кіншаса, ДР Конго", "Kinshasa, DR Congo",
  "Титул WBC у важкій вазі.", "WBC cruiserweight title.")
e(19, 2020, "Сауль «Канело» Альварес – Каллум Сміт", "Saul “Canelo” Alvarez – Callum Smith", "Сан-Антоніо, США", "San Antonio, USA",
  "Перемога Альвареса рішенням суддів. Титул WBC у другій середній вазі.", "Alvarez won on the judges' decision. WBC super middleweight title.")
# ---- 20-30
e(20, 1946, "Шугар Рей Робінсон – Томмі Белл", "Sugar Ray Robinson – Tommy Bell", "Нью-Йорк, США (Медісон-сквер-гарден)", "New York, USA (Madison Square Garden)",
  "Перемога Робінсона. Він здобув перший світовий титул у напівсередній вазі після п'яти років очікування.", "Robinson won. He took his first world welterweight title after five years of waiting.")
e(21, 1974, "Роберто Дюран TKO 1 Масатака Такаяма", "Roberto Duran TKO 1 Masataka Takayama", "Сан-Хосе, Коста-Рика", "San Jose, Costa Rica",
  "Кілька нокдаунів. Бій у легкій вазі.", "Several knockdowns. A lightweight bout.")
e(21, 2019, "Джермалл Чарло KO 11 Тоні Гаррісон", "Jermall Charlo KO 11 Tony Harrison", "Онтаріо, США", "Ontario, USA",
  "Титул WBC у першій середній вазі.", "WBC super welterweight title.")
e(21, 2024, "Олександр Усик UD 12 Тайсон Ф'юрі", "Oleksandr Usyk UD 12 Tyson Fury", "Ер-Ріяд, Саудівська Аравія", "Riyadh, Saudi Arabia",
  "Рахунок 116–112 × 3. Точність CompuBox: 42,3% проти 28,3%. Пояси WBA Super, WBC, WBO, IBO, The Ring, TBRB / лінійний.",
  "Scores 116–112 ×3. CompuBox accuracy: 42.3% against 28.3%. WBA Super, WBC, WBO, IBO, The Ring and TBRB / lineal belts.")
e(21, 2024, "Сергій Богачук TKO 6 Ішмаель Девіс", "Serhii Bohachuk TKO 6 Ishmael Davis", "Ер-Ріяд, Саудівська Аравія", "Riyadh, Saudi Arabia",
  "Відмова бійця. Андеркард Usyk–Fury II.", "The opponent retired. The undercard of Usyk–Fury II.")
e(21, 2024, "Мозес Ітаума KO 1 Демсі Маккін", "Moses Itauma KO 1 Demsey McKean", "Ер-Ріяд, Саудівська Аравія", "Riyadh, Saudi Arabia",
  "Перемога в першому раунді (KO / TKO). Андеркард Usyk–Fury II.", "A first-round win (KO / TKO). The undercard of Usyk–Fury II.")
e(23, 1993, "Ясуей Якушіджі – Чон Іль Бьон", "Yasuei Yakushiji – Jung-Il Byun", "", "",
  "Перемога Якушіджі та завоювання титулу WBC в легшій вазі.", "Yakushiji won and took the WBC bantamweight title.")
e(23, 2008, "Дайсуке Найто TKO 11 Шінго Ямагучі", "Daisuke Naito TKO 11 Shingo Yamaguchi", "", "",
  "Бій у найлегшій вазі.", "A flyweight bout.")
e(23, 2011, "Понгсаклек Вонджонкгам – Хірофумі Мукаї", "Pongsaklek Wonjongkam – Hirofumi Mukai", "", "",
  "Технічна нічия в першому раунді через випадкове зіткнення головами.", "A technical draw in round one after an accidental clash of heads.")
e(23, 2011, "Компаяк Порпрамук – Адріан Ернандес", "Kompayak Porpramook – Adrian Hernandez", "", "",
  "Перемога Порпрамука в домашньому бою та завоювання пояса WBC.", "Porpramook won at home and took the WBC belt.")
e(23, 2019, "Кеншіро Тераджі TKO 4 Ренді Петалкорін", "Kenshiro Teraji TKO 4 Randy Petalcorin", "", "",
  "Три нокдауни в третьому раунді. Титул WBC у першій найлегшій вазі.", "Three knockdowns in round three. WBC light flyweight title.")
e(23, 2023, "Вечір боксу «Day of Reckoning»", "“Day of Reckoning” boxing night", "Саудівська Аравія", "Saudi Arabia",
  "Масштабний турнір за участю Ентоні Джошуа (хедлайнер) і Деонтея Вайлдера. Джошуа переміг Отто Валліна технічним нокаутом у п'ятому раунді, Джозеф Паркер переміг Вайлдера одностайним рішенням.",
  "A major card headlined by Anthony Joshua, with Deontay Wilder also on the bill. Joshua stopped Otto Wallin in round five, and Joseph Parker beat Wilder on a unanimous decision.")
e(26, 1908, "Джек Джонсон TKO 14 Томмі Бернс", "Jack Johnson TKO 14 Tommy Burns", "Сідней, Австралія", "Sydney, Australia",
  "Джонсон став першим темношкірим чемпіоном світу у надважкій вазі.", "Johnson became the first Black heavyweight world champion.")
e(26, 2023, "Наоя Іноуе TKO 10 Марлон Тапалес", "Naoya Inoue TKO 10 Marlon Tapales", "Токіо, Японія", "Tokyo, Japan",
  "Об'єднання всіх чотирьох поясів і титулу The Ring у другій легшій вазі (122 фунти).", "Inoue unified all four belts and The Ring title at super bantamweight (122 lb).", "e3W0DMczmZc")
e(29, 1983, "Народився Дерек Чісора", "Derek Chisora was born", "Велика Британія", "Great Britain",
  "Народився британський боксер надважкої ваги, дворазовий претендент на титул WBC.", "The British heavyweight, a two-time WBC title challenger, was born.")
e(30, 1970, "Помер Сонні Лістон", "Sonny Liston died", "Лас-Вегас, США", "Las Vegas, USA",
  "Помер колишній абсолютний чемпіон світу у надважкій вазі у віці близько 40 років.", "The former undisputed heavyweight world champion died at about 40 years old.")

# Widget picks: day -> (main index key, second key) as (year, title_ua_prefix)
PICKS = {
  1: ((2018, "Деонтей Вайлдер"), (2018, "Олександр Гвоздик")),
  2: ((1963, "Сандро Маццінгі"), (1995, "Вейн Маккаллох")),
  3: ((2005, "Джермейн Тейлор"), (2025, "WBC позбавила")),
  4: ((1998, "Менні Пак'яо"), (2004, "Хосе Луїс Кастільйо")),
  5: ((1947, "Джо Луїс"), None),
  6: ((2008, "Менні Пак'яо"), (1969, "Леотіс Мартін")),
  7: ((2019, "Ентоні Джошуа"), (2002, "Флойд Мейвезер")),
  8: ((2007, "Флойд Мейвезер"), (1984, "Азума Нельсон")),
  9: ((2017, "Василь Ломаченко"), (1955, "Шугар Рей Робінсон")),
  10: ((1968, "Джо Фрейзер"), (1982, "Майкл Доукс")),
  11: ((2004, "Віталій Кличко"), (2010, "Скасований бій")),
  12: ((2009, "Віталій Кличко"), (2020, "Шакур Стівенсон")),
  13: ((2008, "Володимир Кличко"), None),
  14: ((1968, "Педро Адіґе"), (1964, "Народився Анатолій")),
  16: ((1940, "Джо Луїс"), (1995, "Террі Норріс")),
  17: ((1952, "Арчі Мур"), (1978, "Народився Менні")),
  18: ((1993, "Саймон Браун"), (1916, "Джиммі Вайлд")),
  19: ((1997, "Насім Хамед"), (2020, "Сауль")),
  20: ((1946, "Шугар Рей Робінсон"), None),
  21: ((2024, "Олександр Усик"), (2019, "Джермалл Чарло")),
  23: ((2023, "Вечір боксу"), (2019, "Кеншіро Тераджі")),
  26: ((2023, "Наоя Іноуе"), (1908, "Джек Джонсон")),
  29: ((1983, "Народився Дерек"), None),
  30: ((1970, "Помер Сонні"), None),
}
