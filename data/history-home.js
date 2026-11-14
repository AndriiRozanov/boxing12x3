const HISTORY_SEPT = {
  1:{gp:{y:1923,tUk:"Народився Роккі Марчіано",tEn:"Rocky Marciano was born"}},
  2:{gp:{y:1965,tUk:"Народився Леннокс Льюїс",tEn:"Lennox Lewis was born"},sg:{y:1953,tUk:"Сонні Лістон КО 1 Дон Сміт",tEn:"Sonny Liston KO 1 Don Smith"}},
  3:{gp:{y:1908,tUk:"Томі Бернс КО 6 Біллі Ленг",tEn:"Tommy Burns KO 6 Bill Lang"}},
  4:{gp:{y:1983,tUk:"Франциско «Кіко» Бехінес помер днів після титульного поєдинку",tEn:"Francisco \u201cKiko\u201d Bejines died days after a title bout"}},
  5:{gp:{y:1960,tUk:"Кассіус Клей здобув золото Олімпіади",tEn:"Cassius Clay wins Olympic gold"}},
  7:{gp:{y:1894,tUk:"Едісон зняв на плівку демонстраційний поєдинок Корбетта й Кортні",tEn:"Edison films demonstration bout between Corbett and Courtney"}},
  8:{gp:{y:2012,tUk:"Віталій Кличко ТКО 4 Махмуд Чарр",tEn:"Vitali Klitschko TKO 4 Mahmoud Charr"},sg:{y:2017,tUk:"Давід Бенавідес SD 12 Рональд Гаврил",tEn:"David Benavidez SD 12 Ronald Gavril"}},
  9:{gp:{y:2017,tUk:"Олександр Усик ТКО 10 Марко Хук",tEn:"Oleksandr Usyk TKO 10 Marco Huck"},sg:{y:1978,tUk:"Шугар Рей Леонард ТКО 10 Флойд Мейвезер-старший",tEn:"Sugar Ray Leonard TKO 10 Floyd Mayweather Sr."}},
  10:{gp:{y:1993,tUk:"Хуліо Сезар Чавес D-SD 12 Пернелл Уітакер",tEn:"Julio Cesar Chavez D-SD 12 Pernell Whitaker"},sg:{y:1973,tUk:"Мухаммед Алі SD 12 Кен Нортон ІІ",tEn:"Muhammad Ali SD 12 Ken Norton II"}},
  11:{gp:{y:2010,tUk:"Володимир Кличко КО 10 Сем Пітер ІІ",tEn:"Wladimir Klitschko KO 10 Samuel Peter II"}},
  12:{gp:{y:1992,tUk:"Хуліо Сезар Чавес UD 12 Гектор «Мачо» Камачо",tEn:"Julio Cesar Chavez UD 12 Hector \u201cMacho\u201d Camacho"}},
  14:{gp:{y:2013,tUk:"Флойд Мейвезер MD 12 Сауль Альварес",tEn:"Floyd Mayweather MD 12 Saul Alvarez"},sg:{y:2002,tUk:"Оскар Де Ла Хойя ТКО 11 Фернандо Варгас",tEn:"Oscar De La Hoya TKO 11 Fernando Vargas"}},
  15:{gp:{y:1978,tUk:"Мухаммед Алі UD 12 Леон Спінкс",tEn:"Muhammad Ali UD 12 Leon Spinks"},sg:{y:2018,tUk:"Сауль Альварес MD 12 Геннадій Головкін II",tEn:"Saul Alvarez MD 12 Gennadiy Golovkin II"}},
  16:{gp:{y:1981,tUk:"Шугар Рей Леонард ТКО 14 Томас Гернс",tEn:"Sugar Ray Leonard TKO 14 Thomas Hearns"},sg:{y:2017,tUk:"Сауль Альварес D-SD 12 Геннадій Головкін",tEn:"Saul Alvarez D-SD 12 Gennadiy Golovkin"}},
  17:{gp:{y:2016,tUk:"Олександр Усик UD 12 Кшиштоф Гловацький",tEn:"Oleksandr Usyk UD 12 Krzysztof Glowacki"},sg:{y:2022,tUk:"Сауль Альварес UD 12 Геннадій Головкін III",tEn:"Saul Alvarez UD 12 Gennadiy Golovkin III"}},
  18:{gp:{y:2004,tUk:"Бернард Хопкінс КО 9 Оскар Де Ла Хойя",tEn:"Bernard Hopkins KO 9 Oscar De La Hoya"},sg:{y:1999,tUk:"Фелікс Трінідад MD 12 Оскар Де Ла Хойя",tEn:"Felix Trinidad MD 12 Oscar De La Hoya"}},
  19:{gp:{y:2017,tUk:"Помер Джейк ЛаМотта у віці 95 років",tEn:"Jake LaMotta died at the age of 95"}},
  20:{gp:{y:1972,tUk:"Мухаммед Алі RTD 7 Флойд Паттерсон",tEn:"Muhammad Ali RTD 7 Floyd Patterson"}},
  21:{gp:{y:2024,tUk:"Даніель Дюбуа КО 5 Ентоні Джошуа",tEn:"Daniel Dubois KO 5 Anthony Joshua"}},
  22:{gp:{y:2025,tUk:"Теренс Кроуфорд UD 12 Сауль Альварес",tEn:"Terence Crawford UD 12 Saul Alvarez"},sg:{y:1927,tUk:"Джин Танні UD 10 Джек Демпсі ІІ",tEn:"Gene Tunney UD 10 Jack Dempsey II"}},
  23:{gp:{y:1957,tUk:"Кармен Базіліо SD 15 Шугар Рей Робінсон",tEn:"Carmen Basilio SD 15 Sugar Ray Robinson"}},
  24:{gp:{y:1994,tUk:"Олівер Маккол ТКО 2 Леннокс Льюїс",tEn:"Oliver McCall TKO 2 Lennox Lewis"},sg:{y:2005,tUk:"Володимир Кличко UD 12 Сем Пітер",tEn:"Wladimir Klitschko UD 12 Samuel Peter"}},
  25:{gp:{y:2021,tUk:"Олександр Усик UD 12 Ентоні Джошуа",tEn:"Oleksandr Usyk UD 12 Anthony Joshua"},sg:{y:1999,tUk:"Володимир Кличко ТКО 8 Алекс Шульц",tEn:"Wladimir Klitschko TKO 8 Alex Schulz"}},
  26:{gp:{y:1945,tUk:"Шугар Рей Робінсон SD 12 Джейк ЛаМотта",tEn:"Sugar Ray Robinson SD 12 Jake LaMotta"},sg:{y:2009,tUk:"Віталій Кличко RTD 10 Кріс Арреола",tEn:"Vitali Klitschko RTD 10 Chris Arreola"}},
  27:{gp:{y:2019,tUk:"Даніель Дюбуа ТКО 1 Ебенезер Теттех",tEn:"Daniel Dubois TKO 1 Ebenezer Tetteh"}},
  28:{gp:{y:1976,tUk:"Мухаммед Алі UD 15 Кен Нортон ІІІ",tEn:"Muhammad Ali UD 15 Ken Norton III"}},
  29:{gp:{y:2000,tUk:"Бернард Хопкінс ТКО 12 Фелікс Трінідад",tEn:"Bernard Hopkins TKO 12 Felix Trinidad"},sg:{y:1977,tUk:"Мухаммед Алі UD 15 Ерні Шаверс",tEn:"Muhammad Ali UD 15 Ernie Shavers"}},
  30:{gp:{y:2023,tUk:"Сауль Альварес UD 12 Джермелл Чарло",tEn:"Saul Alvarez UD 12 Jermell Charlo"}}
};

