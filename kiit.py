import requests, sys, sqlite3
from lxml import etree
from io import StringIO, BytesIO
prev_tit=''
db_list = []
try:
	conn = sqlite3.connect('kiit.db')
	c = conn.cursor()
	num=1
	c.execute('SELECT title FROM notice WHERE id=1')
	check = c.fetchone()[0]
	prev_tit = str(check)
	s=requests.Session()
	s.get('http://kiittnp.in/tnp/usr/index.php')
	payload={'user_name': '1205048@kiit.ac.in', 'password': '6745', 'user_type': 'Student', 'btn_stu_login': 'Sign In'}
	r1 = s.post('http://kiittnp.in/tnp/usr/indexPage.php', data=payload)
	if len(r1.history) == 0:
		html = r1.text
		parser = etree.HTMLParser()
		tree   = etree.parse(StringIO(html), parser)
		title = tree.xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td/table/tr[2]/td/fieldset/h3')
		titl=str(title[0].text)
		flag=0
		for i in range(len(titl)):
			if titl[i] is not prev_tit[i]:
				flag=1
				break;
		if flag == 0:
			print "already updated"
		else:
			for i in range (2,26):
				title = tree.xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td/table/tr['+str(i)+']/td/fieldset/h3')
				#print title[0].text
				if not title:
					break;
				desc = tree.xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td/table/tr['+str(i)+']/td/fieldset/p/b')
				#print desc[0].text
				hlink = tree.xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td/table/tr['+str(i)+']/td/fieldset/p/a//@href')
				for link in hlink:
					hlink[hlink.index(link)] = 'http://kiittnp.in/tnp' + link[2:]
				#print hlink
				db_list = db_list + [(num,title[0].text,desc[0].text,str(hlink))]
				num=num+1
				#print
				#print
			#print db_list
			#c.execute('CREATE TABLE notice (id integer, title text, date text, link text)')
			c.execute('DELETE FROM notice')
			c.executemany('INSERT INTO notice VALUES (?,?,?,?)',db_list)
			print 'database updated'
			conn.commit()
			conn.close()
	else:
		print "login failed"
except:
	print "Unexpected Error: ", sys.exc_info()[0]
