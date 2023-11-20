from TaskApp import create_app, db
from sqlalchemy import text
app=create_app()
if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    db.drop_all()
    db.session.execute(text("VACUUM"))

    db.create_all()
    
    db.session.commit()
        
    app_ctx.pop() 

    
