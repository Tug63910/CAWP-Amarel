import os
import subprocess
from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from CAWPr.auth import login_required
from CAWPr.db import get_db
from CAWPr.models.predict import classifier

from CAWPr.CAWPspider.CAWPspider.spiders.gs_utils import download_blob

bp=Blueprint('application',__name__)

@bp.route('/')
def index():
	db=get_db()
	db.execute(
		'SELECT p.id, url, state, level, office, profession, created'
		' FROM post p'
		' ORDER BY created ASC'
	)
	posts=db.fetchall()
	return render_template('application/index.html',posts=posts)


@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
	BUCKET_NAME="cawp-47548.appspot.com"
	REMOTE_BLOB_NAME="testGAE"

	if request.method=='POST':
		url=request.form['url']
		error=None

		if not url:
			error='Url required'

		if error is not None:
			flash(error)
		else:
			db=get_db()
			CAWPwd=os.path.join(os.getcwd(),"CAWPr/CAWPspider")
			subprocess.run(["scrapy","crawl","-a","url="+url,"candidate"],cwd=CAWPwd)
			text=download_blob(BUCKET_NAME,REMOTE_BLOB_NAME).decode('utf-8')
			entry=classifier(text)
			db.execute(
				'INSERT INTO post (url, state, level, office, profession,text)'
				' VALUES (%s,%s,%s,%s,%s,%s);',
				(url,entry['state'],entry['level'],entry['office'],entry['profession'], entry['text'])
			)
			return redirect(url_for('application.index'))

	return render_template('application/create.html')

def get_post(post_id):
	db=get_db()
	db.execute(
		'SELECT p.id, url, state, level, office, profession, text'
		' FROM post p'
		' WHERE p.id=%s;',
		(post_id,)
	)
	post=db.fetchone()

	if post is None:
		abort(404,"Post id {0} doesn't exist.".format(post_id))

	return post

@bp.route('/<int:post_id>/update', methods=('GET','POST'))
@login_required
def update(post_id):
	post=get_post(post_id)

	if request.method=='POST':
		url=post['url']
		state=request.form['state']
		level=request.form['level']
		office=request.form['office']
		profession=request.form['profession']
		text=request.form["text"]
		error=None

		if not url:
			error='Url required'
	
		if error is not None:
			flash(error)
		else:
			db=get_db()
			db.execute(
				'UPDATE post SET url=%s, state=%s, level=%s, office=%s, profession=%s, text=%s'
				' WHERE id=%s;',
				(url,state,level,office,profession,text,post_id)
			)
			return redirect(url_for('application.index'))

	return render_template('application/update.html',post=post)
	
@bp.route('/<int:post_id>/delete', methods=('GET','POST',))
@login_required
def delete(post_id):
	get_post(post_id)
	db=get_db()
	db.execute('DELETE FROM post WHERE id = %s;', (post_id,))
	return redirect(url_for('application.index'))

