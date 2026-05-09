from flask import Flask, render_template, request, session, redirect
import pandas as pd

app = Flask(__name__)
app.secret_key = "cs_battleground_key"

# Dashboard ke liye data (Iske bina Index.html crash ho jayega)
compliances = [
    {"id": 1, "name": "Board Minutes", "type": "drafting", "due_date": "2026-04-25", "status": "Pending"},
    {"id": 2, "name": "DIR-3 KYC", "type": "roc", "due_date": "2026-09-30", "status": "Pending"}
]

@app.route('/')
def index():
    return render_template('index.html', compliances=compliances)

@app.route('/dpt3')
def dpt3_page():
    # Session initialization
    if 'score' not in session: session['score'] = 0
    if 'attempts' not in session: session['attempts'] = 3
    if 'total_cos' not in session: session['total_cos'] = 0
    return render_template('dpt3.html', score=session['score'], attempts=session['attempts'], rank=session.get('rank', 'NOOB 🤡'))

@app.route('/launch_battle', methods=['POST'])
def launch_battle():
    excel_file = request.files.get('excel_file')
    pdf_op = float(request.form.get('pdf_opening', 0))
    pdf_cl = float(request.form.get('pdf_closing', 0))

    if excel_file:
        df = pd.read_excel(excel_file)
        ex_op = df['Opening'].sum()
        ex_cl = df['Closing'].sum()

        if ex_op == pdf_op and ex_cl == pdf_cl:
            session['score'] += 1
            session['attempts'] = 3
            msg, status = "MISSION ACCOMPLISHED!", "SUCCESS"
        else:
            session['attempts'] -= 1
            if session['attempts'] <= 0:
                session['attempts'] = 3
                msg, status = "OUT OF LIVES!", "FAILED"
            else:
                msg, status = f"MISMATCH! {session['attempts']} LEFT", "FAILED"
        
        session['total_cos'] += 1
        # Rank Logic
        pct = (session['score'] / session['total_cos']) * 100
        if pct == 100: session['rank'] = "SUPER BOSS 👑"
        elif pct >= 50: session['rank'] = "BOSS 😎"
        else: session['rank'] = "NOOB 🤡"

    return render_template('dpt3.html', msg=msg, status=status, score=session['score'], attempts=session['attempts'], rank=session['rank'])

@app.route('/reset_game')
def reset_game():
    session.clear()
    return redirect('/dpt3')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
