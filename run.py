from app import app, server
from layout import layout
import callbacks

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)