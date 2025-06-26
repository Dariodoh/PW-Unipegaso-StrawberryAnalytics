from app import app, server # Importa app e server da app.py
from layout import layout   # Importa la variabile 'layout' da layout.py
import callbacks            # Importa il file delle callback

# Assegna il layout all'applicazione
app.layout = layout

# Il punto di ingresso per avviare l'applicazione
if __name__ == '__main__':
    app.run(debug=True)