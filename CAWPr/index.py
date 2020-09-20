@bp.route('/')
def index():
	db=get_db()
	db.execute(
		'SELECT p.id,url,party,state,level,office,profession'
		' FROM post p'
		' ORDER BY id ASC;'
	)
	posts=db.fetchall()
	return render_template('application/index.html', posts=posts)
