def content(makeFns):
	w,e,a,af,ae=makeFns('w,e,a,af,ae')
	abbrXls="<abbr title='Excel Binary File Format, бинарный формат файлов Excel'>xls</abbr>"
	abbrXlsx="<abbr title='Excel 2007 workbook'>xlsx</abbr>"
	abbrPdf="<abbr title='Portable Document Format'>pdf</abbr>"
	abbrCsv="<abbr title='comma-separated values, значения, разделённые запятыми'>csv</abbr>"
	abbrOdt="<abbr title='OpenDocument Text'>odt</abbr>"
	def wp(x):
		w("<p>"+x+"</p>\n")
	def wli(x):
		w("<li>"+x+"</li>\n")
	def defCodeList(items,cls=None,end='\n'):
		x="<dl"
		if cls is not None:
			x+=" class='"+e(cls)+"'"
		x+=">"+end
		for dt,dd,*rest in items:
			x+="<dt"
			if rest:
				id,=rest
				x+=" id='"+e(id)+"'"
			x+="><code>"+dt+"</code></dt><dd>"+dd+"</dd>"+end
		x+="</dl>"+end
		return x
	def wDefCodeList(items,cls=None,end='\n'):
		w(defCodeList(items,cls,end))
	def downloadFileList(items,end='\n'):
		return defCodeList(((af('db/'+filename,filename),description) for filename,description in items),cls='downloads')
	def wDownloadFileList(items,end='\n'):
		w(downloadFileList(items,end))

	wp("Если вы не программист, то вам, скорее всего, нужен один из этих двух файлов:")
	wDownloadFileList((
		("departments.xlsx","Ведомственная структура расходов бюджета Санкт-Петербурга"),
		("sections.xlsx","Распределение бюджетных ассигнований бюджета Санкт-Петербурга"),
	))
	wp(
		"В каждом из этих файлов данные на 2014 год и на плановый период 2015 и 2016 годов, а также данные проектов, поправок и принятых законов объединены в одну таблицу со сворачивающимися уровнями. "
		"Далее приводится информация для тех, кто хочет получить подобные файлы самостоятельно или использовать данные, применявшиеся для их получения, иным способом."
	)

	w("<h1>База данных и таблицы расходов бюджета Санкт-Петербурга</h1>\n")
	wp(
		"Данные, использованные для построения базы, прошли несколько уровней обработки. "
		"Эти уровни пронумерованы так, что на каждом из них в качестве исходных данных используются только данные непосредственно предшествующего уровня. "
		"Список уровней:"
        )
	wDefCodeList((
		(a("#1-sources","1-sources"),"исходные данные — документы с различных сайтов</dd>"),
		(a("#2-tables","2-tables"),"таблицы, извлечённые из документов</dd>"),
		("3-db","база данных, полученная из таблиц</dd>"),
		("4-xls","первый вариант отчётов из базы данных — "+abbrXls+"- и "+abbrXlsx+"-файлы</dd>"),
		("4-xlsx","второй, рекомендуемый вариант отчётов из базы данных — только "+abbrXlsx+"-файлы</dd>"),
	))
	wp(
		"Так как промежуточные данные тоже представляют интерес, здесь приводятся результаты каждого этапа. "
		"На данный момент собраны данные для 2014 года."
	)

	w("<h2 id='1-sources'>Исходные данные</h2>")
	wp("Исходными данными являются документы в том виде, в котором они были опубликованы на	официальных сайтах. Документы взяты из следующих источников:")
	w("<ul>\n")
	wli(
		"Раздел "+ae('http://www.fincom.spb.ru/comfin/budjet/budget_for_people.htm',"«Бюджет для граждан»")+" сайта "+ae("http://www.fincom.spb.ru/","Комитета финансов Санкт-Петербурга")+", "
		"откуда использованы "+abbrXlsx+"-файлы для таблиц расходов бюджета. "
		"Это позволяет установить, какими планировались расходы до рассмотрения в Законодательном Собрании, и какими они стали после. "
		"К сожалению, эти данные не полны."
	)
	wli(
		a('xls.html',"Проект по извлечению таблиц из "+abbrPdf+"-файлов")+", "
		"откуда берутся таблицы в формате "+abbrCsv+" для недостающих данных «Бюджета для граждан»."
	)
	wli(
		"Сайт "+ae('http://assembly.spb.ru/',"Законодательного Собрания Санкт-Петербурга")+", "
		"откуда берутся документы с поправками к бюджету. "
		"Это позволяет проследить, как менялись расходы бюджета при рассмотрении в <abbr title='Законодательном Собрании'>ЗС</abbr>. "
		"Полученные документы были вручную преобразованы в формат "+abbrOdt+". "
		"Короткие поправки в исходные данные не включены, они введены вручную и добавляются на следующем уровне."
	)
	w("</ul>\n")
	wDownloadFileList((
		("1-sources.out.zip","архив с документами"),
	))

	w("<h2 id='2-tables'>Таблицы из исходных документов</h2>")
	wp(
		"На этом уровне формируются "+abbrCsv+"-таблицы, из которых далее можно будет собрать базу данных. "
		"Первая строка каждого "+abbrCsv+"файла содержит названия столбцов. "
		"Таблицы размещены в двух каталогах:"
	)
	wDefCodeList((
		("content","Собственно таблицы из документов. В основном это таблицы с изменениями ведомственной структуры расходов бюджета."),
		("meta","Таблицы с данными о самих документах."),
	))
	wp("Далее рассматриваются форматы отдельных файлов.")
	wDefCodeList((
		(
			"meta/authors.csv",
			"Авторы, которые внесли в <abbr title='Законодательное Собрание'>ЗС</abbr> какой-либо документ или поправку. Столбцы:"+
			defCodeList((
				("authorId","числовой идентификатор автора для связи с "+a('#2-tables-meta-documents',"таблицей документов")),
				("authorShortName","короткое имя автора для написания в узких столбцах таблиц документов, получаемых на последнем уровне"),
				("authorLongName","имя автора в том виде, в котором оно указано на сайте <abbr title='Законодательного Собрания'>ЗС</abbr>"),
			),end=''),
			'2-tables-meta-authors'
		),
		(
			"meta/documents.csv",
			"Документы — проекты законов и поправки. Столбцы:"+
			defCodeList((
				("documentNumber","номер документа в <abbr title='Законодательном Собрании'>ЗС</abbr>"),
				("documentDate","дата внесения документа в расширенном формате ISO (YYYY-MM-DD)"),
				("stageNumber","номер варианта закона (0 — первоначальный закон, 1 — первая корректировка, 2 — вторая и т.д.) для связи с "+a('#2-tables-meta-stages',"таблицей вариантов законов")),
				("amendmentFlag","тип проекта/поправки (0 — проект, после которого идут 1 — отдельно внесённые поправки, затем 2 — прочие изменения, приводящие проект закона к конечному виду, в котором он принимается)"),
				("authorId","числовой идентификатор автора (если автор известен, для amendmentFlag=2 считается неизвестным)"),
				("documentAssemblyUrl","ссылка на документ на сайте <abbr title='Законодательного Собрания'>ЗС</abbr>, содержащий данные (если он там опубликован)"),
			),end=''),
			'2-tables-meta-documents'
		),
		(
			"meta/stages.csv",
			"Варианты законов (на данный момент — одного закона 2014 года). Столбцы:"+
                        defCodeList((
				("stageNumber","номер варианта закона"),
				("stageAssemblyUrl","ссылка на страницу с документами, поступившими в <abbr title='Законодательное Собрание'>ЗС</abbr> во время рассмотрения проекта этого варианта"),
			),end=''),
			'2-tables-meta-stages'
		),
	))
	wDownloadFileList((
		("2-tables.out.zip","архив с таблицами"),
	))

	w("<h2>Предыдущие версии файлов</h2>\n")
	wDownloadFileList((
		("db.v1.zip","выпуск к принятию первоначального варианта закона о бюджете 2014 года"),
		("db.v2.zip","выпуск к принятию первой корректировки закона о бюджете 2014 года"),
	))
	wp(ae('https://www.dropbox.com/sh/zgnevck3cij1gm0/AABdfNdrzoimxiWDe_DDPfpCa/db','Ссылка на папку dropbox')+" (на случай, если они поменяют ссылки).")

	# TODO объяснить подробнее
	# w("<p>Названия целевых статей даны в виде, соответствующем закону о бюджете (некоторые из них изменились по сравнению с проектом закона).</p>\n")