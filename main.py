from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initial list of agents
agents = [
    "Elvira Carrera", "Guilherme Vieira-Machado", "Jacey Cherney", "Jenni Spainhour",
    "Jess Evans", "Jill Dunn", "Kim Powell", "Melissa DeCandia", "Nadia Clark",
    "Sonny Johnson", "Sook-Theng Chow", "Sophie Katsarova", "Stefanie Dunnegan",
    "Vinod Open 2", "Vinod Rajendran", "Vinod Test", "William Lai"
]


# Route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form submission and save to CSV
        deactivation_status = []
        for agent in agents:
            status = request.form.get(agent, 'No')
            deactivation_status.append({'Agent': agent, 'Deactivate?': status})

        # Save results to a CSV file
        df = pd.DataFrame(deactivation_status)
        df.to_csv('deactivation_results.csv', index=False)

        return redirect(url_for('success'))

    # GET method: Display the form
    return render_template('index.html', agents=agents)


# Route to confirm submission
@app.route('/success')
def success():
    return "Deactivation choices have been saved!"


if __name__ == '__main__':
    app.run(debug=True)