const HISTORY_OCT = {
  1:{gp:{y:1975,tUk:"Мухаммед Алі RTD 14 Джо Фрейзер",tEn:"Muhammad Ali RTD 14 Joe Frazier"}},
  2:{gp:{y:1980,tUk:"Ларрі Холмс TKO 11 Мухаммед Алі",tEn:"Larry Holmes TKO 11 Muhammad Ali"}},
  3:{gp:{y:1981,tUk:"Алексис Аргуельо ТКО 14 Рей Манчині",tEn:"Alexis Arguello TKO 14 Ray Mancini"},sg:{y:1981,tUk:"Марвін Хаглер ТКО 11 Мустафа Хамшо",tEn:"Marvin Hagler TKO 11 Mustafa Hamsho"}},
  4:{gp:{y:2003,tUk:"Евандер Холіфілд ТКО 9 Джеймс Тоні",tEn:"Evander Holyfield TKO 9 James Toney"}},
  5:{gp:{y:2013,tUk:"Володимир Кличко UD 12 Олександр Повєткін",tEn:"Wladimir Klitschko UD 12 Alexander Povetkin"},sg:{y:2019,tUk:"Геннадій Головкін UD 12 Сергій Дерев'янченко",tEn:"Gennadiy Golovkin UD 12 Sergiy Derevyanchenko"}},
  6:{gp:{y:1978,tUk:"Народився Ріккі Хаттон",tEn:"Ricky Hatton was born"}},
  7:{gp:{y:2000,tUk:"Полі Айяла UD 12 Джонні Тапія",tEn:"Paulie Ayala UD 12 Johnny Tapia"}},
  9:{gp:{y:2021,tUk:"Тайсон Ф'юрі КО 11 Деонтей Вайлдер",tEn:"Tyson Fury KO 11 Deontay Wilder"}},
  10:{gp:{y:2001,tUk:"Помер Едді Фатч",tEn:"Eddie Futch died"}},
  11:{gp:{y:2008,tUk:"Віталій Кличко RTD 8 Сем Пітер",tEn:"Vitali Klitschko RTD 8 Samuel Peter"}},
  12:{gp:{y:2013,tUk:"Василь Ломаченко КО 4 Хосе Луїс Рамірес",tEn:"Vasiliy Lomachenko KO 4 Jose Luis Ramirez"}},
  13:{gp:{y:1939,tUk:"Генрі Армстронг КО 2 Говард Скотт",tEn:"Henry Armstrong KO 2 Howard Scott"},sg:{y:1945,tUk:"Народився Джо Кортес",tEn:"Joe Cortez was born"}},
  14:{gp:{y:1949,tUk:"Еззард Чарльз КО 8 Пет Валентино",tEn:"Ezzard Charles KO 8 Pat Valentino"}},
  15:{gp:{y:1858,tUk:"Народився Джон Лоуренс Салліван",tEn:"John Lawrence Sullivan was born"}},
  16:{gp:{y:2010,tUk:"Віталій Кличко UD 12 Шеннон Бріггс",tEn:"Vitali Klitschko UD 12 Shannon Briggs"},sg:{y:1987,tUk:"Майк Тайсон КО 7 Тайрелл Біггз",tEn:"Mike Tyson KO 7 Tyrell Biggs"}},
  17:{gp:{y:2020,tUk:"Теофімо Лопес UD 12 Василь Ломаченко",tEn:"Teofimo Lopez UD 12 Vasiliy Lomachenko"}},
  18:{gp:{y:1991,tUk:"Рей Мерсер КО 5 Томмі Моррісон",tEn:"Ray Mercer KO 5 Tommy Morrison"}},
  19:{gp:{y:1985,tUk:"Лі Рой Мерфі КО 12 Чісанда Мутті",tEn:"Lee Roy Murphy KO 12 Chisanda Mutti"},sg:{y:1987,tUk:"Марвін Хаглер ТКО 3 Мустафа Хамшо",tEn:"Marvin Hagler TKO 3 Mustafa Hamsho"}},
  20:{gp:{y:1979,tUk:"Джон Тейт UD 15 Геррі Кутзее",tEn:"John Tate UD 15 Gerrie Coetzee"}},
  21:{gp:{y:2000,tUk:"Флойд Мейвезер ТКО 9 Емануель Огастес",tEn:"Floyd Mayweather TKO 9 Emanuel Augustus"}},
  22:{gp:{y:1966,tUk:"Карлос Ортіс ТКО 5 Шугар Рамос",tEn:"Carlos Ortiz TKO 5 Sugar Ramos"}},
  23:{gp:{y:1962,tUk:"Дік Тайгер UD 15 Джин Фулмер",tEn:"Dick Tiger UD 15 Gene Fullmer"},sg:{y:1998,tUk:"Віталій Кличко ТКО 2 Маріо Шіссер",tEn:"Vitali Klitschko TKO 2 Mario Schisser"}},
  25:{gp:{y:1990,tUk:"Евандер Холіфілд КО 3 Джеймс «Бастер» Дуглас",tEn:"Evander Holyfield KO 3 James \u201cBuster\u201d Douglas"}},
  26:{gp:{y:2013,tUk:"Бернард Хопкінс UD 12 Каро Мурат",tEn:"Bernard Hopkins UD 12 Karo Murat"}},
  28:{gp:{y:2023,tUk:"Тайсон Ф'юрі SD 10 Френсіс Нганну",tEn:"Tyson Fury SD 10 Francis Ngannou"}},
  29:{gp:{y:1960,tUk:"Кассіус Клей UD 6 Танні Хансейкер",tEn:"Cassius Clay UD 6 Tunney Hunsaker"},sg:{y:2005,tUk:"Сауль Альварес ТКО 4 Абрахам Гонсалес",tEn:"Saul Alvarez TKO 4 Abraham Gonzalez"}},
  30:{gp:{y:1974,tUk:"Мухаммед Алі КО 8 Джордж Форман",tEn:"Muhammad Ali KO 8 George Foreman"}},
  31:{gp:{y:2020,tUk:"Олександр Усик UD 12 Дерек Чісора",tEn:"Oleksandr Usyk UD 12 Derek Chisora"}}
};

