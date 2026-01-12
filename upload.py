from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from config import Config
from utils.file_processor import FileProcessor
from routes.auth import token_required

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
@token_required
def upload_page():
    """Data upload page"""
    if request.method == 'GET':
        return render_template('upload.html', username=session.get('username'))
    
    try:
        user_id = session.get('user_id')
        upload_type = request.form.get('upload_type')
        
        if upload_type == 'manual':
            # Manual entry
            data = {
                'date': request.form.get('date'),
                'amount': request.form.get('amount'),
                'category': request.form.get('category'),
                'transaction_type': request.form.get('transaction_type'),
                'merchant': request.form.get('merchant', 'Manual Entry'),
                'payment_mode': request.form.get('payment_mode', 'Other')
            }
            
            # Validate
            errors = FileProcessor.validate_manual_entry(data)
            if errors:
                return render_template('upload.html', errors=errors, username=session.get('username'))
            
            # Save to database
            from utils.db_utils import DatabaseManager
            query = """
                INSERT INTO transactions 
                (user_id, date, transaction_type, amount, category, merchant, payment_mode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            DatabaseManager.execute_query(query, (
                user_id, data['date'], data['transaction_type'], 
                float(data['amount']), data['category'], 
                data['merchant'], data['payment_mode']
            ))
            
            return redirect(url_for('dashboard.dashboard_page'))
        
        else:
            # File upload
            if 'file' not in request.files:
                return render_template('upload.html', errors=["No file uploaded"], username=session.get('username'))
            
            file = request.files['file']
            
            if file.filename == '':
                return render_template('upload.html', errors=["No file selected"], username=session.get('username'))
            
            if not FileProcessor.allowed_file(file.filename):
                return render_template('upload.html', errors=["Invalid file type. Please upload CSV or Excel file"], username=session.get('username'))
            
            # Save file
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, f"{user_id}_{filename}")
            file.save(filepath)
            
            # Process file
            try:
                print(f"Processing file: {filepath}")
                
                if filename.endswith('.csv'):
                    df = FileProcessor.process_csv(filepath)
                else:
                    df = FileProcessor.process_excel(filepath)
                
                print(f"Processed {len(df)} rows from file")
                print(f"Columns: {df.columns.tolist()}")
                print(f"Sample data:\n{df.head()}")
                
                # Save to database
                count = FileProcessor.save_transactions_to_db(df, user_id)
                
                print(f"✓ Successfully saved {count} transactions for user {user_id}")
                
                # Clean up file
                os.remove(filepath)
                
                # Add success message
                session['upload_success'] = f"Successfully uploaded {len(df)} transactions!"
                
                return redirect(url_for('dashboard.dashboard_page'))
            
            except Exception as e:
                print(f"Error processing file: {str(e)}")
                import traceback
                traceback.print_exc()
                
                if os.path.exists(filepath):
                    os.remove(filepath)
                return render_template('upload.html', errors=[f"Error processing file: {str(e)}"], username=session.get('username'))
    
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('upload.html', errors=[f"Upload failed: {str(e)}"], username=session.get('username'))