@bp.route('/')
def index():
	db=get_db()
	posts=db.execute(
		'SELECT p.id,url,state,level,office,profession'
		' FROM post p'
		' ORDER BY id ASC'
	).fetchall()
	return render_template('application/index.html', posts=posts)
