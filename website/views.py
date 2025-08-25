from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note_content = request.form.get('note')
        
        if note_content:  # 简化验证：只要有内容就行
            new_note = Note(data=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('笔记已添加')
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required  # 添加登录验证
def delete_note():  
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    note = Note.query.get(note_id)
    
    # 简化：只检查笔记存在且属于当前用户
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    
    return jsonify({})