const HISTORY_NOV = {
  1:{gp:{y:2008,tUk:"Вік Дарчинян KO 9 Крістіан Міхарес",tEn:"Vic Darchinyan KO 9 Cristian Mijares"},sg:{y:2003,tUk:"Флойд Мейвезер TKO 7 Філіп Н'Доу",tEn:"Floyd Mayweather TKO 7 Phillip N'Dou"}},
  2:{gp:{y:1944,tUk:"Народився Майкл Баффер",tEn:"Michael Buffer was born"},sg:{y:2019,tUk:"Сауль Альварес KO 11 Сергій Ковальов",tEn:"Saul Alvarez KO 11 Sergey Kovalev"}},
  3:{gp:{y:1984,tUk:"Хосе Луїс Рамірес TKO 4 Едвін Росаріо",tEn:"Jose Luis Ramirez TKO 4 Edwin Rosario"}},
  4:{gp:{y:1995,tUk:"Ріддік Боу TKO 8 Евандер Холіфілд",tEn:"Riddick Bowe TKO 8 Evander Holyfield"},sg:{y:2006,tUk:"Флойд Мейвезер UD 12 Карлос Балдомір",tEn:"Floyd Mayweather UD 12 Carlos Baldomir"}},
  5:{gp:{y:1994,tUk:"Джордж Форман KO 10 Майкл Мурер",tEn:"George Foreman KO 10 Michael Moorer"}},
  6:{gp:{y:1993,tUk:"Евандер Холіфілд MD 12 Ріддік Боу",tEn:"Evander Holyfield MD 12 Riddick Bowe"},sg:{y:1981,tUk:"Ларрі Холмс TKO 11 Реналдо Снайпс",tEn:"Larry Holmes TKO 11 Renaldo Snipes"}},
  7:{gp:{y:1994,tUk:"Народився Джервонта Девіс",tEn:"Gervonta Davis was born"},sg:{y:1972,tUk:"Народився Хасім Рахман",tEn:"Hasim Rahman was born"}},
  8:{gp:{y:1997,tUk:"Евандер Холіфілд RTD 8 Майкл Мурер",tEn:"Evander Holyfield RTD 8 Michael Moorer"}},
  9:{gp:{y:1996,tUk:"Евандер Холіфілд TKO 11 Майк Тайсон",tEn:"Evander Holyfield TKO 11 Mike Tyson"},sg:{y:2013,tUk:"Олександр Усик TKO 5 Феліпе Ромеро",tEn:"Oleksandr Usyk TKO 5 Felipe Romero"}},
  10:{gp:{y:1983,tUk:"Марвін Хаглер UD 15 Роберто Дюран",tEn:"Marvin Hagler UD 15 Roberto Duran"},sg:{y:2018,tUk:"Олександр Усик TKO 8 Тоні Белью",tEn:"Oleksandr Usyk TKO 8 Tony Bellew"}},
  11:{gp:{y:2000,tUk:"Леннокс Льюїс UD 12 Девід Туа",tEn:"Lennox Lewis UD 12 David Tua"}},
  13:{gp:{y:1982,tUk:"Рей Манчіні KO 14 Кім Дук-Ку",tEn:"Ray Mancini KO 14 Duk Koo Kim"},sg:{y:1999,tUk:"Леннокс Льюїс UD 12 Евандер Холіфілд",tEn:"Lennox Lewis UD 12 Evander Holyfield"}},
  15:{gp:{y:2014,tUk:"Володимир Кличко KO 5 Кубрат Пулєв",tEn:"Wladimir Klitschko KO 5 Kubrat Pulev"},sg:{y:2024,tUk:"Джейк Пол UD 8 Майк Тайсон",tEn:"Jake Paul UD 8 Mike Tyson"}},
  16:{gp:{y:1996,tUk:"Дебют братів Кличків у професійному боксі",tEn:"Klitschko brothers' professional debuts"}},
  17:{gp:{y:2001,tUk:"Леннокс Льюїс KO 4 Хасім Рахман",tEn:"Lennox Lewis KO 4 Hasim Rahman"}},
  19:{gp:{y:2005,tUk:"Флойд Мейвезер TKO 6 Шармба Мітчелл",tEn:"Floyd Mayweather TKO 6 Sharmba Mitchell"}},
  22:{gp:{y:1986,tUk:"Майк Тайсон TKO 2 Тревор Бербік",tEn:"Mike Tyson TKO 2 Trevor Berbick"}},
  23:{gp:{y:2002,tUk:"Віталій Кличко TKO 10 Ларрі Дональд",tEn:"Vitali Klitschko TKO 10 Larry Donald"}},
  25:{gp:{y:1980,tUk:"Рей Леонард TKO 8 Роберто Дюран",tEn:"Sugar Ray Leonard TKO 8 Roberto Duran"},sg:{y:1977,tUk:"Томас Хернс KO 2 Джером Гілл",tEn:"Thomas Hearns KO 2 Jerome Hill"}},
  26:{gp:{y:2011,tUk:"Сауль Альварес TKO 5 Керміт Цинтрон",tEn:"Saul Alvarez TKO 5 Kermit Cintron"}},
  28:{gp:{y:2015,tUk:"Тайсон Ф'юрі UD 12 Володимир Кличко",tEn:"Tyson Fury UD 12 Wladimir Klitschko"}},
  30:{gp:{y:1979,tUk:"Рей Леонард TKO 15 Вілфред Бенітес",tEn:"Sugar Ray Leonard TKO 15 Wilfred Benitez"}}
};
// Місяці, покриті "Цей день в історії" на головній. Останній запис у
// списку - запасний варіант, коли поточний місяць ще не охоплений.
const HISTORY_MONTHS = [
  {idx:8, slug:'september', data:HISTORY_SEPT, days:30, lblUk:'Вер', lblEn:'Sep', nameUk:'вересня', nameEn:'Sep'},
  {idx:9, slug:'october',   data:HISTORY_OCT,  days:31, lblUk:'Жов', lblEn:'Oct', nameUk:'жовтня',  nameEn:'Oct'},
  {idx:10, slug:'november',  data:HISTORY_NOV,  days:30, lblUk:'Лис', lblEn:'Nov', nameUk:'листопада', nameEn:'Nov'}
];

