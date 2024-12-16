import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt

# Define grid dimensions
GRID_ROWS = 5  # Number of rows
GRID_COLS = 7  # Number of columns

class GridWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wavefront Algorithm Grid")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create grid layout
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)

        # Set grid layout stretch factors
        for i in range(GRID_ROWS):
            self.grid_layout.setRowStretch(i, 1)
        for j in range(GRID_COLS):
            self.grid_layout.setColumnStretch(j, 1)

        # Initialize grid and attributes
        self.buttons = {}  # To store button references
        self.start = None  # Start position
        self.destination = None  # Destination position

        # Populate the grid with buttons
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                button = QPushButton(f"({row+1}, {col+1})")  # Text for the block
                button.setCheckable(True)  # Make the button checkable
                button.setStyleSheet("border: 1px solid black; background-color: lightgray;")
                button.clicked.connect(lambda _, r=row, c=col: self.handle_button_click(r, c))
                self.grid_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button

        # Add Execute button
        self.execute_button = QPushButton("Execute Wavefront")
        self.execute_button.clicked.connect(self.execute_wavefront)
        main_layout.addWidget(self.execute_button)

    def handle_button_click(self, row, col):
        button = self.buttons[(row, col)]

        if self.start is None:
            self.start = (row, col)
            button.setStyleSheet("border: 1px solid black; background-color: green;")
            button.setChecked(True)
            button.setText("Start")
        elif self.destination is None and (row, col) != self.start:
            self.destination = (row, col)
            button.setStyleSheet("border: 1px solid black; background-color: red;")
            button.setChecked(True)
            button.setText("Destination")
        else:
            if (row, col) == self.start:
                QMessageBox.warning(self, "Error", "Start block already selected!")
            elif (row, col) == self.destination:
                QMessageBox.warning(self, "Error", "Destination block already selected!")
            else:
                QMessageBox.warning(self, "Error", "Both start and destination are already selected!")

    def execute_wavefront(self):
        if self.start is None or self.destination is None:
            QMessageBox.warning(self, "Error", "Please select both start and destination blocks.")
            return

        # Initialize the wavefront algorithm
        queue = [self.start]
        visited = set()
        distance = {self.start: 0}

        while queue:
            current = queue.pop(0)
            visited.add(current)
            current_distance = distance[current]

            # Get neighbors
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in distance:
                    distance[neighbor] = current_distance + 1
                    queue.append(neighbor)

                    # Update button text and style
                    button = self.buttons[neighbor]
                    button.setStyleSheet("border: 1px solid black; background-color: yellow;")
                    button.setText(str(distance[neighbor]))

    def get_neighbors(self, position):
        row, col = position
        neighbors = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            r, c = row + dr, col + dc
            if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                neighbors.append((r, c))

        return neighbors

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GridWindow()
    window.show()
    sys.exit(app.exec_())
