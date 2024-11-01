from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Initial list of agents grouped by job
agents = {
    "Admin": ["Guilherme Vieira-Machado", "Vinod Open 2", "Vinod Rajendran", "Vinod Test"],
    "Agents": ["Elvira Carrera", "Nadia Clark", "William Lai", "Sook-Theng Chow", "Sophie Katsarova", "Sonny Johnson"],
    "Others": [
        "Jacey Cherney", "Jenni Spainhour", "Jess Evans", "Jill Dunn", "Kim Powell",
        "Melissa DeCandia", "Stefanie Dunnegan"
    ]
}

# Route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form submission and save to CSV
        deactivation_status = []
        session_data = {}  # Dictionary to store data in session

        for group, names in agents.items():
            for agent in names:
                status = request.form.get(f"deactivate_{agent}", 'No')
                notes = request.form.get(f"notes_{agent}", '')

                # Save each agent's status and notes to session_data
                session_data[agent] = {'deactivate': status, 'notes': notes}

                deactivation_status.append({'Agent': agent, 'Group': group, 'Deactivate?': status, 'Notes': notes})

        # Save data to session
        session['form_data'] = session_data

        # Save results to a CSV file
        df = pd.DataFrame(deactivation_status)
        df.to_csv('deactivation_results.csv', index=False)

        return redirect(url_for('success'))

    # GET method: Display the form with session data if available
    form_data = session.get('form_data', {})
    return render_template('index.html', agents=agents, form_data=form_data)


# Route to display organized output
@app.route('/success')
def success():
    form_data = session.get('form_data', {})
    accounts_to_deactivate = [(agent, data['notes']) for agent, data in form_data.items() if data['deactivate'] == 'Yes']
    accounts_to_keep_active = [(agent, data['notes']) for agent, data in form_data.items() if data['deactivate'] == 'No']

    return render_template(
        'success.html',
        accounts_to_deactivate=accounts_to_deactivate,
        accounts_to_keep_active=accounts_to_keep_active
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default port is 10000 if not set
    app.run(host="0.0.0.0", port=port)
