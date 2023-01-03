<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title></title>
</head>

<body>
	<article>
		<div>
			{% for week in weeks %}
			<h1>{{ week.start_date }}~{{week.end_date}}</h1>
			<ul>
				<li></li>
			</ul>
			{% endfor %}
			<h1>KPT</h1>
			<ul>
				<li>K</li>
				<li>P</li>
				<li>T</li>
			</ul>
		</div>
	</article>
</body>

</html>