(function(){
  var box = document.getElementById('history'); if (!box) return;
  var isUk = document.documentElement.lang === 'uk', lp = isUk ? 'ua' : 'en';
  var now = new Date(), curIdx = now.getMonth(), month = null, i;
  for (i = 0; i < HISTORY_MONTHS.length; i++) { if (HISTORY_MONTHS[i].idx === curIdx) { month = HISTORY_MONTHS[i]; break; } }
  var covered = !!month;
  if (!month) month = HISTORY_MONTHS[HISTORY_MONTHS.length - 1];
  var day = covered ? now.getDate() : 1, guard = 0;
  while (!month.data[day] && guard < month.days) { day = day >= month.days ? 1 : day + 1; guard++; }
  var e = month.data[day]; if (!e) return;
  var base = '/' + lp + '/boxing-history/' + month.slug, hub = '/' + lp + '/boxing-history';
  var h = '<div class="sh"><span class="sl">' + (isUk ? 'Цей день в історії боксу' : 'This day in boxing') + '</span><a class="sa" href="' + base + '">' + (isUk ? 'Усі події місяця' : 'All events of the month') + ' →</a></div>';
  h += '<div class="hist-widget"><div class="hist-badge"><div class="hist-badge-month">' + (isUk ? month.lblUk : month.lblEn) + '</div><div class="hist-badge-day">' + day + '</div><div class="hist-badge-year">' + e.gp.y + '</div></div><div class="hist-perf"></div><div class="hist-content">';
  h += '<div class="hist-title">' + (isUk ? e.gp.tUk : e.gp.tEn) + '</div>';
  if (e.sg) h += '<div class="hist-sg"><div class="hist-sg-year">' + (isUk ? 'Також ' : 'Also ') + e.sg.y + '</div><div class="hist-sg-title">' + (isUk ? e.sg.tUk : e.sg.tEn) + '</div></div>';
  h += '<div class="hist-btns"><a class="hist-btn primary" href="' + base + '#d' + day + '">' + (isUk ? 'Події ' + day + ' ' + month.nameUk : 'Events on ' + month.nameEn + ' ' + day) + '</a><a class="hist-btn secondary" href="' + hub + '">' + (isUk ? 'Визначні боксерські дні' : 'This Day in Boxing') + '</a></div></div></div>';
  box.innerHTML = h; box.style.display = '';
})();
